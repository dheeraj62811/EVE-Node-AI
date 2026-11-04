"""
Physical Heuristic Threat Evaluation & Closed-Loop Adaptation Signals
"""

def evaluate_event(features: dict, snr_metrics: dict) -> dict:
    """
    Evaluates physical acoustic features to trigger an alert or advise adaptation.
    """
    centroid = features.get("spectral_centroid_hz", 0.0)
    zcr = features.get("zero_crossing_rate", 0.0)
    bandwidth = features.get("spectral_bandwidth_hz", 0.0)
    snr_after = snr_metrics.get("snr_after_db", 0.0)

    is_chainsaw_candidate = (350.0 <= centroid <= 1800.0) and (zcr < 0.15)
    
    if is_chainsaw_candidate:
        if snr_after < 2.0 or bandwidth > 600.0:
            decision = "TRIGGER_ADAPTIVE_RECONFIGURATION"
            reason = f"Combustion harmonics suspected at {centroid:.1f} Hz, but clutter bandwidth ({bandwidth:.1f} Hz) requires fine-tuning."
            next_params = {"lowcut": 380.0, "highcut": 1600.0, "gate_mult": 2.1}
        else:
            decision = "TRIGGER_ILLEGAL_LOGGING_ALERT"
            reason = f"High-confidence mechanical logging isolated (Centroid: {centroid:.1f} Hz, SNR: {snr_after:.2f} dB)."
            next_params = None
    else:
        decision = "SUPPRESS_AMBIENT_NOISE"
        reason = "Acoustic signature matches environmental wind/rain clutter."
        next_params = None

    return {
        "agent_mode": "STANDARD",
        "agent_decision": decision,
        "reasoning": reason,
        "battery_compute_saved_pct": snr_metrics.get("data_reduction_pct", 60.0),
        "next_filter_params": next_params
    }
