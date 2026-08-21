import json

SOURCE_KEYWORDS = {
    "linkedin": "LinkedIn",
    "naukri": "Naukri",
    "indeed": "Indeed",
    "internshala": "Internshala",
}

def extract_source(via_field: str) -> str:
    if not via_field:
        return "Other"
    via_lower = via_field.lower()
    for keyword, clean_name in SOURCE_KEYWORDS.items():
        if keyword in via_lower:
            return clean_name
    return "Other"

def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def extract_apply_url(apply_options_raw: str):
    try:
        cleaned = apply_options_raw
        if cleaned.startswith('"') and cleaned.endswith('"'):
            cleaned = json.loads(cleaned)
        parsed = json.loads(cleaned)
        if isinstance(parsed, list) and len(parsed) > 0:
            return parsed[0].get("link")
    except Exception:
        return None
    return None

def normalize_job(raw: dict) -> dict:
    return {
        "id": raw.get("job_id"),
        "title": (raw.get("title") or "").strip(),
        "company": (raw.get("company_name") or "").strip(),
        "location": (raw.get("location") or "").strip(),
        "source": extract_source(raw.get("via", "")),
        "description": raw.get("description") or raw.get("formattedDescription") or "",
        "min_experience": safe_int(raw.get("minExperienceRequired")),
        "max_experience": safe_int(raw.get("maxExperienceRequired")),
        "domain": raw.get("domain"),
        "skills_raw": raw.get("skills") if raw.get("skills") != "Not mentioned" else None,
        "posted_at": raw.get("posted_at"),
        "apply_url": extract_apply_url(raw.get("apply_options", "")),
    }

def load_and_normalize(filepath: str) -> list:
    with open(filepath, encoding="utf-8") as f:
        raw_jobs = json.load(f)

    normalized = []
    skipped = 0
    for raw in raw_jobs:
        job = normalize_job(raw)
        if not job["id"] or not job["title"]:
            skipped += 1
            continue
        normalized.append(job)

    print(f"Normalized {len(normalized)} jobs, skipped {skipped} invalid entries.")
    return normalized

if __name__ == "__main__":
    jobs = load_and_normalize("../../data/raw_jobs.json")
    from collections import Counter
    sources = Counter(j["source"] for j in jobs)
    for src, count in sources.most_common():
        print(f"  {src}: {count}")