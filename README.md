# Custom-Architecture
Schematic to deploy agents using different LLMS with custom architectures and settings.

Designed to be able to test different architectures for a certain goal to find the most efficient setup.

The system executes a sequence of **Layers**, each of which sends a prompt to a configured AI model and saves the response to a file.

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
Defines the available AI models by index. Each entry has three fields:

```yaml
ai_models:
  - company: OpenAI       # index 0
    model: gpt-4o-mini
    max_tokens: 4096
  - company: Anthropic    # index 1
    model: claude-haiku-4-5
    max_tokens: 4096
  - company: xAI          # index 2
    model: grok-4-1-fast-reasoning
    max_tokens: 4096
```

Built-in support exists for `OpenAI`, `Anthropic`, and `xAI`. Support for other providers (e.g. Gemini) can be added in `clients.py`.

### `layers.py`
Defines the ordered list of `Layer` objects that make up the pipeline. All parameters are keyword arguments:

### Layer Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `parallel_to_next_layer` | bool | — | If `True`, this layer runs concurrently with the next |
| `model_number` | int | — | Index into `ai_models` in `config.yaml` |
| `prompt` | str | — | The prompt sent to the model |
| `output_destination` | str | — | File path where the response is saved |
| `output_name` | str | — | Label written at the top of the output file |
| `input_destinations` | list[str] | `[]` | Files whose contents are appended to the prompt |
| `recursive_loops` | int | `1` | How many times the loop group repeats (1 = no looping) |
| `recursive_depth` | int | `1` | How many additional layers follow this one in the loop group |
| `conversation_output` | str | `None` | Shared conversation transcript file path (recursive groups only) |

## Layer Execution Modes

- **Sequential** — `parallel_to_next_layer=False`: layer completes before the next begins
- **Parallel** — `parallel_to_next_layer=True`: layer runs concurrently with the next using `ThreadPoolExecutor`
- **Recursive group** — `recursive_loops > 1` on the lead layer: a group of agents loops 'n' times, each reading the shared conversation transcript before responding. The group spans `recursive_depth + 1` layers (the lead + the next `recursive_depth` layers).

## Running

Double-click `run_agents.bat`, or run directly:

```bash
python main.py
```

Outputs are saved to the paths defined in each layer's `output_destination`.
