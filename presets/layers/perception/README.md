# Perception layer fragments

Optional perception features to augment interaction.

Common fields:
- perception_model: Selects the perception model.
  - raven-0 (default & recommended): Advanced visual capabilities, screen share support, ambient queries, and perception tools.
  - basic: Legacy model with limited features.
  - off: Disables the perception layer.
 - ambient_awareness_queries: Array of short passive checks to run during the session.
 - perception_analysis_queries: Array of deeper, on-demand analysis questions.
 - perception_tool_prompt: Guidance for when/how to call perception tools.
 - perception_tools: Array of function tools for perception-specific actions (same shape as LLM tools).

Examples:
```json
{ "perception_model": "raven-0" }
```
```json
{ "perception_model": "basic" }
```
```json
{ "perception_model": "off" }
```

Templates:
- `template.example.json`: Filled example including ambient queries, analysis queries, a tool prompt, and a simple perception tool.
- `template.example.jsonc`: Same as above with inline comments; accepted by the CLI.

here link : https://docs.tavus.io/sections/conversational-video-interface/persona/perception