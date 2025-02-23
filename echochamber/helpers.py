from pathlib import Path


def save_text_to_file(path: Path, content: str, encoding: str=""):
    """
    Saves the given text content to files in the specified directory.
    
    Parameters:
        directory_path (str): The path to the directory where files will be saved.
        files_content (dict): A dictionary where keys are filenames and values are the text to save.
    """
    if not path.exists():
        path.mkdir(parents=True)
        print(f"The directory {str(path)} was created.")

    with path.open('w', encoding=encoding) as file:
        file.write(content)


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