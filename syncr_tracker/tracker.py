import pickle
import socket
import sys


def handle_request(data, addr):
    request = pickle.loads(data)

    if request[0] == 'GET':
        handle_get(data, addr)
    elif request[0] == 'POST':
        handle_post(data, addr)
    else:
        # Return some sort of error
        pass


def handle_get(data, addr):
    pass


def handle_post(data, addr):
    pass


def main():
    """

    :return:
    """
    TCP_IP = sys.argv[1]
    TCP_PORT = sys.argv[2]
    BUFFER_SIZE = 4096

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, int(TCP_PORT)))
    s.listen(1)

    while 1:
        conn, addr = s.accept()
        print('Connection address:', addr)
        while 1:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            handle_request(data, addr)
            print("Received data.")
            conn.send(data)  # echo
        conn.close()


if __name__ == "__main__":
    main()
