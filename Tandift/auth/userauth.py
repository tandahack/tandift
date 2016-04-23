import hashlib, string, random

#TODO Temporary, used until sqlite3 DB established
accounts = {}

class UserAuthentication:
    def __init__(self):
        pass

    def createUser(self, username, password):
        salt = "salt".encode('utf-8')
        saltedHash = hashlib.sha256(salt+password.encode('utf-8')).hexdigest()
        accounts[username] = (saltedHash, salt)

    def deleteUser(self, username):
        del accounts[username]

    def checkPassword(self, username, password):
        salt = accounts[username][1].decode('utf-8')
        saltedHash = hashlib.sha256((salt+password).encode('utf-8')).hexdigest()
        return saltedHash == accounts[username][0]

    def generateSalt(self, saltLength=5):
        salt = ""
        charList = string.ascii_letters + string.digits
        for x in range(saltLength):
            salt += random.choice(charList)
        print(salt)
        return(salt)

