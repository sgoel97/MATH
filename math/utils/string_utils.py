from latex2sympy2 import latex2sympy


def extract_answer(answer):
    if "\\boxed" not in answer:
        return "NA"

    after_boxed = answer.split("\\boxed")[-1]
    paren_stack = []
    for i, char in enumerate(after_boxed):
        if char == "{":
            paren_stack.append(char)
        elif char == "}":
            paren_stack.pop()
        if len(paren_stack) == 0:
            break
    return after_boxed[1:i]


def verify_answer(generated_answer, answer):
    final_answer = extract_answer(generated_answer)
    final_ground_truth = extract_answer(answer)
    try:
        return bool(latex2sympy(final_answer).equals(latex2sympy(final_ground_truth)))
    except:
        return bool(final_answer.strip().lower() == final_ground_truth.strip().lower())
