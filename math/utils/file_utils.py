import json

from utils.template_utils import *
from utils.string_utils import *


def get_temp_path(path):
    return path.parent / f"{path.stem}_temp.jsonl"


def read_data(path):
    if path.is_dir():
        data = []
        for file in path.glob("*.json"):
            with file.open() as f:
                data.append(json.load(f))
        return data

    if path.is_file():
        if path.suffix == ".jsonl":
            with path.open("r") as f:
                data = []
                for line in f:
                    data.append(json.loads(line))
            return data
        else:
            with path.open("r") as f:
                data = json.load(f)
            return data

    raise ValueError(f"Invalid path: {path}")


def write_data(data, path):
    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    with path.open("w") as f:
        if type(data) == str:
            f.write(data)
        else:
            json.dump(data, f)


def raw2prepared(raw_path, dest_path):
    raw_data = read_data(raw_path)

    questions = prepare_question(raw_data)
    questions_metadata = prepare_metadata(raw_path, questions)

    messages = message_template(questions)
    requests = openai_api_template(messages, metadata=questions_metadata)
    jsonl_data = "\n".join(json.dumps(d) for d in requests)
    write_data(jsonl_data, dest_path)
