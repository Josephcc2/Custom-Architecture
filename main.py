import os
import yaml
from openai import OpenAI
import anthropic
from concurrent.futures import ThreadPoolExecutor, as_completed

# ----- Setup -----
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

ai_models = config["ai_models"]

class Layer:
    def __init__(self, parallel_to_next_layer, model_number, prompt, output_destination, output_name, input_destinations=None):
        self.parallel_to_next_layer = parallel_to_next_layer
        self.model_number = model_number
        self.prompt = prompt
        self.output_destination = output_destination
        self.output_name = output_name
        self.input_destinations = input_destinations if input_destinations is not None else []

layers = [
    Layer(
        True,
        0,
        "Rank the 5 most influential scientists of history in order. Do not send any other messages, just the ranking.",
        "outputs/layer_0.txt",
        "ChatGPT's 5 Most Influential Scientists"
    ),
    Layer(
        False,
        2,
        "Rank the 5 most influential scientists of history in order. Do not send any other messages, just the ranking.",
        "outputs/layer_1.txt",
        "Grok's 5 Most Influential Scientists"
    ),
    Layer(
        False,
        1,
        ("Given 2 lists of others' 5 most influential scientists ranked in order, "
         "give your opinion on the current ranking."),
        "outputs/layer_2.txt",
        "Claude's Synthesized List of the 5 Most Influential Scientists",
        input_destinations=["outputs/layer_0.txt", "outputs/layer_1.txt"]
    )
]


# ----- Clients -----
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


# ----- Go Through Each Layer -----
def save_output(index, response):
    destination = layers[index].output_destination
    name = layers[index].output_name
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, "w", encoding="utf-8") as f:
        f.write(f"{name}\n\n{response}")
    print(f"  Saved to: {destination}")

def run_layer(index):
    entry = ai_models[layers[index].model_number]
    company = entry["company"]
    model = entry["model"]
    prompt = layers[index].prompt

    # Prepend any input files to the prompt
    input_sections = []
    for path in layers[index].input_destinations:
        with open(path, "r", encoding="utf-8") as f:
            input_sections.append(f.read())
    if input_sections:
        prompt = prompt + "\n\n" + "\n\n".join(input_sections)

    print(f"[Layer {index}] Prompting {company} ({model})...")
    response = PromptLayer(company, model, prompt)
    return index, company, model, response


pending_layer = 0
while pending_layer < len(layers):
    # Collect a group of layers to run concurrently.
    # A layer is part of the group if it has parallel_to_next_layer == True.
    # The group ends (inclusively) at the first layer where parallel_to_next_layer == False.
    group = []
    i = pending_layer
    while i < len(layers):
        group.append(i)
        if not layers[i].parallel_to_next_layer:
            break
        i += 1

    if len(group) == 1:
        # Single layer — run directly, no threading overhead
        idx, company, model, response = run_layer(group[0])
        print(f"  Response: {response}")
        save_output(idx, response)
    else:
        # Multiple layers — run concurrently
        results = {}
        with ThreadPoolExecutor(max_workers=len(group)) as executor:
            futures = {executor.submit(run_layer, idx): idx for idx in group}
            for future in as_completed(futures):
                idx, company, model, response = future.result()
                results[idx] = (company, model, response)
        # Print results in layer order
        for idx in group:
            company, model, response = results[idx]
            print(f"  [Layer {idx}] Response: {response}")
            save_output(idx, response)

    pending_layer += len(group)
