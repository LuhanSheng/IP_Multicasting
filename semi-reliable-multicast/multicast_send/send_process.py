import socket
import threading
import time


class MulticastSendProcess:

    def __init__(self):
        self.mcast_group_ip = '239.0.0.1'
        self.mcast_group_port = 23456
        self.message_max_size = 2048

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    def multicast_send(self):
        while True:
            message = "this message send via mcast !"
            self.sock.sendto(message.encode(), (self.mcast_group_ip, self.mcast_group_port))
            print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: message send finish')
            time.sleep(5)

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
    multicast_send_process = MulticastSendProcess()
    multicast_send_process.run()
