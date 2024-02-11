import re

def extract_html_block(text):
    patterns = [
        r'(<div data-state-token="[^"]*" decode-data-ved="1"[^>]*>.*?3;\[9\]0;)',
        r'(<div decode-data-ved="1"[^>]*>.*?3;\[9\]0;)',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.DOTALL)

        for match in matches:
            # remove ending string
            cleaned_match = match.replace('3;[9]0;', '')
            return cleaned_match