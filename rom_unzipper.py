import os
import sys
import zipfile
import py7zr

def extract_zip_flat(archive_path, target_dir):
    """
    Extracts files from a ZIP archive into target_dir, flattening any subdirectory structure.
    """
    with zipfile.ZipFile(archive_path, 'r') as archive:
        for member in archive.infolist():
            # Skip directories
            if member.is_dir():
                continue
            # Get only the file name, discarding any subdirectory path
            file_name = os.path.basename(member.filename)
            if not file_name:
                continue
            target_file = os.path.join(target_dir, file_name)
            with archive.open(member) as source, open(target_file, 'wb') as target:
                target.write(source.read())

def extract_7z_flat(archive_path, target_dir):
    """
    Extracts files from a 7z archive into target_dir, flattening any subdirectory structure.
    """
    with py7zr.SevenZipFile(archive_path, mode='r') as archive:
        extracted_files = archive.readall()  # Returns a dict mapping file names to file-like objects
        for file_path, file_obj in extracted_files.items():
            # Skip directories
            if file_path.endswith('/') or not file_path:
                continue
            file_name = os.path.basename(file_path)
            if not file_name:
                continue
            target_file = os.path.join(target_dir, file_name)
            with open(target_file, 'wb') as target:
                target.write(file_obj.read())

def process_directory(directory):
    """
    Scans the given directory for .zip and .7z files and extracts them in a flattened structure.
    """
    for entry in os.listdir(directory):
        if entry.lower().endswith('.zip') or entry.lower().endswith('.7z'):
            archive_path = os.path.join(directory, entry)
            print(f"Processing: {archive_path}")
            try:
                if entry.lower().endswith('.zip'):
                    extract_zip_flat(archive_path, directory)
                elif entry.lower().endswith('.7z'):
                    extract_7z_flat(archive_path, directory)
                print(f"Finished extracting: {entry}")
            except Exception as e:
                print(f"Error extracting {entry}: {e}")

if __name__ == "__main__":
    target_directory = "K:\emu\ROMS\GameCube"
    
    if not os.path.isdir(target_directory):
        print(f"Error: {target_directory} is not a valid directory.")
        sys.exit(1)
    
    process_directory(target_directory)
