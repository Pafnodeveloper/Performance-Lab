import sys
import re

user_arg = sys.argv
sample = sys.argv[2].replace("*", "[\w\s]*")
result = re.match(sample, user_arg[1])

if result:
    print("OK")
else:
    print("KO")
