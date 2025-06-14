import base64
import gzip
from io import BytesIO

# Paste the full base64-encoded string from your message here
base64_audio_data = """
611zdqtagymMxvAaDLLFgMlA6MoLZEAQmYFN87dCUueJ8xmjaxvkEh4ZewtgFRldqw3mCO3SGPJLyOjAgubDsTKLwcf8lu4nFQHYAg4QN8If8zEb0xZ5iDJ8On0YvVkOnNXldPcEjaxUW0kSy3Ib9mzUQ6JXH97e2rpF3IbpcyxGgiCppPgcu6hOzbLAowDnADhqUKwjKpzfCC2PAqyEv3EX6H"""  # Make sure to use the full base64 content


# Decompress the GZIP data
with gzip.GzipFile(fileobj=BytesIO(bytes(base64_audio_data))) as f:
    audio_data = f.read()

# Save the result as a .wav file
with open("output.wav", "wb") as audio_file:
    audio_file.write(audio_data)

print("Audio saved as output.wav")
