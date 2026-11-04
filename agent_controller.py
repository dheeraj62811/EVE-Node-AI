import os
import json

class EvenodeAgenticController:
    def __init__(self, node_id="EVE_Node_01", gps_coords="17.5449 N, 78.5718 E"):
        self.node_id = node_id
        self.gps_coords = gps_coords
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

    def run_cycle(self, simulated_battery=100.0, weather="CLEAR_CALM"):
        payload_path = os.path.join(self.base_dir, "signal_processing", "outputs", "agent_payload.json")
        payload = {}
        if os.path.exists(payload_path):
            with open(payload_path, "r") as f:
                payload = json.load(f)

        features = payload.get("extracted_features", {})
        metrics = payload.get("metrics", {})

        centroid = features.get("spectral_centroid_hz", 0.0)
        zcr = features.get("zero_crossing_rate", 0.0)
        crest = features.get("crest_factor", 1.0)
        kurt = features.get("kurtosis", 3.0)
        motor_ratio = features.get("motor_harmonic_ratio", 0.0)
        impact_ratio = features.get("impact_energy_ratio", 0.0)
        snr_gain = metrics.get("snr_gain_db", 0.0)

        scores = {
            "POACHING_BALLISTIC_DISCHARGE": 0.0,
            "ILLEGAL_LOGGING_CHAINSAW": 0.0,
            "ILLEGAL_LOGGING_TREE_FELLING": 0.0,
            "BENIGN_FOREST_BIOPHONY": 0.10
        }

        # 1. BIOPHONY / BIRD SOUND CHECK:
        # High spectral centroid (> 2100 Hz) or high Zero Crossing Rate indicates birds, insects, or canopy wind
        is_high_pitch_avian = centroid >= 2100.0 or zcr >= 0.24

        # 2. POACHING (GUNSHOTS):
        # Must have extreme peak/kurtosis AND be in the lower-frequency acoustic shockwave band (< 1600 Hz)
        if (kurt > 8.0 or crest > 6.0) and not is_high_pitch_avian and centroid <= 1600.0:
            scores["POACHING_BALLISTIC_DISCHARGE"] = min(0.98, (kurt / 12.0) * 0.5 + (crest / 8.0) * 0.5)

        # 3. CHAINSAW / MOTORIZED CUTTING:
        if (motor_ratio >= 0.38 and 300.0 <= centroid <= 2200.0 and zcr < 0.22) or (motor_ratio >= 0.55):
            motor_score = (motor_ratio * 1.3)
            if 350.0 <= centroid <= 1800.0:
                motor_score += 0.25
            scores["ILLEGAL_LOGGING_CHAINSAW"] = min(0.97, motor_score)

        # 4. TREE FELLING / AXE CHOPS:
        # Percussive impacts with low-frequency energy in 50-900 Hz band
        if not is_high_pitch_avian and (impact_ratio >= 0.22 or (crest >= 3.2 and centroid <= 1600.0)):
            felling_score = (impact_ratio * 1.6)
            if crest >= 3.2:
                felling_score += min(0.35, (crest - 3.0) * 0.15)
            if kurt >= 2.5:
                felling_score += 0.15
            scores["ILLEGAL_LOGGING_TREE_FELLING"] = min(0.96, felling_score)

        # 5. BIOPHONY (Default or High Pitch):
        if is_high_pitch_avian:
            scores["BENIGN_FOREST_BIOPHONY"] = 0.94
        elif max(scores["POACHING_BALLISTIC_DISCHARGE"], scores["ILLEGAL_LOGGING_CHAINSAW"], scores["ILLEGAL_LOGGING_TREE_FELLING"]) < 0.35:
            scores["BENIGN_FOREST_BIOPHONY"] = 0.88

        # Winner Selection
        classification = max(scores, key=scores.get)
        confidence = round(scores[classification], 2)
        threat = classification != "BENIGN_FOREST_BIOPHONY"

        if classification == "POACHING_BALLISTIC_DISCHARGE":
            evidence = f"Low-frequency ballistic muzzle-blast transient detected (Kurtosis: {kurt}, Centroid: {centroid} Hz)."
            action = "CODE RED: Armed poaching detected. Dispatch armed tactical rangers immediately."
        elif classification == "ILLEGAL_LOGGING_CHAINSAW":
            evidence = f"Periodic internal combustion motor harmonics isolated (Motor Band: {int(motor_ratio*100)}%, Centroid: {centroid} Hz)."
            action = "Priority Interdiction: Dispatch rapid response ranger unit to intercept active mechanized logging."
        elif classification == "ILLEGAL_LOGGING_TREE_FELLING":
            evidence = f"Acoustic impact spikes and structural timber crack detected (Crest: {crest}, Impact Band: {int(impact_ratio*100)}%, Event Centroid: {centroid} Hz)."
            action = "Priority Alert: Dispatch local forestry response team to investigate active tree felling."
        else:
            evidence = f"High-frequency acoustic distribution consistent with natural canopy bird songs and ambient biophony (Centroid: {centroid} Hz)."
            action = "Maintain passive listening cycle. No tactical deployment needed."

        trace_log = {
            "node_id": self.node_id,
            "battery": simulated_battery,
            "weather": weather,
            "snr_raw": metrics.get("snr_before_db", 0.0),
            "snr_cleaned": metrics.get("snr_after_db", 0.0),
            "snr_gain": snr_gain,
            "centroid": centroid,
            "kurtosis": kurt,
            "crest": crest,
            "motor_ratio": motor_ratio,
            "impact_ratio": impact_ratio,
            "scores": scores,
            "classification": classification,
            "confidence": confidence,
            "threat": threat,
            "action": action
        }

        os.makedirs(os.path.join(self.base_dir, "evidence"), exist_ok=True)
        with open(os.path.join(self.base_dir, "evidence", "agent_reasoning_trace.json"), "w") as f:
            json.dump(trace_log, f, indent=2)

        dispatch = {
            "incident_classification": classification,
            "threat_detected": threat,
            "confidence_score": confidence,
            "sensor_node": self.node_id,
            "geo_coordinates": self.gps_coords,
            "evidence_summary": evidence,
            "recommended_tactical_action": action,
            "class_probabilities": scores
        }

        os.makedirs(os.path.join(self.base_dir, "outputs"), exist_ok=True)
        with open(os.path.join(self.base_dir, "outputs", "ranger_incident_dispatch.json"), "w") as f:
            json.dump(dispatch, f, indent=2)

        return dispatch
