import re,os

def newmd(name,md):
    path = os.getcwd()
    test = path+"\\"+name+".md"
    print(test)
    f = open(test,"w",encoding="utf-8")
    f.write(md)
    f.close
    print("done")


with open("test.py", "r", encoding="utf-8") as f:
    str = f.read()

sline = str.split("\n")

mdstr = []
# 信标，记录上一行信息
s = -1
# 信表，记录首次（0为首次）
first = 0

for line in sline:
    if line == "" or line.isspace():
        if s == 1:
            mdstr.append("```")
        s = 0
        mdstr.append(line)
        continue
    # 判断开头有无#
    if re.match(r"^#", line):
        if s == 1:
            mdstr.append("```")
        s = 0
        if first == 0:
            mdstr.append(line)
            first = 1
            continue
        line = line.replace("# ", "")
        line = line.replace("#", "")
        mdstr.append(line)
    else:
        if s == 0:
            mdstr.append("```py")
            s = 1
        mdstr.append(line)

print(mdstr)

print("\n".join(mdstr))

newmd("test1","\n".join(mdstr))


