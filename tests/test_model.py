from preprocessing.text_extraction import extract_text
from preprocessing.text_cleaning import clean_text
from models.embedding_model import generate_embedding
from matching.similarity import calculate_similarity


# -----------------------------
# 1. Extract resume
# -----------------------------

file_path = "data/resumes/sample_resume.pdf"

with open(file_path, "rb") as file:
    resume_text = extract_text(file)


# -----------------------------
# 2. Clean resume
# -----------------------------

resume_text = clean_text(resume_text)


# -----------------------------
# 3. Job Description
# -----------------------------

job_description = """
We are looking for a Machine Learning Engineer.

Required skills:
Python, TensorFlow, PyTorch, SQL,
Machine Learning, Deep Learning,
Computer Vision and Scikit-learn.

The candidate should have experience
developing machine learning models,
data preprocessing, model evaluation
and deploying AI applications.
"""


# -----------------------------
# 4. Generate embeddings
# -----------------------------

resume_embedding = generate_embedding(resume_text)

job_embedding = generate_embedding(job_description)


# -----------------------------
# 5. Calculate similarity
# -----------------------------

score = calculate_similarity(
    resume_embedding,
    job_embedding
)


print("\n====================================")
print("       AI RESUME SCREENING")
print("====================================")

print(f"\nSemantic Match Score: {score}%")

print("\nResume embedding shape:")
print(resume_embedding.shape)

print("\nJob description embedding shape:")
print(job_embedding.shape)

print("\n====================================")