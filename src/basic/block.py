from abs import ABC, abstractmethod

class Block(ABC):
    @property
    @abstractmethod
    def template(self):
        pass

