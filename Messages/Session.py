from Messages.Message import Message


class Session(Message):
    def __init__(self):
        super().__init__()
        self.session_id = "20200722"
        self.session_data = {"data": {"tn": 605748, "trn": 704518}}
        self.ticket_id = None

    def get_session_id(self):
        return self.session_id

    def set_session_id(self, id):
        self.session_id = id
