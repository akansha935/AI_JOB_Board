import sys
sys.path.append("..")

from app.database import engine, SessionLocal, Base
from app.models import Job
from normalize import load_and_normalize
from dedupe import deduplicate

def load_jobs_to_db(jobs: list):
    # Create tables if they don't exist yet
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        # Clear existing data for a clean reload (safe for dev)
        session.query(Job).delete()

        inserted = 0
        for job in jobs:
            db_job = Job(
                id=job["id"],
                title=job["title"],
                company=job["company"],
                location=job["location"],
                source=job["source"],
                description=job["description"],
                min_experience=job["min_experience"],
                max_experience=job["max_experience"],
                domain=job["domain"],
                skills_raw=job["skills_raw"],
                posted_at=job["posted_at"],
                apply_url=job["apply_url"],
            )
            session.add(db_job)
            inserted += 1

            # Commit in batches of 500 to avoid memory/timeout issues
            if inserted % 500 == 0:
                session.commit()
                print(f"  Inserted {inserted}/{len(jobs)}...")

        session.commit()
        print(f"Done. Inserted {inserted} jobs into the database.")

    except Exception as e:
        session.rollback()
        print(f"Error during load: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    jobs = load_and_normalize("../../data/raw_jobs.json")
    deduped = deduplicate(jobs)
    load_jobs_to_db(deduped)