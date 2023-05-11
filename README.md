# Kiv-v1.10 🔥
source code of dynamic Kiv programming language v1.1.0 (finale version of v1)
# Run 🕹️
If your os supports .exe
- add builds folder to enviroment variables then
- ```kiv file.kiv```
- else
- ```python PATH/To/repositry/kiv file.kiv```
# Shell 🐢
- ```python PATH/To/repositry/kiv/kivshell.py```
# Future 🔮
this is sll a beta version meaning not all binaries are found very few buildin functions and libraries and bad perfermonce hopefully all if this will be fixed in kiv v2
# Syntax
```
function add(x,y) do
  return x+y
end
 
while true do
  for i=0 until 5 do
    if i==4 do
      break
    elseif i==3 do
      continue
    end
    print(add(i,1))
    end
  end
end
```
