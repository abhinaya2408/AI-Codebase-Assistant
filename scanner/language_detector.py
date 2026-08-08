from pathlib import Path
from collections import Counter


# ============================================================
# FILE EXTENSION -> LANGUAGE
# ============================================================

LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",

    ".java": "Java",

    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".hpp": "C++",

    ".c": "C",
    ".h": "C/C++",

    ".cs": "C#",

    ".go": "Go",

    ".rs": "Rust",

    ".php": "PHP",

    ".rb": "Ruby",

    ".swift": "Swift",

    ".kt": "Kotlin",
    ".kts": "Kotlin",

    ".dart": "Dart",

    ".scala": "Scala",

    ".r": "R",

    ".sql": "SQL",

    ".html": "HTML",
    ".htm": "HTML",

    ".css": "CSS",
    ".scss": "SCSS",

    ".vue": "Vue",
}


# ============================================================
# DIRECTORIES TO IGNORE
# ============================================================

IGNORED_DIRECTORIES = {
    ".git",
    "__pycache__",
    "node_modules",
    "venv",
    ".venv",
    "env",
    ".env",
    ".idea",
    ".vscode",
    "dist",
    "build",
    "target",
    ".next",
    ".dart_tool",
}


# ============================================================
# DETECT LANGUAGES
# ============================================================

def detect_languages(repo_path: str) -> dict:
    """
    Detect programming languages used in a repository.

    Args:
        repo_path: Path of the repository to analyze.

    Returns:
        Dictionary containing:
            languages
            file_counts
            total_source_files
    """

    repo = Path(repo_path)

    # --------------------------------------------------------
    # Check repository
    # --------------------------------------------------------

    if not repo.exists():
        raise FileNotFoundError(
            f"Repository path does not exist: {repo_path}"
        )

    if not repo.is_dir():
        raise NotADirectoryError(
            f"Repository path is not a directory: {repo_path}"
        )

    # --------------------------------------------------------
    # Count languages
    # --------------------------------------------------------

    language_counts = Counter()

    for file_path in repo.rglob("*"):

        # Ignore directories
        if not file_path.is_file():
            continue

        # Ignore unwanted directories
        if any(
            ignored in file_path.parts
            for ignored in IGNORED_DIRECTORIES
        ):
            continue

        # Get file extension
        extension = file_path.suffix.lower()

        # Find language
        language = LANGUAGE_MAP.get(extension)

        if language:
            language_counts[language] += 1

    # --------------------------------------------------------
    # Prepare result
    # --------------------------------------------------------

    return {
        "languages": list(language_counts.keys()),

        "file_counts": dict(
            language_counts
        ),

        "total_source_files": sum(
            language_counts.values()
        ),
    }