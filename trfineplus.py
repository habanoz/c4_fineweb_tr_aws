import argparse
import tempfile
import dataclasses
from datatrove.executor import LocalPipelineExecutor
from datatrove.pipeline.readers import HuggingFaceDatasetReader
from datatrove.pipeline.writers import HuggingFaceDatasetWriter,JsonlWriter
from trfineplus_filter import TrFinePlusFilter
from trfineplus_formatter import TrFinePlusFormatter

parser = argparse.ArgumentParser()
parser.add_argument("dataset", type=str, help="huggingface dataset name. Example: stas/openwebtext-10k")
parser.add_argument("new_dataset", type=str, help="Target huggingface dataset name. Example: stas/openwebtext-10k")
parser.add_argument("output_path", type=str, help="Output directory")

parser.add_argument("-sb", "--subset", type=str, help="dataset subset.", default=None)
parser.add_argument("-s", "--split", type=str, help="dataset split. `train` by default", default="train")
parser.add_argument("-lm", "--limit", type=int, help="Limit number of rows to process", default=-1)
parser.add_argument(
    "-tk",
    "--text_key",
    type=str,
    help="Column that actually contains the text to be " "tokenized. `text` by default.",
    default="text",
)

parser.add_argument("-ts", "--tasks", type=int, help="Number of tasks to run. 1000 by default", default=1000)
parser.add_argument("-rs", "--random_start", type=int, help="Random start time delay in seconds", default=180)
parser.add_argument("-w", "--workers", type=int, help="Random start time delay in seconds", default=-1)
args = parser.parse_args()

from datatrove.pipeline.filters.lambda_filter import LambdaFilter
    
def _adapter(self, document) -> dict:
    data = {key: val for key, val in dataclasses.asdict(document).items() if val}
    if "metadata" in data:
        del data["metadata"]
    return data
    
if __name__ == "__main__":

    OUT_DS_NAME = args.output_path
    assert args.new_dataset!=args.dataset
    
    MAIN_OUTPUT_PATH = f"{OUT_DS_NAME}"
    FILTERING_OUTPUT_PATH = f"{MAIN_OUTPUT_PATH}/fineplus_processing"
    TEMP_PATH = f"{MAIN_OUTPUT_PATH}/temp"

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
            TrFinePlusFilter(JsonlWriter(f"{FILTERING_OUTPUT_PATH}/removed/fineplus")),
            TrFinePlusFormatter(),
            HuggingFaceDatasetWriter(
                dataset=args.new_dataset, 
                compression="gzip",
                local_working_dir=TEMP_PATH,
                cleanup=True,
                adapter=_adapter
            )
        ],
        tasks=args.tasks,
        #local_rank_offset=i*n_cpus,
        #local_tasks=n_cpus,
        workers=args.workers,
        logging_dir=f"{MAIN_OUTPUT_PATH}/logs/fineplus_processing",
        # don't hit the bucket all at once with the list requests
        randomize_start_duration=args.random_start
    )
    hf_to_json_executor.run()

    