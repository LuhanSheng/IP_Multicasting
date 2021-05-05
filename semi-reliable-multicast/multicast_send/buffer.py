def buffer(filename):
    buf = []
    f = open(filename, 'rb')
    lines = f.read()
    size = 2000
    packet_num = int(len(lines) / size)
    for i in range(0, packet_num):
        temp_buf = [i, lines[i * size: (i + 1) * size]]
        buf.append(temp_buf)
    return buf

if __name__ == '__main__':
    buffer = buffer('test.mp4')
    f = open('new.mp4', 'wb')
    for b in buffer:
        f.write(b[1])
    f.close()
