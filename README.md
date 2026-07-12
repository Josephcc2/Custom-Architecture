# Custom-Architecture
Schematic to deploy agents using different LLMS with custom architectures and settings.

Designed to be able to test different architectures for a certain goal to find the most efficient setup.

The system executes a sequence of **Layers**, each of which sends a prompt to a configured AI model and saves the response to a file. After all layers complete, a **Voting System** evaluates the output against a user-defined goal before surfacing the result.

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

*If on MacOS, replace 'set' with 'export'*

## Configuration

### `config.yaml`
Defines two lists of models: one for the pipeline workers (`ai_models`) and one for the post-run evaluators (`voting_models`).

```yaml
ai_models:
  - company: OpenAI       # index 0
    model: gpt-4o-mini
    max_tokens: 4096
    persona: You are a helpful assistant.
  - company: Anthropic    # index 1
    model: claude-haiku-4-5
    max_tokens: 4096
    persona: You are a helpful assistant.
  - company: xAI          # index 2
    model: grok-4-1-fast-reasoning
    max_tokens: 4096
    persona: You are a helpful assistant.

voting_models:
  - company: OpenAI
    model: gpt-4o-mini
    max_tokens: 2048
  - company: Anthropic
    model: claude-haiku-4-5
    max_tokens: 2048
  - company: xAI
    model: grok-4-1-fast-reasoning
    max_tokens: 2048
```

`ai_models` fields: `company`, `model`, `max_tokens`, `persona`.
`voting_models` fields: `company`, `model`, `max_tokens`. Voters use a hardcoded impartial evaluator persona — no `persona` field needed.

Built-in support exists for `OpenAI`, `Anthropic`, and `xAI`. Support for other providers (e.g. Gemini) can be added in `clients.py`.

### `layers_file` (in `config.yaml`)
Specifies which pipeline script to load at runtime. Set this to the name of any file inside the `layers/` folder, without the `.py` extension:

```yaml
layers_file: research
```

This will load `layers/research.py` as the active pipeline.

### `layers/` Folder
Contains one or more pipeline definition scripts. Each file is self-contained and must expose four module-level names:

- **`context`** — shared background included in every agent's prompt, regardless of layer (e.g. framing the agents as collaborators in a multi-model pipeline).
- **`task`** — the task the pipeline works on (used inside layer prompts). Unlike a short topic, this can span multiple lines or paragraphs to capture as much detail as the task needs.
- **`goal`** — a plain English description of what the final output must satisfy for the vote to pass. Only used when voting is enabled.
- **`layers`** — the ordered list of `Layer` objects that make up the pipeline.

To add a new pipeline, create a new `.py` file in the `layers/` folder with those four names defined, then update `layers_file` in `config.yaml` to match. No changes to `main.py` are needed.
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

## Voting System

After all layers complete, the voting system runs automatically. All `voting_models` are prompted in parallel and each returns a verdict. The results are tallied and printed before the final output is surfaced.

### `vote_config` fields

| Field | Type | Description |
|---|---|---|
| `enabled` | bool | If `False`, the pipeline runs and exits without any voting or synthesis |
| `mode` | str | `"pass_fail"` or `"select_best"` |
| `input_files` | list[str] | File(s) the voters read and evaluate |
| `input_labels` | list[str] | Labels for each file in `select_best` mode (e.g. `"OUTPUT_A"`, `"OUTPUT_B"`) |
| `synthesizer_model` | int | Index into `ai_models` for the model that applies voter corrections. Only used in `pass_fail` mode. |

### Voting Modes

**`pass_fail`** — voters judge a single output file against the `goal` string. Each voter responds with either `PASS` (and a brief reason) or `FAIL` (and a precise, actionable list of corrections needed). A majority of `PASS` votes causes the result to be printed to the terminal. A majority of `FAIL` votes triggers the **vote synthesis** step: all voter correction lists are compiled and sent to the `synthesizer_model`, which applies them directly to the output file. The vote then runs again on the revised output. This loop continues until the output passes.

**`select_best`** — voters are given two or more output files (labeled by `input_labels`) and pick whichever best satisfies the `goal`. The most-voted label wins and that file is printed to the terminal.

### Example `vote_config`

```yaml
vote_config:
  enabled: true
  mode: pass_fail
  input_files:
    - outputs/final_report.md
  input_labels:        # only used in select_best mode
    - OUTPUT_A
    - OUTPUT_B
  synthesizer_model: 1 # index into ai_models; applies corrections on vote failure
```

## Running

Double-click `run_agents.bat`, or run directly:

```bash
python main.py
```

Outputs are saved to the paths defined in each layer's `output_destination`.
