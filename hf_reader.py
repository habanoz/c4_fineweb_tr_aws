import argparse

from datatrove.executor import LocalPipelineExecutor
from datatrove.pipeline.readers import HuggingFaceDatasetReader
from datatrove.pipeline.writers.jsonl import JsonlWriter

parser = argparse.ArgumentParser()
parser.add_argument("dataset", type=str, help="huggingface dataset name. Example: stas/openwebtext-10k")
parser.add_argument(
    "output_path", type=str, help="Where to save individual tokenization files and the final merged " "files."
)

parser.add_argument("-sb", "--subset", type=str, help="dataset subset.")
parser.add_argument("-s", "--split", type=str, help="dataset split. `train` by default", default="train")
parser.add_argument("-lm", "--limit", type=int, help="Limit number of rows to process", default=0)
parser.add_argument(
    "-tk",
    "--text_key",
    type=str,
    help="Column that actually contains the text to be " "tokenized. `text` by default.",
    default="text",
)

parser.add_argument("-ts", "--tasks", type=int, help="Number of tasks to run. 1000 by default", default=1000)
parser.add_argument("-rs", "--random_start", type=int, help="Random start time delay in seconds", default=180)

args = parser.parse_args()

if __name__ == "__main__":

    """
        we first ran the following pipeline for each dump
    """
    OUT_DS_NAME = args.output_path
    
    # we first ran the following pipeline for each dump

    MAIN_OUTPUT_PATH = f"{OUT_DS_NAME}"
    
    DATA_INPUT_PATH = f"{MAIN_OUTPUT_PATH}/data_input"
    FILTERING_OUTPUT_PATH = f"{MAIN_OUTPUT_PATH}/base_processing"

    hf_to_json_executor = LocalPipelineExecutor(
        pipeline=[
            HuggingFaceDatasetReader(
                dataset=args.dataset,  # dataset name
                dataset_options={
                    "name":args.subset,
                    "split": args.split  # any other options that should be passed to load_dataset
                },
                streaming=True,
                limit = args.limit,
                text_key=args.text_key,  # the column that actually contains the text to be tokenized
            ),
            JsonlWriter(f"{DATA_INPUT_PATH}/output/{OUT_DS_NAME}"),
        ],
        tasks=args.tasks,
        logging_dir=f"{MAIN_OUTPUT_PATH}/logs/data_input/{OUT_DS_NAME}",
        # don't hit the bucket all at once with the list requests
        randomize_start_duration=args.random_start
    )
    hf_to_json_executor.run()

    