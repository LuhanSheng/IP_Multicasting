import socket
import struct
import threading
import time
import random

class MulticastReceiveProcess:
    def __init__(self):
        self.mcast_group_ip = '239.0.0.1'
        self.mcast_group_port = 23456
        self.message_max_size = 2048
        self.window_size = 4
        self.base = 0
        self.window_is_received = [-1, -1, -1, -1]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.struct = struct.Struct('IIII')

    def multicast_receive(self):
        self.sock.bind(("0.0.0.0", self.mcast_group_port))
        # 加入组播组
        mreq = struct.pack("=4sl", socket.inet_aton(self.mcast_group_ip), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        while True:
            data, address = self.sock.recvfrom(self.message_max_size)
            if random.random() < 0.5:
                continue
            (message_id, is_ack, is_nak, message_length) = self.struct.unpack(data[0:16])
            self.unicast_send(address, message_id, 1, 0, 0)
            message = data[16:]
            print(
                f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Receive data from {address}: {message_id}')
            current = message_id - self.base
            if current > 0:
                for i in range(self.base, message_id):
                    self.unicast_send(address, i, 0, 1, 0)
                    self.base += 1
                self.base += 1
            elif current == 0:
                self.base += 1
            else:
                pass

    def unicast_send(self, destination, message_id, is_ack, is_nak, message_length):
        data = (message_id, is_ack, is_nak, message_length)
        packed_data = self.struct.pack(*data)
        self.sock.sendto(packed_data, destination)


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
    l = range(4,8)
    for i in l:
        print(i)
    # multicast_receive_process = MulticastReceiveProcess()
    # multicast_receive_process.run()
