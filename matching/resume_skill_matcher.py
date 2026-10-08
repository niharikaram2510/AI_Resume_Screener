import re

from models.resume_ner import extract_skills
from preprocessing.data_loader import load_job_roles


IMPORTANCE_WEIGHTS = {
    "High": 3,
    "Medium": 2,
    "Low": 1
}


def normalize_skill(skill):
    """
    Normalize skill names for comparison.
    """

    skill = skill.lower().strip()

    skill = skill.rstrip(
        ".,;:"
    )

    skill = re.sub(
        r"\s+",
        " ",
        skill
    )

    replacements = {
        "scikit learn": "scikit-learn",
        "scikitlearn": "scikit-learn",
        "tensorflow": "tensorflow",
        "pytorch": "pytorch",
        "numpy": "numpy",
        "pandas": "pandas",
        "mongodb": "mongodb",
        "devops": "devops",
        "fastapi": "fastapi",
        "matplotlib": "matplotlib"
    }

    return replacements.get(
        skill,
        skill
    )


def exact_skill_match(
    skill,
    resume_text
):
    """
    Check whether a required skill
    explicitly appears in the resume.
    """

    pattern = (
        r"(?<!\w)"
        + re.escape(skill.lower())
        + r"(?!\w)"
    )

    return bool(
        re.search(
            pattern,
            resume_text.lower()
        )
    )


def match_resume_to_role(
    resume_text,
    job_role
):
    """
    Match resume skills using:
    1. Transformer NER
    2. Exact resume verification
    3. Importance-weighted scoring
    """

    df = load_job_roles()

    role_data = df[
        df["job_role"].str.lower()
        == job_role.lower()
    ]

    role_data = role_data.drop_duplicates(
        subset=["skill"]
    )

    # Transformer extraction
    transformer_skills = extract_skills(
        resume_text
    )

    transformer_normalized = {
        normalize_skill(skill)
        for skill in transformer_skills
    }

    matched = []
    missing = []

    total_weight = 0
    matched_weight = 0

    for _, row in role_data.iterrows():

        skill = row["skill"]
        importance = row["importance"]

        weight = IMPORTANCE_WEIGHTS[
            importance
        ]

        total_weight += weight

        normalized_required = normalize_skill(
            skill
        )

        # Two independent signals
        ner_match = (
            normalized_required
            in transformer_normalized
        )

        text_match = exact_skill_match(
            skill,
            resume_text
        )

        if ner_match or text_match:

            matched.append({
                "skill": skill,
                "importance": importance,
                "source": (
                    "Transformer"
                    if ner_match
                    else "Resume Text"
                ),
                "weight": weight
            })

            matched_weight += weight

        else:

            missing.append({
                "skill": skill,
                "importance": importance,
                "weight": weight
            })

    if total_weight > 0:

        score = (
            matched_weight
            / total_weight
        ) * 100

    else:

        score = 0

    # Combine detected skills
    detected_skills = list(
        dict.fromkeys(
            transformer_skills
            + [
                row["skill"]
                for _, row in role_data.iterrows()
                if exact_skill_match(
                    row["skill"],
                    resume_text
                )
            ]
        )
    )

    return {
        "job_role": job_role,
        "detected_skills": detected_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "skill_score": round(
            score,
            2
        )
    }