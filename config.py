
class config():
    def __init__(self):
        import MySQLdb
        self.__crunchUser = StringVar()
        self.__crunchPass = StringVar()
        self.__directory = StringVar()

        self.__RDSHost = StringVar()
        self.__PORT = 0
        self.__RDSUser = StringVar()
        self.__RDSPass = StringVar()
        self.__RDSDb = StringVar()

        self.__sender_email = StringVar() # Enter your address
        self.__receiver_email = StringVar()  # Enter receiver address
        self.__password = StringVar()

        self.MySQLdb = MySQLdb
        self.mydb = self.MySQLdb.connect(host = self.__RDSHost,
            port=self.__PORT,
            user = self.__RDSUser,
            passwd = self.__RDSPass,
            db = self.__RDSDb)

    def getDirectory(self):
        return self.__directory

    def getRadUser(self):
        return self.__crunchUser

    def getRadPass(self):
        return self.__crunchPass
