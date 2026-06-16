from layer import Layer

topic = "Effects of caffeine on sleep"

# ----- Goal & Voting Config -----
# goal: what the final output must satisfy for the vote to pass.
goal = (
    "The final report must be at least 1000 words, cite a minimum of 5 real sources "
    "in Chicago format, and cover both short-term and long-term effects of caffeine on sleep."
)

vote_config = {
    # "pass_fail"  → voters judge a single output against the goal.
    #                If it passes, the output is surfaced. If it fails, voters list
    #                corrections which a synthesizer merges into a revised output,
    #                then the vote runs again.
    # "select_best" → voters pick the best output from multiple candidates.
    "mode": "pass_fail",

    # File(s) the voters will read and evaluate.
    # For "pass_fail": one file. For "select_best": two or more files.
    "input_files": ["outputs/final_report.md"],

    # Labels for each input file (used in "select_best" prompts, e.g. "OUTPUT_A", "OUTPUT_B").
    # Must match the length of input_files when mode is "select_best". Ignored in "pass_fail".
    "input_labels": ["OUTPUT_A", "OUTPUT_B"],

    # Index into ai_models (in config.yaml) for the model that synthesizes voter
    # corrections back into the output file. Only used in "pass_fail" mode.
    "synthesizer_model": 2,
}

layers = [
    # Phase 1
    Layer(
        parallel_to_next_layer=True,
        model_number=0,
        prompt=(
            f"Create a comprehensive report on {topic}. Inlcude sources and use Chicago formatting."
        ),
        output_destination="outputs/report_chatgpt.txt",
        output_name="ChatGPT's Original Report",
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=1,
        prompt=(
            f"Create a comprehensive report on {topic}. Inlcude sources and use Chicago formatting."
        ),
        output_destination="outputs/report_claude.txt",
        output_name="Claude's Original Report",
    ),

    # Phase 2
    Layer(
        parallel_to_next_layer=True,
        model_number=2,
        prompt=(
            f"You have been given a report on {topic} which was written by ChatGPT. Suggest improvements for the report. "
            "Keep in mind that the report should be backed the *real*, fact-based sources and be in Chicago formatting."
        ),
        output_destination="outputs/chatgpt_revised.txt",
        output_name="Grok's Imporvements For ChatGPT",
        input_destinations=["outputs/report_chatgpt.txt"]
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=2,
        prompt=(
            f"You have been given a report on {topic} which was written by ChatGPT. Suggest improvements for the report. "
            "Keep in mind that the report should be backed the *real*, fact based sources and be in Chicago formatting."
        ),
        output_destination="outputs/claude_revised.txt",
        output_name="Grok's Improvements For Claude",
        input_destinations=["outputs/report_claude.txt"]
    ),

    # Phase 3
    Layer(
        parallel_to_next_layer=True,
        model_number=0,
        prompt=(
            f"You originally wrote a report on {topic}. Your report was revised by Grok who has suggested possible improvements. "
            "Taking those improvements in mind, revise your report. Keep in mind that the report should be backed by *real*, fact-based "
            "sources and be in Chicago formatting."
        ),
        output_destination="outputs/revised_report_chatgpt.txt",
        output_name="ChatGPT's Revised Report",
        input_destinations=["outputs/report_chatgpt.txt", "outputs/chatgpt_revised.txt"]
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=1,
        prompt=(
            f"You originally wrote a report on {topic}. Your report was revised by Grok who has suggested possible improvements. "
            "Taking those improvements in mind, revise your report. Keep in mind that the report should be backed by *real*, fact-based "
            "sources and be in Chicago formatting."
        ),
        output_destination="outputs/revised_report_claude.txt",
        output_name="Claude's Revised Report",
        input_destinations=["outputs/report_claude.txt", "outputs/claude_revised.txt"]
    ),

    # Phase 4
    Layer(
        parallel_to_next_layer=False,
        model_number=0,
        prompt=(
            f"You are in a debate with Claude and Grok to create a single report on {topic} from two "
            "previous reports. Make a concise argument for what should be changed to create a single report. "
            "Keep in mind that the report should be backed by *real*, fact-based sources and be in Chicago formatting. "
            "If a conversation history is provided, read it carefully and respond directly to the opposing agents' "
            "most recent argument — do not just repeat yourself. Stay focused and persuasive."
        ),
        output_destination="outputs/debate_chatgpt.txt",
        output_name="ChatGPT",
        input_destinations=["outputs/revised_report_chatgpt.txt", "outputs/revised_report_claude.txt"],
        recursive_loops=3,
        recursive_depth=2,
        conversation_output="outputs/conversation.txt"
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=1,
        prompt=(
            f"You are in a debate with ChatGPT and Grok to create a single report on {topic} from two "
            "previous reports. Make a concise argument for what should be changed to create a single report. "
            "Keep in mind that the report should be backed by *real*, fact-based sources and be in Chicago formatting. "
            "If a conversation history is provided, read it carefully and respond directly to the opposing agents' "
            "most recent argument — do not just repeat yourself. Stay focused and persuasive."
        ),
        output_destination="outputs/debate_claude.txt",
        output_name="Claude",
        input_destinations=["outputs/revised_report_chatgpt.txt", "outputs/revised_report_claude.txt"]
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=2,
        prompt=(
            f"You are in a debate with ChatGPT and Claude to create a single report on {topic} from two "
            "previous reports. Make a concise argument for what should be changed to create a single report. "
            "Keep in mind that the report should be backed by *real*, fact-based sources and be in Chicago formatting. "
            "If a conversation history is provided, read it carefully and respond directly to the opposing agents' "
            "most recent argument — do not just repeat yourself. Stay focused and persuasive."
        ),
        output_destination="outputs/debate_grok.txt",
        output_name="Grok",
        input_destinations=["outputs/revised_report_chatgpt.txt", "outputs/revised_report_claude.txt"]
    ),

    # Synthesize
    Layer(
        parallel_to_next_layer=False,
        model_number=1,
        prompt=(
            "You have been given a transcript of a debate between three AI agents on creating a "
            f"single scientific report from 2 other reports on {topic} as well as the 2 original reports. "
            "Read the full conversation carefully, then synthesize what was said into a single, final report. "
            "Keep in mind that the report should be backed by *real*, fact-based sources and be in Chicago formatting."
        ),
        output_destination="outputs/final_report.md",
        output_name="Claude's Final Report",
        input_destinations=["outputs/revised_report_chatgpt.txt", "outputs/revised_report_claude.txt", "outputs/conversation.txt"]
    )
]
