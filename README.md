# Kiv-v1.10 🔥
source code of dynamic Kiv programming language v1.1.0 (finale version of v1)
# If your os supports .exe
- add builds folder to enviroment variables then
- ```kiv file.kiv```
# Run 🕹️
If os supports .exe
- kiv file.kiv
else
- ```python PATH/To/repositry/kiv file.kiv```
# Shell 🐢
If os supports .exe
- kivshell
else
- ```python PATH/To/repositry/kiv/kivshell.py```
# Future 🔮
this is sll a beta version meaning not all binaries are found very few buildin functions and libraries and bad perfermonce hopefully all if this will be fixed in kiv v2
# Syntax
```
import "time" // builtin module
sleep(1) // pauses the program for 1 second
// comment
function add(x,y) do // start after do
  return x+y
end // end here
var subtract = function(x,y) -> x-y // lambda + vrariables
while true do // while loop
  for i=0 until 5 do
    if i==4 do
      break
    elseif i==3 do
      continue
    end // end is after condition block so after else | elseif (if found) if only if is found after if
    print(add(i,1))
    end
  end
end
```
