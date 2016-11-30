
class Error(Exception):
    def __init__(self, msg, row=None, elem=None):
        super(Exception, self).__init__('Error: index element - {0}, element - {1}. '.format(row, elem) + str(msg))