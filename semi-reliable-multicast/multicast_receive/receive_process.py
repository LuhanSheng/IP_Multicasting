import socket
import struct
import threading
import time
import random
from evaluate import evaluate

class MulticastReceiveProcess:
    def __init__(self):
        self.mcast_group_ip = '239.0.0.1'
        self.mcast_group_port = 23456
        self.message_max_size = 2048
        self.window_size = 4
        self.base = 0
        self.window_is_received = [-1, -1, -1, -1]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.connect(('8.0.0.1', 80))
        self.ip = self.sock.getsockname()[0]
        self.struct = struct.Struct('IIII')
        self.total_packet_num = 200
        self.cached_block_num = set()
        self.timer = threading.Timer(10, self.exit)
        self.f = open(str(self.ip) + '_receive.txt', 'w')

    def multicast_receive(self):
        self.sock.bind(("0.0.0.0", self.mcast_group_port))
        # 加入组播组
        mreq = struct.pack("=4sl", socket.inet_aton(self.mcast_group_ip), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        while True:
            data, address = self.sock.recvfrom(self.message_max_size)
            self.timer.cancel()
            self.new_timer()
            self.timer.start()
            if random.random() < 0.1:
                continue
            (message_id, is_ack, is_nak, message_length) = self.struct.unpack(data[0:16])
            self.unicast_send(address, message_id, 1, 0, 0)
            message = data[16:]
            self.f.write(str(message_id) + "\n")
            print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Receive data from {address}: {message_id}')
            current = message_id - self.base
            if current > self.window_size:
                self.base = message_id - self.window_size
            elif current > 0:
                self.cached_block_num.add(message_id)
                for i in range(self.base, message_id):
                    if i not in self.cached_block_num:
                        self.unicast_send(address, i, 0, 1, 0)
                        print("Send NAK", message_id)
            elif current == 0:
                self.base += 1
                while self.base in self.cached_block_num:
                    self.cached_block_num.remove(self.base)
                    self.base += 1
            else:
                pass
            if self.base == self.total_packet_num - 1:
                break
        f.close()
        evaluate(self.ip, self.total_packet_num)
        
    def unicast_send(self, destination, message_id, is_ack, is_nak, message_length):
        data = (message_id, is_ack, is_nak, message_length)
        packed_data = self.struct.pack(*data)
        self.sock.sendto(packed_data, destination)

    def exit(self):
        self.f.close()
        evaluate(self.ip, self.total_packet_num)  
        
    def new_timer(self):
        self.timer = threading.Timer(0.1, self.exit)

    def run(self):
        thread_routines = [
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
