import numpy as np
from scipy.io import wavfile
from scipy.fft import rfft, rfftfreq

def wav_to_ascii(filename, base_freq=0, tone_duration=0.2):
    # Read WAV file
    sample_rate, data = wavfile.read(filename)
    
    # Convert to mono if stereo
    if data.ndim > 1:
        data = data.mean(axis=1)
    
    # Calculate samples per tone
    samples_per_tone = int(sample_rate * tone_duration)
    num_tones = len(data) // samples_per_tone
    
    ascii_string = []
    
    for i in range(num_tones):
        # Extract tone segment
        start = i * samples_per_tone
        end = start + samples_per_tone
        segment = data[start:end]
        
        # Compute FFT
        fft_result = rfft(segment)
        fft_magnitude = np.abs(fft_result)
        frequencies = rfftfreq(len(segment), 1/sample_rate)
        
        # Find dominant frequency
        dominant_freq = frequencies[np.argmax(fft_magnitude)]
        print(dominant_freq)
        
        # Convert to ASCII (adjust base_freq as needed)
        ascii_val = int(round(dominant_freq - base_freq)/1000)
        ascii_string.append(chr(ascii_val))
    
    return ''.join(ascii_string)

# Usage example
base_freq = 220 # Adjust based on encoding scheme
tone_duration = 0.75  # Duration per character in seconds

result = wav_to_ascii("output.wav", 
                      base_freq=base_freq,
                      tone_duration=tone_duration)
print("Decoded message:", result)
