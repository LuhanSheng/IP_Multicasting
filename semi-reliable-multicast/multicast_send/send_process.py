import socket
import threading
import time


class MulticastSendProcess:

    def __init__(self):
        self.mcast_group_ip = '239.0.0.1'
        self.mcast_group_port = 23456
        self.message_max_size = 2048
        self.base = 0
        self.next_seq_num = 0
        self.window_size = 4
        self.window_is_full = False
        self.window_is_ack = [False, False, False, False]
        self.window_is_nak = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.file_buffer = [[0, bytes(1000)],
                            [1, bytes(1000)],
                            [2, bytes(1000)],
                            [3, bytes(1000)],
                            [4, bytes(1000)],
                            [5, bytes(1000)],
                            [6, bytes(1000)],
                            [7, bytes(1000)],
                            [8, bytes(1000)],
                            [9, bytes(1000)]]

    def multicast_send(self, buffer_block):
        message = str(buffer_block[0]).encode() + buffer_block[1]
        self.sock.sendto(message, (self.mcast_group_ip, self.mcast_group_port))
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: message '+ str(buffer_block[0]) +' send finish')

    def send_buffer(self):
        buffer_length = len(self.file_buffer)
        while True:
            if buffer_length >= self.base and not self.window_is_full:
                self.multicast_send(self.file_buffer[self.next_seq_num])
                self.next_seq_num += 1
                self.window_is_full = False if self.next_seq_num - self.base < self.window_size else True

    def multicast_receive(self):
        while True:
            message, address = self.sock.recvfrom(self.message_max_size)
            current = int(message) - 48
            window_current = current - self.base
            if window_current <=3:
            	self.window_is_ack[window_current] = True
            print(current, address)
            # if self.base == current:
            #     self.base += 1
            #     self.window_is_full = False if self.next_seq_num - self.base < self.window_size else True
            #     print(self.next_seq_num, self.base)
            #     print(self.window_is_full)

    def check_window(self):
        while True:
            if self.window_is_ack[0]:
                self.window_is_ack.pop(0)
                self.window_is_ack.append(False)
                self.base += 1
                self.window_is_full = False if self.next_seq_num - self.base < self.window_size else True

    def run(self):
        thread_routines = [
            self.check_window,
            self.send_buffer,
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
