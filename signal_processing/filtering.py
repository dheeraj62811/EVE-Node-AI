import scipy.signal as signal

def apply_bandpass(data, sr, lowcut=250.0, highcut=3500.0, order=4):
    """Strips sub-250Hz wind rumble and high-frequency hiss."""
    nyq = 0.5 * sr
    b, a = signal.butter(order, [lowcut / nyq, highcut / nyq], btype='band')
    return signal.filtfilt(b, a, data)

def apply_insect_notch(data, sr, insect_freq=4200.0, quality_factor=30.0):
    """Surgical Notch Filter to remove continuous cicada/insect frequency band."""
    nyq = 0.5 * sr
    if insect_freq >= nyq:
        return data
    b, a = signal.iirnotch(insect_freq / nyq, quality_factor)
    return signal.filtfilt(b, a, data)
