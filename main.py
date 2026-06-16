import os
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from clients import PromptLayer
from layers import layers, goal

# ----- Setup -----
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

ai_models = config["ai_models"]
voting_models = config["voting_models"]
vote_config = config["vote_config"]


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


# ----- Voting -----
VOTER_PERSONA = (
    "You are a strict, impartial evaluator. Your only job is to judge whether a piece of work "
    "meets a defined goal. You do not offer encouragement or hedging — only a clear verdict and "
    "precise, actionable corrections where needed."
)

SYNTHESIZER_PERSONA = (
    "You are a precise editor. You are given a document and a list of corrections from multiple "
    "reviewers. Apply every correction faithfully and return the complete, revised document. "
    "Do not add commentary — output only the revised document."
)


def build_vote_prompt(mode, goal, input_files, input_labels):
    """Build the voting prompt based on mode and input files."""
    file_contents = []
    for path in input_files:
        with open(path, "r", encoding="utf-8") as f:
            file_contents.append(f.read())

    if mode == "pass_fail":
        return (
            f"GOAL:\n{goal}\n\n"
            f"OUTPUT TO EVALUATE:\n{file_contents[0]}\n\n"
            "Does this output sufficiently meet the goal above?\n"
            "Respond with PASS or FAIL on the very first line (nothing else on that line).\n"
            "If PASS: briefly state why it meets the goal.\n"
            "If FAIL: list only the specific corrections needed to meet the goal. "
            "Be precise and actionable — do not rewrite the document, just list what must change."
        )
    elif mode == "select_best":
        sections = "\n\n".join(
            f"{label}:\n{content}"
            for label, content in zip(input_labels, file_contents)
        )
        options = " or ".join(input_labels)
        return (
            f"GOAL:\n{goal}\n\n"
            f"{sections}\n\n"
            f"Which of the outputs above best satisfies the goal?\n"
            f"Respond with {options} on the very first line (nothing else on that line), "
            "then on a new line give a brief reason for your choice."
        )
    else:
        raise ValueError(f"Unknown vote mode: {mode}")


def run_vote(mode, goal, input_files, input_labels):
    """
    Run all voting models in parallel. Returns a list of dicts:
      pass_fail:   [{"company": ..., "model": ..., "verdict": ..., "feedback": ...}, ...]
      select_best: [{"company": ..., "model": ..., "verdict": ..., "reason": ...}, ...]
    """
    prompt = build_vote_prompt(mode, goal, input_files, input_labels)

    def prompt_voter(entry):
        company = entry["company"]
        model = entry["model"]
        max_tokens = entry["max_tokens"]
        print(f"[Vote] Prompting {company} ({model})...")
        response = PromptLayer(company, model, prompt, max_tokens, VOTER_PERSONA)
        lines = response.strip().splitlines()
        verdict = lines[0].strip().upper() if lines else "UNKNOWN"
        body = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""

        if mode == "pass_fail":
            return {"company": company, "model": model, "verdict": verdict, "feedback": body}
        else:
            return {"company": company, "model": model, "verdict": verdict, "reason": body}

    results = []
    with ThreadPoolExecutor(max_workers=len(voting_models)) as executor:
        futures = [executor.submit(prompt_voter, entry) for entry in voting_models]
        for future in as_completed(futures):
            results.append(future.result())

    return results


def tally_votes(results, mode, input_labels):
    """
    Tally voter results and print a summary.

    pass_fail mode:
      - Returns True (passed) or False (failed).
      - On failure, also returns a compiled string of all voter corrections.
    select_best mode:
      - Returns the winning label string.

    Return value:
      pass_fail → (bool, corrections_str | None)
      select_best → (str, None)
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{ts}] ====== VOTE RESULTS ======")

    if mode == "pass_fail":
        passes = 0
        fails = 0
        correction_blocks = []

        for r in results:
            verdict = r["verdict"]
            feedback = r.get("feedback", "")
            print(f"  {r['company']} ({r['model']}): {verdict}")
            if feedback:
                print(f"    {feedback}\n")
            if verdict == "PASS":
                passes += 1
            else:
                fails += 1
                if feedback:
                    correction_blocks.append(f"[{r['company']} — {r['model']}]\n{feedback}")

        passed = passes > fails
        outcome = "PASSED" if passed else "FAILED"
        print(f"  Tally: {passes} PASS / {fails} FAIL → Vote {outcome}")
        print("=" * 30 + "\n")

        corrections = "\n\n".join(correction_blocks) if correction_blocks else None
        return passed, corrections

    elif mode == "select_best":
        counts = {label: 0 for label in input_labels}
        for r in results:
            print(f"  {r['company']} ({r['model']}): {r['verdict']}")
            reason = r.get("reason", "")
            if reason:
                print(f"    {reason}\n")
            if r["verdict"] in counts:
                counts[r["verdict"]] += 1
        winner = max(counts, key=counts.get)
        print(f"  Tally: {counts} → Winner: {winner}")
        print("=" * 30 + "\n")
        return winner, None


def run_vote_synthesis(corrections, input_file, synthesizer_model_index):
    """
    Takes the compiled voter corrections and the current output file, prompts the
    synthesizer model to apply all corrections, and overwrites the output file
    with the revised result.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        current_output = f.read()

    prompt = (
        f"ORIGINAL DOCUMENT:\n{current_output}\n\n"
        f"CORRECTIONS FROM REVIEWERS:\n{corrections}\n\n"
        "Apply every correction listed above to the original document. "
        "Return only the complete revised document with no additional commentary."
    )

    entry = ai_models[synthesizer_model_index]
    company = entry["company"]
    model = entry["model"]
    max_tokens = entry["max_tokens"]

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] [Vote Synthesis] Prompting {company} ({model}) to apply corrections...")

    revised = PromptLayer(company, model, prompt, max_tokens, SYNTHESIZER_PERSONA)

    with open(input_file, "w", encoding="utf-8") as f:
        f.write(revised)

    print(f"[Vote Synthesis] Revised output saved to: {input_file}\n")


# ----- Main -----
def run_pipeline(start_layer=0):
    """Run layers starting from start_layer. Returns when all layers are complete."""
    pending_layer = start_layer
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
            idx, company, model, response = run_layer(group[0])
            save_output(idx, response)
            log_complete(idx, company, model)
        else:
            results = {}
            with ThreadPoolExecutor(max_workers=len(group)) as executor:
                futures = {executor.submit(run_layer, idx): idx for idx in group}
                for future in as_completed(futures):
                    idx, company, model, response = future.result()
                    results[idx] = (company, model, response)
            for idx in group:
                company, model, response = results[idx]
                save_output(idx, response)
                log_complete(idx, company, model)

        pending_layer += len(group)


def main():
    run_pipeline(start_layer=0)

    if not vote_config["enabled"]:
        print("\n[Voting disabled. Pipeline complete.]\n")
        return

    mode = vote_config["mode"]
    input_files = vote_config["input_files"]
    input_labels = vote_config["input_labels"]
    synthesizer_model = vote_config["synthesizer_model"]

    while True:
        vote_results = run_vote(mode, goal, input_files, input_labels)
        outcome, corrections = tally_votes(vote_results, mode, input_labels)

        if mode == "pass_fail":
            if outcome:
                # Vote passed — print final output for the user
                print("\n✅ Vote passed. Final output:\n")
                with open(input_files[0], "r", encoding="utf-8") as f:
                    print(f.read())
                break
            else:
                # Vote failed — synthesizer applies voter corrections and we re-vote
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{ts}] ❌ Vote failed. Applying voter corrections...\n")
                run_vote_synthesis(corrections, input_files[0], synthesizer_model)

        elif mode == "select_best":
            # Winning label determined — print that file and exit
            winner_index = input_labels.index(outcome)
            winner_file = input_files[winner_index]
            print(f"\n✅ Vote complete. Winning output: {outcome}\n")
            with open(winner_file, "r", encoding="utf-8") as f:
                print(f.read())
            break


if __name__ == "__main__":
    main()
