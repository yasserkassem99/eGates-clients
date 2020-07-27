import socket
import pickle
import threading
from Messages.message_types import *
from config import *
from Controllers.message_receiving import (
    recive_header_message,
    recive_full_message
)
from Controllers.HandleMessage import MessageHandler
from Messages.ConfigMessage import ConfigMessage
from Messages.Session import Session
from utils.utils import *
from Controllers.FilesWatcher import FilesWatcher
class ClientSocket:
    def __init__(self):
        # create the server socket
        # TCP socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to server
        self.client_socket.connect((SERVER_HOST, SERVER_PORT))
        # new thread for listening
        listening_thread = threading.Thread(
            target=self.listen_for_message, name="listening_thread"
        )
        listening_thread.start()
        files_watcher_thread = threading.Thread(target=FilesWatcher,name='files_watcher_thread')
        files_watcher_thread.start()

    # listening for messages
    def listen_for_message(self):
        while True:
            message_size = recive_header_message(self.client_socket)
            if message_size:
                    full_message = recive_full_message(message_size, self.client_socket)
                    handle_message_thread = threading.Thread(
                        target=MessageHandler,
                        name="handle_message_thread",
                        args=[full_message, self.client_socket],
                    )
                    handle_message_thread.start()
            else:
                # print("Closed connection from:")
                continue

    # send message to server
    def send_msg(self, msg_obj=None):
        """
        serialize msg object to send it to server, send msg with header containe msg size,and its type
        """
        serialized_msg = pickle.dumps(msg_obj)
        msg_header = general_message_header(len(serialized_msg),BUFFER_LENGTH)
        full_msg = bytes(msg_header.encode("utf-8")) + serialized_msg
        # send msg to server
        self.client_socket.send(full_msg)


if __name__ == "__main__":
    x = ClientSocket()
    msg = ConfigMessage()
    msg1 = Session()
    msg2 = Session()
    msg.set_type(CLIENT_CONFIG_MESSAGE)
    msg1.set_type(SESSION_DATA)
    msg2.set_type(SESSION_CLOSE)
    x.send_msg(msg.json())
    x.send_msg(msg1.json())
    x.send_msg(msg2.json())

    
    
    
    
    
