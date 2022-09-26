from configparser import ConfigParser
import ast
import logging

class uofastconfiguration(object):

    def __init__(self):
        UOhost = ""
        UOaccount = ""
        UOservice = ""
        UOport = 0
        UOuser = ""
        UOpassword = ""
        initial_connections = 0
        max_connections = 0
        session_timeout = 0
        reap_interval = 0
        Mainlogname = ""
        UOConnectionLogs = ""

        config = ConfigParser()

        try:
            config.read('UOFast.cfg')
        except Exception as e:
            print("System exception reading UOFast.cfg")
            print(str(e))
            quit
        
        # UOPY connection settings
        self.UOhost     = config.get('UOConnectionSettings', 'UOhost')
        self.UOaccount  = config.get('UOConnectionSettings', 'UOaccount')
        self.UOservice  = config.get('UOConnectionSettings', 'UOservice')
        self.UOport     = int(config.get('UOConnectionSettings', 'UOport'))
        self.UOuser     = config.get('UOConnectionSettings', 'UOuser')
        self.UOpassword = config.get('UOConnectionSettings', 'UOpassword')
        
        # Pool Connection variabled
        self.initial_connections = int(config.get('PoolSettings', 'initial_connections'))
        self.max_connections = int(config.get('PoolSettings', 'max_connections'))
        self.session_timeout = int(config.get('PoolSettings', 'session_timeout'))
        self.reap_interval = int(config.get('PoolSettings', 'reap_interval'))
       
        # Application settings
        self.Mainlogname = config.get('ApplicationSettings', 'Mainlogname')
        self.UOConnectionLogs = config.get('ApplicationSettings', 'UOConnectionLogs')
        
class uofastlogging(object):

    # Gets or creates a logger
    logger = logging.getLogger(__name__)  

    def __init__(self, logger_name, logfilename):
        # set log level        
        
        # define file handler and set formatter
        self.setup_logger(logger_name, logfilename, level=logging.INFO, logdir="uofastlogs")
        
    def setup_logger(self, logger_name, log_file, level=logging.INFO, logdir="uofastlogs"):
        l = logging.getLogger(logger_name)
        formatter = logging.Formatter('%(asctime)s %(message)s')
        fileHandler = logging.FileHandler(logdir + "\\" + log_file, mode='w')
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)

        l.setLevel(level)
        l.addHandler(fileHandler)
        l.addHandler(streamHandler)    
        self.logger = l