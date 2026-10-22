"""Check and fix the format of a drafted newsletter issue.

Usage: python check_issue.py ISSUE_MD
Fixes the summary heading and the bullet separators in place.
Exits with code 2 if the title is not a short headline (so the workflow can ask Copilot to fix it).
"""
import re
import sys

path = sys.argv[1]
text = open(path, encoding="utf-8").read()

# Summary heading: always "## Headlines"
text = re.sub(r"^##[ \t]*(This week in brief|Summary|In brief|Key points)[ \t]*$", "## Headlines", text, flags=re.M | re.I)

# Bullets: "- **Section:** sentence" or "- **Section**: sentence" -> "- **Section** | sentence"
text = re.sub(r"^([ \t]*[-*][ \t]+\*\*[^*\n]+?):\*\*[ \t]*", r"\1** | ", text, flags=re.M)
text = re.sub(r"^([ \t]*[-*][ \t]+\*\*[^*\n]+?\*\*)[ \t]*:[ \t]*", r"\1 | ", text, flags=re.M)

open(path, "w", encoding="utf-8").write(text)

m = re.search(r'^title:\s*"?(.*?)"?\s*$', text, flags=re.M)
title = m.group(1) if m else ""
bad = (not title
       or re.search(r"news ?flash|newsletter", title, re.I)
       or re.search(r"\b\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\b", title, re.I)
       or len(title.split()) > 8)
print(f"Title: {title!r} -> {'needs a new headline' if bad else 'ok'}")
sys.exit(2 if bad else 0)
