import datetime
import socket
import sys

import bencode
from constants import DROP_ID_BYTE_SIZE
from constants import DROP_IP_INDEX
from constants import DROP_NODE_INDEX
from constants import DROP_PORT_INDEX
from constants import KEY_INDEX
from constants import NODE_ID_BYTE_SIZE
from constants import TYPE_INDEX
from constants import VALUE_INDEX

drop_availability = dict()


def handle_request(conn, request, addr):
    if request[TYPE_INDEX] == 'GET':
        print("GET request")
        handle_get(conn, request, addr)
    elif request[TYPE_INDEX] == 'POST':
        print("POST request")
        handle_post(conn, request, addr)
    else:
        # Return some sort of error
        pass


def handle_get(conn, request, addr):
    pass


def handle_post(conn, request, addr):
    if len(request[KEY_INDEX]) == NODE_ID_BYTE_SIZE:
        request_post_node_id(conn, request, addr)
    if len(request[KEY_INDEX]) == DROP_ID_BYTE_SIZE:
        request_post_drop_id(conn, request, addr)


def request_post_node_id(conn, request, addr):
    pass


def request_post_drop_id(conn, request, addr):
    if request[KEY_INDEX] in drop_availability.keys():
        drop_availability[request[KEY_INDEX]].append(
            request[VALUE_INDEX].append(datetime.datetime),
        )
    else:
        drop_availability[request[KEY_INDEX]] = [
            request[VALUE_INDEX].append(datetime.datetime),
        ]
    print(
        "Drop Availability Updated - ", request[KEY_INDEX],
        "\n\tNode: ", request[VALUE_INDEX][DROP_NODE_INDEX],
        "\n\tIP: ", request[VALUE_INDEX][DROP_IP_INDEX],
        "\n\tPort: ", request[VALUE_INDEX][DROP_PORT_INDEX],
    )
    conn.send(bencode.encode('Drop availability updated'))


def main():
    """

    :return:
    """
    tcp_ip = sys.argv[1]
    tcp_port = sys.argv[2]
    buffer_size = 4096

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((tcp_ip, int(tcp_port)))
    s.listen(1)

    while 1:
        conn, addr = s.accept()
        print('Connection address:', addr)
        while 1:
            data = conn.recv(buffer_size)
            if not data:
                break
            print('Data received')
            request = bencode.decode(data)
            handle_request(conn, request, addr)
        conn.close()


if __name__ == "__main__":
    main()
