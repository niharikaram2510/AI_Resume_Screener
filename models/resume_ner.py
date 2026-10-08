import re

from transformers import pipeline

from preprocessing.data_loader import load_job_roles


MODEL_NAME = "oksomu/resume-ner"


resume_ner = pipeline(
    "token-classification",
    model=MODEL_NAME,
    aggregation_strategy="simple"
)


def get_known_skills():
    """
    Load all skills from the job-role knowledge base.
    """

    df = load_job_roles()

    skills = (
        df["skill"]
        .dropna()
        .drop_duplicates()
        .tolist()
    )

    return skills


def clean_entity(text):
    """
    Clean a Transformer-extracted entity.
    """

    text = text.replace("##", "")
    text = text.strip(" ,.;:|-/")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def is_valid_skill(skill):
    """
    Remove obvious NER noise.
    """

    if not skill:
        return False

    if len(skill) < 2:
        return False

    if not re.search(
        r"[A-Za-z0-9]",
        skill
    ):
        return False

    return True


def normalize_skill(skill):
    """
    Normalize common resume skill variations.
    """

    mapping = {
        "MangoDB": "MongoDB",
        "Devops": "DevOps",
        "Numpy": "NumPy",
        "Pandas": "Pandas",
        "Python": "Python",
        "Fastapi": "FastAPI",
        "Flask": "Flask",
        "Matplotlib": "Matplotlib"
    }

    return mapping.get(
        skill,
        skill
    )


def extract_resume_entities(text):
    """
    Extract entities using the Resume-NER Transformer.
    """

    return resume_ner(text)


def extract_skills(text):
    """
    Extract and clean skills detected by the Transformer.
    """

    results = extract_resume_entities(text)

    skills = []

    for result in results:

        if result["entity_group"] != "SKILL":
            continue

        skill = clean_entity(
            result["word"]
        )

        if not is_valid_skill(skill):
            continue

        skill = normalize_skill(
            skill
        )

        if skill not in skills:

            skills.append(skill)

    return skills