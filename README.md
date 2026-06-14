# Custom-Architecture
Schematic to deploy agents using different LLMS with custom architectures and settings.

Designed to be able to test different architectures for a certain goal to find the most efficient setup.

## Setup
Ensure you have Python latest release installed on your system.

First, install the SDKs for each LLM:

```bash
pip install openai
```
```bash
pip install anthropic
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

## Customizing
Layers can be edited in `layers.py`.

Layers dictate the architecture for the agents. Layers have the following variables:
- `parallel_to_next_layer`(bool) Decides if to run the next layer in sync with current layer. Can stack among multiple layers. Does not work with recursion.
- `model_number`(int) Which LLM to use from `config.yaml`. 0 correlates to the first model, 1 to the second, and so on.
- `prompt`(string) The prompt that the agent in that layer receives.
- `output_destination`(string) File path to store agent's output.
- `output_name`(string) Header appended to the beginning of the agent's output. Does not affect outputs.
- `input_destination`(string[]) Optional list of file paths for inputs that the agent is given. Inputs are appended to the end of the prompt.

**Recursion**

- `recursive_loops`(int) How many times the loop group repeats. 1 = no looping (normal behavior). Used to repeat multiple layers before moving on.
- `recursive_depth`(int) How many additional layers after this one are included in the loop group. A value of `1` mean that the current layer and the next are in the loop, a value of `2` means that there are a total of 3 layers in the loop.
- `conversation_output` File path where the full agent conversation is appended to each loop. Ignored when `recursive_loops` == 1. Agents recieve the conversation when in a loop.

---
LLMs can be modified in `config.yaml`.

There is currently only built in support for ChatGPT, Claude, and Grok. This means that all of those models will work when put in the config file. Other models, such as Gemini, can have support added through `clients.py`.

## Running the Project
To run the project, run the `run_agents.bat` file. Outputs can be found in the fiels that they were generated to.
