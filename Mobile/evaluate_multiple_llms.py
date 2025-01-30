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
                
                #get header
                if header is None:
                  header = next(reader)
                else:
                  next(reader) #skip header

                for row in reader:
                  all_rows.append(row)
        except Exception as e:
             print(f"Error reading file {file}: {e}")
             
    
    with open(final_output_file, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header) #get header
        writer.writerows(all_rows)


def main():
    """Main function to run evaluations, combine results and run the progress bar"""
    # llm_models = ["gemma:2b", "gemma2:2b", "llama3.2:1b", "llama3.2:3b"]  # Models to evaluate
    llm_models = ["gemma:2b", "llama3.2:1b"]  # Models to evaluate

    all_output_files = []

    # Run Evaluations for all LLMs
    for model in tqdm(llm_models, desc="Evaluating Models"):
      output_file = run_evaluation(model)
      all_output_files.append(output_file)

    # Combine the individual csv files into one master file
    final_output_file = "combined_llm_results.csv"
    combine_results(all_output_files, final_output_file)

    print(f"Combined results written to {final_output_file}")

    # Delete the outputed model specific files
    # for file in all_output_files:
    #   if file is not None:
    #     os.remove(file)

    # print("NOTE: Individual model files removed")
    print("NOTE: Individual model files not removed")
if __name__ == "__main__":
    main()