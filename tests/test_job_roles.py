from preprocessing.data_loader import (
    get_job_roles,
    get_required_skills
)


print("\n==============================")
print("AVAILABLE JOB ROLES")
print("==============================")

roles = get_job_roles()

print("Total Job Roles:", len(roles))

for role in roles:
    print("-", role)


job_role = "Machine Learning Engineer"

print("\n==============================")
print(f"SKILLS FOR: {job_role}")
print("==============================")

skills = get_required_skills(job_role)

for skill in skills:
    print("•", skill)

print("\nTotal Required Skills:", len(skills)) 