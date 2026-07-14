import glob
import re

for filepath in glob.glob('design/*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove @jerseycityindustrytalk and its preceding comma/space
    content = re.sub(r',\s*@jerseycityindustrytalk', '', content)
    content = re.sub(r'@jerseycityindustrytalk\s*', '', content)
    
    # Handle the link in the HTML (using unicode string instead of literal character)
    content = re.sub(r' \u2014 <a href="https://www\.instagram\.com/jerseycityindustrytalk/">link</a>', '', content)
    content = re.sub(r'<a href="https://www\.instagram\.com/jerseycityindustrytalk/">.*?</a>', '', content)
    content = content.replace('industrytalk', '')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
