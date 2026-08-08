from dependency_detector import detect_dependencies


def main():

    print("\n================================")
    print("  RepoSage Dependency Detector")
    print("================================\n")

    repository_path = input(
        "Enter repository path: "
    ).strip()

    if not repository_path:

        print(
            "Error: Repository path cannot be empty."
        )

        return

    try:

        result = detect_dependencies(
            repository_path
        )

        print(
            "\n===== DEPENDENCY ANALYSIS ====="
        )

        # ----------------------------------------------------
        # Dependency files
        # ----------------------------------------------------

        print(
            "\nDependency Files:"
        )

        if result["dependency_files"]:

            for file in result[
                "dependency_files"
            ]:
                print(f"- {file}")

        else:

            print(
                "- No dependency files found."
            )

        # ----------------------------------------------------
        # Ecosystems
        # ----------------------------------------------------

        print(
            "\nEcosystems:"
        )

        if result["ecosystems"]:

            for ecosystem in result[
                "ecosystems"
            ]:
                print(f"- {ecosystem}")

        else:

            print(
                "- No known ecosystem detected."
            )

        # ----------------------------------------------------
        # Dependencies
        # ----------------------------------------------------

        print(
            "\nDependencies:"
        )

        if result["dependencies"]:

            for dependency in result[
                "dependencies"
            ]:
                print(
                    f"- {dependency}"
                )

        else:

            print(
                "- No dependencies extracted."
            )

        print(
            "\nDependency detection "
            "completed successfully."
        )

    except Exception as e:

        print(
            f"\nError: {e}"
        )


if __name__ == "__main__":
    main()