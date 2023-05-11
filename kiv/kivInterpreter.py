from kivNumber import *
from kivTokens import *
from kivRuntimeResult import RuntimeResult
from kivErrors import *
from kivFunction import Function
from kivString import String
from kivList import List
from kivFunction import *

class Interpreter:
	def visit(self,node,context):
		method = f"visit_{type(node).__name__}"
		method = getattr(self,method,self.no_visit_method)
		return method(node,context)
	def no_visit_method(self,node,context):
		raise  Exception(f'No visit_{type(node).__name__} method defined')
	def visit_IntNode(self,node,context):        
		return  RuntimeResult().success(
			Int(node.tok.value).set_context(context).set_pos(node.pos_start,node.pos_end)
			)	
	def visit_FloatNode(self,node,context):        
		return  RuntimeResult().success(
			Float(node.tok.value).set_context(context).set_pos(node.pos_start,node.pos_end)
			)	
	def visit_BinOpNode(self,node,context):
		res = RuntimeResult()
	
		left =  res.register(self.visit(node.left_node,context))
		if res.should_return(): return res
		right = res.register(self.visit(node.right_node,context))

		if node.op_tok.type == TT_PLUS:
			result,error = left.added_to(right)
		elif node.op_tok.type == TT_MINUS:
			result,error = left.subbed_by(right)
		elif node.op_tok.type == TT_MUL:  
			result,error = left.multed_by(right)
		elif node.op_tok.type == TT_DIV:
			result,error = left.dived_by(right)
		elif node.op_tok.type == TT_POW:
			result,error = left.powed_by(right)
		elif node.op_tok.type == TT_EQEQ:
			result,error = left.get_comparison_eq(right)
		elif node.op_tok.type == TT_NE:
			result,error = left.get_comparison_ne(right)
		elif node.op_tok.type == TT_GT:
			result,error = left.get_comparison_gt(right)
		elif node.op_tok.type == TT_GTE:
			result,error = left.get_comparison_gte(right)
		elif node.op_tok.type == TT_LT:
			result,error = left.get_comparison_lt(right)
		elif node.op_tok.type == TT_LTE:
			result,error = left.get_comparison_lte(right)
		elif node.op_tok.matches(TT_KEYWORD, '&'):           
			result, error = left.anded_by(right)
		elif node.op_tok.matches(TT_KEYWORD, '|'):
			result, error = left.ored_by(right)
		
		if error:
			return res.failure(error)
		return res.success(result.set_pos(node.pos_start,node.pos_end))
	def visit_IfNode(self, node, context):
		res = RuntimeResult()
		
		for condition, expr,should_return_null in node.cases:
			condition_value = res.register(self.visit(condition, context))
			if res.should_return(): return res

			if condition_value.is_true():
				expr_value = res.register(self.visit(expr, context))
				if res.should_return(): return res
				return res.success(Int(0) if should_return_null else expr_value)

		if node.else_case:
			expr,should_return_null = node.else_case
			else_value = res.register(self.visit(expr, context))
			if res.should_return(): return res
			return res.success(Int(0) if should_return_null else else_value)

		return res.success(Int(0))
	def visit_ImportNode(self,node,context):
		res = RuntimeResult()
		if node.file.value == "time":
			context.symbol_table.symbols |= ModuleTime.symbols
			return res.success(Int(0))
		try:
			file_ctx = open(node.file.value)
		except:
			try:
				import os
				file_ctx = open(os.getenv("KIV_MODULES") +"\\"+ node.file.value)
			except:
				return res.failure(
				ImportError(
				node.pos_start,
				node.pos_end,
				f" '{node.file.value}' is not defined",
				)
				)
		from kivImport import run_import
		_,err,symbols = run_import(file_ctx.name,file_ctx.read())
		if err:
			print(err.as_string())
		context.symbol_table.symbols |= symbols

		return res.success(Int(0))
		
	def visit_UnaryOpNode(self,node,context):
		res = RuntimeResult()

		number = res.register(self.visit(node.node,context))
		if res.should_return():
			return res
		error =  None
		if node.op_tok.type == TT_MINUS:
			number,error = number.multed_by(Int(-1).set_context(context))
		elif node.op_tok.matches(TT_KEYWORD, 'not'):
			number, error = number.notted()
		if error:
			return res.failure(error)
		return res.success(number.set_pos(node.pos_start,node.pos_end))
	def visit_VarAccessNode(self,node,context):
		res = RuntimeResult()
		varname = node.varname_tok.value
		value = context.symbol_table.get(varname)

		if not value:
			return res.failure(
				RuntimeError(
				node.pos_start,
				node.pos_end,
				f" '{varname}' is not defined",
				context
				)
			)
		value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
		return res.success(value)
	def visit_WhileNode(self, node, context):
		res = RuntimeResult()
		elements = []
		while True:
			condition = res.register(self.visit(node.condition_node, context))
			if res.should_return(): return res

			if not condition.is_true(): break

			value = res.register(self.visit(node.body_node, context))
			if res.should_return() and not res.loop_should_continue and not res.loop_should_break: return res
			if res.loop_should_continue:
				continue
			if res.loop_should_break:
				break
			elements.append(value)
		return res.success(Int(0) if node.should_return_null else List(elements).set_context(context).set_pos(node.pos_start,node.pos_end))
	def visit_ForNode(self, node, context):
		res = RuntimeResult()
		elements = []
		start_value = res.register(self.visit(node.start_value_node, context))
		if res.should_return(): return res

		end_value = res.register(self.visit(node.end_value_node, context))
		if res.should_return(): return res
		
		if node.step_value_node:
			step_value = res.register(self.visit(node.step_value_node, context))
			if res.should_return(): return res
		else:
			step_value = Int(1)

		i = start_value.value

		if step_value.value >= 0:
			condition = lambda: i < end_value.value
		else:
			condition = lambda: i > end_value.value
		
		while condition():
			context.symbol_table.set(node.var_name_tok.value, Int(i))
			i += step_value.value
			value = res.register(self.visit(node.body_node, context))

			if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res
			if res.loop_should_continue:
				continue
			if res.loop_should_break:
				break
			elements.append(value)
		return res.success(
			Int(0) if node.should_return_null else 
			List(elements).set_context(context).set_pos(node.pos_start,node.pos_end))

	def visit_VarAssignNode(self,node,context):
		res = RuntimeResult()
		varname = node.varname_tok.value
		value = res.register(self.visit(node.value_tok,context))
		if res.should_return(): return res
		context.symbol_table.set(varname,value)
		return res.success(value)
	def visit_FuncDefNode(self, node, context):
		res = RuntimeResult()

		func_name = node.var_name_tok.value if node.var_name_tok else None
		body_node = node.body_node
		arg_names = [arg_name.value for arg_name in node.arg_name_toks]
		func_value = Function(func_name, body_node, arg_names,node.should_auto_return).set_context(context).set_pos(node.pos_start, node.pos_end)
		
		if node.var_name_tok:
			context.symbol_table.set(func_name, func_value)

		return res.success(func_value)

	def visit_CallNode(self, node, context):
		res = RuntimeResult()
		args = []

		value_to_call = res.register(self.visit(node.node_to_call, context))
		if res.should_return(): return res
		value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

		for arg_node in node.arg_nodes:
			args.append(res.register(self.visit(arg_node, context)))
			if res.should_return(): return res

		return_value = res.register(value_to_call.execute(args))
		if res.should_return(): return res
		return_value = return_value.copy().set_pos(node.pos_start,node.pos_end).set_context(context)
		return res.success(return_value)
	
	def visit_StringNode(self,node,context):
		return RuntimeResult().success(
			String(
			node.tok.value
			).set_context(context).set_pos(node.pos_start,node.pos_end)
		)
	def visit_BoolNode(self,node,context):
		return  RuntimeResult().success(
			Bool(node.tok.value).set_context(context).set_pos(node.pos_start,node.pos_end)
			)	
	def visit_ListNode(self,node,context):
		res = RuntimeResult()
		elements = []

		for element_node in node.element_nodes:
			elements.append(res.register(self.visit(element_node, context)))
			if res.should_return(): return res
	
		return res.success(List(elements).set_context(context).set_pos(node.pos_start,node.pos_end))
	def visit_ReturnNode(self,node,context):
		res = RuntimeResult()
		if node.node_to_return:
			value = res.register(self.visit(node.node_to_return,context))
			if res.should_return(): return res 
		else:
			value = Int(0)
		return res.success_return(value)
	def visit_ContinueNode(self,node,context):
		return RuntimeResult().success_continue()
	def visit_BreakNode(self,node,context):
		return RuntimeResult().success_break()
	