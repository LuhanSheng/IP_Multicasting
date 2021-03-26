from receive_process import MulticastSendProcess


def main():
    multicast_send_process = MulticastSendProcess()
    multicast_send_process.run()


if __name__ == '__main__':
    main()
