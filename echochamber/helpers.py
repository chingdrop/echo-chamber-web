from pathlib import Path


def delete_files_in_directory(path: Path):
    """
    Deletes all files in the specified directory.
    
    Parameters:
        directory_path (str): The path to the directory whose files are to be deleted.
    """
    if not path.exists() or not path.is_dir():
        print(f"The directory {str(path)} does not exist or is not a directory.")
        return
    
    for file in path.glob('*'):
        if file.is_file():
            file.unlink()
            print(f"Deleted: {file}")