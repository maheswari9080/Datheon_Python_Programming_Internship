"""File categories and configurable extension mapping for Task 3 File Organizer."""

from typing import Dict, List, Optional

# Default category mappings
DEFAULT_CATEGORY_EXTENSIONS: Dict[str, List[str]] = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".bmp"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".webm"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp", ".json", ".xml"],
    "Spreadsheets": [".csv", ".xls", ".xlsx", ".ods"],
    "Presentations": [".ppt", ".pptx", ".odp"],
}

FALLBACK_CATEGORY: str = "Other"


class CategoryMapper:
    """Resolves target folder categories based on file extensions."""

    def __init__(self, custom_mapping: Optional[Dict[str, List[str]]] = None) -> None:
        self.category_map = custom_mapping if custom_mapping is not None else DEFAULT_CATEGORY_EXTENSIONS
        # Invert for fast O(1) extension lookup: extension -> category name
        self.ext_to_category: Dict[str, str] = {}
        for category, extensions in self.category_map.items():
            for ext in extensions:
                self.ext_to_category[ext.lower().strip()] = category

    def get_category(self, filename: str) -> str:
        """Determine the category for a given filename based on its extension."""
        parts = filename.rsplit(".", 1)
        if len(parts) < 2 or not parts[1]:
            return FALLBACK_CATEGORY
        ext = f".{parts[1].lower()}"
        return self.ext_to_category.get(ext, FALLBACK_CATEGORY)

    @property
    def all_category_names(self) -> List[str]:
        """Return list of all recognized category directory names."""
        names = list(self.category_map.keys())
        if FALLBACK_CATEGORY not in names:
            names.append(FALLBACK_CATEGORY)
        return names
