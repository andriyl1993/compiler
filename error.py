
class Error(object):
    def __init__(self, msg=""):
        self.msg = "Error: " + str(msg)

    def print_mess(self):
        return self.msg