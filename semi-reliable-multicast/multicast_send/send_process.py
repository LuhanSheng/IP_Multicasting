import sys
import socket
import struct
import threading
import time
from buffer import buffer

class MulticastSendProcess:

    def __init__(self):
        self.mcast_group_ip = '239.0.0.1'
        self.mcast_group_port = 23456
        self.message_max_size = 2048
        self.base = 0
        self.next_seq_num = 0
        self.window_size = 10
        self.window_is_full = False
        self.window_is_ack = [0 for i in range(self.window_size)]
        self.window_is_nak = [0, 0, 0, 0]
        self.total_nak_num = 0
        self.message_nak_num = {}
        self.group_size = 4
        self.block_num = 2000
        self.struct = struct.Struct('IIII')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # Send block_num datagrams of 10000 bytes in size
        self.file_buffer = [[i, bytes(10000)] for i in range(self.block_num)]
        # Send file
        # self.file_buffer = buffer('test.mp4')
        self.block_num = len(self.file_buffer)
        self.congestion_window = 1
        self.timer = threading.Timer(0.03, self.resent_message)
        self.start = time.time()
        self.total_multicast = 0
        self.rate_total_multicast = 1
        self.ack_rate = 1
        self.f = open('send.txt', 'w')
        self.f2 = open('rate.txt', 'w')
        self.ack_num = 0 
        self.rate_ack_num = 1

    def multicast_send(self, buffer_block):
        data = (buffer_block[0], 0, 0, len(buffer_block[1]))
        s = struct.Struct('IIII')
        packed_data = s.pack(*data) + buffer_block[1]
        self.sock.sendto(packed_data, (self.mcast_group_ip, self.mcast_group_port))
        self.total_multicast += 1
        self.rate_total_multicast += 1
        self.f.write(str(self.total_multicast) + " " + str(self.congestion_window) + "\n\n" + str(self.total_multicast) + " " + str(self.congestion_window) + "\n")
        self.f2.write(str(self.total_multicast) + " " + str(self.ack_rate) + "\n\n" + str(self.total_multicast) + " " + str(self.ack_rate) + "\n")
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: message ' + str(buffer_block[0]) + ' send finish')

    def send_buffer(self):
        self.timer.start()
        # if window is not full, then send segment.
        while True:
            if self.block_num >= self.base and not self.window_is_full and self.next_seq_num - self.base < self.congestion_window and self.next_seq_num < self.block_num:
                # self.f.write((self.base) + " " + str(self.congestion_window))
                self.multicast_send(self.file_buffer[self.next_seq_num])
                self.next_seq_num += 1
                self.window_is_full = False if self.next_seq_num - self.base < self.window_size else True

    def multicast_receive(self):
        while True:
            data, address = self.sock.recvfrom(self.message_max_size)
            (message_id, is_ack, is_nak, message_length) = self.struct.unpack(data[0:16])
            window_current = message_id - self.base
            if is_ack:
                self.ack_num += 1
                self.rate_ack_num += 1
                if self.ack_num % (self.group_size * 10) == 0 and self.group_size > 3:
                    rate = self.rate_ack_num/self.rate_total_multicast
                    if rate > self.group_size/2:
                        self.ack_rate = 0.9 * self.ack_rate
                    elif rate <= self.group_size/2:
                        self.ack_rate = min(1.11 * self.ack_rate, 1)
                    else:
                        self.ack_rate = 1
                    self.rate_ack_num = 1 
                    self.rate_total_multicast = 1
                    data = (0, 1, 1, len(str(self.ack_rate).encode()))
                    s = struct.Struct('IIII')
                    packed_data = s.pack(*data) + str(self.ack_rate).encode()
                    self.sock.sendto(packed_data, (self.mcast_group_ip, self.mcast_group_port))

            if window_current <= self.window_size - 1:
                if is_ack and window_current >= 0:
                    self.window_is_ack[window_current] += 1
                    self.check_window()
                    print(message_id, "ACK", address)
                elif is_nak:
                    self.total_nak_num += 1
                    self.congestion_window = max(self.congestion_window - 1 / self.group_size, 1)
                    if self.message_nak_num.get(message_id) is None:
                        self.message_nak_num[message_id] = 1
                    else:
                        self.message_nak_num[message_id] += 1
                    print(message_id, "NAK", address)
                    self.check_nak(address, self.group_size * 10)
                else:
                    pass
            else:
                raise ValueError

#self.multicast_send([0, str(self.ack_rate)])

    def check_window(self):
        while self.window_is_ack[0] > 0:       
            self.window_is_ack.pop(0)
            self.window_is_ack.append(0)
            self.base += 1
            self.timer.cancel()
            self.new_timer()
            self.timer.start()
            self.congestion_window += 1
            self.window_is_full = False if self.next_seq_num - self.base < self.window_size else True

    def unicast_send(self, destination, message_id, is_ack, is_nak, message_length):
        data = (message_id, is_ack, is_nak, message_length)
        packed_data = self.struct.pack(*data)
        self.sock.sendto(packed_data, destination)

# self.group_size / 2
    def check_nak(self, address, num):
        if self.total_nak_num > num:
            while len(self.message_nak_num) > 0:
                buffer_id, nak_num = self.message_nak_num.popitem()
                if nak_num > 0:
                    self.multicast_send(self.file_buffer[buffer_id])
                    self.total_nak_num -= nak_num
                # else:
                #     self.unicast_send(address, message_id, 1, 0, 0)

    def resent_message(self):
        if self.base == self.block_num:
            self.check_nak("address", 0)
            print('Running time: %s Seconds'%str(time.time() - self.start))
            print('Total send number:', self.total_multicast)
            print('Total ACK number:', self.ack_num)
            print('Total block number:', self.block_num)
            print('Effeciency:', self.block_num/self.total_multicast)
            self.f.close()
            self.f2.close()
            sys.exit()
        print("resend message: ", self.base)
        self.timer.cancel()
        self.multicast_send(self.file_buffer[self.base])
        self.new_timer()
        self.timer.start()
        self.congestion_window = max(self.congestion_window / 2, 1)

    def new_timer(self):
        self.timer = threading.Timer(0.03, self.resent_message)

    def run(self):
        thread_routines = [
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
