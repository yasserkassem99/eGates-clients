import pickle
from config import *
from Messages.Ack import Ack
from Messages.message_types import *
from utils.utils import *

class MessageHandler:
    def __init__(self, msg, server_socket):
        self.msg = msg
        self.server_socket = server_socket
        self.handle_message_scenario()

    # here we send the message to its path (switch case)
    def handle_message_scenario(self):
        message_type = self.msg.get("message_type")
        print(message_type)
        if message_type == SERVER_CONFIG_MESSAGE:
            if self.msg.get("ack"):
                ack_message = Ack()
                self.send_msg_to_server(ack_message.json())
            print(self.msg.get("config_data"))
        elif message_type == SESSION_TICKET:
            print(self.msg.get('ticket_id'))
        elif message_type == SESSION_CLOSE:
            print('close session')
        elif message_type == "PDF":
            self.write_pdf_file()


    def write_pdf_file(self):
        pdf_content = self.msg.get('data')
        with open(f'{get_project_root()}/pdf_files/Waybill.pdf', "wb") as f:
            f.write(pdf_content)

        

    # send message to client
    def send_msg_to_server(self, msg_obj=None):
        """
        serialize msg object to send it to server, send msg with header containe msg size,and its type
        """
        serialized_msg = pickle.dumps(msg_obj)
        msg_header = general_message_header(len(serialized_msg),BUFFER_LENGTH)
        full_msg = bytes(msg_header.encode("utf-8")) + serialized_msg

        # send msg to client
        self.server_socket.send(full_msg)

