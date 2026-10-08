from models.embedding_model import model
from preprocessing.data_loader import load_job_roles
from sklearn.metrics.pairwise import cosine_similarity


def extract_jd_skills(job_description):
    """
    Find known skills from the job description.
    """

    df = load_job_roles()

    known_skills = (
        df["skill"]
        .dropna()
        .drop_duplicates()
        .tolist()
    )

    jd_lower = job_description.lower()

    found_skills = []

    for skill in known_skills:

        if skill.lower() in jd_lower:
            found_skills.append(skill)

    return found_skills


def calculate_jd_match(
    resume_text,
    job_description
):
    """
    Calculate resume-to-job-description
    semantic and skill-based similarity.
    """

    if not job_description.strip():
        return {
            "jd_score": 0,
            "jd_skills": [],
            "matched_jd_skills": []
        }

    # -----------------------------------------
    # Semantic similarity
    # -----------------------------------------

    resume_embedding = model.encode(
        [resume_text]
    )

    jd_embedding = model.encode(
        [job_description]
    )

    semantic_score = cosine_similarity(
        resume_embedding,
        jd_embedding
    )[0][0]

    semantic_score = max(
        0,
        min(
            1,
            float(semantic_score)
        )
    ) * 100

    # -----------------------------------------
    # Skill coverage
    # -----------------------------------------

    jd_skills = extract_jd_skills(
        job_description
    )

    resume_lower = resume_text.lower()

    matched_jd_skills = [
        skill
        for skill in jd_skills
        if skill.lower() in resume_lower
    ]

    if jd_skills:

        skill_score = (
            len(matched_jd_skills)
            / len(jd_skills)
        ) * 100

    else:

        skill_score = semantic_score

    # -----------------------------------------
    # Hybrid JD score
    # -----------------------------------------

    jd_score = (
        skill_score * 0.60
        +
        semantic_score * 0.40
    )

    return {
        "jd_score": round(
            jd_score,
            2
        ),

        "semantic_score": round(
            semantic_score,
            2
        ),

        "jd_skills": jd_skills,

        "matched_jd_skills":
            matched_jd_skills
    }