import os

path = input("path for KIV_MODULES: ")
os.environ["KIV_MODULES"] = path
print(os.getenv("KIV_MODULES"))