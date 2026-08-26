import logging
from pathlib import Path
import shutil

# Configure logging to output timestamped status and error messages
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define file type categories mapping extension groups to destination folders
FILE_CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".svg", ".bmp", ".webp"},
    "Documents": {".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"},
    "Code": {".py", ".js", ".html", ".css", ".json", ".cpp", ".c", ".java"},
    "Archives": {".zip", ".tar", ".gz", ".7z", ".rar"},
}

def get_category(file_path: Path) -> str:
    """Returns the matching category folder name based on the file extension."""
    ext = file_path.suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"

def organize_folder(target_dir_path: str) -> None:
    """Organizes files in the target folder into category subfolders."""
    target_dir = Path(target_dir_path).resolve()

    # Validate directory existence
    if not target_dir.exists() or not target_dir.is_dir():
        logging.error(f"Provided path is not a valid directory: {target_dir}")
        return

    logging.info(f"Starting organization for: {target_dir}")

    # Process items in the target directory
    for item in target_dir.iterdir():
        # Skip subdirectories to avoid recursive directory moving
        if item.is_dir():
            continue

        category = get_category(item)
        category_dir = target_dir / category

        # Safely create the category folder if it doesn't exist yet
        try:
            category_dir.mkdir(exist_ok=True)
        except PermissionError:
            logging.error(f"Permission denied creating folder: {category_dir}")
            continue

        destination_path = category_dir / item.name

        # Prevent overwriting if a file with the same name exists at destination
        if destination_path.exists():
            logging.warning(
                f"Skipped '{item.name}': File already exists in '{category}'."
            )
            continue

        # Move the file with error handling for locked or in-use files
        try:
            shutil.move(str(item), str(destination_path))
            logging.info(f"Moved: '{item.name}' -> '{category}/'")
        except PermissionError:
            logging.error(
                f"Skipped '{item.name}': File is locked, in use, or access is denied."
            )
        except Exception as e:
            logging.error(f"Failed to move '{item.name}': {e}")

if __name__ == "__main__":
    folder_input = input("Enter the path of the folder to organize: ").strip()
    organize_folder(folder_input)