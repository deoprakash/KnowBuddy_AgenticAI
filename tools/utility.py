def format_ai_summary(content: str) -> list:
    """
    Returns a list of cleaned bullet points from the AI summary.
    """
    import re

    match = re.search(r"1\.\s", content)
    if match:
        content = content[match.start():]

    lines = re.split(r'\n\d+\.\s', content)
    lines = [line.strip() for line in lines if line.strip()]
    return lines
