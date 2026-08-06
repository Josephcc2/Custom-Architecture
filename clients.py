import os
import anthropic
from openai import OpenAI

gptClient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
claudeClient = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
grokClient = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)


# Prompt OpenAI
def GPTRespond(prompt, model, max_tokens, persona, history=None):
    messages = [{"role": "system", "content": persona}]
    messages.extend(history or [])
    messages.append({"role": "user", "content": prompt})
    response = gptClient.chat.completions.create(
        model=model,
        max_completion_tokens=max_tokens,
        messages=messages,
    )
    return response.choices[0].message.content


# Prompt Claude
def ClaudeRespond(prompt, model, max_tokens, persona, history=None):
    messages = list(history or [])
    messages.append({"role": "user", "content": prompt})
    response = claudeClient.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=persona,
        messages=messages,
    )
    return response.content[0].text


# Prompt Grok
def GrokRespond(prompt, model, max_tokens, persona, history=None):
    messages = [{"role": "system", "content": persona}]
    messages.extend(history or [])
    messages.append({"role": "user", "content": prompt})
    response = grokClient.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=messages,
    )
    return response.choices[0].message.content


def PromptLayer(company, model, prompt, max_tokens, persona, history=None):
    company_lower = company.lower()
    if company_lower == "openai":
        return GPTRespond(prompt, model, max_tokens, persona, history)
    elif company_lower == "anthropic":
        return ClaudeRespond(prompt, model, max_tokens, persona, history)
    elif company_lower == "xai":
        return GrokRespond(prompt, model, max_tokens, persona, history)
    else:
        raise ValueError(f"Unknown company: {company}")


# ----- Agent Memory -----
# Each Agent (an entry in ai_models, identified by its model_number) can build up a messages[]
# history of its own past user/assistant turns, which gets prepended to future calls to that
# same Agent so it can see its own prior prompts and responses natively — not text pasted into
# a single prompt string. Memory is kept in a plain in-memory dict only: nothing is written to
# disk, so it does not survive past the current run of main.py, and there's no cap on how many
# turns accumulate.
#
# Saving is still routed per-company (mirroring PromptLayer) so each Agent's memory-handling can
# diverge later (e.g. a provider-specific message format) without changing calling code.

_agent_messages = {}  # {model_number: [{"role": "user"/"assistant", "content": ...}, ...]}


def LoadMemory(model_number):
    """Return this Agent's messages[] history (empty list if it has none yet this run)."""
    return _agent_messages.setdefault(model_number, [])


def _append_turn(model_number, prompt, response):
    memory = LoadMemory(model_number)
    memory.append({"role": "user", "content": prompt})
    memory.append({"role": "assistant", "content": response})


# Save memory for GPT
def GPTSaveMemory(model_number, prompt, response):
    _append_turn(model_number, prompt, response)


# Save memory for Claude
def ClaudeSaveMemory(model_number, prompt, response):
    _append_turn(model_number, prompt, response)


# Save memory for Grok
def GrokSaveMemory(model_number, prompt, response):
    _append_turn(model_number, prompt, response)


def SaveMemory(company, model_number, prompt, response):
    """Direct a prompt/response pair to the given Agent's (ai_models[model_number]'s) memory."""
    company_lower = company.lower()
    if company_lower == "openai":
        GPTSaveMemory(model_number, prompt, response)
    elif company_lower == "anthropic":
        ClaudeSaveMemory(model_number, prompt, response)
    elif company_lower == "xai":
        GrokSaveMemory(model_number, prompt, response)
    else:
        raise ValueError(f"Unknown company: {company}")
