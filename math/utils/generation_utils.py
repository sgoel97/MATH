import json

from utils.file_utils import read_data, write_data
from utils.string_utils import verify_answer


def count_errors(orig_path):
    output_data = read_data(orig_path)

    error_count = 0
    for output in output_data:
        if "choices" not in output[1]:
            error_count += 1

    return error_count


def get_metrics(orig_path):
    output_data = read_data(orig_path)

    correct = incorrect = 0
    for output in output_data:
        if output[2]["correct"]:
            correct += 1
        else:
            incorrect += 1

    return {
        "correct": correct,
        "incorrect": incorrect,
        "accuracy": correct / (correct + incorrect),
    }


def evaluate(raw_path, dest_path):
    output_data = read_data(dest_path)
    for output in output_data:
        metadata = output[2]
        question = read_data(raw_path / f"{metadata['filename']}.json")
        generated_answer = output[1]["choices"][0]["message"]["content"]

        correct = bool(verify_answer(generated_answer, question["solution"]))
        metadata["correct"] = correct

    output_data_str = "\n".join(list(map(json.dumps, output_data)))
    write_data(output_data_str, dest_path)
