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
def GPTRespond(prompt, model):
    response = gptClient.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content


# Prompt Claude
def ClaudeRespond(prompt, model):
    response = claudeClient.messages.create(
        model=model,
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return response.content[0].text


# Prompt Grok
def GrokRespond(prompt, model):
    response = grokClient.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content


def PromptLayer(company, model, prompt):
    company_lower = company.lower()
    if company_lower == "openai":
        return GPTRespond(prompt, model)
    elif company_lower == "anthropic":
        return ClaudeRespond(prompt, model)
    elif company_lower == "xai":
        return GrokRespond(prompt, model)
    else:
        raise ValueError(f"Unknown company: {company}")
