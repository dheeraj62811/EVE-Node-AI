import os
import numpy as np
from signal_processing.acquisition import acquire_or_synthesize_audio
from signal_processing.pipeline import process_audio_pipeline
from signal_processing.output import export_results

def run_pipeline(audio_source=None, lowcut=250.0, highcut=3500.0, gate_mult=1.6, mode="STANDARD"):
    sample_rate = 16000
    if audio_source is not None:
        audio, sample_rate = audio_source
    else:
        audio, sample_rate = acquire_or_synthesize_audio(sample_rate=sample_rate)

    raw, filt, cleaned, metrics, features = process_audio_pipeline(
        audio, 
        sample_rate=sample_rate, 
        lowcut=lowcut, 
        highcut=highcut, 
        gate_mult=gate_mult, 
        mode=mode
    )

    base_dir = os.path.dirname(os.path.abspath(__file__))
    evaluation = {"mode": mode, "status": "DSP_READY"}
    export_results(raw, filt, cleaned, sample_rate, metrics, features, evaluation, base_dir)
    return metrics, features
