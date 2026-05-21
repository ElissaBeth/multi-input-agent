import re

def fmt_time(dt, tz):
    return dt.astimezone(tz).strftime('%A, %B %d %Y %I:%M %p %Z')

def sanitize(text: str) -> str:
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return text.strip()

def html_to_discord(text):
    if text is None: return ''
    text = str(text)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<(b|strong)>(.*?)</\1>', r'**\2**', text, flags=re.DOTALL)
    text = re.sub(r'<(i|em)>(.*?)</\1>', r'*\2*', text, flags=re.DOTALL)
    text = re.sub(r'<code>(.*?)</code>', r'`\1`', text, flags=re.DOTALL)
    text = re.sub(r'<pre>(.*?)</pre>', r'```\1```', text, flags=re.DOTALL)
    text = re.sub(r'<u>(.*?)</u>', r'__\1__', text, flags=re.DOTALL)
    text = re.sub(r'<s>(.*?)</s>', r'~~\1~~', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)  # strip remaining tags
    return text
