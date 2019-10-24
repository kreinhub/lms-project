import re
import os


basedir = os.path.abspath(os.path.dirname(__file__))
basename = "datafile_1.txt"
try:
    with open(f"{basedir}/{basename}", "r") as f:
        raw_text = f.read()
except FileNotFoundError:
    print('No file')

# var = re.findall(r"<html(.*)</html>", raw_text, re.DOTALL)
var = re.split(r"(<html.*</html>)", raw_text)
string = ''.join(var)

print(len(var))
print(string)

# cut_regex = re.compile(re.findall(r"</html>(.*)<html>", raw_text, re.DOTALL))
# result = re.sub(re.findall(r"</html>(.*)<html>", raw_text, re.DOTALL), "", string)

# result = re.sub(r"</html>(.*)<html>", r" ", string)


# print(result)

# pattern = re.compile(r"<html(.*)</html>",re.DOTALL)
# matches = pattern.finditer(raw_text)

# for i,match in enumerate(matches):
#     # if match.group(1).startswith('-'):
#     # print(match.group(1)[:10])
#     # else:
#     print(f"letter #{i}: ",match.group(1))


