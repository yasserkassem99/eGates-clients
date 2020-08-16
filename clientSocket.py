import sys
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
from Messages.Autocomplete import Autocomplete
from utils.utils import *
from Controllers.FilesWatcher import FilesWatcher
import eventlet
from socketio import Client,Server,WSGIApp


# socket as server
sio = Server(cors_allowed_origins='*')
app = WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})



class ClientSocket:
    def __init__(self,sio):
        self.sio = sio
        # create the server socket
        # TCP socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to server
        self.client_socket.connect((SERVER_HOST, SERVER_PORT))
        # new thread for listening
        self.listening_thread = threading.Thread(
            target=self.listen_for_message, name="listening_thread"
        )
        self.listening_thread.start()
        self.files_watcher_thread = threading.Thread(target=FilesWatcher,name='files_watcher_thread')
        self.files_watcher_thread.start()

    # listening for messages
    def listen_for_message(self):
        while True:
            message_size = recive_header_message(self.client_socket)
            if message_size:
                    full_message = recive_full_message(message_size, self.client_socket)
                    handle_message_thread = threading.Thread(
                        target=MessageHandler,
                        name="handle_message_thread",
                        args=[full_message, self.client_socket, self.sio],
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



#################################################################################
#event handlers for the connection where this device work as server for a client
#################################################################################
@sio.event
def connect(sid, environ):
    print('connect ', sid)
    

@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    
    
@sio.event
def my_message(sid, environ):
    print('my_message ', sid)
    configMessage = ConfigMessage()
    configMessage.set_type(CLIENT_CONFIG_MESSAGE)
    client.send_msg(configMessage.json())


client = ClientSocket(sio)

if __name__ == "__main__":
    # x = ClientSocket()
    # msg = ConfigMessage()
    # msg.set_type(CLIENT_CONFIG_MESSAGE)
    # x.send_msg(msg.json())
    eventlet.wsgi.server(eventlet.listen(('192.168.1.10', 5001)), app)


    
    
    
    
    
