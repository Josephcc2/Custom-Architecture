from layer import Layer

topic = "Effects of caffeine on sleep"

# ----- Goal -----
# What the final output must satisfy for the vote to pass.
goal = (
    f"A final report on {topic} which must cite at least 3 real sources, use markdown "
    "and Chicago format, and be easy to understand "
    "by those without knowledge on the topic."
)

og_prompt = (
    "Review the context you got and create a full report based on the provided scientific papers. "
    "Do not create a section for each paper, instead use the information from all of the papers"
    "combined to create your report. "
    f"Make sure the report is detailed and contains any and all relevant information to {topic}. "
    "Assume that the reader of your report does not know much about the topic, so explain"
    "systems that they would not be familliar with. "
    "Do not use information that is not given from the research papers. "
    "expected_output: >\n"
    f"A fully fledged report about {topic} with the main topics, each with a full section of information. "
    "Formatted as markdown without '```'"
    "The report must be in chicago formatting with footnotes when sources are referenced. "
)

debate_prompt = (
    "You are currently in a 3-way debate. "
    "The debaters are as follows: GPT, Claude, and Grok. "

    f"We are fact-checking, improving, and combining two fact-based reports about: {topic} into one final report. "
    "Criticize the two reports and suggest improvements. "
    "Suggest anything from formatting changes, to removing unneeded sections, combining sections, "
    "adding new sections, or anything else you think could make the report better. "
    "All suggestions MUST be backed by a scientific paper which must also be cited in your response. "
    "The final report must have at least between 3-5 references, and no more than 7. "
    "The final report must be in chicago formatting with footnotes when sources are referenced. "
    "Each section must include a citation of which references were used as [X] where X is the number of the reference. "
    "Respond concisely but with justification. "
    f"The final report is meant to be an in-depth answer to the user's scientific question: {topic}. "
    "Consider others' suggestions and make sure to respond to them with your opinions. "
    f"Stay strictly on topic. "
    "If you have nothing new to add, you may simply say 'pass'. "
    "You have a total of 7 rounds of discussion before you must make a final decision. "
    "Your final decision is the full report with all the changes agreed upon.\n\n"

    "The report should be formatted as markdown without [```]. Don't add anything unnecessary, such as using html in the report. "
    "Make sure to confirm the **full** report by round 7 so that your final answers are the same. "
    "By round 7, you must all have reached a full consensus. "
    "Begin your statement by going straight to the details, "
    "there is no need to restate the round number or insert your name.\n"
)

layers = [
    # Phase 1
    Layer(
        parallel_to_next_layer=True,
        model_number=0,
        prompt=(
            "Conduct a thorough research about {topic}. "
            "Make sure you find any interesting and relevant scientific papers.\n"
            f"Create a list with 3 to 5 of the most relevant scientific papers about {topic}. "
            "With each paper, include the title, author(s), publication date, and direct link or way to access the paper. "
            "Do no add any extra or unnecessary commentary."
        ),
        output_destination="outputs/ChatGPT/sources.txt",
        output_name="Sources:",
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=1,
        prompt=(
            "Conduct a thorough research about {topic}. "
            "Make sure you find any interesting and relevant scientific papers.\n"
            f"Create a list with 3 to 5 of the most relevant scientific papers about {topic}. "
            "With each paper, include the title, author(s), publication date, and direct link or way to access the paper. "
            "Do no add any extra or unnecessary commentary."
        ),
        output_destination="outputs/Claude/sources.txt",
        output_name="Sources:",
    ),

    Layer(
        parallel_to_next_layer=True,
        model_number=0,
        prompt=(
            "Review the context you got and create a full report based on the provided scientific papers. "
            "Do not create a section for each paper, instead use the information from all of the papers "
            "combined to create your report. "
            f"Make sure the report is detailed and contains any and all relevant information to {topic}. "
            "Assume that the reader of your report does not know much about the topic, so explain "
            "systems that they would not be familliar with. "
            "Do not use information that is not given from the research papers.\n\n"
            f"The expectation is a fully fledged report about {topic} with the main topics, "
            "each with a full section of information. Formatted as markdown without '```'"
        ),
        output_destination="outputs/ChatGPT/mock_report.txt",
        output_name="ChatGPT's Mock Report:",
        input_destinations=["outputs/ChatGPT/sources.txt"]
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=1,
        prompt=(
            "Review the context you got and create a full report based on the provided scientific papers. "
            "Do not create a section for each paper, instead use the information from all of the papers "
            "combined to create your report. "
            f"Make sure the report is detailed and contains any and all relevant information to {topic}. "
            "Assume that the reader of your report does not know much about the topic, so explain "
            "systems that they would not be familliar with. "
            "Do not use information that is not given from the research papers.\n\n"
            f"The expectation is a fully fledged report about {topic} with the main topics, "
            "each with a full section of information. Formatted as markdown without '```'"
        ),
        output_destination="outputs/Claude/mock_report.txt",
        output_name="Claude's Mock Report:",
        input_destinations=["outputs/Claude/sources.txt"]
    ),

    Layer(
        parallel_to_next_layer=True,
        model_number=0,
        prompt=(
            "You are a designer. "
            "Review the context you got and section the report into groups as needed. "
            "Create citations for all of the scientific papers at the end of the report. "
            "Do not add or change any information in the report.\n\n"

            f"The expected output is a fully fledged report about {topic} sectioned into groups, "
            "each with a full section of information. A single list of citations at the end of the report. "
            "The whole paper in chicago formatting. Formatted as markdown without '```'"
        ),
        output_destination="outputs/ChatGPT/report.txt",
        output_name="ChatGPT's Report:",
        input_destinations=["outputs/ChatGPT/sources.txt", "outputs/ChatGPT/mock_report.txt"]
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=1,
        prompt=(
            "You are a designer. "
            "Review the context you got and section the report into groups as needed. "
            "Create citations for all of the scientific papers at the end of the report. "
            "Do not add or change any information in the report.\n\n"

            f"The expected output is a fully fledged report about {topic} sectioned into groups, "
            "each with a full section of information. A single list of citations at the end of the report. "
            "The whole paper in chicago formatting. Formatted as markdown without '```'"
        ),
        output_destination="outputs/Claude/report.txt",
        output_name="Claude's Report:",
        input_destinations=["outputs/Claude/sources.txt", "outputs/Claude/mock_report.txt"]
    ),

    # Phase 2
    Layer(
        parallel_to_next_layer=True,
        model_number=2,
        prompt=(
            f"You have been given a report on {topic} which was written by ChatGPT. Suggest improvements for the report. "
            "Keep in mind that the report should be backed the *real*, fact-based sources and be in Chicago formatting."
        ),
        output_destination="outputs/ChatGPT/revisions.txt",
        output_name="Grok's Imporvements For ChatGPT:",
        input_destinations=["outputs/ChatGPT/report.txt"]
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=2,
        prompt=(
            f"You have been given a report on {topic} which was written by ChatGPT. Suggest improvements for the report. "
            "Keep in mind that the report should be backed the *real*, fact based sources and be in Chicago formatting."
        ),
        output_destination="outputs/Claude/revisions.txt",
        output_name="Grok's Improvements For Claude:",
        input_destinations=["outputs/Claude/report.txt"]
    ),

    # Phase 3
    Layer(
        parallel_to_next_layer=True,
        model_number=0,
        prompt=(
            "You were originally given the following instrctions to create a report.\n\n"
            f"Original instructions:\n{og_prompt}\n\n"
            f"The topic is as follows:\n{topic}\n\n"
            f"The original report that you created is provided below. "
            "Grok revised your report, fact-checking the report and adding new content. "
            "Revise the report based on Grok's revisions and your original instructions. "
            "Do not add any unnecessary final remarks, provide just the report."
        ),
        output_destination="outputs/ChatGPT/revised_report.txt",
        output_name="ChatGPT's Revised Report:",
        input_destinations=["outputs/ChatGPT/report.txt", "outputs/ChatGPT/revisions.txt"]
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=1,
        prompt=(
            "You were originally given the following instrctions to create a report.\n\n"
            f"Original instructions:\n{og_prompt}\n\n"
            f"The topic is as follows:\n{topic}\n\n"
            f"The original report that you created is provided below. "
            "Grok revised your report, fact-checking the report and adding new content. "
            "Revise the report based on Grok's revisions and your original instructions. "
            "Do not add any unnecessary final remarks, provide just the report."
        ),
        output_destination="outputs/Claude/revised_report.txt",
        output_name="Claude's Revised Report:",
        input_destinations=["outputs/Claude/report.txt", "outputs/Claude/revisions.txt"]
    ),

    # Phase 4
    Layer(
        parallel_to_next_layer=False,
        model_number=0,
        prompt=debate_prompt,
        output_destination="outputs/ChatGPT/debate.txt",
        output_name="ChatGPT",
        input_destinations=["outputs/ChatGPT/revised_report.txt", "outputs/Claude/revised_report.txt"],
        recursive_loops=7,
        recursive_depth=2,
        conversation_output="outputs/conversation.txt"
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=1,
        prompt=debate_prompt,
        output_destination="outputs/Claude/debate.txt",
        output_name="Claude",
        input_destinations=["outputs/ChatGPT/revised_report.txt", "outputs/Claude/revised_report.txt"],
    ),
    Layer(
        parallel_to_next_layer=False,
        model_number=2,
        prompt=debate_prompt,
        output_destination="outputs/debate_grok.txt",
        output_name="Grok",
        input_destinations=["outputs/ChatGPT/revised_report.txt", "outputs/Claude/revised_report.txt"],
    ),

    # Synthesize
    Layer(
        parallel_to_next_layer=False,
        model_number=2,
        prompt=(
            f"Original prompt:\n{debate_prompt}\n\n"

            "You have been given a transcript of the debate between three AI agents on creating a "
            f"single scientific report from 2 other reports on {topic} as well as the 2 original reports. "

            "Based on your previous conversation, come to a final **merged consensus** on the new, full, report. "
            "All scientific papers that were used to add additional data to the report MUST be cited at the end of the report. "
            "The report should be formatted as markdown without [```]. "
            "Stay strictly on topic and provide only the final agreed report. "
            "Do not add any unnecessary final remarks, provide just the report."
        ),
        output_destination="outputs/final_report.md",
        output_name="Final Report",
        input_destinations=["outputs/ChatGPT/revised_report.txt", "outputs/Claude/revised_report.txt", "outputs/conversation.txt"]
    )
]
