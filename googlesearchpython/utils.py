import re

def extract_html_block(text):
    # regex pattern
    pattern = r'(<div data-state-token="[^"]*" decode-data-ved="1"[^>]*>.*?3;\[9\]0;)'
    
    # find matches
    matches = re.findall(pattern, text, re.DOTALL)

    # process matches
    for match in matches:
        # remove ending string
        cleaned_match = match.replace('3;[9]0;', '')
        return cleaned_match
