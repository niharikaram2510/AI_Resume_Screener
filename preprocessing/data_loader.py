import pandas as pd


JOB_ROLES_FILE = "data/job_roles.csv"


def load_job_roles():
    """Load the job-role skill dataset."""

    return pd.read_csv(JOB_ROLES_FILE)


def get_job_roles():
    """Return all available job roles."""

    df = load_job_roles()

    return sorted(df["job_role"].unique())


def get_required_skills(job_role):
    """Return required skills for a selected job role."""

    df = load_job_roles()

    role_data = df[
        df["job_role"].str.lower() == job_role.lower()
    ]

    return role_data["skill"].drop_duplicates().tolist()