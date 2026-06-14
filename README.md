# Custom-Architecture
Schematic to deploy agents using different LLMS with custom architectures and settings.

Designed to be able to test different architectures for a certain goal to find the most efficient setup.

## Setup
Ensure you have Python latest release installed on your system.

First, install the SDKs for each LLM.

Example:

```bash
pip install anthropic
```

Next, set your API keys as environment variables.

Example:

```bash
set ANTHROPIC_API_KEY=your_api_key_here
```

## Customizing
Layers can be edited in `main.py`
LLMs can be modified in `config.yaml`

## Running the Project
To run the project, run the `run_agents.bat` file
