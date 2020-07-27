import pickle
from config import *
import socket
from utils.utils import get_project_root

def recive_header_message(client_socket):
    # get message header(size), recive only HEADER_LENGTH bytes
    msg_header = client_socket.recv(HEADER_LENGTH)
    if not msg_header:
        return (None, None)
    header = msg_header.decode("utf-8").split("_")
    message_size = int(header[0])
    message_type = header[1]
    if message_type:
        return (message_size, message_type)
    return (message_size, None)


def recive_full_message(message_size, client_socket):
    full_msg = client_socket.recv(message_size)
    msg_obj = pickle.loads(full_msg)
    return msg_obj


def recive_pdf_message(message_size, client_socket):
    with open(f'{get_project_root()}/pdf_files/Waybill.pdf', "wb") as f:
            bytes_read = client_socket.recv(message_size, socket.MSG_WAITALL)
            f.write(bytes_read)

