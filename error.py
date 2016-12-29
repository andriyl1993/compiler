
class Error(Exception):
    def __init__(self, msg, row=None, elem=None):
        self.error_message = 'Error: element - {0}.'.format(elem) + str(msg)
        super(Exception, self).__init__('Error: element - {0}. '.format(row, elem) + str(msg))

    def print_err(self, y, x):
        print "Row - %s. Column - %s. " % (y, x) + self.error_message