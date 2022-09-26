import time
import logging
from gevent import socket
import uopy
import UOFastConfig

class Connection(object):
    """A base connection class.

    Arbitrary connections can be defined by extending this class.
    """

    def open(self):
        """Opens a connection."""

        raise NotImplementedError()

    def close(self):
        """Closes the connection."""

        raise NotImplementedError()

    def get(self):
        """Returns the raw connection."""
        raise NotImplementedError()

    def is_connected(self):
        """Returns whether the connection has been established.

        :rtype: bool
        """
        raise NotImplementedError()

    def is_expired(self):
        """Returns whether the connection is expired.

        :rtype: bool
        """
        return False

    def reconnect(self):
        """Attempts to reconnect the connection."""

        try:
            if self.is_connected():
                self.close()
            self.open()
        except:
            logging.exception('Failed to reconnect')


class m_connection(Connection):
    """TCP connection pool of UOPY objects
    :param str host: Hostname.
    :param int port: Port.
    :param int lifetime: Maximum lifetime (in seconds) of the connection.
    :param int timeout: Socket timeout.
    """
    logger=None

    def __init__(self, user, pw, lifetime=600, timeout=None):
        self.configparams = None #UOFastConfig.UOFastConfiguration()
        self.logger=None
        self._lifetime = lifetime
        self._timeout = timeout
        self._connected = False
        self._created = None
        self._busy = None
        self.sessport=""
        
        self._sock = self.uconnect(user, pw)
        
    def uconnect(self, uuser, pw):
        
        self.configparams = UOFastConfig.uofastconfiguration()
          
        try:
            conn = uopy.connect(host =self.configparams.UOhost, 
            user = self.configparams.UOuser,
            password = self.configparams.UOpassword,
            account = self.configparams.UOaccount,
            service=self.configparams.UOservice, 
            port=self.configparams.UOport)
            
            self.sessport = str(conn.get_atvar(uopy.AtVar.USER_NO))
            sessionlogfile = self.configparams.UOConnectionLogs.replace(".log",self.sessport + ".log")    
            
            self.logger = UOFastConfig.uofastlogging(self.sessport, sessionlogfile).logger
            self.logger_info("Connected to uopy")
            self.logger_info(sessionlogfile)
            
            self._connected = True
        except uopy.UOError as  e:
            print("Error " , e.message)
        return conn
    
    def logger_info(self, msg):
        #self.logger = logging.getLogger(self.sessport) 
        self.logger.info(msg)
    
    @property
    def socket(self):
        return self._sock

    def get(self):
        return self._sock

    def open(self):
        if self._timeout:
            self._sock.settimeout(self._timeout)

        self._connected = True
        self._created = time.time()

    def close(self):
        if self._connected:
            print("closing connection..")
            self._sock.close()
            self._connected = False

    def is_connected(self):
        return self._connected

    def is_expired(self):
        if time.time() - self._created > self._lifetime:
            return True
        else:
            return False

    def send(self, data):
        assert self._connected

        self._sock.send(data)

    def recv(self, size=1024):
        assert self._connected

        return self._sock.recv(size)
