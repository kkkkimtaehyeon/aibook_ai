import base64

from zyphra import ZyphraClient


def generate_speech_with_voice_cloning(text, reference_audio_path, output_path):
    try:
        # 1. Read and Encode the Audio File
        with open(reference_audio_path, "rb") as f:
            audio_base64 = base64.b64encode(f.read()).decode('utf-8')

        # 2. Initialize the Zyphra Client
        client = ZyphraClient(api_key="zsk-19fd7847a6f53851a25eb97555d7b8a19a253972a958dcaa504be01f0c8d38d4")  # Replace with your API key

        # 3. Make the API Call
        output_path = client.audio.speech.create(
            text=text,
            language_iso_code="ko",  # IMPORTANT: Set the correct language!
            speaking_rate=15,  # Adjust as needed
            spaker_audio=audio_base64,  # Use the base64 encoded audio
            output_path=output_path,
        )

        print(f"Voice cloning successful. Audio saved to: {output_path}")
        return output_path

    except FileNotFoundError:
        print(f"Error: Reference audio file not found at: {reference_audio_path}")
        return None
    except Exception as e:
        print(f"An error occurred during voice cloning: {e}")
        return None


generate_speech_with_voice_cloning("안녕하세요 오디오 테스트입니다.", "./my.wav", "./output_audio.wav")