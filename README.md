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
- `parallel_to_next_layer`

---
LLMs can be modified in `config.yaml`.

There is currently only built in support for ChatGPT, Claude, and Grok. This means that all of those models will work when put in the config file. Other models, such as Gemini, can have support added through `clients.py`.

## Running the Project
To run the project, run the `run_agents.bat` file. Outputs can be found in the fiels that they were generated to.
