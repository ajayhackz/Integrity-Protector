import os
import hashlib
import time

# ANSI escape codes for colors
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


# Function to calculate the hash of a file
def calculate_file_hash(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(2048), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Function to collect baseline hashes and contents
def collect_baseline(directory):
    files_data = {}
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            files_data[filepath] = {
                'hash': calculate_file_hash(filepath),
                'content': open(filepath, 'r', encoding='utf-8', errors='ignore').read()
            }
    with open('baseline.txt', 'w') as baseline_file:
        for path, data in files_data.items():
            baseline_file.write(f"{path}|{data['hash']}|{data['content']}\n")
    print("Baseline collected.")

# Function to monitor files against the baseline
def normalize_content(content):
    """ Normalize content by stripping whitespace and normalizing line endings. """
    return content.strip().replace('\r\n', '\n').replace('\r', '\n')

def monitor_files(directory):
    # Load baseline hashes and contents
    file_data_dict = {}
    with open('baseline.txt', 'r') as baseline_file:
        for line in baseline_file:
            line = line.strip()
            if line:  # Only process non-empty lines
                parts = line.split('|', 2)
                if len(parts) == 3:  # Ensure there are exactly 3 parts
                    path, hash_value, content = parts
                    file_data_dict[path] = {
                        'hash': hash_value,
                        'content': normalize_content(content)  # Normalize baseline content
                    }
                else:
                    print(f"Skipping malformed line in baseline: {line}")

    while True:
        time.sleep(2)  # Check every 2 seconds
        current_files = os.listdir(directory)
        for filepath in current_files:
            full_path = os.path.join(directory, filepath)
            if os.path.isfile(full_path):
                current_hash = calculate_file_hash(full_path)
                current_content = normalize_content(open(full_path, 'r', encoding='utf-8', errors='ignore').read())
                
                if full_path in file_data_dict:
                    if current_hash != file_data_dict[full_path]['hash']:
                        print(f"{RED}{full_path} has been changed!{RESET}")
                        print(f"Previous content:\n{file_data_dict[full_path]['content']}")
                        print(f"Modified content:\n{current_content}")
                    else:
                        # If the hash is the same, we can still check for content changes
                        if current_content != file_data_dict[full_path]['content']:
                            print(f"{RED}{full_path} has been changed in content!{RESET}")
                            print(f"Previous content:\n{file_data_dict[full_path]['content']}")
                            print(f"Modified content:\n{current_content}")
                else:
                    print(f"{GREEN}{full_path} has been created!{RESET}")
        
        # Check for deleted files
        for baseline_file in list(file_data_dict.keys()):
            if not os.path.exists(baseline_file):
                print(f"{baseline_file} has been deleted.")
                del file_data_dict[baseline_file]
                
# Main function to run the script
def main():
    print("What would you like to do?")
    print("A) Collect new Baseline")
    print("B) Begin monitoring files with saved Baseline")
    response = input("Please enter 'A' or 'B': ").strip().upper()

    if response == 'A':
        directory = input("Enter the directory to collect baseline: ")
        print(f"Collecting baseline from {directory}...")
        collect_baseline(directory)
    elif response == 'B':
        directory = input("Enter the directory to monitor: ")
        print(f"Monitoring files in {directory}...")
        monitor_files(directory)
    else:
        print("Invalid option selected.")

if __name__ == "__main__":
    main()
