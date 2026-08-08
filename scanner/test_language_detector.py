from language_detector import detect_languages


def main():

    print("\n================================")
    print("   RepoSage Language Detector")
    print("================================\n")

    repository_path = input(
        "Enter repository path: "
    ).strip()

    if not repository_path:
        print("Error: Repository path cannot be empty.")
        return

    try:

        result = detect_languages(
            repository_path
        )

        print(
            "\n===== LANGUAGE ANALYSIS ====="
        )

        # ----------------------------------------------------
        # Languages
        # ----------------------------------------------------

        print("\nLanguages:")

        if result["languages"]:

            for language in result["languages"]:
                print(f"- {language}")

        else:

            print("- No supported programming languages found.")

        # ----------------------------------------------------
        # File counts
        # ----------------------------------------------------

        print("\nFile Counts:")

        if result["file_counts"]:

            for language, count in sorted(
                result["file_counts"].items(),
                key=lambda item: item[1],
                reverse=True
            ):
                print(
                    f"- {language}: {count}"
                )

        else:

            print("- No source files found.")

        # ----------------------------------------------------
        # Total
        # ----------------------------------------------------

        print(
            "\nTotal Source Files: "
            f"{result['total_source_files']}"
        )

        print(
            "\nLanguage detection completed successfully."
        )

    except Exception as e:

        print(
            f"\nError: {e}"
        )


if __name__ == "__main__":
    main()