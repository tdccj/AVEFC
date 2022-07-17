# coding = utf-8
# 录播自动转封装v3.0.b @tdccj
# 备份功能开发失败，暂时不考虑，转封装后质量有待对比
# ！！！不得在录播目录下以flv备份
# 可以考虑多长时间没有修改文件之后开始转封装

from watchdog.events import FileSystemEventHandler

print("watchdog_1装载成功")
from watchdog.observers import Observer

print("watchdog_2装载成功")
import time

print("time装载成功")
import os

print("os装载成功")

i = 0
jishu = 0
i2 = 1  # 此处切勿与i相同
lu_jing = ""


def main():
    print("v3.0.b")
    global i, jishu, i2, lu_jing
    cwd = os.getcwd()  # 获取当前目录
    The_Path = read(cwd)
    if __name__ == "__main__":  # 用observe对目录进行检测
        path = The_Path
        event_handler = Watch()
        observer = Observer()
        try:
            observer.schedule(event_handler, path, recursive=True)
            observer.start()
            print("监控运行")
        except FileNotFoundError:
            zm = open(cwd + "\\录播自动转封装设置.zm", "w")
            The_Path = input("输入路径2")
            zm.write(The_Path)
            zm.close()
            try:
                path = The_Path
                event_handler = Watch()
                observer = Observer()
                observer.schedule(event_handler, path, recursive=True)
                observer.start()
            except FileNotFoundError:
                print("路径仍然错误，请重启")
        try:
            while True:  # 用来保证程序持续执行
                time.sleep(3)
                if i != 0:
                    if i == i2:
                        jishu = jishu + 1
                        print(jishu)
                    if jishu > 4:
                        zhuan_fengzhuang(lu_jing)
                    i2 = i

        except KeyboardInterrupt:  # 除了程序被用户中断
            observer.stop()


def read(cwd):  # 读取配置文件
    try:
        zm = open(cwd + "\\录播自动转封装设置.zm", "r")
        The_Path = zm.readline()
        print(The_Path)
        zm.close()

    except FileNotFoundError:
        zm = open(cwd + "\\录播自动转封装设置.zm", "w")
        The_Path = input("输入路径")
        zm.write(The_Path)
        zm.close()

    print("监控中")
    return The_Path


def zhuan_fengzhuang(lu_jing):  # 用来执行转封装操作
    global i
    try:
        print("开始转封装")
        path = os.path.split(lu_jing)
        os.system(f"copy /a {lu_jing} {path[0]}\\backup\\{path[1]}")    #备份
        print(f"{path[0]}\\backup\\{path[1]}")
        lu_jing_out = lu_jing[:-3] + "mp4"
        os.rename(lu_jing, lu_jing_out)
        print(f"转封装完毕:{lu_jing_out}")
    except FileExistsError:
        zhuan_fengzhuang(lu_jing)
    except FileNotFoundError:
        print("转封装失败")
    i = 0


class Watch(FileSystemEventHandler):  # 用来接受events的反馈
    def on_modified(self, event):
        global lu_jing
        Time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print(f'文件修改:{event.src_path}', Time)
        lu_jing = str(event.src_path)
        if lu_jing[-3:] == "flv":  # 判断是否为录播文件
            print("判断为TRUE")
            global i
            i = i + 1


if __name__ == "__main__":
    try:
        main()
    finally:
        time.sleep(10)
