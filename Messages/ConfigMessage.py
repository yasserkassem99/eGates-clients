import os
from Messages.Message import Message


class ConfigMessage(Message):
    def __init__(self):
        super().__init__()
        """
        Message of type config sent from server.
        attributes:
        1- message_type
        2- config_data
        """
        self.config_data = None
        self.ack = True
        

    def get_config_data(self):
        return self.config_data

    def set_config_data(self, data):
        self.config_data = data

