# Weekly newsletter: instructions

GitHub Copilot follows this file every week (workflow `.github/workflows/newsletter.yml`). Edit it to change the newsletter; the next run uses the new version. The four PubMed searches at the end are run by the workflow itself.

## Schedule and output

- Runs every Monday morning, and on demand from the Actions tab.
- Covers the previous 7 days.
- Copilot writes exactly one file, `_newsletter/YYYY-MM-DD.md` (today's date). The workflow then opens a pull request; Mark reviews and merges it.

## News sources

Open these pages, find items from the last 7 days, and follow links to the full articles as needed. Other reputable sources found from these pages may be used.

- Federal Council media releases: https://www.admin.ch/gov/en/start/documentation/media-releases.html
- FOPH (BAG/OFSP) news: https://www.bag.admin.ch/en/current
- SBK-ASI (Swiss nurses association): https://www.sbk-asi.ch
- SGI-SSMI: https://sgi-ssmi.ch/fr/news
- La Source School of Nursing: https://www.ecolelasource.ch/fr/actualites
- Swissinfo health news: https://www.swissinfo.ch/eng/
- WHO news: https://www.who.int/news
- ICN (International Council of Nurses) news: https://www.icn.ch/news

## Front matter

```yaml
---
title: "Weekly newsletter: D Month YYYY"
collection: newsletter
date: YYYY-MM-DD
excerpt: "One sentence: the single most important item of the week."
---
```

Any text containing an apostrophe goes in double quotes.

## Structure (max. about 1,000 words, two A4 pages)

1. `## This week in brief`: one bullet per section below, each the key sentence of that section, with the section name in bold.
2. `## Swiss health policy`: Federal Council, FOPH (BAG/OFSP), parliament, cantons, votes, tariffs (e.g. TARDOC), nursing initiative implementation. 2 to 4 items.
3. `## Nursing and healthcare in Switzerland`: SBK-ASI, SGI-SSMI, hospitals, H+, universities, Obsan, Swiss media. 2 to 4 items.
4. `## Nursing and healthcare worldwide`: WHO, ICN, major journals and international news. 2 to 4 items.
5. `## New research`: all new PubMed records from the four searches below, as **one executive-summary paragraph of max. 100 words** (links not counted). Group the findings by theme rather than listing papers one by one. Cite every article inline as a numbered link, e.g. `[1](https://pubmed.ncbi.nlm.nih.gov/PMID/)`, so each new article is linked exactly once. Base the summary on titles and abstracts only. If there are no new records this week, write one line saying so.
6. Optional `## Coming up`: relevant events in the next weeks.

End with: `<p style="font-size: 0.8em; color: var(--global-text-color-light, #6b6b6b);">Searched and synthesised with AI assistance (GitHub Copilot); reviewed and approved by Mark Marston before publication. For information only, not medical, legal or policy advice. <a href="/newsletter/#about">About this newsletter</a></p>`

## Accuracy rules

- Every item links to its original source (official site, journal, or reputable media). No source, no item.
- Only report what the source says; no speculation, no invented figures, dates or quotes.
- Items must be dated within the covered week (research: entered in PubMed within the last 7 days).
- Prefer primary sources (admin.ch, bag.admin.ch, who.int, icn.ch, sbk-asi.ch, sgi-ssmi.ch) over secondary reporting. French and German sources are fine; write in English.
- If a section has nothing relevant, say so in one line rather than padding it.
- Neutral, factual tone. No political opinions.

## PubMed searches

The workflow runs the four searches below through PubMed E-utilities (records entered in the last 7 days), removes duplicates and saves the results to `pubmed.md`. Use only `pubmed.md` for the New research section. To change a search, edit its text below; keep the `### Search N: Name` heading and the code block.

### Search 1: Family-centred care nursing interventions

```
("Family Nursing" [MeSH Terms] OR ("Family" [tiab] AND "Centered" [tiab] AND "Nurs*" [tiab]) OR (family AND intervention) OR (Family AND centered AND care)) AND (Nurs* OR "health personnel" [MeSH Terms] OR (healthcare AND professional*) OR (interprofessional AND team)) AND ((training AND program) OR (intervention AND participatory AND design AND development) OR (structured AND communication) OR (ethic* AND (consultation OR meeting)) OR (care AND coordinator) OR (nurse AND "decision making") OR "Decision Making, Shared" [MeSH Terms] OR "Decision Making" [MeSH Terms]) AND (randomized controlled trial [Publication Type] OR systematic review [Publication Type] OR meta analysis [Publication Type] OR experimental design [MeSH Terms] OR ((effective* [tiab] OR efficiency [tiab] OR efficient [tiab] OR feasibility [tiab]) AND study [tiab]))
```

### Search 2: Family-centred interventions in paediatric critical care

```
("Adaptive Clinical Trial" [pt] OR "Clinical Study" [pt] OR "Clinical Trial" [pt] OR "Clinical Trial, Phase I" [pt] OR "Clinical Trial, Phase II" [pt] OR "Clinical Trial, Phase III" [pt] OR "Clinical Trial, Phase IV" [pt] OR "Clinical Trial Protocol" [pt] OR "Clinical Trial, Veterinary" [pt] OR "Comparative Study" [pt] OR "Controlled Clinical Trial" [pt] OR "Equivalence Trial" [pt] OR "Guideline" [pt] OR "Meta-Analysis" [pt] OR "Multicenter Study" [pt] OR "Network Meta-Analysis" [pt] OR "Observational Study" [pt] OR "Practice Guideline" [pt] OR "Pragmatic Clinical Trial" [pt] OR "Randomized Controlled Trial" [pt] OR "Review" [pt] OR "Scoping Review" [pt] OR "Systematic Review" [pt] OR "Validation Study" [pt]) AND (((("critical care" [MeSH Terms] AND "pediatrics" [MeSH Terms]) OR ("intensive care units" [MeSH Terms] AND "pediatrics" [MeSH Terms]) OR "intensive care, neonatal" [MeSH Terms] OR "intensive care units, neonatal" [MeSH Terms] OR "intensive care units, pediatric" [MeSH Terms] OR ((("critical*" OR "intensive" OR "intermediate" OR "intermediary") AND ("care" OR "unit*")) AND ("pediatric*" OR "paediatric*" OR "child*"))) AND ("intervention" OR "concept" OR "model" OR "action" OR "principles")) AND (("care" OR "caring" OR "nurse" OR "nursing" OR "centre" OR "centered" OR "centred" OR "practice" OR "integrat*") AND ("family" [MeSH Terms] OR "family nursing" [MeSH Terms] OR "Family Practice" [MeSH Terms] OR "family" OR "families")))
```

### Search 3: Family-centred care in paediatric critical care

```
("family" AND ("centred" OR "centered") AND ("care" OR "nurs*")) AND ("PICU" OR (("pediatric" OR "paediatric") AND ("critical" OR "intensive" OR "intermediate") AND ("care" OR "nursing")))
```

### Search 4: Paediatric critical care diaries

```
("diary" [tiab] OR "diaries" [tiab]) AND ("PICU" [tiab] OR (("pediatric" [tiab] OR "paediatric" [tiab]) AND ((("critical" [tiab] OR "intensive" [tiab] OR "intermediate" [tiab]) AND ("care" [tiab] OR "nursing" [tiab])) OR "intensive care" [mh])))
```
