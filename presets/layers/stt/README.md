# STT layer fragments

Configure how speech is captured and turns are detected.

Common fields:
- stt_engine: Speech-to-text engine (e.g., "tavus-advanced").
- participant_pause_sensitivity: Sensitivity to participant pauses (e.g., "low", "medium", "high").
- participant_interrupt_sensitivity: Sensitivity to detecting participant interruptions (e.g., "low", "medium", "high").
- hotwords: Phrases to bias recognition or activate behaviors.
- smart_turn_detection: Controls how Tavus detects when it’s your turn to talk vs. when the participant is speaking, specifically in live conversational mode.
- smart_turn_detection_params: Optional tuning parameters for turn detection (if supported).

Example:
```json
{
  "stt_engine": "tavus-advanced",
  "participant_pause_sensitivity": "high",
  "participant_interrupt_sensitivity": "high",
  "hotwords": "You are TeamWise a meeting facilitator.",
  "smart_turn_detection": false
}
```