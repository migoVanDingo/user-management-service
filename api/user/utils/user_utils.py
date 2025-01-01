import bcrypt

class UserUtils:
    @staticmethod
    def hash_password(password):
        bytes = password.encode('utf-8') 
        salt = bcrypt.gensalt() 

        hash = bcrypt.hashpw(bytes, salt) 
        return hash.decode('utf-8')
    
    @staticmethod
    def verify_password(password, hash):
        userBytes = password.encode('utf-8') 
        hash = hash.encode('utf-8')

        # checking password 
        return bcrypt.checkpw(userBytes, hash)