
def evaluate(totalPacketNum):
    f = open('receive.txt', 'r')
    lines = f.readlines()
    s = set()
    l = []

    for line in lines:
        s.add(line[0:-1])
        l.append(line[0:-1])
        print(line[0:-1])

    print("Total number of received: ", len(s))
    print("Effective number of received: ", len(l))
    print("Percentage of received: ", len(l) / totalPacketNum * 100, "%")


if __name__ == '__main__':
    evaluate(52)
