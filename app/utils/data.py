from pathlib import Path
import pandas as pd


def get_solutions(data_dir: str) -> dict:
    data_dir = Path(data_dir)
    tasks = {}

    tasks_table = pd.read_excel(data_dir / "tasks.xlsx")
    for i, row in tasks_table.iterrows():
        tasks[int(row["id"])] = {
            "description": row["description"],
            "author_solution": row["author_solution"],
        }

    tests = {
        task_id: [] for task_id in tasks.keys()
    }
    tests_table = pd.read_excel(data_dir / "tests.xlsx")
    for i, row in tests_table.iterrows():
        tests[int(row["task_id"])].append({
            "number": int(row["number"]),
            "type": row["type"],
            "input": row["input"],
            "output": row["output"],
        })

    solutions = {}
    solutions_table = pd.read_excel(data_dir / "solutions.xlsx")
    for i, row in solutions_table.iterrows():
        solutions[int(row["id"])] = {
            "task": tasks[int(row["task_id"])],
            "tests": {
                "open": list(sorted(filter(lambda x: x["type"] == "open", tests[int(row["task_id"])]), key=lambda x: x["number"])),
                "closed": list(sorted(filter(lambda x: x["type"] == "closed", tests[int(row["task_id"])]), key=lambda x: x["number"])),
            },
            "student_solution": row["student_solution"],
            "author_comment": row["author_comment"],
        }

    return solutions