
class Error(Exception):
    def __init__(self, msg, row=None, elem=None):
        self.error_message = 'Error: index element - {0}, element - {1}.'.format(row, elem) + str(msg)
        super(Exception, self).__init__('Error: index element - {0}, element - {1}. '.format(row, elem) + str(msg))

    def print_err(self, y, x):
        print "Row - %s. Column - %s. " % (y, x) + self.error_message