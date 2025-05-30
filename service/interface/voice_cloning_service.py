from abc import ABC, abstractmethod


class VoiceCloningService(ABC):
    @abstractmethod
    def get_speaker_audio(self, reference_audio_url: str) -> str:
        """
        Get speaker audio in base64 format from the reference audio URL.
        """
        pass

    @abstractmethod
    def generate_speech(self, base64_audio: str, text: str) -> bytes:
        """
        Generate speech using the base64 audio and the provided text.
        """
        pass