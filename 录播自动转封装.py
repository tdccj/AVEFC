# coding = utf-8
# 录播自动转封装v2.0 @tdccj
# 备份功能开发失败，暂时不考虑，转封装后质量有待对比
# 可以考虑多长时间没有修改文件之后开始转封装

from watchdog.events import FileSystemEventHandler

print("watchdog_1装载成功")
from watchdog.observers import Observer

print("watchdog_2装载成功")
import time

print("time装载成功")
import os

print("os装载成功")


def main():
    print("v2.0")
    cwd = os.getcwd()  # 获取当前目录
    The_Path = read(cwd)
    Time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    lu_jing = "创建变量"
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
                time.sleep(1)

        except KeyboardInterrupt:  # 除了程序被用户中断
            observer.stop()


def read(cwd):     #读取配置文件
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


def zhuan_ma(lu_jing):  # 用来执行转封装操作
    try:
        # os.system(f"copy /a {lu_jing} {lu_jing[:-3]+'_backup.flv'} ") #备份问题需要等文件修改问题解决
        lu_jing_out = lu_jing[:-3] + "mp4"
        os.rename(lu_jing, lu_jing_out)
        print(f"转封装完毕:{lu_jing_out}")
    except FileExistsError:
        zhuan_ma(lu_jing)
    except FileNotFoundError:
        print("转封装失败")


class Watch(FileSystemEventHandler):  # 用来接受events的反馈
    def on_modified(self, event):
        Time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print(f'文件修改:{event.src_path}', Time)
        lu_jing = str(event.src_path)

        if lu_jing[-3:] == "flv":  # 判断是否为录播文件
            print("判断为TRUE")
            zhuan_ma(lu_jing)


if __name__ == "__main__":
    main()
