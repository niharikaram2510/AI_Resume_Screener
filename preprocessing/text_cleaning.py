import re


def clean_text(text):
    """
    Clean extracted resume text while preserving
    useful line and section information.
    """

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive spaces within lines
    lines = []

    for line in text.split("\n"):

        line = re.sub(r"[ \t]+", " ", line)
        line = line.strip()

        if line:
            lines.append(line)

    # Remove excessive blank lines
    text = "\n".join(lines)

    return text.strip()