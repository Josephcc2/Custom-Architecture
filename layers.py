from layer import Layer

layers = [
    # ----- Recursive debate: ChatGPT vs Grok (3 loops, depth 1 = 2 agents) -----
    # Layer 0 — ChatGPT argues its position. Kicks off the recursive group.
    Layer(
        False,
        0,
        (
            "You are debating which programming language is the best general-purpose language. "
            "You personally champion Python. Make a concise argument (3–5 sentences) for why Python is the best. "
            "If a conversation history is provided, read it carefully and respond directly to the opposing agent's "
            "most recent argument — do not just repeat yourself. Stay focused and persuasive."
        ),
        "outputs/debate_chatgpt.txt", # individual output saved each loop (overwritten per loop)
        "ChatGPT (Python advocate)",
        recursive_loops=3,
        recursive_depth=1,
        conversation_output="outputs/conversation.txt" # shared conversation file built across all loops
    ),

    # Layer 1 — Grok argues against. Included in the recursive group because depth=1.
    Layer(
        False,
        2,
        (
            "You are debating which programming language is the best general-purpose language. "
            "You personally champion Rust. Make a concise argument (3–5 sentences) for why Rust is the best. "
            "If a conversation history is provided, read it carefully and respond directly to the opposing agent's "
            "most recent argument — do not just repeat yourself. Stay focused and persuasive."
        ),
        "outputs/debate_grok.txt", # individual output saved each loop (overwritten per loop)
        "Grok (Rust advocate)",
        # recursive_loops and recursive_depth are not set here — only the lead layer (Layer 0) controls the group
    ),

    # ----- Layer 2 — Claude reads the full conversation and delivers a verdict -----
    Layer(
        False,
        1,
        (
            "You have been given a transcript of a debate between two AI agents: one arguing for Python "
            "and one arguing for Rust as the best general-purpose programming language. "
            "Read the full conversation carefully, then deliver a balanced and well-reasoned verdict. "
            "Which agent made the stronger case, and why? Keep your response to one short paragraph."
        ),
        "outputs/verdict.txt",
        "Claude's Verdict",
        input_destinations=["outputs/conversation.txt"] # reads the full debate transcript
    ),
]
