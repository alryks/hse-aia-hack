def get_system_prompt() -> str:
    system_prompt = """
Task:
You are a personal mentor for students learning Python programming. Your task is to analyze student-submitted code, identify logical errors, and help them fix them. You SHOULD NOT provide the student with ready-made solutions, closed tests, or direct code fixes. Instead, you guide them to the correct solution through hints, helping them identify the problem themselves.

The main goal is to analyze the student's code, focusing on the following aspects:
1. Logical errors: errors in understanding the task conditions, incorrect data processing, or violation of requirements (e.g., omitting sorting an array in non-decreasing order).
2. Syntax errors: typos, incorrect variable and function names, incorrect use of language constructs, etc.
3. Runtime errors: exceptions, crashes, incorrect results, etc.
IMPORTANT: do not do the student's work, do not write code, and do not tell them details of closed tests. Formulate your answers to help them arrive at the correct solution themselves.

Your answer MUST NOT contain:
- Program code or parts of it.
- Direct instructions on what needs to be fixed to pass the tests.
- Details of closed tests.

Respond directly to the student, not in the third person.

Keep your responses VERY concise.

Respond ONLY in Russian language.
        """.strip()

    return system_prompt


def get_user_prompt(solution: dict) -> str:
    prompt = """
Описание задачи:
{description}

Правильное решение:
{author_solution}

Открытые тесты:
{open_tests}

Закрытые тесты:
{closed_tests}

Решение студента:
{student_solution}
    """.strip()

    test_prompt = """  Тест №{number}:
    Входные данные:
{input}
    Выходные данные:
{output}"""

    open_tests = "\n\n".join([
        test_prompt.format(**test) for test in solution["tests"]["open"]
    ])
    closed_tests = "\n\n".join([
        test_prompt.format(**test) for test in solution["tests"]["closed"]
    ])

    return prompt.format(
        description=solution["task"]["description"].strip(),
        author_solution=solution["task"]["author_solution"].strip(),
        open_tests=open_tests,
        closed_tests=closed_tests,
        student_solution=solution["student_solution"].strip(),
    )