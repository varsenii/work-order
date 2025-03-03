import ollama
from pydantic import BaseModel


class Model(BaseModel):
    name: str
    system_message: str

    def chat(
        self,
        prompt: str,
        stream: bool = True,
        print_response: bool = False,
        temperature: float = 0.7,
        num_ctx: int = 4096,
        response_json_schema: str | None = None,
    ):
        response_stream = ollama.chat(
            model=self.name,
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": prompt},
            ],
            stream=stream,
            format=response_json_schema,
            options={"temperature": temperature, "num_ctx": num_ctx},
        )

        if print_response:
            print("Response:")

        complete_response = ""
        for chunk in response_stream:
            message = chunk["message"]["content"]
            complete_response += message

            if print_response:
                print(message, end="", flush=True)

        if print_response:
            print("\n")

        return complete_response
