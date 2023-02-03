
class AuthService(object):
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AuthService, cls).__new__(cls)
        return cls.instance
            
    def __init__(self):
        
        self.__is_authenticated = False
        self.__credentials = None
        
    def is_authenticated(self):
        return self.__is_authenticated
        
    def authenticate_with_credentials(self, creds):
        self.__is_authenticated = True
        self.__credentials = creds