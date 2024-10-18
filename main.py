import os

import pandas as pd
from dotenv import load_dotenv

from app.utils.prompts import get_system_prompt, get_user_prompt
from app.models.llama3 import Llama3
from app.utils.submit import generate_submit

from app.utils.data import get_solutions

if __name__ == "__main__":
    load_dotenv()
    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

    system_prompt = get_system_prompt()

    llama3 = Llama3(HUGGINGFACE_TOKEN,
                    system_prompt,
                    {
                        "n_ctx": 4096
                    },
                    {
                        "temperature": 0,
                        "top_p": 0.9,
                        "top_k": 50,
                        "max_tokens": 0
                    })

    solutions = get_solutions("data/raw/test")


    def predict(row: pd.Series) -> str:
        solution = solutions[int(row["id"])]
        prompt = get_user_prompt(solution)

        return llama3.ask(prompt)


    generate_submit(
        test_solutions_path="data/raw/test/solutions.xlsx",
        predict_func=predict,
        save_path="data/processed/submission.csv",
        use_tqdm=True,
    )
