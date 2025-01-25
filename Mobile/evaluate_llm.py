import csv
import subprocess
import time
import os

def run_llm(question, options):
    """Runs the LLM and returns the answer and computation time."""
    try:
        start_time = time.time()
        # Construct the prompt.  Adjust as needed for your LLM and prompt engineering.
        prompt = f"""Question: {question}\nOptions: {options}\nAnswer:"""

        #  Execute the ollama command.  Replace with your actual ollama command.
        #  This example assumes you have a model named "my-awesome-model"  and are using the default parameters.  Adjust the command to fit your setup.
        process = subprocess.run(
            ["ollama", "run", "my-awesome-model", "--input", prompt],
            capture_output=True, text=True, check=True
        )
        answer = process.stdout.strip()  #Remove leading/trailing whitespace
        # answer = "NULL" #added for testing purposes
        end_time = time.time()
        computation_time = end_time - start_time
        return answer, computation_time
    except subprocess.CalledProcessError as e:
        print(f"Error running ollama: {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None


def process_csv_files(input_dir, output_file, llm_model):
    """Processes all CSV files in the input directory."""

    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['llm_model', 'category', 'question_asked', 'expected_answer', 'recieved_answer', 'computation_time', 'correct']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for filename in os.listdir(input_dir):
            if filename.endswith(".csv"):
                filepath = os.path.join(input_dir, filename)
                category = os.path.splitext(filename)[0]  # Extract filename without .csv
                try:
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        reader = csv.DictReader(infile)
                        for row in reader:
                            question = row['question']
                            options = [row['option 1'], row['option 2'], row['option 3'], row['option 4']]
                            expected_answer = row['answer']

                            answer, computation_time = run_llm(question, options)

                            correct = 1 if answer.lower() == expected_answer.lower() else 0
                            if answer is None:
                                correct = -1
                                computation_time = 0 # Or another representation for error


                            writer.writerow({
                                'llm_model': llm_model,
                                'category': category,
                                'question_asked': question,
                                'expected_answer': expected_answer,
                                'recieved_answer': answer if answer else "Error",
                                'computation_time': computation_time,
                                'correct': correct
                            })

                except Exception as e:
                    print(f"Error processing file {filename}: {e}")



# Configuration
input_directory = "data"  # Replace with your input directory
output_csv_file = "output.csv"
llm_model_name = "gemma:2b"  # Replace with your LLM model name

#Run the processing
process_csv_files(input_directory, output_csv_file, llm_model_name)