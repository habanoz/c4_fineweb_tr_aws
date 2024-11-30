import argparse
import tempfile
from datatrove.executor import LocalPipelineExecutor
from datatrove.pipeline.writers import HuggingFaceDatasetWriter
from datatrove.pipeline.readers import JsonlReader

parser = argparse.ArgumentParser()
parser.add_argument("input_path", type=str, help="Path of the input files")
parser.add_argument("output_path", type=str, help="Path of the output files")
parser.add_argument("dataset", type=str, help="Name of the new dataset: org/new_ds_name")

parser.add_argument("-ts", "--tasks", type=int, help="Number of tasks to run. 1000 by default", default=1000)
parser.add_argument("-w", "--workers", type=int, help="Number of tasks to run. 1000 by default", default=1000)
parser.add_argument("-rs", "--random_start", type=int, help="Random start time delay in seconds", default=180)
args = parser.parse_args()

if __name__ == "__main__":
    hf_to_json_executor = LocalPipelineExecutor(
        pipeline=[
            JsonlReader(args.input_path),
            HuggingFaceDatasetWriter(
                dataset=args.dataset, 
                local_working_dir=f"{args.output_path}/temp",
                cleanup=True
            ),
            
        ],
        tasks=args.tasks,
        workers=args.workers,
        logging_dir=f"{args.output_path}/logs",
        # don't hit the bucket all at once with the list requests
        randomize_start_duration=args.random_start
    )
    hf_to_json_executor.run()

    