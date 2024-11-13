#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup

url = "https://paperswithcode.com/methods"  # Replace this with the URL of the website you want to parse


def parse(url, category="category"):
    # Fetch the content of the website
    response = requests.get(url)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all the 'a' tags with the specified attribute values
        method_tags = soup.find_all(
            "a",
            href=True,
            attrs={"href": lambda x: x.startswith(f"/methods/{category}/")},
        )

        # Extract and print the method names
        methods = [
            tag.text
            for tag in method_tags
            if tag.attrs.get("href", "").startswith(f"/methods/{category}/")
            and not tag.text.startswith(" See all")
        ]
        # print(methods)
        return methods
    else:
        print(
            f"Failed to fetch the website content. Status code: {response.status_code}"
        )


areas = [
    "General",
    "Computer Vision",
    "Natural Language Processing",
    "Reinforcement Learning",
    "Audio",
    "Sequential",
    "Graphs",
]

base_url = "https://paperswithcode.com/methods/area/"


def area_to_url(area):
    area_slug = area.lower().replace(" ", "-")
    return f"{base_url}{area_slug}"


res = {}
for area in areas:
    res[area] = parse(area_to_url(area))
data = res
for k, v in data.items():
    v.append("Other")

import json

# Save the dictionary to a JSON file
with open("categories.json", "w") as file:
    json.dump(data, file)

# Load the JSON file back into a Python dictionary
with open("categories.json", "r") as file:
    loaded_data = json.load(file)
