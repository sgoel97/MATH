def prepare_question(question):
    if type(question) == dict:
        question["solution"] = question["solution"].replace("\\!", "")
        return question
    elif type(question) == list:
        return [prepare_question(q) for q in question]


def message_template(question):
    if type(question) == dict:
        return [
            {
                "role": "system",
                "content": "You are a helpful assistant who solves math problems. Box the final answer to each question using the latex \\boxed tag.",
            },
            {"role": "user", "content": question["problem"]},
        ]
    elif type(question) == list:
        return [message_template(q) for q in question]


def prepare_metadata(questions_path, questions):
    question_index = range(len(questions))
    questions_filenames = list(questions_path.glob("*.json"))

    return [
        {
            "row_id": question_index[i],
            "filename": questions_filenames[i].name.replace(".json", ""),
        }
        for i in range(len(questions))
    ]


def openai_api_template(message, metadata=None):
    if type(message[0]) == dict:
        return {
            "model": "gpt-3.5-turbo",
            "messages": message,
            "metadata": metadata,
        }
    elif type(message) == list:
        if metadata is None:
            return [openai_api_template(m) for m in message]
        return [openai_api_template(m, metadata[i]) for i, m in enumerate(message)]
