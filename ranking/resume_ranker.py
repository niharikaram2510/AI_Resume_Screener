from preprocessing.text_extraction import extract_text
from preprocessing.text_cleaning import clean_text
from preprocessing.section_extraction import extract_sections
from preprocessing.data_loader import get_required_skills

from matching.job_role_matcher import get_best_job_role
from matching.resume_skill_matcher import match_resume_to_role
from matching.jd_matcher import calculate_jd_match

from scoring.score_calculator import (
    detect_career_stage,
    calculate_section_scores,
    calculate_overall_score,
    get_experience_label
)


# ============================================================
# ANALYZE ONE RESUME
# ============================================================

def analyze_resume(
    file,
    requested_role,
    job_description=""
):
    """
    Analyze one resume against the requested job role.
    """

    # ========================================================
    # 1. EXTRACT RESUME TEXT
    # ========================================================

    raw_text = extract_text(file)

    resume_text = clean_text(
        raw_text
    )

    if not resume_text:

        raise ValueError(
            f"Could not extract text from {file.name}"
        )


    # ========================================================
    # 2. SEMANTIC JOB ROLE MATCHING
    # ========================================================

    role_result = get_best_job_role(
        requested_role
    )

    selected_role = role_result[
        "job_role"
    ]


    # ========================================================
    # 3. EXTRACT RESUME SECTIONS
    # ========================================================

    sections = extract_sections(
        resume_text
    )


    # ========================================================
    # 4. DETECT CAREER STAGE
    # ========================================================

    career_stage = detect_career_stage(
        sections
    )


    # ========================================================
    # 5. SKILL MATCHING
    # ========================================================

    skill_result = match_resume_to_role(
        resume_text,
        selected_role
    )

    skill_score = skill_result[
        "skill_score"
    ]


    # IMPORTANT:
    # resume_skill_matcher.py does not return required_skills.
    # Therefore we get them directly from the job-role knowledge base.

    required_skills = get_required_skills(
        selected_role
    )


    # ========================================================
    # 6. SECTION SCORES
    # ========================================================

    section_scores = calculate_section_scores(
        resume_text,
        required_skills,
        selected_role
    )


    # ========================================================
    # 7. ADAPTIVE OVERALL SCORE
    # ========================================================

    base_score = calculate_overall_score(
        skill_score,
        section_scores["experience"],
        section_scores["projects"],
        section_scores["education"],
        section_scores["certifications"],
        career_stage
    )


    # ========================================================
    # 8. JOB DESCRIPTION MATCHING
    # ========================================================

    jd_result = calculate_jd_match(
        resume_text,
        job_description
    )

    jd_score = jd_result.get(
        "jd_score",
        0
    )


    # ========================================================
    # 9. FINAL SCORE
    # ========================================================

    if job_description.strip():

        final_score = (
            base_score * 0.70
            +
            jd_score * 0.30
        )

    else:

        final_score = base_score


    final_score = round(
        final_score,
        2
    )


    # ========================================================
    # 10. MATCHED SKILLS
    # ========================================================

    matched_skills = [
        item["skill"]
        for item in skill_result[
            "matched_skills"
        ]
    ]


    # ========================================================
    # 11. MISSING SKILLS
    # ========================================================

    missing_skills = [
        item["skill"]
        for item in skill_result[
            "missing_skills"
        ]
    ]


    # ========================================================
    # 12. CANDIDATE STRENGTHS
    # ========================================================

    strengths = []


    if skill_score >= 80:

        strengths.append(
            "Strong required-skill coverage"
        )


    if section_scores["experience"] >= 50:

        strengths.append(
            "Relevant experience"
        )


    if section_scores["projects"] >= 50:

        strengths.append(
            "Relevant project experience"
        )


    if section_scores["education"] >= 80:

        strengths.append(
            "Relevant educational background"
        )


    if section_scores["certifications"] >= 80:

        strengths.append(
            "Relevant certifications"
        )


    if jd_score >= 70 and job_description.strip():

        strengths.append(
            "Strong alignment with the job description"
        )


    if not strengths:

        strengths.append(
            "Some relevant evidence was identified"
        )


    # ========================================================
    # 13. RETURN COMPLETE RESULT
    # ========================================================

    return {

        "candidate":
            file.name,

        "requested_role":
            requested_role,

        "matched_role":
            selected_role,

        "role_similarity":
            role_result["similarity"],

        "career_stage":
            career_stage,

        "experience_label":
            get_experience_label(
                career_stage
            ),

        "skill_score":
            skill_score,

        "experience_score":
            section_scores[
                "experience"
            ],

        "project_score":
            section_scores[
                "projects"
            ],

        "education_score":
            section_scores[
                "education"
            ],

        "certification_score":
            section_scores[
                "certifications"
            ],

        "base_score":
            base_score,

        "jd_score":
            jd_score,

        "jd_semantic_score":
            jd_result.get(
                "semantic_score",
                0
            ),

        "jd_skills":
            jd_result.get(
                "jd_skills",
                []
            ),

        "matched_jd_skills":
            jd_result.get(
                "matched_jd_skills",
                []
            ),

        "overall_score":
            final_score,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "strengths":
            strengths,

        "resume_text":
            resume_text
    }


# ============================================================
# RANK MULTIPLE RESUMES
# ============================================================

def rank_resumes(
    files,
    requested_role,
    job_description=""
):
    """
    Analyze and rank multiple resumes.
    """

    results = []


    # ========================================================
    # ANALYZE EACH RESUME
    # ========================================================

    for file in files:

        try:

            result = analyze_resume(
                file,
                requested_role,
                job_description
            )

            results.append(
                result
            )

        except Exception as error:

            results.append(
                {
                    "candidate":
                        file.name,

                    "error":
                        str(error),

                    "overall_score":
                        0
                }
            )


    # ========================================================
    # SORT BY OVERALL SCORE
    # ========================================================

    results.sort(
        key=lambda x:
            x.get(
                "overall_score",
                0
            ),
        reverse=True
    )


    # ========================================================
    # ASSIGN RANKS
    # ========================================================

    for index, result in enumerate(
        results,
        start=1
    ):

        result["rank"] = index


    return results