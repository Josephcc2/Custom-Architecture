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
def GPTRespond(prompt, model, max_tokens, persona):
    response = gptClient.chat.completions.create(
        model=model,
        max_completion_tokens=max_tokens,
        messages=[
            {"role": "system", "content": persona},
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content


# Prompt Claude
def ClaudeRespond(prompt, model, max_tokens, persona):
    response = claudeClient.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=persona,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return response.content[0].text


# Prompt Grok
def GrokRespond(prompt, model, max_tokens, persona):
    response = grokClient.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": persona},
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content


def PromptLayer(company, model, prompt, max_tokens, persona):
    company_lower = company.lower()
    if company_lower == "openai":
        return GPTRespond(prompt, model, max_tokens, persona)
    elif company_lower == "anthropic":
        return ClaudeRespond(prompt, model, max_tokens, persona)
    elif company_lower == "xai":
        return GrokRespond(prompt, model, max_tokens, persona)
    else:
        raise ValueError(f"Unknown company: {company}")
