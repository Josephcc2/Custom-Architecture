# Custom-Architecture
Schematic to deploy agents using different LLMS with custom architectures and settings.

Designed to be able to test different architectures for a certain goal to find the most efficient setup.

## Setup
Ensure you have Python latest release installed on your system.

First, install dependencies:

```bash
pip install anthropic openai pyyaml
```

Next, set your API keys as environment variables:

```bash
set OPENAI_API_KEY=your_api_key_here
```
```bash
set ANTHROPIC_API_KEY=your_api_key_here
```
```bash
set XAI_API_KEY=your_api_key_here
```

## Configuration

### `config.yaml`
Defines the available AI models by index. Each entry has a `company` and `model` field.

```yaml
ai_models:
  - company: OpenAI       # index 0
    model: gpt-4o-mini
  - company: Anthropic    # index 1
    model: claude-haiku-4-5
  - company: xAI          # index 2
    model: grok-4-1-fast-reasoning
```

### `layers.py`
Defines the ordered list of `Layer` objects that make up the pipeline. Edit this file to change what the agents do.

### Layer Parameters

| Parameter | Type | Description |
|---|---|---|
| `parallel_to_next_layer` | bool | If `True`, this layer runs concurrently with the next |
| `model_number` | int | Index into `ai_models` in `config.yaml` |
| `prompt` | str | The prompt sent to the model |
| `output_destination` | str | File path where the response is saved |
| `output_name` | str | Label written at the top of the output file |
| `input_destinations` | list[str] | Optional files whose contents are appended to the prompt |
| `recursive_loops` | int | How many times the loop group repeats (1 = no looping) |
| `recursive_depth` | int | How many additional layers follow this one in the loop group |
| `conversation_output` | str | Shared conversation transcript file (used by recursive groups) |

## Recursive Groups

Set `recursive_loops > 1` on the **lead layer** to create a looping agent group. The group spans `recursive_depth + 1` layers (the lead plus the next `recursive_depth` layers). Each agent in the group reads the shared conversation transcript before responding, enabling multi-turn back-and-forth between agents.

---
LLMs can be modified in `config.yaml`.

There is currently only built in support for ChatGPT, Claude, and Grok. This means that all of those models will work when put in the config file. Other models, such as Gemini, can have support added through `clients.py`.

## Running the Project
To run the project, run the `run_agents.bat` file. Outputs can be found in the fiels that they were generated to.
