from abc import ABC, abstractmethod

class AuthInterface(ABC):
    @abstractmethod
    def verify_login(self, email, password):
        """
        Verify user credentials and return login status.
        """
        pass

    @abstractmethod
    def register(self, name, email, password, is_verified):
        """
        Register a new user and return registration status.
        """
        pass
