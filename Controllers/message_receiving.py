import pickle
from config import *
import socket
from utils.utils import get_project_root

def recive_header_message(client_socket):
    # get message header(size), recive only HEADER_LENGTH bytes
    msg_header = client_socket.recv(HEADER_LENGTH)
    if not msg_header:
        return 
    header = msg_header.decode("utf-8")
    message_size = int(header)
    return message_size


def recive_full_message(message_size, client_socket):
    full_msg = client_socket.recv(message_size,socket.MSG_WAITALL)
    msg_obj = pickle.loads(full_msg)
    return msg_obj
