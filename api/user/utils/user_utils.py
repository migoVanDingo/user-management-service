import random
import secrets
import string
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
    
    @staticmethod
    def generate_plaintext_token(length: int = 25) -> str:
        """
        Generate a secure random plaintext token.

        Args:
            length (int): Length of the generated token (default is 25).

        Returns:
            str: Randomly generated plaintext token.
        """
        characters = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(characters) for _ in range(length))
        return token