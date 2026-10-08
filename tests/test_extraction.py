from preprocessing.text_extraction import extract_text
from preprocessing.text_cleaning import clean_text


file_path = "data/resumes/sample_resume.pdf"


with open(file_path, "rb") as file:
    text = extract_text(file)


cleaned_text = clean_text(text)


print("\n========== CLEANED RESUME TEXT ==========\n")
print(cleaned_text)
print("\n=========================================\n")