import os
import csv
import time
import ollama
from tqdm import tqdm

def process_csv(csv_file_path, model_name):
    """Processes a single CSV file and returns data for analysis."""
    category = os.path.splitext(os.path.basename(csv_file_path))[0]
    data_rows = []

    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # Skip header if one exists
            
            for row in tqdm(reader, desc=f"Processing {category}", unit=" rows"):
                if len(row) != 6:
                    print(f"Skipping row due to incorrect format: {row}")
                    continue
                
                question, *options, expected_answer = row
                expected_answer = expected_answer.strip().upper()  # Standardize expected answer

                # Create the full prompt for the LLM
                prompt = f"Question: {question}\nOptions:\nA. {options[0]}\nB. {options[1]}\nC. {options[2]}\nD. {options[3]}\nAnswer (choose A, B, C, or D): "

                start_time = time.time()
                try:
                    response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': prompt}])
                    llm_answer = response['message']['content'].strip().upper()  # Standardize LLM answer
                except Exception as e:
                    print(f"Error communicating with Ollama: {e}")
                    llm_answer = "ERROR"
                    computation_time = -1
                    correct = -1
                    data_rows.append([model_name, category, question, expected_answer, llm_answer, computation_time, correct])
                    continue
                
                end_time = time.time()
                computation_time = end_time - start_time
                
                # Determine if the LLM's answer is correct
                llm_answer_letter = llm_answer if llm_answer in {"A", "B", "C", "D"} else "ERROR"
                correct = int(llm_answer_letter == expected_answer)

                data_rows.append([model_name, category, question, expected_answer, llm_answer, computation_time, correct])

    except Exception as e:
        print(f"Error processing file {csv_file_path}: {e}")
    
    return data_rows


def main():
    """Main function to process CSV files and write results."""
    csv_folder = "./data"  # Replace with your actual folder path
    model_name = "gemma:2b"  # Replace with your ollama model name
    output_csv_file = "llm_eval_results.csv"
    header = ["llm_model", "category", "question_asked", "expected_answer", "received_answer", "computation_time", "correct"]

    all_results = []

    # Get all CSV files
    for filename in os.listdir(csv_folder):
        if filename.endswith(".csv"):
            csv_file_path = os.path.join(csv_folder, filename)
            results = process_csv(csv_file_path, model_name)
            all_results.extend(results)

    # Write to CSV
    with open(output_csv_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(all_results)

    print(f"Results written to {output_csv_file}")

if __name__ == "__main__":
    main()