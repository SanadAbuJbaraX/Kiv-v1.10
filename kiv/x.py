import string

def generate_lowercaseToUpperDict():
    print("[",end="")
    for index,value in enumerate(string.ascii_lowercase):
        print(f"[\"{value}\",\"{string.ascii_uppercase[index]}\"],",end="")
    print("]")
def generate_UppertolowerDict():
    print("[",end="")
    for index,value in enumerate(string.ascii_uppercase):
        print(f"[\"{value}\",\"{string.ascii_lowercase[index]}\"],",end="")
    print("]")
def chars():
    print(string.ascii_letters)
def upper():
    print(string.ascii_uppercase)
def lower():
    print(string.ascii_lowercase)
x = {"open":1,"close":2}
add = {"write":3,"open":1}
x |= add
print(x)