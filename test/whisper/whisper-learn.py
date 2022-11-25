import whisper
import os
model = whisper.load_model("base")

# load audio and pad/trim it to fit 30 seconds
mp3File = os.path.abspath("./1.mp3")
print(os.path.exists(mp3File), mp3File)
audio = whisper.load_audio(mp3File)
audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
options = whisper.DecodingOptions()
result = whisper.decode(model, mel, options)

# print the recognized text
print(result.text)