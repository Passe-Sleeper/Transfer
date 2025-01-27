import os
import csv
import subprocess
from tqdm import tqdm


def run_evaluation(model_name):
    """Runs the evaluation script for a specific model and returns the output file name."""
    output_csv_file = f"llm_eval_results_{model_name.replace('/', '_')}.csv"
    try:
        subprocess.run(
            [
                "python",
                "evaluate_llm.py",
                "--model_name",
                model_name,
                "--output_csv_file",
                output_csv_file
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return output_csv_file
    except subprocess.CalledProcessError as e:
        print(f"Error running evaluation for model {model_name}:\n{e.stderr}")
        return None


def combine_results(csv_files, final_output_file):
    """Combines results from multiple CSV files into a single CSV."""
    all_rows = []
    header = None

    for file in csv_files:
        if file is None:
            continue  # Skip if an error occurred during evaluation
        try:
            with open(file, "r", encoding="utf-8") as infile:
                reader = csv.reader(infile)
                file_header = next(reader)
                if header is None:
                    header = file_header
                    all_rows.append(header)
                elif header != file_header:
                    print(f"Header mismatch in file {file}")
                    continue
                all_rows.extend(row for row in reader)
        except Exception as e:
            print(f"Error reading file {file}: {e}")

    try:
        with open(final_output_file, "w", encoding="utf-8", newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(all_rows)
    except Exception as e:
        print(f"Error writing combined results to {final_output_file}: {e}")