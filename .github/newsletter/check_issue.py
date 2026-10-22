"""Check and fix the format of a drafted newsletter issue.

Usage: python check_issue.py ISSUE_MD
Fixes the summary heading and turns the Headlines into a two-column table, in place.
Exits with code 2 if the title is not a short headline (so the workflow can ask Copilot to fix it).
"""
import re
import sys

path = sys.argv[1]
text = open(path, encoding="utf-8").read()

# Summary heading: always "## Headlines"
text = re.sub(r"^##[ \t]*(This week in brief|Summary|In brief|Key points)[ \t]*$", "## Headlines", text, flags=re.M | re.I)

# Headlines: always a two-column table "| **Section** | sentence |", no bullets, no header row
def headlines_table(match):
    rows = []
    for line in match.group(2).splitlines():
        line = line.strip()
        if not line:
            continue
        if re.fullmatch(r"\|?[\s:|-]+\|?", line):  # table separator line: drop it and any plain header row before it
            if rows and "**" not in rows[-1]:
                rows.pop()
            continue
        m = (re.match(r"^[-*][ \t]+\*\*(.+?):\*\*[ \t]*(.+)$", line)
             or re.match(r"^[-*][ \t]+\*\*(.+?)\*\*[ \t]*[|:][ \t]*(.+)$", line)
             or re.match(r"^\|[ \t]*\*\*(.+?)\*\*[ \t]*\|[ \t]*(.+?)[ \t]*\|?$", line))
        if m:
            rows.append(f"| **{m.group(1).strip().rstrip(':')}** | {m.group(2).strip().rstrip('|').strip()} |")
        else:
            rows.append(line)
    return match.group(1) + "\n\n" + "\n".join(rows) + "\n\n"

text = re.sub(r"^(## Headlines)[ \t]*\n(.*?)(?=^## |\Z)", headlines_table, text, count=1, flags=re.M | re.S)

open(path, "w", encoding="utf-8").write(text)

m = re.search(r'^title:\s*"?(.*?)"?\s*$', text, flags=re.M)
title = m.group(1) if m else ""
bad = (not title
       or re.search(r"news ?flash|newsletter", title, re.I)
       or re.search(r"\b\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\b", title, re.I)
       or len(title.split()) > 8)
print(f"Title: {title!r} -> {'needs a new headline' if bad else 'ok'}")
sys.exit(2 if bad else 0)
