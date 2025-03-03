import ollama
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.pdf_processing import extract_text_from_pdf
from utils.json import canonilize_json
from sys_msgs.sys_msgs import system_message
from work_order import WorkOrder

# MODEL = "gemma2:2b"
# MODEL = "llama3.2:3b"
# MODEL = "llama3:8b"
# MODEL = "qwen2.5:0.5b"
MODEL = "qwen2.5:0.5b-instruct"


def main():
    data_dir = os.path.sep.join([os.getcwd(), "data", "Work orders"])

    # pdf_names = os.listdir(data_dir)
    pdf_names = [
        "New_1.pdf",
        "New_2.pdf",
        "New_3.pdf",
        "NuovoTemplate ODL ESEMPIO 3.pdf",
    ]

    for i, pdf_name in enumerate(pdf_names, start=1):
        print(f"------------- Word order {i}: {pdf_name} -----------------------")
        pdf_path = os.path.sep.join([data_dir, pdf_name])
        text = extract_text_from_pdf(pdf_path=pdf_path)
        print(text, end="\n\n")

        response_stream = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": text},
            ],
            stream=True,
            format=WorkOrder.model_json_schema(),
            options={"temperature": 0, "num_ctx": 4096},
        )

        print("Response:")
        for chunk in response_stream:
            message = chunk["message"]["content"]

            # if message in ["```", "json"]:
            #     continue
            print(message, end="", flush=True)

        print("\n")


if __name__ == "__main__":
    main()
