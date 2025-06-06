from abc import ABC, abstractmethod


class TTSService(ABC):
    @abstractmethod
    def generate_speech(self, text):
        pass
