import ollama
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from enum import Enum
from utils.pdf_processing import extract_text_from_pdf
from utils.json import canonilize_json
from utils.dataset import Dataset
from utils.model import Model
from sys_msgs.sys_msgs import system_message
from work_order import WorkOrder

# MODEL = "gemma2:2b"
# MODEL = "llama3.2:3b"
# MODEL = "llama3:8b"
# MODEL = "qwen2.5:0.5b"
MODEL = "qwen2.5:0.5b-instruct"

SEED = 42


class Metric(Enum):
    EMA = "EMA"
    PRECISION = "Precision"
    RECALL = "Recall"
    F1 = "F1 Score"


def evaluate_model(model, dataset: str, metrics: list, verbose: bool = False):
    match_count = 0
    total_count = len(dataset)

    # Perform inference on all inputs
    for example in dataset:
        response = model.chat(
            example.input,
            stream=True,
            print_response=False,
            temperature=0,
            num_ctx=4096,
            response_json_schema=WorkOrder.model_json_schema(),
        )

        # Canonize the predicted and expected JSONs
        output_normalized = canonilize_json(example.output)
        response_normalized = canonilize_json(response)

        if verbose:
            print(f"[INFO] Expected output:\n {output_normalized}", end="\n\n")
            print(f"[INFO] Actual output:\n {response_normalized}", end="\n\n")

        # Calculate the metrics
        if output_normalized == response_normalized:
            match_count += 1
            if verbose:
                print("[INFO] Match!", end="\n\n")
        else:
            if verbose:
                print("[INFO] Missmatch!", end="\n\n")

        if verbose:
            print(f"[INFO] {match_count} matches in {total_count} predictions")

    return match_count / total_count


if __name__ == "__main__":
    model = Model(
        name=MODEL,
        system_message=system_message,
    )

    dataset = Dataset.from_json("data/dataset_raw.json")
    dataset.split(train_size=0.6, val_size=0.2, test_size=0.2, seed=SEED)
    test_split = dataset.splits["test"]

    ema = evaluate_model(model=model, dataset=test_split, metrics=["ema"], verbose=True)
    print(f"Exact match accuracy: {ema}")
