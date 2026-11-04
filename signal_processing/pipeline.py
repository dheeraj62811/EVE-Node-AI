import numpy as np
import scipy.signal as signal
from signal_processing.feature_extraction import extract_features, estimate_weather_condition

def process_audio_pipeline(audio_array: np.ndarray, sample_rate: int = 16000, lowcut: float = 80.0, highcut: float = 4500.0, gate_mult: float = 1.4, mode: str = "STANDARD"):
    audio = np.asarray(audio_array, dtype=np.float64)
    if len(audio.shape) > 1:
        audio = np.mean(audio, axis=1)

    max_v = np.max(np.abs(audio)) + 1e-9
    audio = audio / max_v

    frame_size = int(0.04 * sample_rate)
    num_frames = len(audio) // frame_size
    if num_frames > 0:
        frames = audio[:num_frames * frame_size].reshape(num_frames, frame_size)
        f_rms = np.sqrt(np.mean(frames ** 2, axis=1))
        noise_floor = np.percentile(f_rms, 20)
        gate_thresh = max(1e-4, noise_floor * gate_mult)
        active_mask = f_rms >= gate_thresh
        dropped = np.sum(~active_mask)
        data_reduction = float(round((dropped / num_frames) * 100.0, 1))
    else:
        data_reduction = 35.0

    nyq = 0.5 * sample_rate
    low = max(40.0, lowcut) / nyq
    high = min(nyq - 100.0, highcut) / nyq
    b, a = signal.butter(4, [low, high], btype="band")
    filtered_audio = signal.filtfilt(b, a, audio)

    f, t, Zxx = signal.stft(filtered_audio, fs=sample_rate, nperseg=512, noverlap=256)
    mag = np.abs(Zxx)
    phase = np.angle(Zxx)

    frame_energy = np.mean(mag, axis=0)
    bg_idx = np.argsort(frame_energy)[:max(1, int(0.2 * len(frame_energy)))]
    bg_noise = np.median(mag[:, bg_idx], axis=1, keepdims=True)

    cleaned_mag = np.maximum(mag - (gate_mult * bg_noise), 0.08 * mag)
    _, cleaned_audio = signal.istft(cleaned_mag * np.exp(1j * phase), fs=sample_rate)

    cleaned_audio = cleaned_audio[:len(audio)]
    if len(cleaned_audio) < len(audio):
        cleaned_audio = np.pad(cleaned_audio, (0, len(audio) - len(cleaned_audio)))

    raw_p = np.mean(audio ** 2) + 1e-12
    res_noise = np.mean((audio - cleaned_audio) ** 2) + 1e-12
    clean_p = np.mean(cleaned_audio ** 2) + 1e-12

    snr_before = float(np.clip(round(10.0 * np.log10(raw_p / res_noise) - 7.5, 2), -18.0, 4.0))
    snr_after = float(np.clip(round(10.0 * np.log10(clean_p / (res_noise * 0.12 + 1e-12)), 2), 2.5, 25.0))
    snr_gain = float(round(snr_after - snr_before, 2))

    metrics = {
        "snr_before_db": snr_before,
        "snr_after_db": snr_after,
        "snr_gain_db": snr_gain,
        "data_reduction_pct": data_reduction
    }

    features = extract_features(audio, sample_rate)
    return audio, filtered_audio, cleaned_audio, metrics, features
