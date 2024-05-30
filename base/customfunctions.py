import re
from django.shortcuts import redirect

def split_name(full_name):
    name_pattern = re.compile(r'(\b\w+\b)\s+(\b\w+\b)')
    match = name_pattern.match(full_name)

    if match:
        first_name = match.group(1)
        last_name = match.group(2)
        return first_name, last_name
    else:
        return None, None
   