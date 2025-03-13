import os
import re

def remove_duplicates_with_parens(directory):
    """
    Removes duplicate files in the specified directory based on file name, ignoring extensions
    and parenthetical suffixes. Keeps files with "(USA)" or "(US)" in parentheses.

    Args:
        directory (str): The directory to scan for duplicate files.
    """
    # Dictionary to track files by their base name (excluding parentheses and extensions)
    file_map = {}

    # Regular expression to match and remove parenthetical suffixes
    parens_pattern = re.compile(r" \(.*?\)")

    for root, _, files in os.walk(directory):
        for file in files:
            # Extract the base name without parentheses or extensions
            base_name = os.path.splitext(file)[0]
            sanitized_name = parens_pattern.sub("", base_name)
            file_path = os.path.join(root, file)

            if sanitized_name in file_map:
                existing_file_path = file_map[sanitized_name]
                existing_base_name = os.path.splitext(os.path.basename(existing_file_path))[0]

                # Determine which file to keep
                if "(USA)" in base_name or "(US)" in base_name:
                    # Keep the current file and delete the existing one if it's less preferred
                    if not ("(USA)" in existing_base_name or "(US)" in existing_base_name):
                        print(f"Deleting: {existing_file_path}")
                        os.remove(existing_file_path)
                        file_map[sanitized_name] = file_path
                elif "(USA)" in existing_base_name or "(US)" in existing_base_name:
                    # Keep the existing file and delete the current one
                    print(f"Deleting: {file_path}")
                    os.remove(file_path)
                else:
                    # If neither has "(USA)" or "(US)", keep the first and delete the second
                    print(f"Deleting: {file_path}")
                    os.remove(file_path)
            else:
                # Add the file to the map if it's the first encounter
                file_map[sanitized_name] = file_path

if __name__ == "__main__":
    directory_to_scan = input("Enter the directory path to scan for duplicates: ").strip()
    directory_to_scan = os.path.normpath(directory_to_scan)

    if os.path.isdir(directory_to_scan):
        remove_duplicates_with_parens(directory_to_scan)
        print("Duplicate removal complete.")
    else:
        print(f"The provided path '{directory_to_scan}' is not a valid directory.")
