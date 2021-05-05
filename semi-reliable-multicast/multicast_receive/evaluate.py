
def evaluate(ip, totalPacketNum):
    f = open(str(ip) + '_receive.txt', 'r')
    lines = f.readlines()
    s = set()
    l = []

    for line in lines:
        s.add(line[0:-1])
        l.append(line[0:-1])

    print("Total number of received: ", len(l))
    print("Effective number of received: ", len(s))
    print("Percentage of received: ", len(s) / totalPacketNum * 100, "%")


if __name__ == '__main__':
    import socket
    s = "0.26".encode()
    d = float(s)
    print(d)
    # print([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
    #            [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
    # evaluate(52)
