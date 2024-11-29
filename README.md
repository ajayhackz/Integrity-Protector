# Integrity-Protector

# Explanation of the Code:

    calculate_file_hash: Computes the MD5 hash of a file.
    collect_baseline: Gathers the hashes of all files in a specified directory and saves them to baseline.txt.
    monitor_files: Continuously checks for changes in the files against the baseline and alerts the user if any changes are detected.
    main: Provides a user interface to either collect a new baseline or start monitoring files.

# Usage:

    Run the script and choose to either collect a new baseline or monitor existing files.
    Ensure the directory you want to monitor is specified correctly.
