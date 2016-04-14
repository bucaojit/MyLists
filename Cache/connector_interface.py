import abc

#
#  Interface for Database Connectivity
#
class Connector(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def connect(self):
        return
    
    @abc.abstractmethod
    def disconnect(self):
        return

    @abc.abstractmethod
    def insert(self, values):
    # Insert form data into database
        return

    @abc.abstractmethod
    def delete(self, values):
    # Delete row/doc from database
        return
 
    @abc.abstractmethod
    def search(self, values):
    # Find entries matching search criteria
        return
    
