from Messages.Message import Message


class Autocomplete(Message):
    def __init__(self):
        super().__init__()
        self.tn = None
        self.driver_phone = None
        self.driver_nn = None
        self.bond_number = None

    def set_tn(self, tn):
        self.tn = tn
    def set_driver_phone(self, driver_phone):
        self.driver_phone = driver_phone
    def set_driver_nn(self, driver_nn):
        self.driver_nn = driver_nn
    def set_bond_number(self, bond_number):
        self.bond_number = bond_number
