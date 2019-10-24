import re


# s = "abcde\n		fghij<FooBar>";
# rx = r"(.*)<FooBar>";
# m = re.search(rx, s, flags=re.S)
# if m:
# 	print(m.group(1))

string = """123
<h1>HI</h1>
<pre>hui</pre>
<p>pesda    </p>

<pre>Zalupa 123
</pre>

123
<h1>HI</h1>
<pre>hui</pre>
<p>pesda    </p>

<pre>Zalupa 123
</pre>
"""

# for i in string.split():
#     print(i)


# regex = re.compile(r"<pre>(.*)</pre>")
# for i in string.split():
#     match = re.search(regex, i)
#     if match:
#         print(match.group())

print(re.findall(r"<pre>(.*)</pre>", string, re.DOTALL))