from preprocessing.text_extraction import extract_text
from preprocessing.text_cleaning import clean_text
from preprocessing.section_extraction import (
    extract_sections
)


# -----------------------------
# Load Resume
# -----------------------------

file_path = "data/resumes/sample_resume.pdf"

with open(file_path, "rb") as file:
    resume_text = extract_text(file)


# -----------------------------
# Clean Resume
# -----------------------------

resume_text = clean_text(
    resume_text
)


# -----------------------------
# Extract Sections
# -----------------------------

sections = extract_sections(
    resume_text
)


# -----------------------------
# Display Sections
# -----------------------------

print("\n==============================================")
print("             RESUME SECTIONS")
print("==============================================")


for section, content in sections.items():

    print("\n----------------------------------------------")

    print("SECTION:", section.upper())

    print("----------------------------------------------")

    print(content)


print("\n==============================================")