import sys
import socket
import struct
import threading
import time
import binascii


class MulticastSendProcess:

    def __init__(self):
        self.mcast_group_ip = '239.0.0.1'
        self.mcast_group_port = 23456
        self.message_max_size = 2048
        self.base = 0
        self.next_seq_num = 0
        self.window_size = 60
        self.window_is_full = False
        self.window_is_ack = [0 for i in range(self.window_size)]
        self.window_is_nak = [0, 0, 0, 0]
        self.total_nak_num = 0
        self.message_nak_num = {}
        self.group_size = 4
        self.struct = struct.Struct('IIII')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.block_num = 1000
        self.file_buffer = [[i, bytes(1000)] for i in range(self.block_num)]
        self.congestion_window = 1
        self.start = time.time()
        self.total_multicast = 0
        self.f = open('send.txt', 'w')

    def multicast_send(self, buffer_block):
        data = (buffer_block[0], 0, 0, len(buffer_block[1]))
        s = struct.Struct('IIII')
        packed_data = s.pack(*data) + buffer_block[1]
        self.sock.sendto(packed_data, (self.mcast_group_ip, self.mcast_group_port))
        self.total_multicast += 1
        self.f.write(str(self.total_multicast) + " " + str(self.congestion_window) + "\n\n" + str(self.total_multicast) + " " + str(self.congestion_window) + "\n")
        print(
            f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: message ' + str(buffer_block[0]) + ' send finish')

    def send_buffer(self):
        while True:
            if self.next_seq_num < self.block_num:
                self.multicast_send(self.file_buffer[self.next_seq_num])
                self.next_seq_num += 1
            else:
                break


    def run(self):
        thread_routines = [
            self.send_buffer,
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
