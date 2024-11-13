import google.generativeai as genai


def create_schema(level, current_classification):
    base_properties = {
        "field": genai.protos.Schema(
            type=genai.protos.Type.STRING, enum=["Computer Science"]
        ),
        "discipline": genai.protos.Schema(
            type=genai.protos.Type.STRING, enum=["Artificial Intelligence"]
        ),
        "sub_discipline": genai.protos.Schema(
            type=genai.protos.Type.STRING,
            enum=[
                "General",
                "Computer Vision",
                "Natural Language Processing",
                "Reinforcement Learning",
                "Audio",
                "Sequential",
                "Graphs",
            ],
        ),
    }

    additional_properties = {}
    if level == 4:
        additional_properties = {
            "classification_reason_sub_discipline": genai.protos.Schema(
                type=genai.protos.Type.STRING
            ),
            "area": genai.protos.Schema(type=genai.protos.Type.STRING),
            "classification_reason_area": genai.protos.Schema(
                type=genai.protos.Type.STRING
            ),
        }
    elif level == 5:
        additional_properties = {
            "area": genai.protos.Schema(
                type=genai.protos.Type.STRING, enum=[current_classification["area"]]
            ),
            "classification_reason_topic": genai.protos.Schema(
                type=genai.protos.Type.STRING
            ),
            "topic": genai.protos.Schema(type=genai.protos.Type.STRING),
        }
    elif level == 6:
        additional_properties = {
            "area": genai.protos.Schema(
                type=genai.protos.Type.STRING, enum=[current_classification["area"]]
            ),
            "topic": genai.protos.Schema(
                type=genai.protos.Type.STRING, enum=[current_classification["topic"]]
            ),
            "classification_reason_subtopic": genai.protos.Schema(
                type=genai.protos.Type.STRING
            ),
            "subtopic": genai.protos.Schema(type=genai.protos.Type.STRING),
            "problems_addressed": genai.protos.Schema(
                type=genai.protos.Type.ARRAY,
                items=genai.protos.Schema(type=genai.protos.Type.STRING),
            ),
            "follow_up_tasks": genai.protos.Schema(
                type=genai.protos.Type.ARRAY,
                items=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "task": genai.protos.Schema(type=genai.protos.Type.STRING),
                        "difficulty": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            enum=["1", "2", "3", "4", "5"],
                        ),
                    },
                    required=["task", "difficulty"],
                ),
            ),
            "further_research": genai.protos.Schema(type=genai.protos.Type.STRING),
            "outstanding_paper_award_probability": genai.protos.Schema(
                type=genai.protos.Type.NUMBER
            ),
            "startup_based_on_paper": genai.protos.Schema(
                type=genai.protos.Type.STRING
            ),
            "alternative_classifications": genai.protos.Schema(
                type=genai.protos.Type.ARRAY,
                items=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "field": genai.protos.Schema(type=genai.protos.Type.STRING),
                        "discipline": genai.protos.Schema(
                            type=genai.protos.Type.STRING
                        ),
                        "sub_discipline": genai.protos.Schema(
                            type=genai.protos.Type.STRING
                        ),
                        "area": genai.protos.Schema(type=genai.protos.Type.STRING),
                        "topic": genai.protos.Schema(type=genai.protos.Type.STRING),
                        "subtopic": genai.protos.Schema(type=genai.protos.Type.STRING),
                    },
                    required=[
                        "field",
                        "discipline",
                        "sub_discipline",
                        "area",
                        "topic",
                        "subtopic",
                    ],
                ),
            ),
        }

    properties = {**base_properties, **additional_properties}

    required_fields = ["field", "discipline", "sub_discipline"] + list(
        additional_properties.keys()
    )

    return genai.protos.Schema(
        type=genai.protos.Type.OBJECT, properties=properties, required=required_fields
    )
