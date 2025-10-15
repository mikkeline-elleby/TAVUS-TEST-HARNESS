# LLM tools

Function-calling tools for the LLM live here. Include tools by name or file and they will be merged into `layers.llm.tools`.

Accepted file shapes:
- Single tool object: `{ "type": "function", "function": { ... } }`
- Array of tools: `[ { ... }, { ... } ]`

Templates:
- `template.example.json` – single-tool JSON you can copy and edit
- `template.example.jsonc` – same with comments (JSONC is accepted)

Usage examples:
- By name (resolved here): `--tools summarize_discussion,cluster_ideas`
- By file: `--tools presets/layers/llm/tools/template.example.jsonc`

Notes:
- Pass multiple tools by comma in `--tools` or as an array in persona config; no bundle file needed.
- Tools use JSON Schema in `function.parameters` to validate inputs.
- The model calls by `function.name`, so keep names stable and descriptive.
