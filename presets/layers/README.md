# Modular layers

Modular layer fragments let you assemble persona `layers` without embedding large JSON blocks. Use them by name with `--layers-dir` and per-layer flags, or list them in your persona config.

Kinds:
- llm: Large Language Model settings for reasoning and tool use.
- tts: Text-to-Speech voice and delivery.
- stt: Speech-to-Text capture and turn detection.
- perception: Optional perception features.

Usage examples:
```bash
# Use by flags
bin/tune.sh persona \
  --persona-name "Assistant" \
  --system-prompt "..." \
  --default-replica-id r4317e64d25a \
  --layers-dir presets/layers \
  --llm tavus_llama \
  --tts cartesia_sonic \
  --stt tavus_advanced \
  --perception basic
```

```json
{
  "persona_name": "Assistant",
  "system_prompt": "...",
  "default_replica_id": "r4317e64d25a",
  "layers_dir": "presets/layers",
  "llm": "tavus_llama",
  "tts": "cartesia_sonic",
  "stt": "tavus_advanced",
  "perception": "basic"
}
```

Folder structure:
- llm/: JSON objects (e.g., `{ "model": "tavus-llama", "tools": [...] }`). Tools can be merged from separate tool files.
- tts/: JSON objects (e.g., `{ "tts_engine": "cartesia", "tts_model_name": "sonic", "voice_settings": { ... } }`).
- stt/: JSON objects (e.g., `{ "stt_engine": "tavus-advanced", "smart_turn_detection": false }`).
  - smart_turn_detection: Controls how Tavus detects when it’s your turn to talk vs. when the participant is speaking, specifically in live conversational mode.
- perception/: JSON objects. Start simple, add fields as needed.

Notes:
- When a full `layers` object is present, modular layers merge into it. For LLM, `tools` arrays are appended.
