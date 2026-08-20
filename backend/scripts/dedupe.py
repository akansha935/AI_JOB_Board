import sys
sys.path.append("..")

from rapidfuzz import fuzz
from collections import defaultdict
from normalize import load_and_normalize

def normalize_text(s: str) -> str:
    return (s or "").strip().lower()

def deduplicate(jobs: list, title_threshold=88) -> list:
    """
    Groups jobs by (normalized company), then fuzzy-matches titles within
    each company group to catch near-duplicate postings across sources.
    Keeps the first-seen record, merges 'sources' seen for that job.
    """
    by_company = defaultdict(list)
    for job in jobs:
        key = normalize_text(job["company"])
        by_company[key].append(job)

    final_jobs = []
    duplicates_removed = 0

    for company, company_jobs in by_company.items():
        kept = []  # list of (job, sources_set)
        for job in company_jobs:
            title_norm = normalize_text(job["title"])
            matched = False
            for kept_job, sources_set in kept:
                kept_title_norm = normalize_text(kept_job["title"])
                similarity = fuzz.token_sort_ratio(title_norm, kept_title_norm)
                if similarity >= title_threshold:
                    sources_set.add(job["source"])
                    duplicates_removed += 1
                    matched = True
                    break
            if not matched:
                kept.append((job, {job["source"]}))

        for job, sources_set in kept:
            job["all_sources"] = sorted(sources_set)
            final_jobs.append(job)

    print(f"Deduplication: {len(jobs)} -> {len(final_jobs)} jobs "
          f"({duplicates_removed} duplicates merged)")
    return final_jobs

if __name__ == "__main__":
    jobs = load_and_normalize("../../data/raw_jobs.json")
    deduped = deduplicate(jobs)