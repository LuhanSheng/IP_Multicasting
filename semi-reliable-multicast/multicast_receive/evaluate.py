
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
    l = [0 for i in range(4)]
    print(l)
    evaluate(52)
