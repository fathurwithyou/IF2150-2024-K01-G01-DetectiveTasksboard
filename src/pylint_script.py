import os
import subprocess

def run_pylint_on_all_files(root_dir, output_file):
    python_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".py"):
                python_files.append(os.path.join(dirpath, filename))

    if not python_files:
        print("No Python files found in the directory.")
        return

    print(f"Found {len(python_files)} Python files. Running pylint...\n")
    
    with open(output_file, "w") as log_file:
        for file in python_files:
            print(f"Linting {file}...")
            log_file.write(f"Linting {file}...\n")
            try:
                result = subprocess.run(
                    ["pylint", "--disable=line-too-long,trailing-whitespace,too-many-lines", file],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                log_file.write(result.stdout)
                log_file.write(result.stderr)
            except subprocess.CalledProcessError as e:
                log_file.write(f"Pylint failed for {file} with error code {e.returncode}\n")
            log_file.write("-" * 80 + "\n")
    
    print(f"Results written to {output_file}")

if __name__ == "__main__":
    folder_to_lint = os.getcwd()
    output_log = "pylint_results.txt"
    print(f"Using current working directory: {folder_to_lint}")
    run_pylint_on_all_files(folder_to_lint, output_log)
