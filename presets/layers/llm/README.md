# LLM layer fragments

Configure how the language model behaves and which function tools it can call.

Common fields:
- model: LLM model identifier (e.g., "tavus-llama").
- tools: Array of function-calling tool definitions. Tools from modular files are appended to any tools already present here.

Tool object shape (summary):
- type: "function".
- function:
  - name: Stable function name the model will call.
  - description: What the function does.
  - parameters: JSON Schema (object with properties/required) describing inputs.

Example:
```json
{
  "model": "tavus-llama",
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "summarize_discussion",
        "description": "Summarizes the current discussion into bullet points.",
        "parameters": {
          "type": "object",
          "properties": {
            "transcript": { "type": "string" }
          },
          "required": ["transcript"]
        }
      }
    }
  ]
}
```

Defaults and variants:
- Default in templates: `llm: "tavus_llama"` → sets `model: "tavus-llama"`.
- Also provided here:
  - `tavus_llama_4` → `model: "tavus-llama-4"`
  - `tavus_gpt_4o` → `model: "tavus-gpt-4o"`
  - `tavus_gpt_4o_mini` → `model: "tavus-gpt-4o-mini"`
Switch by changing the `llm` value in your persona config.