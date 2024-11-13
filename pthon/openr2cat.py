import json

import cohere
from openreview_cat import get_reviews
from pdf_parser import process_paper

cohere_api_key = "None"
co = cohere.Client(api_key=cohere_api_key)


def openr2cat(s):
    pdf_link = f"https://openreview.net/{s.content['pdf']['value']}"
    processed_text = process_paper(pdf_link)

    example_output = """
    {"classification_reasoning": "<your reasoning here in 30 words or less>",
    "branch": "<level 1 category>",
    "sub_branch": "<level 2 category>",
    "area": "<level 3 category>",
    "sub_area": "<level 4 category>",
    "problem": "<concrete problem>",
    "further_research": ["<concrete task 1>", "<concrete task 2>","<concrete task 3>"],
    "outstanding_paper_award_probability": <number from 0 to 1>}"""

    with open("../categories.json", "r") as file:
        categories = json.load(file)

    conference_category = s.content["primary_area"]["value"]

    reviews = get_reviews(s)

    prompt = f"""### Existing categories

{categories}

### Input paper

{processed_text}

### Conference category

{conference_category}

### Reviews

{reviews}

### Example output

{example_output}

### Instructions

Classify the input paper into one of the existing categories, where first one is branch and child is sub_branch. Try to use existing categories as much as possible, but if you're sure you can't fit the paper into them - create a new category and add a reasoning for it. Be as short and as general as possible, avoid rare abbreviations, do NOT create "Other" category. Further research should not be abstract and should have direct instructions. Add classification reasoning. Output valid json only."""
    prompt = prompt.replace("\x00", "")
    preamble_template = """

    ## Task & Context
    You are an expert research paper classifier. You read the research paper and classify it into hierarchical classes, which are used on the website to cluster papers under the same topics and problems. Your goal is to reuse existing categories as much as possible. You do not create new categories or change their order unless absolutely necessary. You never return "Other" and always return complete json based on the example.

    ## Style Guide
    You output json only, you don't try to continue the paper.
    """
    response = co.chat(
        model="command-r-plus",
        message=prompt,
        preamble=preamble_template,
        return_prompt=False,
        temperature=0.2,
    )
    return response, pdf_link
