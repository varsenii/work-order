from pydantic import BaseModel
import json


class Example(BaseModel):
    input: str
    output: str
    instruction: str | None = None


class Dataset(BaseModel):
    examples: list[Example]
    instruction: str | None = None

    def add_example(self, example: Example):
        self.examples.append(example)

    def update_system_msg(self, new_instruction: str):
        self.instruction = new_instruction
        for example in self.examples:
            example.instruction = new_instruction

    def save_as_json(self, path: str):
        with open(path, "w") as f:
            json.dump(self.model_dump()["examples"], f, indent=4)
