import argparse
import os.path

from datatrove.executor import LocalPipelineExecutor
from datatrove.pipeline.filters import (
    C4QualityFilter,
    FineWebQualityFilter,
    GopherQualityFilter,
    GopherRepetitionFilter,
)
from datatrove.pipeline.readers import JsonlReader
from datatrove.pipeline.writers.jsonl import JsonlWriter
from datatrove.utils.typeshelper import Languages

parser = argparse.ArgumentParser()
parser.add_argument(
    "output_path", type=str, help="Where to save individual tokenization files and the final merged " "files."
)
parser.add_argument("-ts", "--tasks", type=int, help="Number of tasks to run. 1000 by default", default=1000)
parser.add_argument("-rs", "--random_start", type=int, help="Random start time delay in seconds", default=180)
parser.add_argument("-w", "--workers", type=int, help="Random start time delay in seconds", default=-1)

stop_words = ['bir', 'bu', 'da', 'daha', 'de', 'en', 'gibi', 'göre', 'her', 'ile', 'ise', 'için', 'kadar', 'olan', 'olarak', 've', 'çok', "tarafından", "ilgili", "üzere", "bu", "şu", "o", "tüm", "veya"]

args = parser.parse_args()

import nltk
nltk.download('punkt_tab')
  
if __name__ == "__main__":

    OUT_DS_NAME = args.output_path
    
    # we first ran the following pipeline for each dump

    MAIN_OUTPUT_PATH = f"{OUT_DS_NAME}"
    os.makedirs(MAIN_OUTPUT_PATH, exist_ok  = True)
    
    DATA_INPUT_PATH = f"{MAIN_OUTPUT_PATH}/data_input"
    FILTERING_OUTPUT_PATH = f"{MAIN_OUTPUT_PATH}/base_processing"

    main_processing_executor = LocalPipelineExecutor(
        pipeline=[
           JsonlReader(f"{DATA_INPUT_PATH}/output"),
            GopherRepetitionFilter(
                language = Languages.turkish,
                exclusion_writer=JsonlWriter(
                    f"{FILTERING_OUTPUT_PATH}/removed/3_gopher_rep")
            ),
            GopherQualityFilter(
                stop_words=stop_words,
                min_stop_words=4,
                language = Languages.turkish,
                max_non_alpha_words_ratio = 0.75,
                exclusion_writer=JsonlWriter(
                    f"{FILTERING_OUTPUT_PATH}/removed/4_gopher_qual")
            ),
            C4QualityFilter(
                filter_no_terminal_punct=False,
                language = Languages.turkish,
                exclusion_writer=JsonlWriter(
                    f"{FILTERING_OUTPUT_PATH}/removed/5_c4"),
            ),
            FineWebQualityFilter(
                language = Languages.turkish,
                exclusion_writer=JsonlWriter(
                    f"{FILTERING_OUTPUT_PATH}/removed/6_fineweb_qual")
            ),
            JsonlWriter(f"{FILTERING_OUTPUT_PATH}/output"),
        ],
        tasks=args.tasks,
        workers=args.workers,
        logging_dir=f"{MAIN_OUTPUT_PATH}/logs/base_processing",
        # don't hit the bucket all at once with the list requests
        randomize_start_duration=args.random_start
    )
    main_processing_executor.run()
    