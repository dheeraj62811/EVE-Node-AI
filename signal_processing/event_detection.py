def evaluate_event_and_adapt(features, snr_after, reduction_pct, current_mode="STANDARD"):
    """
    Agentic Reasoning Step: Evaluates processed signal features, estimates threat, 
    and decides whether to adapt filter parameters or trigger an alert.
    """
    centroid = features["spectral_centroid_hz"]
    zcr = features["zero_crossing_rate"]
    
    # Check if harmonic mechanical signature (like a chainsaw) is present in 350-1600 Hz
    is_mechanical_signature = (350 <= centroid <= 1600) and (zcr < 0.15)
    
    if snr_after < 2.0 and current_mode == "STANDARD":
        decision = "ADAPT_FILTER_NARROW_BAND"
        reason = "Low post-filter SNR detected. Narrowing bandpass to [350Hz - 1800Hz] and increasing spectral gate to 2.2x."
        recommended_params = {"lowcut": 350.0, "highcut": 1800.0, "gate_multiplier": 2.2}
    elif is_mechanical_signature:
        decision = "TRIGGER_ILLEGAL_LOGGING_ALERT"
        reason = f"High-confidence mechanical harmonic threat isolated (Centroid: {centroid} Hz, SNR: {snr_after:.1f} dB)."
        recommended_params = None
    else:
        decision = "RETURN_TO_LOW_POWER_SLEEP"
        reason = "No mechanical threat signature found after noise removal. Conserving edge battery."
        recommended_params = None
        
    return {
        "agent_mode": current_mode,
        "agent_decision": decision,
        "reasoning": reason,
        "battery_compute_saved_pct": round(reduction_pct, 1),
        "next_filter_params": recommended_params
    }
