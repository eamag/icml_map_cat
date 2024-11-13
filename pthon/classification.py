import google.generativeai as genai
import textwrap
from schema import create_schema
import time
from google.api_core.exceptions import InternalServerError

levels = {
    4: "area",
    5: "topic",
    6: "subtopic",
}

hierarchy = """
1. Field: Computer Science
This is the broadest level, encompassing all research within the field of computer science.
2. Discipline: Artificial Intelligence
This layer represents a major subfield within computer science, focusing on the development of intelligent machines.
3. Sub-Discipline: Machine Learning
This is a subset of Artificial Intelligence focusing specifically on algorithms that allow machines to learn from data.
4. Area: Optimization Techniques in Machine Learning
This level represents a specific area within Machine Learning, focusing on optimization methods used in learning algorithms.
5. Topic: AdamW Optimizer
This is a specific topic within the area of Optimization Techniques, focusing on a particular optimization algorithm.
6. Subtopic: New Variants of AdamW
This level represents a more specific focus within the topic of the AdamW optimizer, looking at new variations or modifications of the original algorithm.
"""


def create_function_declaration(level, current_classification):
    desc = f"Classifies paper into level {level} category"
    if level == 6:
        desc += " and provides additional information about tasks, research and alternatives"
    return genai.protos.FunctionDeclaration(
        name=f"level{level}_func",
        description=textwrap.dedent(desc),
        parameters=create_schema(level, current_classification),
    )


def classify_level(level, processed_text, current_classification, categories_str):
    system_prompt = """You are an expert research paper classifier. You read the research paper and classify it into hierarchical classes, which are used on the website to cluster papers under the same topics and problems. 
    You MUST reuse existing categories as much as possible. You do not create new categories unless you cannot match any of the required categories. You use API to fill the classification website for scientists.
    """

    instructions = f"""Classify the paper above into the lower category level. Use available categories as much as possible, create a new one only if your classification doesn't match any of them. 
    Lower category must be stricter more detailed. For example if sub_branch is Graph Representation Learning, area CAN NOT be Representation Learning, and should be something like Contrastive Learning. Levels are {levels}. Give a reasoning for the classification in a separate field.
    """
    if level == 6:
        instructions += """Your most important goal is also to include the list of at least two concise problems, a short description of the next research an ambitious developer can do following up this paper,
        the chance of receiving outstanding award at ICML 2024, and, most importantly, at least 5 concrete tasks with varied levels of difficulty from 1 to 5 that ambitious people can do to improve in this sub area of science.
        Additionally, you have to include at least two alternative non-overlapping classifications to make the classification more robust.
        At last you have to access what are the real life implications of this, and provide one very short and concise step by step example of findings from this paper applied to a problem to create a startup that solves this problem."""

    prompt = f"""## The hierarchical structure of scientific knowledge
    {hierarchy}
    ## Input paper
    {processed_text}
    ## Available categories
    {categories_str}
    ## Instructions
    {instructions}
    ## Classification so far
    {current_classification}
    ## Your classification for {levels[level]}:"""

    model_name = "models/gemini-1.5-flash"
    # if level == 6:
    #     model_name = "models/gemini-1.5-pro"
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_prompt,
        tools=[create_function_declaration(level, current_classification)],
    )
    retry_count = 10
    wait_time = 3
    for attempt in range(retry_count + 1):
        try:
            result = model.generate_content(
                prompt, tool_config={"function_calling_config": "ANY"}
            )
            print(f"tokens used {result.usage_metadata.total_token_count}")
            fc = result.candidates[0].content.parts[0].function_call
            return type(fc).to_dict(fc)["args"] if fc is not None else result
        except (InternalServerError, KeyError, IndexError) as e:
            if attempt < retry_count:
                print(
                    f"{e} occurred. Retrying in {wait_time*attempt} seconds..., attempt {attempt}"
                )
                time.sleep(wait_time * attempt)
            else:
                raise e
