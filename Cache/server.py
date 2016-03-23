'''
Created on Mar 20, 2016

@author: oliver
'''

class server:
    '''
    classdocs
    '''
    db_conn = ()
    app = ()


    def __init__(self, db_conn, app):
        '''
        Constructor
        '''
        self.db_conn = db_conn 
        self.app = app
    def runserver(self):
        @self.app.route('/entry')
        def form_entry():
           return "Entry Point"
        
