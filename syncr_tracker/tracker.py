import base64
import datetime
import hashlib
import os
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
    """
    Dispatches GET and POST requests
    :param conn: TCP socket connection between server and client
    :param request: [POST/GET, node/drop id, potential value data]
    :param addr: (IP, port)
    :return:
    """
    if request[TYPE_INDEX] == 'GET':
        print("GET request")
        handle_get(conn, request, addr)
    elif request[TYPE_INDEX] == 'POST':
        print("POST request")
        handle_post(conn, request)
    else:
        # Return some sort of error
        pass


def handle_get(conn, request, addr):
    pass


def handle_post(conn, request):
    """
    Dispatches POST requests
    :param conn: TCP socket connection between server and client
    :param request: [POST, node/drop id, pubkey or node ip port tuple]
    :return:
    """
    if len(request[KEY_INDEX]) == NODE_ID_BYTE_SIZE:
        request_post_node_id(conn, request)
    if len(request[KEY_INDEX]) == DROP_ID_BYTE_SIZE:
        request_post_drop_id(conn, request)


def request_post_node_id(conn, request):
    """
    Adds the pubkey to disk if it is a legal pairing
    :param conn: TCP socket connection between server and client
    :param request: [POST, node_id, pubkey]
    :return:
    """
    if request[KEY_INDEX] == hashlib.sha256(request[VALUE_INDEX]
                                            .encode('utf-8')).digest():
        add_node_key_pairing(request)
        print('Node/Key pairing added')
        conn.send(bencode.encode('Node/Key pairing added'))
    else:
        print('Node/Key pairing rejected for mismatch key')
        conn.send(bencode.encode('Node/Key pairing rejected for mismatch key'))


def add_node_key_pairing(request):
    """
    Adds pubkey to disk
    :param request: [POST, node_id, pubkey]
    :return:
    """
    if not os.path.exists('pub_keys/'):
        os.makedirs('pub_keys/')
    with open(generate_node_key_file_name(request[KEY_INDEX]), "wb") \
            as pub_file:
        pub_file.write(request[VALUE_INDEX].encode('utf-8'))


def request_post_drop_id(conn, request):
    """
    Adds node, ip, port tuples to appropriate drops in hashmap
    :param conn: TCP socket connection between server and client
    :param request: [POST, drop_id, [node_id, IP, port]]
    :param addr: (IP, port)
    :return:
    """
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


def generate_node_key_file_name(node_id):
    """
    Takes a node key provides where it's public key is stored
    :param node_id:
    :return: public key file
    """
    return "pub_keys/{}.pub".format(base64.b64encode(node_id, altchars=b'+-')
                                    .decode('utf-8'))


def main():
    """
    Runs the server loop taking in GET and POST requests and handling them
    accordingly
    :return:
    """
    tcp_ip = sys.argv[1]
    tcp_port = sys.argv[2]
    buffer_size = 4096

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((tcp_ip, int(tcp_port)))
    s.listen(5)

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
