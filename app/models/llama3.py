from app.models.base import BaseModel
from typing import Optional

from huggingface_hub import hf_hub_download
from llama_cpp import Llama


class Llama3(BaseModel):
    def __init__(
            self,
            token: str,
            system_prompt: Optional[str] = None,
            init_kwargs=None,
            call_kwargs=None
    ):
        super().__init__(system_prompt)

        if init_kwargs is None:
            init_kwargs = {}
        if call_kwargs is None:
            call_kwargs = {}
        self.kwargs = call_kwargs

        model_name = "srnm/Meta-Llama-3.1-8B-Instruct-HSE-AI-Hack-tuned-Q8_0-GGUF"
        model_file = "meta-llama-3.1-8b-instruct-hse-ai-hack-tuned-q8_0.gguf"
        model_path = hf_hub_download(model_name, filename=model_file)

        custom_kwargs = {
            "model_path": model_path,
            "n_gpu_layers": -1,
            "n_threads": 10,
            "verbose": False,
        }

        init_kwargs = {
            kwarg: init_kwargs[kwarg] for kwarg in init_kwargs if kwarg not in custom_kwargs
        }

        self.model = Llama(
            **custom_kwargs,
            **init_kwargs,
        )

    def ask(self, user_message: str, clear_history: bool = True) -> Optional[str]:
        if clear_history:
            self.messages = []
            if self.system_prompt:
                self.messages.append({"role": "system", "content": self.system_prompt})

        self.messages.append({"role": "user", "content": user_message})
        self.kwargs["messages"] = self.messages

        output = self.model.create_chat_completion(**self.kwargs)["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": output})

        return output