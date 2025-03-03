import ollama
import os
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.pdf_processing import extract_text_from_pdf
from utils.dataset import Dataset, Example
from sys_msgs.sys_msgs import system_message
from work_order import WorkOrder

# MODEL = "llama3.2:3b"
# MODEL = "qwen2.5:0.5b"
MODEL = "llama3:8b"


def main():
    data_dir = os.path.sep.join([os.getcwd(), "data"])

    pdf_names = os.listdir(data_dir)
    # pdf_names = [
    #     # "New_1.pdf",
    #     # "New_2.pdf",
    #     # "New_3.pdf",
    #     # "NuovoTemplate ODL ESEMPIO 3.pdf",
    # ]

    examples = []

    # for i, pdf_name in enumerate(pdf_names, start=1):
    #     print(f"------------- Word order {i}: {pdf_name} -----------------------")
    #     pdf_path = os.path.sep.join([data_dir, pdf_name])
    #     text = extract_text_from_pdf(pdf_path=pdf_path)
    #     print(text, end="\n\n")

    #     response_stream = ollama.chat(
    #         model=MODEL,
    #         messages=[
    #             {"role": "system", "content": system_message},
    #             {"role": "user", "content": text},
    #         ],
    #         stream=True,
    #         format=WorkOrder.model_json_schema(),
    #         options={"temperature": 0, "num_ctx": 4096},
    #     )

    #     print("Response:")
    #     complete_response = ""
    #     for chunk in response_stream:
    #         message = chunk["message"]["content"]
    #         complete_response += message
    #         print(message, end="", flush=True)

    #         if chunk["done"]:
    #             complete_response = json.loads(complete_response)
    #             examples.append(
    #                 Example(input=text, output=json.dumps(complete_response))
    #             )

    #     print("\n")

    # dataset = Dataset(examples=examples)
    # # dataset.update_system_msg(new_instruction="You are a good assistant!")
    # dataset.save_as_json("./raw_dataset.json")

    dataset = Dataset.from_json("data/dataset_raw.json")
    dataset.split(train_size=0.6, val_size=0.2, test_size=0.2, seed=42)
    dataset.save_as_json("data/dataset_splits.json")
    # dataset.push_to_hub(dataset_hf_path)


if __name__ == "__main__":
    main()
