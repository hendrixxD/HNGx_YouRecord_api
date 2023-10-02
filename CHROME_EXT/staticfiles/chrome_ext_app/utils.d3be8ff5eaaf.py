from pydub import AudioSegment

def extract_audio(video_file):
    # Extract audio from the video and return audio data
    video_path = 'media/' + video_file.name
    audio = AudioSegment.from_file(video_path)
    audio_data = audio.raw_data
    return audio_data

def transcribe_audio(audio_data):
    # Transcribe audio using OpenAI Whisper API
    response = openai.Transcription.create(model="whisper", audio=audio_data)
    transcription = response['text']
    return transcription
