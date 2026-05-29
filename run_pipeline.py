import os

print("\nSTEP 1")
os.system("python preprocess.py")

print("\nSTEP 2")
os.system("python table_detect.py")

print("\nSTEP 3")
os.system("python extract_cells.py")

print("\nDONE")