
def evaluate(ip, totalPacketNum):
    f = open(str(ip) + '_receive.txt', 'r')
    lines = f.readlines()
    s = set()
    l = []

    for line in lines:
        s.add(line[0:-1])
        l.append(line[0:-1])
        print(line[0:-1])

    print("Total number of received: ", len(l))
    print("Effective number of received: ", len(s))
    print("Percentage of received: ", len(s) / totalPacketNum * 100, "%")


if __name__ == '__main__':
    import socket

    # 获取计算机名称
    hostname =
    # 获取本机IP
    ip = socket.gethostbyname(socket.gethostname())
    print(ip)
    # evaluate(52)
