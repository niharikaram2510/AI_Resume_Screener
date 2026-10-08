from matching.job_role_matcher import (
    find_best_job_roles,
    get_best_job_role
)


job_role = input(
    "Enter Job Role: "
)


results = find_best_job_roles(
    job_role
)


print("\n==============================================")
print("             JOB ROLE MATCHING")
print("==============================================")


print("\nInput:")
print(job_role)


print("\nTop Matching Roles:")

for i, result in enumerate(
    results,
    start=1
):

    print(
        f"{i}. "
        f"{result['job_role']} "
        f"→ {result['similarity']}%"
    )


best = get_best_job_role(
    job_role
)


print("\n----------------------------------------------")

print(
    "\nBest Matching Role:",
    best["job_role"]
)

print(
    "Similarity:",
    best["similarity"],
    "%"
)


print("\n==============================================")