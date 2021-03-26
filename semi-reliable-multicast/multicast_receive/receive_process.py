import socket
import struct
import sys
import threading
import time


class MulticastReceiveProcess:
    def __init__(self):
        self.mcast_group_ip = '239.0.0.1'
        self.mcast_group_port = 23456
        self.message_max_size = 2048

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    def multicast_send(self):
        self.sock.bind(("0.0.0.0", self.mcast_group_port))
        # 加入组播组
        mreq = struct.pack("=4sl", socket.inet_aton(self.mcast_group_ip), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        while True:
            try:
                message, addr = self.sock.recvfrom(self.message_max_size)
                print(
                    f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Receive data from {addr}: {message.decode()}')
            except:
                print("while receive message error occur")
                sys.exit()

    def multicast_receive(self):
        while True:
            message, address = self.sock.recvfrom(self.message_max_size)
            print(message, address)

    def run(self):
        thread_routines = [
            self.multicast_send,
            self.multicast_receive
        ]
        threads = []
        for thread_routine in thread_routines:
            thread = threading.Thread(target=thread_routine)
            thread.daemon = True
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()


if __name__ == '__main__':
    multicast_receive_process = MulticastReceiveProcess()
    multicast_receive_process.run()
