# 去除代码空格/缩进
import re, os

# 创建新文件并输出
def newmd(name, txt):
    path = os.getcwd()
    test = path + "\\" + name
    print(test)
    f = open(test, "w", encoding="utf-8")
    f.write(txt)
    f.close
    print("done")


def wipeSpace(input, output, num=1):
    with open(input, "r", encoding="utf-8") as f:
        pys = f.read()

    sline = pys.split("\n")

    newline = []

    # 遍历每一行
    for line in sline:
        # 检测空行或者空格行
        if line == "" or line.isspace():
            # 跳过
            continue

        line = line[4 * num :]
        newline.append(line)

    print(newline)

    print("\n".join(newline))

    newmd(output, "\n".join(newline))


# 第一个参数为源文件全名称
# 第二个参数为新文件全名称
# 第三个参数为缩进量，1 代表 '4个空格'
wipeSpace(
    "test.txt",
    "wipespace.txt",
    1
)
