# This file is not used in the program, but holds other architecutres that I have built with this project
# For each one, the `layers.py` and `config.yaml` files are both provided with a short desciption of the architecture
# To use, simply take the code for the layers, and paste it into your 'layers.py' file and do the same for the config

# Anti-aggregation report creation
# Generates a report on the given topic. Multiple agents work together to create the report and
# the architecture avoids having a single LLM aggregate their responses to remove bias.
# Instead, all 3 agents work together to create an agreed upon final report.
# The final report can be found in outputs/final_report.md

# `layers.py`
from layer import Layer

topic = "Effects of caffeine on sleep"

# ----- Goal -----
# What the final output must satisfy for the vote to pass. (not used for this architecutre)
goal = (
    f"A final report on {topic} which must cite at least 3 real sources, use markdown "
    "and Chicago format, and be easy to understand "
    "by those without knowledge on the topic."
)

layers = [
    # Parallel
    Layer(
        parallel_to_next_layer=True,
        model_number=0,
        prompt=(
            f"Conduct a thorough research about {topic}. "
            f"Write a thorough report on {topic} in Chicago formatting and markdown. "
            f"Include 3 to 5 of the most relevant scientific papers about {topic}. "
            "With each paper, include the title, author(s), publication date, and direct link or way to access the paper. "
            "Do no add any extra or unnecessary commentary."
        ),
        output_destination="outputs/ChatGPT/first_report.md",
        output_name="ChatGPT's First Report:",
    ),
    Layer(
        parallel_to_next_layer=True,
        model_number=1,
        prompt=(
            f"Conduct a thorough research about {topic}. "
            f"Write a thorough report on {topic} in Chicago formatting and markdown. "
            f"Include 3 to 5 of the most relevant scientific papers about {topic}. "
            "With each paper, include the title, author(s), publication date, and direct link or way to access the paper. "
            "Do no add any extra or unnecessary commentary."
        ),
        output_destination="outputs/Claude/first_report.md",
        output_name="Claude's First Report:",
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=2,
        prompt=(
            f"Conduct a thorough research about {topic}. "
            f"Write a thorough report on {topic} in Chicago formatting and markdown. "
            f"Include 3 to 5 of the most relevant scientific papers about {topic}. "
            "With each paper, include the title, author(s), publication date, and direct link or way to access the paper. "
            "Do no add any extra or unnecessary commentary."
        ),
        output_destination="outputs/Grok/first_report.md",
        output_name="Grok's First Report:",
    ),

    # Feedback
    Layer(
        parallel_to_next_layer=True,
        model_number=0,
        prompt=(
            f"Conduct a thorough research about {topic}. "
            f"Claude wrote a report on {topic}. Provide suggestions and "
            "feedback to Claude to imp[rove the report. The report must "
            "be in Chicago formatting, use markdown, and have 3-5 real sources that "
            "are relevant to the paper. If Claude fails any of these then be sure to note those "
            "in addition to you other feedback."
        ),
        output_destination="outputs/Claude/chatgpt_revisions.md",
        output_name="ChatGPT's Feedback:",
        input_destinations=["outputs/Claude/first_report.md"]
    ),
    Layer(
        parallel_to_next_layer=True,
        model_number=0,
        prompt=(
            f"Conduct a thorough research about {topic}. "
            f"Grok wrote a report on {topic}. Provide suggestions and "
            "feedback to Grok to imp[rove the report. The report must "
            "be in Chicago formatting, use markdown, and have 3-5 real sources that "
            "are relevant to the paper. If Grok fails any of these then be sure to note those "
            "in addition to you other feedback."
        ),
        output_destination="outputs/Grok/chatgpt_revisions.md",
        output_name="ChatGPT's Feedback:",
        input_destinations=["outputs/Grok/first_report.md"]
    ),

    Layer(
        parallel_to_next_layer=True,
        model_number=1,
        prompt=(
            f"Conduct a thorough research about {topic}. "
            f"ChatGPT wrote a report on {topic}. Provide suggestions and "
            "feedback to ChatGPT to imp[rove the report. The report must "
            "be in Chicago formatting, use markdown, and have 3-5 real sources that "
            "are relevant to the paper. If ChatGPT fails any of these then be sure to note those "
            "in addition to you other feedback."
        ),
        output_destination="outputs/ChatGPT/claude_revisions.md",
        output_name="Claude's Feedback:",
        input_destinations=["outputs/ChatGPT/first_report.md"]
    ),
    Layer(
        parallel_to_next_layer=True,
        model_number=1,
        prompt=(
            f"Conduct a thorough research about {topic}. "
            f"Grok wrote a report on {topic}. Provide suggestions and "
            "feedback to Grok to imp[rove the report. The report must "
            "be in Chicago formatting, use markdown, and have 3-5 real sources that "
            "are relevant to the paper. If Grok fails any of these then be sure to note those "
            "in addition to you other feedback."
        ),
        output_destination="outputs/Grok/claude_revisions.md",
        output_name="Claude's Feedback:",
        input_destinations=["outputs/Grok/first_report.md"]
    ),

    Layer(
        parallel_to_next_layer=True,
        model_number=2,
        prompt=(
            f"Conduct a thorough research about {topic}. "
            f"Claude wrote a report on {topic}. Provide suggestions and "
            "feedback to Claude to imp[rove the report. The report must "
            "be in Chicago formatting, use markdown, and have 3-5 real sources that "
            "are relevant to the paper. If Claude fails any of these then be sure to note those "
            "in addition to you other feedback."
        ),
        output_destination="outputs/Claude/grok_revisions.md",
        output_name="Grok's Feedback:",
        input_destinations=["outputs/Claude/first_report.md"]
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=2,
        prompt=(
            f"Conduct a thorough research about {topic}. "
            f"ChatGPT wrote a report on {topic}. Provide suggestions and "
            "feedback to ChatGPT to imp[rove the report. The report must "
            "be in Chicago formatting, use markdown, and have 3-5 real sources that "
            "are relevant to the paper. If ChatGPT fails any of these then be sure to note those "
            "in addition to you other feedback."
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
            f"Conduct a thorough research about {topic}. "
            f"You initially wrote a report on {topic}. Claude and Grok reviewed "
            "your report and have provided you with feedback. Taking their feedback into mind, "
            "rewrite your report so that it takes in all of their suggestions.\n"
            "The report must be in Chicago formatting, use markdown, and have  "
            "3-5 real sources that are relevant to the paper."
        ),
        output_destination="outputs/ChatGPT/revised_report.md",
        output_name="ChatGPT's Revised Report:",
        input_destinations=["outputs/ChatGPT/first_report.md", "outputs/ChatGPT/claude_revisions.md", "outputs/ChatGPT/grok_revisions.md"]
    ),
    Layer(
        parallel_to_next_layer=True,
        model_number=1,
        prompt=(
            f"Conduct a thorough research about {topic}. "
            f"You initially wrote a report on {topic}. ChatGPT and Grok reviewed "
            "your report and have provided you with feedback. Taking their feedback into mind, "
            "rewrite your report so that it takes in all of their suggestions.\n"
            "The report must be in Chicago formatting, use markdown, and have  "
            "3-5 real sources that are relevant to the paper."
        ),
        output_destination="outputs/Claude/revised_report.md",
        output_name="Claude's Revised Report:",
        input_destinations=["outputs/Claude/first_report.md", "outputs/Claude/chatgpt_revisions.md", "outputs/Claude/grok_revisions.md"]
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=2,
        prompt=(
            f"Conduct a thorough research about {topic}. "
            f"You initially wrote a report on {topic}. Claude and ChatGPT reviewed "
            "your report and have provided you with feedback. Taking their feedback into mind, "
            "rewrite your report so that it takes in all of their suggestions.\n"
            "The report must be in Chicago formatting, use markdown, and have  "
            "3-5 real sources that are relevant to the paper."
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
            f"Conduct a thorough research about {topic}. "
            f"You are presented with 3 reports on {topic}. "
            "Using markdown, create a list of pros and cons of the details "
            "for each of the three reports. Also, rank each report from 1-3.\n"
            "Keep in mind that each report must be in Chicago formatting, use markdown, "
            "and have 3-5 real sources that are relevant to the paper. Do not provide "
            "any unecessary commentary."
        ),
        output_destination="outputs/ChatGPT/pros_cons.md",
        output_name="ChatGPT's Pros and Cons:",
        input_destinations=["outputs/ChatGPT/revised_report.md", "outputs/Claude/revised_report.md", "outputs/Grok/revised_report.md"]
    ),
    Layer(
        parallel_to_next_layer=True,
        model_number=1,
        prompt=(
            f"Conduct a thorough research about {topic}. "
            f"You are presented with 3 reports on {topic}. "
            "Using markdown, create a list of pros and cons of the details "
            "for each of the three reports. Also, rank each report from 1-3.\n"
            "Keep in mind that each report must be in Chicago formatting, use markdown, "
            "and have 3-5 real sources that are relevant to the paper. Do not provide "
            "any unecessary commentary."
        ),
        output_destination="outputs/Claude/pros_cons.md",
        output_name="Claude's Pros and Cons:",
        input_destinations=["outputs/ChatGPT/revised_report.md", "outputs/Claude/revised_report.md", "outputs/Grok/revised_report.md"]
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=2,
        prompt=(
            f"Conduct a thorough research about {topic}. "
            f"You are presented with 3 reports on {topic}. "
            "Using markdown, create a list of pros and cons of the details "
            "for each of the three reports. Also, rank each report from 1-3.\n"
            "Keep in mind that each report must be in Chicago formatting, use markdown, "
            "and have 3-5 real sources that are relevant to the paper. Do not provide "
            "any unecessary commentary."
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
            f"Conduct a thorough research about {topic}.\n\n"
            "You re currently in a 3-way debate about deciding the "
            f"pros and cons and rankings for 3 reports on {topic}. "
            "Given the original reports and everyone's feedback, "
            "come to an agreement with each LLM on the pros and cons for each "
            "report as well as a ranking for the 3 reports.\n"

            "Keep in mind that each report must be in Chicago formatting, use markdown, "
            "and have 3-5 real sources that are relevant to the paper. Do not provide "
            "any unecessary commentary. You have 7 rounds to come to an agreement. "
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
            f"Conduct a thorough research about {topic}.\n\n"
            "You re currently in a 3-way debate about deciding the "
            f"pros and cons and rankings for 3 reports on {topic}. "
            "Given the original reports and everyone's feedback, "
            "come to an agreement with each LLM on the pros and cons for each "
            "report as well as a ranking for the 3 reports.\n"

            "Keep in mind that each report must be in Chicago formatting, use markdown, "
            "and have 3-5 real sources that are relevant to the paper. Do not provide "
            "any unecessary commentary. You have 7 rounds to come to an agreement. "
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
            f"Conduct a thorough research about {topic}.\n\n"
            "You re currently in a 3-way debate about deciding the "
            f"pros and cons and rankings for 3 reports on {topic}. "
            "Given the original reports and everyone's feedback, "
            "come to an agreement with each LLM on the pros and cons for each "
            "report as well as a ranking for the 3 reports.\n"

            "Keep in mind that each report must be in Chicago formatting, use markdown, "
            "and have 3-5 real sources that are relevant to the paper. Do not provide "
            "any unecessary commentary. You have 7 rounds to come to an agreement. "
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
            f"Topic: {topic}\n\n"

            f"You are now in a 5-round collaborative drafting session with Claude and Grok to write the FINAL report on {topic}. "
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
            "and have 3-5 real sources that are relevant to the paper. The tone of the paper should be "
            "accessible to those with little scientific knowledge on the topic. "
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
            f"Topic: {topic}\n\n"
            f"You are now in a 5-round collaborative drafting session with ChatGPT and Grok to write the FINAL report on {topic}. "
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
            "Do not add conversational filler, preambles, or sign-offs in your final output—only the Chicago formatted markdown report."
            "Keep in mind that each report must be in Chicago formatting, use markdown, "
            "and have 3-5 real sources that are relevant to the paper. The tone of the paper should be "
            "accessible to those with little scientific knowledge on the topic. "
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
            f"Topic: {topic}\n\n"
            f"You are now in a 5-round collaborative drafting session with ChatGPT and Claude to write the FINAL report on {topic}. "
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
            "Do not add conversational filler, preambles, or sign-offs in your final output—only the Chicago formatted markdown report."
            "Keep in mind that each report must be in Chicago formatting, use markdown, "
            "and have 3-5 real sources that are relevant to the paper. The tone of the paper should be "
            "accessible to those with little scientific knowledge on the topic. "
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


# `config.yaml`
ai_models:
  - company: OpenAI
    model: gpt-5-nano
    max_tokens: 8192
    persona: You are a scientific debater and writer who focuses on making sure each section of the report has plenty of information, expanding on smaller sections where necessary.
  - company: Anthropic
    model: claude-haiku-4-5
    max_tokens: 8192
    persona: You are a scientific debater and writer focused on small details with a strong sense of attention to detail. You also focus on making sure that every scientific paper is cited correctly and that there are papers supporting every claim.
  - company: xAI
    model: grok-4.3
    max_tokens: 8192
    persona: You are a scientific debater and writer focused on following the given instructions and making sure that the report is set up properly. You also like to focus on adding style in the report's writing while making sure that the report is easy to read by those without knowledge on the topic.

# Note: only enter an ODD amount of LLMs here so that voting can run smoothly
voting_models:
  - company: OpenAI
    model: gpt-4o-mini
    max_tokens: 2048
  - company: Anthropic
    model: claude-haiku-4-5
    max_tokens: 4096
  - company: xAI
    model: grok-4.3
    max_tokens: 8192

vote_config:
  # Whether voting is enabled at all. If false, the pipeline runs and exits
  # without any vote or synthesis step.
  enabled: false

  # pass_fail  → voters judge a single output against the goal. If it fails,
  #              voters list corrections which a synthesizer merges into a
  #              revised output, then the vote runs again.
  # select_best → voters pick the best output from multiple candidates.
  mode: pass_fail

  # File(s) the voters will read and evaluate.
  # For pass_fail: one file. For select_best: two or more files.
  input_files:
    - outputs/final_report.md

  # Labels for each input file (used in select_best prompts, e.g. OUTPUT_A, OUTPUT_B).
  # Must match the length of input_files when mode is select_best. Ignored in pass_fail.
  input_labels:
    - OUTPUT_A
    - OUTPUT_B

  # Index into ai_models for the model that applies voter corrections back into
  # the output file. Only used in pass_fail mode.
  synthesizer_model: 2
