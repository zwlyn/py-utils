# -*- encoding: utf-8 -*-
from __future__ import print_function
import sys, os
import functools
import subprocess
import time
from threading import Thread
# 做python2.7和3的兼容
if sys.version_info[:2] < (3, 0):  # 做print在python2和3的兼容，使python2中的print可以使用end、flush等关键字
    old_print = print
    def print(*args, **kwargs):
        flush = kwargs.pop('flush', False)
        old_print(*args, **kwargs)
        if flush:
            file = kwargs.get('file', sys.stdout)
            file.flush() if file is not None else sys.stdout.flush()

print = functools.partial(print, flush=True)  # 将print的flush=True设为默认属性（能够将打印直接输出到屏幕）


class Popen:
    def __init__(self):
        self.process = None
        self.returncode = -1

    def __call__(self, command, shell=True, exit=True, user=None, timeout=None):
        """
        实例化后执行该函数
        封装subprocess的Popen,实时打印command的输出(阻塞)
        获取返回码和执行结果
        command: str shell命令
        shell: bool 是否执行shell
        exit: bool 命令返回为非0时是否强制结束
        user:  bool 以哪个用户执行命令
        timeout: int 规定命令执行的时间不能超过多少秒，超过后直接返回状态码0
        :return: (返回码, 执行结果)
        """
        try:
            self.result = ""
            self.is_timeout = False
            if user:
                command = self.run_as(command, user)
            self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()
            self.wait(timeout)
            self.returncode = self.process.wait() if not self.is_timeout else 0
            if self.returncode:  # 复用subprocess的报错机制
                raise subprocess.CalledProcessError(self.returncode, self.process)
            return (self.returncode, self.result)
        except Exception:
            print(Exception, self.result, flush=True)
            if exit: sys.exit(1)
            return (self.returncode, self.result)


    def run_as(self, command, user):
        """
        以什么用户的身份执行命令
        """
        return 'su - {user} -c "{command}"'.format(command=command, user=user)

    def worker(self):
        """
        实时输出和记录结果的线程函数
        """
        for line in iter(self.process.stdout.readline, b''):
            return_line = line.decode("gbk", "ignore")  # "utf-8"
            print(return_line, end="", flush=True)
            self.result += return_line

    def wait(self, timeout=None):
        """
        阻塞主进程直到执行完或超时
        """
        during = 0
        while self.process.poll() is None:
            time.sleep(1)
            during += 1
            if timeout and timeout <= during:  # 超时则退出
                self.is_timeout = True
                break

popen = Popen()