# Persona config reference

Use these fields in a persona JSON config (or via flags). The CLI will merge modular layers and tools when specified.

Top-level fields:
- persona_name: Display name of the persona (required for pipeline_mode=full).
- pipeline_mode: CVI pipeline mode. One of: full, echo. Default: full.
- system_prompt: The system instruction for the LLM; required when pipeline_mode=full.
- context: Additional background context the LLM can use.
- default_replica_id: Replica that the persona will use by default.
- document_ids: Array of document IDs to ground the persona.
- document_tags: Array of tags used to select documents.
- objectives_id: Attach an Objectives configuration by ID (created in Tavus dashboard).
- guardrails_id: Attach a Guardrails configuration by ID (created in Tavus dashboard).

Layers (choose one approach):
1) Inline a full `layers` object with llm/tts/stt/perception sub-objects.
2) Use modular layer fragments by name or file:
   - layers_dir: Directory that contains modular layer fragments (default: presets/layers).
   - llm: Name or path of an LLM layer fragment (resolved under layers_dir/llm).
   - tts: Name or path of a TTS layer fragment (layers_dir/tts).
   - stt: Name or path of an STT layer fragment (layers_dir/stt).
   - perception: Name or path of a perception fragment (layers_dir/perception).

LLM layer (common fields):
- model: LLM model name (e.g., tavus-llama).
- tools: Array of tool definitions (function calling) – can be merged from `tools` below.

TTS layer (common fields):
- tts_engine: Speech synthesis engine (e.g., cartesia).
- tts_model_name: Voice model. Example: sonic.
- voice_settings: Object with voice behavior, e.g., speed, emotion list.
- tts_emotion_control: Enable advanced emotion control if supported.

STT layer (common fields):
- stt_engine: Speech-to-text engine (e.g., tavus-advanced).
- participant_pause_sensitivity: How sensitive the model is to pauses from the participant (e.g., high).
- participant_interrupt_sensitivity: How sensitive interruption detection is (e.g., high).
- hotwords: Phrases to bias transcription or activation.
- smart_turn_detection: Controls how Tavus detects agent vs. participant speaking turns during live conversations.

Perception layer (examples):
- enabled: Toggle perception features. Additional perception fields can be added as your use case grows.

Modular tools:
- tools_dir: Directory where tool JSON files live (default: presets/layers/llm/tools).
- tools: Array of tool names or paths. Each tool file can be:
  - a single tool object, or
  - an array of tool objects, or
  - an object with a top-level `tools` array.
