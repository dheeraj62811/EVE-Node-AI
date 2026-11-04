from .acquisition import acquire_signal
from .preprocessing import preprocess_signal
from .filtering import apply_bandpass, apply_insect_notch
from .noise_reduction import spectral_denoise
from .segmentation import energy_gate_segmentation
from .signal_analysis import compute_snr
from .feature_extraction import extract_features
from .event_detection import evaluate_event_and_adapt
from .output import save_all_outputs

def run_pipeline(lowcut=250.0, highcut=3500.0, gate_mult=1.6, mode="STANDARD"):
    print(f"\n[RUNNING PIPELINE - MODE: {mode}]")
    
    # 1. Acquisition & Preprocessing
    raw_noisy, clean_ref, sr = acquire_signal()
    norm_noisy, sr = preprocess_signal(raw_noisy, sr)
    
    # 2. Filtering (Notch out 4.2kHz insects + Bandpass out wind)
    notched = apply_insect_notch(norm_noisy, sr, insect_freq=4200.0)
    bandpassed = apply_bandpass(notched, sr, lowcut=lowcut, highcut=highcut)
    
    # 3. Spectral Noise Reduction (Remove wideband rain)
    cleaned = spectral_denoise(bandpassed, sr, gate_multiplier=gate_mult)
    
    # 4. Segmentation / Data Reduction (Battery-saving frame gate)
    active_sig, active_mask, rms, thresh, reduction_pct = energy_gate_segmentation(cleaned, sr)
    
    # 5. Signal Analysis (Baseline vs Processed SNR on active window)
    snr_before = compute_snr(clean_ref, norm_noisy, mask=active_mask)
    snr_after = compute_snr(clean_ref, cleaned, mask=active_mask)
    
    # 6. Feature Extraction & Agentic Decision
    features = extract_features(active_sig, sr)
    agent_out = evaluate_event_and_adapt(features, snr_after, reduction_pct, current_mode=mode)
    
    # 7. If Agent requests filter adaptation, re-run automatically!
    if agent_out["agent_decision"] == "ADAPT_FILTER_NARROW_BAND":
        print(f" -> Agent Reasoning: {agent_out['reasoning']}")
        params = agent_out["next_filter_params"]
        return run_pipeline(
            lowcut=params["lowcut"], 
            highcut=params["highcut"], 
            gate_mult=params["gate_multiplier"], 
            mode="ADAPTIVE_DEEP_CLEAN"
        )
        
    payload = {
        "metrics": {
            "snr_before_db": round(snr_before, 2),
            "snr_after_db": round(snr_after, 2),
            "snr_gain_db": round(snr_after - snr_before, 2),
            "data_reduction_pct": round(reduction_pct, 1)
        },
        "extracted_features": features,
        "agent_evaluation": agent_out
    }
    
    save_all_outputs(norm_noisy, cleaned, sr, rms, thresh, payload)
    print(" -> Pipeline Complete! Saved audio to 'processed/' and evidence to 'outputs/'.")
    print(f" -> SNR Gain: +{payload['metrics']['snr_gain_db']} dB | Battery/Frames Saved: {payload['metrics']['data_reduction_pct']}%")
    print(f" -> Agent Decision: {agent_out['agent_decision']} ({agent_out['reasoning']})")

if __name__ == "__main__":
    run_pipeline()
