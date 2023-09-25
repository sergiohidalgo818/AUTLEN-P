import re

RE1 = "a|(ab)*|(aba)*|b|(ba)*|(bab)*"


expr = RE1
string = "aba"
match = re.fullmatch(expr, string)


print(str(bool(match)))