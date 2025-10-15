# TTS layer fragments

Configure how the agent speaks.

Common fields:
- tts_engine: Speech synthesis engine (e.g., "cartesia").
- tts_model_name: Voice model (e.g., "sonic").
- voice_settings: Object controlling delivery.
  - speed: e.g., "slow", "normal", "fast".
  - emotion: Array of tags (e.g., ["positivity:high", "curiosity"]).
- tts_emotion_control: Enable advanced emotion shaping if supported.

Example:
```json
{
  "tts_engine": "cartesia",
  "tts_model_name": "sonic",
  "voice_settings": {
    "speed": "normal",
    "emotion": ["positivity:high", "curiosity"]
  },
  "tts_emotion_control": false
}
```