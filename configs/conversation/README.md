# Conversation config reference

These fields shape a conversation create request to Tavus. Provide either a persona_id (preferred) or a replica_id.

Core fields:
- persona_id: Use a Persona by ID. Preferred over directly providing a replica.
- replica_id: Fallback if you aren’t using a persona. The CLI can auto-pick a completed replica when neither is provided.
- conversation_name: Friendly name for this conversation.
- conversational_context: The prompt context for the conversation (greeting, goals, constraints). The CLI can synthesize one from meeting helper flags if omitted.
- audio_only: Set true for audio-only mode (no video).
- document_ids: Array of document IDs to ground the conversation.
- document_tags: Array of tags to select documents.
- document_retrieval_strategy: How to retrieve documents; one of: speed, quality, balanced.
- memory_stores: Array of memory store names to read/write memory.
- test_mode: When true, validates without joining/billing. Set false when you intend to join.
- callback_url: Webhook endpoint for events. Do not include this field if you don’t have a real URL (null values cause 400s).
- custom_greeting: Optional opening line from the replica.
- properties: Arbitrary JSON object for experimental or per-feature flags (provide via a separate file using --properties-file).

Tips:
- Set persona_id using `python bin/set_persona_id.py --config <conversation.json> --from-latest-log` after creating/updating a persona.
- Keep `test_mode` false when you want the persona to actually join. Open the conversation_url in a browser.
- Do not include a `language` field; the API rejects unknown fields.
