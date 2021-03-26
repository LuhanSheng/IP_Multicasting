# -*- coding: utf-8 -*-

import socket
import time

#client 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
PORT = 3662

while True:
      start = time.time()  #获取当前时间
      print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(start)))  #以指定格式显示当前时间
      msg=input("本客户端10.0.0.1，请输入要发送的内容：")  
      server_address = ("localhost", PORT)  # 接收方 服务器的ip地址和端口号
      client_socket.sendto(str.encode(msg), server_address) #将msg内容发送给指定接收方
      now = time.time() #获取当前时间
      run_time = now-start #计算时间差，即运行时间
      print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now)))
      print("run_time: %d seconds\n" %run_time)
