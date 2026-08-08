from pathlib import Path
import json
import re


# ============================================================
# DEPENDENCY FILES
# ============================================================

DEPENDENCY_FILES = {
    "requirements.txt": "Python",
    "requirements-dev.txt": "Python",
    "pyproject.toml": "Python",
    "Pipfile": "Python",

    "package.json": "JavaScript/TypeScript",

    "pom.xml": "Java",
    "build.gradle": "Java",
    "build.gradle.kts": "Kotlin/Gradle",

    "go.mod": "Go",

    "Cargo.toml": "Rust",

    "pubspec.yaml": "Dart/Flutter",
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
    ".idea",
    ".vscode",
    "dist",
    "build",
    "target",
    ".dart_tool",
}


# ============================================================
# FIND DEPENDENCY FILES
# ============================================================

def find_dependency_files(repo_path: str) -> list:
    """
    Find dependency files inside any repository.

    Args:
        repo_path: Path of repository.

    Returns:
        List of dependency file paths.
    """

    repo = Path(repo_path)

    if not repo.exists():
        raise FileNotFoundError(
            f"Repository path does not exist: {repo_path}"
        )

    if not repo.is_dir():
        raise NotADirectoryError(
            f"Repository path is not a directory: {repo_path}"
        )

    found_files = []

    for file_name in DEPENDENCY_FILES:

        matches = repo.rglob(file_name)

        for file_path in matches:

            if not file_path.is_file():
                continue

            # Ignore unwanted directories
            if any(
                ignored in file_path.parts
                for ignored in IGNORED_DIRECTORIES
            ):
                continue

            found_files.append(file_path)

    return found_files


# ============================================================
# PARSE requirements.txt
# ============================================================

def parse_requirements_file(
    file_path: Path
) -> list:
    """
    Extract dependencies from requirements.txt.
    """

    dependencies = []

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                line = line.strip()

                # Ignore empty lines
                if not line:
                    continue

                # Ignore comments
                if line.startswith("#"):
                    continue

                # Ignore option lines
                if line.startswith("-"):
                    continue

                # Remove inline comments
                line = line.split("#")[0].strip()

                # Remove version information
                dependency = re.split(
                    r"[<>=!~]",
                    line
                )[0].strip()

                if dependency:
                    dependencies.append(
                        dependency
                    )

    except Exception as e:

        print(
            f"Warning: Could not read "
            f"{file_path}: {e}"
        )

    return dependencies


# ============================================================
# PARSE package.json
# ============================================================

def parse_package_json(
    file_path: Path
) -> list:
    """
    Extract dependencies from package.json.
    """

    dependencies = []

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        dependencies.extend(
            data.get(
                "dependencies",
                {}
            ).keys()
        )

        dependencies.extend(
            data.get(
                "devDependencies",
                {}
            ).keys()
        )

        dependencies.extend(
            data.get(
                "peerDependencies",
                {}
            ).keys()
        )

    except Exception as e:

        print(
            f"Warning: Could not read "
            f"{file_path}: {e}"
        )

    return list(dependencies)


# ============================================================
# PARSE PYPROJECT.TOML
# ============================================================

def parse_pyproject_file(
    file_path: Path
) -> list:
    """
    Extract basic dependencies from pyproject.toml.

    This parser intentionally uses simple text parsing
    so we don't need an additional TOML dependency yet.
    """

    dependencies = []

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        # Find dependency arrays such as:
        #
        # dependencies = [
        #     "fastapi",
        #     "uvicorn"
        # ]

        matches = re.findall(
            r'["\']([^"\']+)["\']',
            content
        )

        for match in matches:

            # Avoid treating random TOML values
            # as dependencies
            if (
                match
                and not match.startswith("python")
            ):
                dependencies.append(match)

    except Exception as e:

        print(
            f"Warning: Could not read "
            f"{file_path}: {e}"
        )

    return dependencies


# ============================================================
# SELECT PARSER
# ============================================================

def parse_dependency_file(
    file_path: Path
) -> list:
    """
    Select appropriate parser according
    to dependency file type.
    """

    file_name = file_path.name.lower()

    if file_name in {
        "requirements.txt",
        "requirements-dev.txt",
    }:
        return parse_requirements_file(
            file_path
        )

    if file_name == "package.json":
        return parse_package_json(
            file_path
        )

    if file_name == "pyproject.toml":
        return parse_pyproject_file(
            file_path
        )

    # More parsers will be added later.
    return []


# ============================================================
# MAIN DEPENDENCY DETECTOR
# ============================================================

def detect_dependencies(
    repo_path: str
) -> dict:
    """
    Detect dependencies for ANY repository.

    Returns:

    {
        "dependency_files": [],
        "dependencies": [],
        "ecosystems": []
    }
    """

    dependency_files = (
        find_dependency_files(
            repo_path
        )
    )

    dependencies = []

    ecosystems = set()

    # --------------------------------------------------------
    # Process every dependency file
    # --------------------------------------------------------

    for file_path in dependency_files:

        ecosystem = DEPENDENCY_FILES.get(
            file_path.name
        )

        if ecosystem:
            ecosystems.add(
                ecosystem
            )

        parsed_dependencies = (
            parse_dependency_file(
                file_path
            )
        )

        dependencies.extend(
            parsed_dependencies
        )

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    unique_dependencies = list(
        dict.fromkeys(
            dependencies
        )
    )

    return {

        "dependency_files": [
            str(file)
            for file in dependency_files
        ],

        "dependencies": (
            unique_dependencies
        ),

        "ecosystems": sorted(
            ecosystems
        ),
    }