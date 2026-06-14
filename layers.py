from layer import Layer

topic = "Effects of caffeine on sleep"

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
