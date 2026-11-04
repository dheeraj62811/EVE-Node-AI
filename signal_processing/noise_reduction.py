import numpy as np
import librosa

def spectral_denoise(data, sr, n_fft=1024, hop_length=512, gate_multiplier=1.6):
    """Estimates stationary rain noise from initial frames and gates the STFT spectrum."""
    stft = librosa.stft(data, n_fft=n_fft, hop_length=hop_length)
    mag, phase = np.abs(stft), np.angle(stft)
    
    # Use first 0.5 seconds as ambient noise profile
    noise_frames = max(1, int((0.5 * sr) / hop_length))
    noise_profile = np.mean(mag[:, :noise_frames], axis=1, keepdims=True)
    
    # Soft spectral mask
    mask = np.where(mag > (noise_profile * gate_multiplier), 1.0, 0.05)
    cleaned_mag = mag * mask
    
    cleaned_stft = cleaned_mag * np.exp(1j * phase)
    return librosa.istft(cleaned_stft, hop_length=hop_length, length=len(data))
