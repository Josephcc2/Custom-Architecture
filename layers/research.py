from layer import Layer

# ----- Context -----
# Shared background prepended to every agent's prompt, regardless of which layer or
# step it's performing. Edit this to change what every agent should always know.
context = (
    "You are one of three AI models — ChatGPT, Claude, and Grok — working together in "
    "a multi-stage research pipeline. Over the course of this pipeline, each model "
    "independently researches and drafts a report, reviews and critiques the other two "
    "models' reports, revises its own report using that feedback, debates with the "
    "other models to reach a shared ranking and consensus on pros and cons, and "
    "finally negotiates with the other models to converge on one single, identical "
    "final report. Keep this larger pipeline in mind at every step, and treat the "
    "other models as collaborators working toward the same shared outcome rather than "
    "competitors."
)

# ----- Task -----
# The task this pipeline works on. Unlike a short topic, this can span multiple lines
# or paragraphs to capture detail a single phrase couldn't.
task = """Research the effects of caffeine on sleep and produce a report accessible to a general, non-scientific audience.

The report should address:
- How caffeine affects sleep onset, duration, and overall quality
- Caffeine's half-life and how the timing of consumption relates to sleep disruption
- Individual variability in caffeine sensitivity (e.g. genetics, age, tolerance, habitual use)
- Practical, evidence-based guidance on caffeine cutoff times for better sleep

Every claim should be grounded in real, citable scientific research rather than anecdotal or unsourced claims."""

# ----- Goal -----
# What the final output must satisfy for the vote to pass.
# Not wired into voting for this particular layers file
goal = (
    f"A final report which must cite at least 3 real sources, use markdown "
    "and Chicago format, and be easy to understand "
    "by those without knowledge on the topic."
)

# Shared header prepended to every layer's prompt below, so every agent sees the same
# context and task no matter which step it's performing.
agent_preamble = f"Context:\n{context}\n\nTask:\n{task}\n\n"

layers = [
    # Parallel
    Layer(
        parallel_to_next_layer=True,
        model_number=0,
        prompt=(
            f"{agent_preamble}"
            "Conduct thorough research on the task above. "
            "Write a thorough report addressing the task in Chicago formatting and markdown. "
            "Include 3 to 5 of the most relevant scientific papers related to the task. "
            "With each paper, include the title, author(s), publication date, and direct link or way to access the paper. "
            "Do not add any extra or unnecessary commentary."
        ),
        output_destination="outputs/ChatGPT/first_report.md",
        output_name="ChatGPT's First Report:",
    ),
    Layer(
        parallel_to_next_layer=True,
        model_number=1,
        prompt=(
            f"{agent_preamble}"
            "Conduct thorough research on the task above. "
            "Write a thorough report addressing the task in Chicago formatting and markdown. "
            "Include 3 to 5 of the most relevant scientific papers related to the task. "
            "With each paper, include the title, author(s), publication date, and direct link or way to access the paper. "
            "Do not add any extra or unnecessary commentary."
        ),
        output_destination="outputs/Claude/first_report.md",
        output_name="Claude's First Report:",
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=2,
        prompt=(
            f"{agent_preamble}"
            "Conduct thorough research on the task above. "
            "Write a thorough report addressing the task in Chicago formatting and markdown. "
            "Include 3 to 5 of the most relevant scientific papers related to the task. "
            "With each paper, include the title, author(s), publication date, and direct link or way to access the paper. "
            "Do not add any extra or unnecessary commentary."
        ),
        output_destination="outputs/Grok/first_report.md",
        output_name="Grok's First Report:",
    ),

    # Feedback
    Layer(
        parallel_to_next_layer=True,
        model_number=0,
        prompt=(
            f"{agent_preamble}"
            "Claude wrote a report addressing the task above. Provide suggestions and "
            "feedback to Claude to improve the report. The report must "
            "be in Chicago formatting, use markdown, and have 3-5 real sources that "
            "are relevant to the task. If Claude fails any of these then be sure to note those "
            "in addition to your other feedback."
        ),
        output_destination="outputs/Claude/chatgpt_revisions.md",
        output_name="ChatGPT's Feedback:",
        input_destinations=["outputs/Claude/first_report.md"]
    ),
    Layer(
        parallel_to_next_layer=True,
        model_number=0,
        prompt=(
            f"{agent_preamble}"
            "Grok wrote a report addressing the task above. Provide suggestions and "
            "feedback to Grok to improve the report. The report must "
            "be in Chicago formatting, use markdown, and have 3-5 real sources that "
            "are relevant to the task. If Grok fails any of these then be sure to note those "
            "in addition to your other feedback."
        ),
        output_destination="outputs/Grok/chatgpt_revisions.md",
        output_name="ChatGPT's Feedback:",
        input_destinations=["outputs/Grok/first_report.md"]
    ),

    Layer(
        parallel_to_next_layer=True,
        model_number=1,
        prompt=(
            f"{agent_preamble}"
            "ChatGPT wrote a report addressing the task above. Provide suggestions and "
            "feedback to ChatGPT to improve the report. The report must "
            "be in Chicago formatting, use markdown, and have 3-5 real sources that "
            "are relevant to the task. If ChatGPT fails any of these then be sure to note those "
            "in addition to your other feedback."
        ),
        output_destination="outputs/ChatGPT/claude_revisions.md",
        output_name="Claude's Feedback:",
        input_destinations=["outputs/ChatGPT/first_report.md"]
    ),
    Layer(
        parallel_to_next_layer=True,
        model_number=1,
        prompt=(
            f"{agent_preamble}"
            "Grok wrote a report addressing the task above. Provide suggestions and "
            "feedback to Grok to improve the report. The report must "
            "be in Chicago formatting, use markdown, and have 3-5 real sources that "
            "are relevant to the task. If Grok fails any of these then be sure to note those "
            "in addition to your other feedback."
        ),
        output_destination="outputs/Grok/claude_revisions.md",
        output_name="Claude's Feedback:",
        input_destinations=["outputs/Grok/first_report.md"]
    ),

    Layer(
        parallel_to_next_layer=True,
        model_number=2,
        prompt=(
            f"{agent_preamble}"
            "Claude wrote a report addressing the task above. Provide suggestions and "
            "feedback to Claude to improve the report. The report must "
            "be in Chicago formatting, use markdown, and have 3-5 real sources that "
            "are relevant to the task. If Claude fails any of these then be sure to note those "
            "in addition to your other feedback."
        ),
        output_destination="outputs/Claude/grok_revisions.md",
        output_name="Grok's Feedback:",
        input_destinations=["outputs/Claude/first_report.md"]
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=2,
        prompt=(
            f"{agent_preamble}"
            "ChatGPT wrote a report addressing the task above. Provide suggestions and "
            "feedback to ChatGPT to improve the report. The report must "
            "be in Chicago formatting, use markdown, and have 3-5 real sources that "
            "are relevant to the task. If ChatGPT fails any of these then be sure to note those "
            "in addition to your other feedback."
        ),
        output_destination="outputs/ChatGPT/grok_revisions.md",
        output_name="Grok's Feedback:",
        input_destinations=["outputs/ChatGPT/first_report.md"]
    ),

    # Review
    Layer(
        parallel_to_next_layer=True,
        model_number=0,
        prompt=(
            f"{agent_preamble}"
            "You initially wrote a report addressing the task above. Claude and Grok reviewed "
            "your report and have provided you with feedback. Taking their feedback into mind, "
            "rewrite your report so that it takes in all of their suggestions.\n"
            "The report must be in Chicago formatting, use markdown, and have "
            "3-5 real sources that are relevant to the task."
        ),
        output_destination="outputs/ChatGPT/revised_report.md",
        output_name="ChatGPT's Revised Report:",
        input_destinations=["outputs/ChatGPT/first_report.md", "outputs/ChatGPT/claude_revisions.md", "outputs/ChatGPT/grok_revisions.md"]
    ),
    Layer(
        parallel_to_next_layer=True,
        model_number=1,
        prompt=(
            f"{agent_preamble}"
            "You initially wrote a report addressing the task above. ChatGPT and Grok reviewed "
            "your report and have provided you with feedback. Taking their feedback into mind, "
            "rewrite your report so that it takes in all of their suggestions.\n"
            "The report must be in Chicago formatting, use markdown, and have "
            "3-5 real sources that are relevant to the task."
        ),
        output_destination="outputs/Claude/revised_report.md",
        output_name="Claude's Revised Report:",
        input_destinations=["outputs/Claude/first_report.md", "outputs/Claude/chatgpt_revisions.md", "outputs/Claude/grok_revisions.md"]
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=2,
        prompt=(
            f"{agent_preamble}"
            "You initially wrote a report addressing the task above. Claude and ChatGPT reviewed "
            "your report and have provided you with feedback. Taking their feedback into mind, "
            "rewrite your report so that it takes in all of their suggestions.\n"
            "The report must be in Chicago formatting, use markdown, and have "
            "3-5 real sources that are relevant to the task."
        ),
        output_destination="outputs/Grok/revised_report.md",
        output_name="Grok's Revised Report:",
        input_destinations=["outputs/Grok/first_report.md", "outputs/Grok/claude_revisions.md", "outputs/Grok/chatgpt_revisions.md"]
    ),


    # --- Aggregate ---
    Layer(
        parallel_to_next_layer=True,
        model_number=0,
        prompt=(
            f"{agent_preamble}"
            "You are presented with 3 reports addressing the task above. "
            "Using markdown, create a list of pros and cons of the details "
            "for each of the three reports. Also, rank each report from 1-3.\n"
            "Keep in mind that each report must be in Chicago formatting, use markdown, "
            "and have 3-5 real sources that are relevant to the task. Do not provide "
            "any unnecessary commentary."
        ),
        output_destination="outputs/ChatGPT/pros_cons.md",
        output_name="ChatGPT's Pros and Cons:",
        input_destinations=["outputs/ChatGPT/revised_report.md", "outputs/Claude/revised_report.md", "outputs/Grok/revised_report.md"]
    ),
    Layer(
        parallel_to_next_layer=True,
        model_number=1,
        prompt=(
            f"{agent_preamble}"
            "You are presented with 3 reports addressing the task above. "
            "Using markdown, create a list of pros and cons of the details "
            "for each of the three reports. Also, rank each report from 1-3.\n"
            "Keep in mind that each report must be in Chicago formatting, use markdown, "
            "and have 3-5 real sources that are relevant to the task. Do not provide "
            "any unnecessary commentary."
        ),
        output_destination="outputs/Claude/pros_cons.md",
        output_name="Claude's Pros and Cons:",
        input_destinations=["outputs/ChatGPT/revised_report.md", "outputs/Claude/revised_report.md", "outputs/Grok/revised_report.md"]
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=2,
        prompt=(
            f"{agent_preamble}"
            "You are presented with 3 reports addressing the task above. "
            "Using markdown, create a list of pros and cons of the details "
            "for each of the three reports. Also, rank each report from 1-3.\n"
            "Keep in mind that each report must be in Chicago formatting, use markdown, "
            "and have 3-5 real sources that are relevant to the task. Do not provide "
            "any unnecessary commentary."
        ),
        output_destination="outputs/Grok/pros_cons.md",
        output_name="Grok's Pros and Cons:",
        input_destinations=["outputs/ChatGPT/revised_report.md", "outputs/Claude/revised_report.md", "outputs/Grok/revised_report.md"]
    ),

    # Debate
    Layer(
        parallel_to_next_layer=False,
        model_number=0,
        prompt=(
            "You are ChatGPT.\n"
            f"{agent_preamble}"
            "You're currently in a 3-way debate about deciding the "
            "pros and cons and rankings for 3 reports addressing the task above. "
            "Given the original reports and everyone's feedback, "
            "come to an agreement with each LLM on the pros and cons for each "
            "report as well as a ranking for the 3 reports.\n"

            "Keep in mind that each report must be in Chicago formatting, use markdown, "
            "and have 3-5 real sources that are relevant to the task. Do not provide "
            "any unnecessary commentary. You have 7 rounds to come to an agreement. "
            "Do your best to meet in the middle with the other LLMs.\n"

            "Do not only list pros and cons for each report and their rankings. "
            "Instead, give reasons for your decisions so that you can persuade the "
            "other LLMs to agree with you.\n"

            "If you have nothing else to add, then simply confirm the ranking "
            "of the reports and the pros and cons list. The pros and cons list "
            "must be the exact same as the other LLMs'.\n"

            "Do not restate the whole report and on the first rounds "
            "focus on finding what differences there are between each LLM's "
            "ranking and pros and cons.\n"

            "Your final message should very simply list the agreed "
            "ranking for the 3 reports, followed by the agreed pros and cons "
            "for each report. The pros and cons list must have the exact "
            "same amount of reasons for each LLM."
        ),
        output_destination="outputs/ChatGPT/debate.md",
        output_name="ChatGPT",
        input_destinations=[
            "outputs/ChatGPT/revised_report.md", "outputs/Claude/revised_report.md", "outputs/Grok/revised_report.md",
            "outputs/ChatGPT/pros_cons.md", "outputs/Claude/pros_cons.md", "outputs/Grok/pros_cons.md"
        ],
        recursive_loops=7,
        recursive_depth=2,
        conversation_output="outputs/conversation.md"
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=1,
        prompt=(
            "You are Claude.\n"
            f"{agent_preamble}"
            "You're currently in a 3-way debate about deciding the "
            "pros and cons and rankings for 3 reports addressing the task above. "
            "Given the original reports and everyone's feedback, "
            "come to an agreement with each LLM on the pros and cons for each "
            "report as well as a ranking for the 3 reports.\n"

            "Keep in mind that each report must be in Chicago formatting, use markdown, "
            "and have 3-5 real sources that are relevant to the task. Do not provide "
            "any unnecessary commentary. You have 7 rounds to come to an agreement. "
            "Do your best to meet in the middle with the other LLMs.\n"

            "Do not only list pros and cons for each report and their rankings. "
            "Instead, give reasons for your decisions so that you can persuade the "
            "other LLMs to agree with you.\n"

            "If you have nothing else to add, then simply confirm the ranking "
            "of the reports and the pros and cons list. The pros and cons list "
            "must be the exact same as the other LLMs'.\n"

            "Do not restate the whole report and on the first rounds "
            "focus on finding what differences there are between each LLM's "
            "ranking and pros and cons.\n"

            "Your final message should very simply list the agreed "
            "ranking for the 3 reports, followed by the agreed pros and cons "
            "for each report. The pros and cons list must have the exact "
            "same amount of reasons for each LLM."
        ),
        output_destination="outputs/Claude/debate.md",
        output_name="Claude",
        input_destinations=[
            "outputs/ChatGPT/revised_report.md", "outputs/Claude/revised_report.md", "outputs/Grok/revised_report.md",
            "outputs/ChatGPT/pros_cons.md", "outputs/Claude/pros_cons.md", "outputs/Grok/pros_cons.md"
        ],
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=2,
        prompt=(
            "You are Grok.\n"
            f"{agent_preamble}"
            "You're currently in a 3-way debate about deciding the "
            "pros and cons and rankings for 3 reports addressing the task above. "
            "Given the original reports and everyone's feedback, "
            "come to an agreement with each LLM on the pros and cons for each "
            "report as well as a ranking for the 3 reports.\n"

            "Keep in mind that each report must be in Chicago formatting, use markdown, "
            "and have 3-5 real sources that are relevant to the task. Do not provide "
            "any unnecessary commentary. You have 7 rounds to come to an agreement. "
            "Do your best to meet in the middle with the other LLMs.\n"

            "Do not only list pros and cons for each report and their rankings. "
            "Instead, give reasons for your decisions so that you can persuade the "
            "other LLMs to agree with you.\n"

            "If you have nothing else to add, then simply confirm the ranking "
            "of the reports and the pros and cons list. The pros and cons list "
            "must be the exact same as the other LLMs'.\n"

            "Do not restate the whole report and on the first rounds "
            "focus on finding what differences there are between each LLM's "
            "ranking and pros and cons.\n"

            "Your final message should very simply list the agreed "
            "ranking for the 3 reports, followed by the agreed pros and cons "
            "for each report. The pros and cons list must have the exact "
            "same amount of reasons for each LLM."
        ),
        output_destination="outputs/Grok/debate.md",
        output_name="Pros and Cons list",
        input_destinations=[
            "outputs/ChatGPT/revised_report.md", "outputs/Claude/revised_report.md", "outputs/Grok/revised_report.md",
            "outputs/ChatGPT/pros_cons.md", "outputs/Claude/pros_cons.md", "outputs/Grok/pros_cons.md"
        ],
    ),

    # Debate to create final report

    # --- Final Report Collaborative Drafting ---
    # The LLMs use the consensus from the previous debate to negotiate the final text.
    # By the end of the loop, they must all output the exact same final report.
    Layer(
        parallel_to_next_layer=False,
        model_number=0,
        prompt=(
            "You are ChatGPT.\n"
            f"{agent_preamble}"

            "You are now in a 5-round collaborative drafting session with Claude and Grok to write the FINAL report addressing the task above. "
            "You must use the agreed-upon pros, cons, and rankings from your previous debate to guide this draft.\n\n"

            "In the early rounds, propose drafts of the text while explaining what you changed, critique the others' additions, "
            "and negotiate the exact wording "
            "line-by-line or section-by-section. Lean into your specific strengths as an AI.\n"
            "DO NOT just keep creating drafts of the report. Instead, always make sure to (unless it's the last round) "
            "explain your reasoning. This is a debate to create the final report. Your final response should be "
            "just the agreed upon final report.\n\n"

            "IMPORTANT: Your ultimate goal is to converge on the EXACT SAME text. "
            "Once you have all agreed on the text (and definitely in your final round), you must output NOTHING BUT the final agreed-upon report. "
            "It must be completely identical to what Claude and Grok will output. "
            "Do not add conversational filler, preambles, or sign-offs in your final output—only the Chicago formatted markdown report.\n"
            "Keep in mind that each report must be in Chicago formatting, use markdown, "
            "and have 3-5 real sources that are relevant to the task. The tone of the report should be "
            "accessible to those with little scientific knowledge on the subject. "
            "Do your best to meet in the middle with the other LLMs."
        ),
        output_destination="outputs/ChatGPT/final_report.md",
        output_name="ChatGPT",
        input_destinations=[
            "outputs/ChatGPT/revised_report.md", "outputs/Claude/revised_report.md",
            "outputs/Grok/revised_report.md", "outputs/Grok/debate.md"
        ],
        recursive_loops=5,
        recursive_depth=2,
        conversation_output="outputs/final_report_drafting_conversation.md"
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=1,
        prompt=(
            "You are Claude.\n"
            f"{agent_preamble}"
            "You are now in a 5-round collaborative drafting session with ChatGPT and Grok to write the FINAL report addressing the task above. "
            "You must use the agreed-upon pros, cons, and rankings from your previous debate to guide this draft.\n\n"

            "In the early rounds, propose drafts of the text while explaining what you changed, critique the others' additions, "
            "and negotiate the exact wording "
            "line-by-line or section-by-section. Lean into your specific strengths as an AI.\n"
            "DO NOT just keep creating drafts of the report. Instead, always make sure to (unless it's the last round) "
            "explain your reasoning. This is a debate to create the final report. Your final response should be "
            "just the agreed upon final report.\n\n"

            "IMPORTANT: Your ultimate goal is to converge on the EXACT SAME text. "
            "Once you have all agreed on the text (and definitely in your final round), you must output NOTHING BUT the final agreed-upon report. "
            "It must be completely identical to what ChatGPT and Grok will output. "
            "Do not add conversational filler, preambles, or sign-offs in your final output—only the Chicago formatted markdown report.\n"
            "Keep in mind that each report must be in Chicago formatting, use markdown, "
            "and have 3-5 real sources that are relevant to the task. The tone of the report should be "
            "accessible to those with little scientific knowledge on the subject. "
            "Do your best to meet in the middle with the other LLMs."
        ),
        output_destination="outputs/Claude/final_report.md",
        output_name="Claude",
        input_destinations=[
            "outputs/ChatGPT/revised_report.md", "outputs/Claude/revised_report.md",
            "outputs/Grok/revised_report.md", "outputs/Grok/debate.md"
        ]
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=2,
        prompt=(
            "You are Grok.\n"
            f"{agent_preamble}"
            "You are now in a 5-round collaborative drafting session with ChatGPT and Claude to write the FINAL report addressing the task above. "
            "You must use the agreed-upon pros, cons, and rankings from your previous debate to guide this draft.\n\n"

            "In the early rounds, propose drafts of the text while explaining what you changed, critique the others' additions, "
            "and negotiate the exact wording "
            "line-by-line or section-by-section. Lean into your specific strengths as an AI.\n"
            "DO NOT just keep creating drafts of the report. Instead, always make sure to (unless it's the last round) "
            "explain your reasoning. This is a debate to create the final report. Your final response should be "
            "just the agreed upon final report.\n\n"

            "IMPORTANT: Your ultimate goal is to converge on the EXACT SAME text. "
            "Once you have all agreed on the text (and definitely in your final round), you must output NOTHING BUT the final agreed-upon report. "
            "It must be completely identical to what ChatGPT and Claude will output. "
            "Do not add conversational filler, preambles, or sign-offs in your final output—only the Chicago formatted markdown report.\n"
            "Keep in mind that each report must be in Chicago formatting, use markdown, "
            "and have 3-5 real sources that are relevant to the task. The tone of the report should be "
            "accessible to those with little scientific knowledge on the subject. "
            "Do your best to meet in the middle with the other LLMs."
        ),
        output_destination="outputs/final_report.md",
        output_name="Final Report",
        input_destinations=[
            "outputs/ChatGPT/revised_report.md", "outputs/Claude/revised_report.md",
            "outputs/Grok/revised_report.md", "outputs/Grok/debate.md"
        ]
    )
]
