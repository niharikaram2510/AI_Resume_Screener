from ranking.resume_ranker import rank_resumes


def main():

    print("\n==============================================")
    print("       AI RESUME SCREENING - RANKING")
    print("==============================================\n")

    requested_role = input(
        "Enter job role: "
    ).strip()

    file_paths = input(
        "Enter resume paths separated by commas: "
    ).split(",")

    files = []

    for path in file_paths:

        path = path.strip()

        try:
            files.append(
                open(path, "rb")
            )

        except FileNotFoundError:
            print(
                f"\nFile not found: {path}"
            )

    if not files:
        print("\nNo valid resumes found.")
        return

    results = rank_resumes(
        files,
        requested_role
    )

    print("\n==============================================")
    print("              RANKING RESULTS")
    print("==============================================")

    for result in results:

        print("\n----------------------------------------------")

        print(
            f"Rank: #{result['rank']}"
        )

        print(
            f"Candidate: {result['candidate']}"
        )

        if "error" in result:

            print(
                f"Error: {result['error']}"
            )

            continue

        print(
            f"Matched Role: "
            f"{result['matched_role']}"
        )

        print(
            f"Role Similarity: "
            f"{result['role_similarity']}%"
        )

        print(
            f"Career Stage: "
            f"{result['career_stage']}"
        )

        print(
            f"Skill Match: "
            f"{result['skill_score']}%"
        )

        print(
            f"Experience: "
            f"{result['experience_score']}%"
        )

        print(
            f"Projects: "
            f"{result['project_score']}%"
        )

        print(
            f"Education: "
            f"{result['education_score']}%"
        )

        print(
            f"Certifications: "
            f"{result['certification_score']}%"
        )

        print(
            f"OVERALL SCORE: "
            f"{result['overall_score']}%"
        )

        print("\nMatched Skills:")

        for skill in result[
            "matched_skills"
        ]:
            print(f"  ✓ {skill}")

        print("\nMissing Skills:")

        for skill in result[
            "missing_skills"
        ]:
            print(f"  ✗ {skill}")

    print(
        "\n=============================================="
    )


if __name__ == "__main__":
    main()