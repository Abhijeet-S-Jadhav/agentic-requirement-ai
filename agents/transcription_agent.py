import whisper
import os

class TranscriptionAgent:
    def __init__(self):
        # We use the 'base' model. It's a good balance of speed and accuracy for free local use.
        # Options: tiny, base, small, medium, large (larger = slower but more accurate)
        print("Loading Local Whisper Model (this may take a moment)...")
        self.model = whisper.load_model("base")

    def transcribe_audio(self, audio_file_path):
        """
        Transcribes audio file to text using Local Whisper (CPU/GPU).
        """
        if not os.path.exists(audio_file_path):
            return {"error": "File not found"}

        try:
            print(f"Transcription Agent: Processing {audio_file_path} locally...")
            
            # The actual transcription happens here
            result = self.model.transcribe(audio_file_path)
            transcript_text = result["text"]
            
            print("✅ Transcription Complete.")
            return {"text": transcript_text}
        
        except Exception as e:
            return {"error": f"Transcription Failed: {str(e)}. Ensure FFmpeg is installed."}