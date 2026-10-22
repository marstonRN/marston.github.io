"""Run the PubMed searches listed in instructions.md and write the new records to a Markdown file.

Usage: python fetch_pubmed.py INSTRUCTIONS_MD OUTPUT_MD [DAYS]
Only the Python standard library is used.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
TOOL = "marston-newsletter"


def get(endpoint, params):
    params = dict(params, tool=TOOL)
    data = urllib.parse.urlencode(params).encode()
    for attempt in range(4):
        try:
            with urllib.request.urlopen(EUTILS + endpoint, data=data, timeout=60) as r:
                return r.read()
        except Exception as e:  # network hiccup or rate limit: wait and retry
            if attempt == 3:
                raise
            time.sleep(2 ** (attempt + 1))
        finally:
            time.sleep(0.4)  # stay under 3 requests per second


def read_searches(path):
    text = open(path, encoding="utf-8").read()
    found = re.findall(r"^### Search \d+: (.+?)\s*\n+```\n(.+?)\n```", text, re.M | re.S)
    if not found:
        sys.exit("No searches found in " + path)
    return [(name.strip(), " ".join(q.split())) for name, q in found]


def search(query, days):
    term = f'({query}) AND ("last {days} days"[edat])'
    raw = get("esearch.fcgi", {"db": "pubmed", "term": term, "retmax": 100, "retmode": "json"})
    res = json.loads(raw)["esearchresult"]
    if res.get("errorlist") and any(res["errorlist"].values()):
        print("PubMed reported a problem with the search:", res["errorlist"], file=sys.stderr)
    return res.get("idlist", [])


def fetch(pmids):
    if not pmids:
        return []
    root = ET.fromstring(get("efetch.fcgi", {"db": "pubmed", "id": ",".join(pmids), "retmode": "xml"}))
    records = []
    for art in root.iter("PubmedArticle"):
        text = lambda path: " ".join("".join(e.itertext()) for e in art.findall(path)).strip()
        authors = art.findall(".//AuthorList/Author")
        first = ""
        if authors:
            a = authors[0]
            first = (a.findtext("LastName") or a.findtext("CollectiveName") or "").strip()
            if len(authors) > 1:
                first += " et al."
        year = text(".//JournalIssue/PubDate/Year") or text(".//ArticleDate/Year") or text(".//JournalIssue/PubDate/MedlineDate")[:4]
        records.append({
            "pmid": text(".//MedlineCitation/PMID"),
            "title": text(".//ArticleTitle"),
            "journal": text(".//Journal/Title"),
            "year": year,
            "authors": first,
            "types": ", ".join(t.text for t in art.findall(".//PublicationTypeList/PublicationType") if t.text),
            "abstract": text(".//Abstract/AbstractText"),
        })
    return records


def main():
    instructions, out = sys.argv[1], sys.argv[2]
    days = int(sys.argv[3]) if len(sys.argv) > 3 else 7
    matched = {}  # pmid -> list of search names, in first-seen order
    for name, query in read_searches(instructions):
        ids = search(query, days)
        print(f"{name}: {len(ids)} new records")
        for pmid in ids:
            matched.setdefault(pmid, []).append(name)
    records = []
    ids = list(matched)
    for i in range(0, len(ids), 100):
        records += fetch(ids[i:i + 100])
    lines = [f"# New PubMed records (last {days} days)", "", f"{len(records)} unique records.", ""]
    for n, r in enumerate(records, 1):
        abstract = r["abstract"]
        if len(abstract) > 1500:
            abstract = abstract[:1500].rsplit(" ", 1)[0] + " [...]"
        lines += [
            f"## {n}. {r['title']}",
            f"- Authors: {r['authors']}",
            f"- Journal: {r['journal']} ({r['year']})",
            f"- Publication type: {r['types']}",
            f"- Found by: {'; '.join(matched.get(r['pmid'], []))}",
            f"- Link: https://pubmed.ncbi.nlm.nih.gov/{r['pmid']}/",
            "",
            abstract or "(no abstract)",
            "",
        ]
    open(out, "w", encoding="utf-8").write("\n".join(lines))
    print(f"Wrote {len(records)} records to {out}")


if __name__ == "__main__":
    main()
