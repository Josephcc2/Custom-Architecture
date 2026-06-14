import os
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from clients import PromptLayer
from layers import layers

# ----- Setup -----
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

ai_models = config["ai_models"]


# ----- Helpers -----
def save_output(index, response):
    destination = layers[index].output_destination
    name = layers[index].output_name
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, "w", encoding="utf-8") as f:
        f.write(f"{name}\n\n{response}")


def log_complete(index, company, model):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] Layer {index} complete — {company} ({model})")


def run_layer(index, extra_prompt=""):
    """Run a single layer. If extra_prompt is provided, it is appended to the layer's base prompt."""
    entry = ai_models[layers[index].model_number]
    company = entry["company"]
    model = entry["model"]
    max_tokens = entry["max_tokens"]
    persona = entry["persona"]
    prompt = layers[index].prompt

    # Prepend any input files to the prompt
    input_sections = []
    for path in layers[index].input_destinations:
        with open(path, "r", encoding="utf-8") as f:
            input_sections.append(f.read())
    if input_sections:
        prompt = prompt + "\n\n" + "\n\n".join(input_sections)

    # Append any extra context (e.g. the conversation so far from a recursive loop)
    if extra_prompt:
        prompt = prompt + "\n\n" + extra_prompt

    print(f"[Layer {index}] Prompting {company} ({model})...")
    response = PromptLayer(company, model, prompt, max_tokens, persona)
    return index, company, model, response


def append_to_conversation(conversation_path, label, response):
    """Append a single agent turn to the shared conversation file."""
    os.makedirs(os.path.dirname(conversation_path), exist_ok=True)
    with open(conversation_path, "a", encoding="utf-8") as f:
        f.write(f"--- {label} ---\n{response}\n\n")


# ----- Recursive Group Runner -----
def run_recursive_group(start_index):
    """
    Runs a recursive loop group starting at start_index.
    The group spans (recursive_depth + 1) layers: [start_index, start_index + recursive_depth].
    Each layer runs sequentially within a loop, repeated recursive_loops times.
    All agent outputs are appended to conversation_output after each turn.
    Returns the number of layers consumed.
    """
    lead = layers[start_index]
    num_loops = lead.recursive_loops
    depth = lead.recursive_depth
    conversation_path = lead.conversation_output

    group_indices = list(range(start_index, start_index + depth + 1))

    print(f"\n[Recursive Group] Layers {group_indices}, {num_loops} loop(s), conversation → {conversation_path}\n")

    # Clear / create the conversation file at the start
    os.makedirs(os.path.dirname(conversation_path), exist_ok=True)
    open(conversation_path, "w", encoding="utf-8").close()

    for loop_num in range(1, num_loops + 1):
        print(f"  [Loop {loop_num}/{num_loops}]")
        for idx in group_indices:
            # Build the conversation-so-far context to pass into this agent's prompt
            with open(conversation_path, "r", encoding="utf-8") as f:
                conversation_so_far = f.read().strip()

            if conversation_so_far:
                extra = f"The conversation so far:\n\n{conversation_so_far}"
            else:
                extra = ""

            idx, company, model, response = run_layer(idx, extra_prompt=extra)
            label = f"Loop {loop_num} | Layer {idx} | {layers[idx].output_name}"

            save_output(idx, response)
            append_to_conversation(conversation_path, label, response)
            log_complete(idx, company, model)

    print(f"\n  [Recursive Group] Complete. Conversation saved to: {conversation_path}\n")
    return len(group_indices)


# ----- Main -----
def main():
    pending_layer = 0
    while pending_layer < len(layers):
        lead = layers[pending_layer]

        # --- Recursive group ---
        if lead.recursive_loops > 1:
            consumed = run_recursive_group(pending_layer)
            pending_layer += consumed
            continue

        # --- Normal group (parallel or single) ---
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
            save_output(idx, response)
            log_complete(idx, company, model)
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
                save_output(idx, response)
                log_complete(idx, company, model)

        pending_layer += len(group)


if __name__ == "__main__":
    main()
