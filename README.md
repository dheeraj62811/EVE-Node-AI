**# Energy-Aware Adaptive Bioacoustic Sensing

**Agentic AI for illegal logging detection in forest environments**

A hackathon prototype that combines signal processing with an adaptive AI-agent controller to identify possible mechanical threats—such as chainsaws—in noisy forest recordings.

## Problem

Forest acoustic sensors must distinguish possible threats from wind, rain, insects, and other environmental sounds. Continuously processing or transmitting all audio can also consume significant battery and compute resources.

## Proposed system

The signal-processing pipeline cleans and analyzes audio, then provides the agent with a JSON payload containing signal-quality metrics and extracted features. The agent observes this payload, evaluates the evidence and sensor context, and can request a bounded second DSP pass with adjusted filter parameters before generating a recommendation.

The intended loop is:

**Observe → Reason → Adapt → Recommend**

This repository currently contains the agent controller. The signal-processing pipeline is a separate team component and must be added and integrated before the full system can be demonstrated.

## Current features

- Reads `outputs/agent_payload.json`.
- Evaluates post-processing SNR, spectral centroid, and zero-crossing rate.
- Logs its observations, reasoning, and decisions.
- Can request one DSP reprocessing pass if signal quality is low or features are ambiguous, provided the DSP module is connected.
- Checks supplied battery, weather, node, GPS, and neighboring-node context.
- Recommends raising the segmentation percentile when battery is below the configured threshold.
- Writes a structured incident report and an event trace.

## Important status and limitations

This prototype uses a **hand-written heuristic policy**. It does **not** contain a trained machine-learning model, and it does not call an LLM.

The reported `confidence_score` is a heuristic score, not a calibrated probability. The example payload in `outputs/agent_payload.json` uses values from the project brief; they are illustrative and are not independently measured experimental results.

The battery-related segmentation change is currently a recommendation only. It will not modify the actual signal-processing pipeline until an explicit integration hook is implemented.

The system does not contact rangers or dispatch emergency services. Any alert is a recommendation for human verification.

## Requirements

- Python 3.9 or newer recommended.
- The agent-only demo uses the Python standard library and requires no additional packages.
- The integrated system may require additional libraries used by the signal-processing pipeline.

## Run the agent demo

From the project directory:

```bash
python agent_controller.py --demo --battery 28 --node-id Node_01 --weather monsoon_rain --gps "Sector 4"
To test the low-battery recommendation, run:

```bash
python agent_controller.py --demo --battery 15
To test the low-battery recommendation, run:

```bash
python agent_controller.py --demo --battery 15
```

The demo writes or updates these files:

- `outputs/agent_payload.json` — example input payload.
- `outputs/incident_report.json` — structured agent recommendation.
- `outputs/agent_trace.jsonl` — timestamped observations and decisions.

## Connect the signal-processing pipeline

