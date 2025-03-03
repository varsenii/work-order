from pydantic import BaseModel
import json
from enum import Enum
from sklearn.model_selection import train_test_split


class Split(Enum):
    TRAIN = "train"
    VALIDATION = "val"
    TEST = "test"


class Example(BaseModel):
    input: str
    output: str
    instruction: str | None = None

    @classmethod
    def from_json(cls, data):
        try:
            return cls.model_validate_json(data)
        except Exception as e:
            print(e)

    @classmethod
    def from_dictionary(cls, example_dict):
        return cls(
            instruction=example_dict["instruction"],
            input=example_dict["input"],
            output=example_dict["output"],
        )


class Dataset(BaseModel):
    examples: list[Example] | None = None
    instruction: str | None = None
    splits: dict | None = None

    @classmethod
    def from_json(cls, path):
        with open(path, "r") as f:
            dataset_json = json.load(f)

        examples = [Example.from_dictionary(example) for example in dataset_json]
        return cls(examples=examples)

    def add_example(self, example: Example):
        self.examples.append(example)

    def update_system_msg(self, new_instruction: str):
        self.instruction = new_instruction
        for example in self.examples:
            example.instruction = new_instruction

    def save_as_json(self, path: str):
        with open(path, "w") as f:
            json.dump(self.model_dump(exclude_none=True), f, indent=4)

    def split(
        self,
        train_size: float = (0.8,),
        val_size: float = (0.2,),
        test_size: float | None = (None,),
        seed: int | None = (None,),
    ):
        self.splits = {}

        if val_size:
            examples_train, examples_val = train_test_split(
                self.examples, test_size=val_size, shuffle=True, random_state=seed
            )
            self.splits[Split.VALIDATION.value] = examples_val

        if test_size:
            # Recalculate test_size based on the remaining fraction.
            computed_test_size = 1 - train_size - val_size
            examples_train, examples_test = train_test_split(
                examples_train,
                test_size=computed_test_size,
                shuffle=True,
                random_state=seed,
            )
            self.splits[Split.TEST.value] = examples_test

        self.splits[Split.TRAIN.value] = examples_train
        self.examples = None
