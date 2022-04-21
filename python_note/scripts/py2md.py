import re,os

def newmd(name,md):
    path = os.getcwd()
    test = path+"\\"+name+".md"
    print(test)
    f = open(test,"w",encoding="utf-8")
    f.write(md)
    f.close
    print("done")

def py2md(input,output):
    with open(input, "r", encoding="utf-8") as f:
        pys = f.read()

    sline = pys.split("\n")

    mdstr = []
    # 信标，记录上一行信息
    s = -1
    # 信表，记录首次（0为首次），实现标题
    first = 0
    # 信标，告诉下行上上行是代码，上行是空格的情况
    # 默认为0，表示没发生上述情况

    #遍历删除"#"（除了第一行）,并添加代码块
    for line in sline:
        # 检测空行或者空格行
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

    # 二次遍历解决代码间空格问题,暂未解决

    for line in mdstr:
        pass

    print("\n".join(mdstr))

    newmd(output,"\n".join(mdstr))

# 第一个参数为脚本运行目录下的py文件
# 第二个参数为转换成markdown文档的名称
py2md('test.py','mark')
