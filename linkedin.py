#!/usr/bin/env python3

import csv
import json
import re
import time
from pathlib import Path
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

BAD_WORDS = {
    "home",
    "welcome",
    "learn",
    "discover",
    "future",
    "innovation",
    "solutions",
    "attention required",
    "couples",
    "today",
    "better"
}

# ----------------------------------------------------
# Project initialization
# ----------------------------------------------------

BASE = Path(".")

OUTPUT = BASE / "output"
LOGS = BASE / "logs"
CHECKPOINTS = BASE / "checkpoints"
CACHE = BASE / "cache"

OUTPUT.mkdir(exist_ok=True)
LOGS.mkdir(exist_ok=True)
CHECKPOINTS.mkdir(exist_ok=True)
CACHE.mkdir(exist_ok=True)

RESULTS_FILE = OUTPUT / "linkedin_results.csv"
FAILED_FILE = OUTPUT / "failed.csv"
LOG_FILE = LOGS / "app.log"
CHECKPOINT_FILE = CHECKPOINTS / "progress.json"

if not RESULTS_FILE.exists():

    with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Company Domain",
            "Company Name",
            "LinkedIn URL",
            "Processed At",
            "Status"
        ])

if not FAILED_FILE.exists():

    with open(FAILED_FILE, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Company Domain",
            "Reason"
        ])

if not CHECKPOINT_FILE.exists():

    with open(CHECKPOINT_FILE, "w") as f:

        json.dump(
            {
                "processed": 0,
                "last_domain": None,
                "updated": None
            },
            f,
            indent=4
        )

LOG_FILE.touch(exist_ok=True)

if not Path("domains.csv").exists():

    with open(
        "domains.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)
        writer.writerow(["Company Domain"])

    print()
    print("domains.csv created.")
    print("Add one domain per line and rerun.")
    exit(0)

def clean(text):

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def fallback_name(domain):

    parts = domain.split(".")

    if len(parts) >= 2:
        name = parts[-2]
    else:
        name = parts[0]

    return (
        name.replace("-", " ")
            .replace("_", " ")
            .title()
    )


def normalize_company(name, domain):

    if not name:
        return fallback_name(domain)

    lower = name.lower()

    for word in BAD_WORDS:

        if word in lower:
            return fallback_name(domain)

    return name


def get_company_name(domain):

    try:

        r = requests.get(
            "https://" + domain,
            timeout=15,
            headers=HEADERS,
            allow_redirects=True
        )

        soup = BeautifulSoup(r.text, "lxml")

        og = soup.find(
            "meta",
            property="og:site_name"
        )

        if og:

            value = og.get("content")

            if value:

                return normalize_company(
                    clean(value),
                    domain
                )

        app = soup.find(
            "meta",
            attrs={
                "name": "application-name"
            }
        )

        if app:

            value = app.get("content")

            if value:

                return normalize_company(
                    clean(value),
                    domain
                )

        scripts = soup.find_all(
            "script",
            type="application/ld+json"
        )

        for s in scripts:

            try:

                data = json.loads(s.string)

                if isinstance(data, dict):

                    if data.get("@type") == "Organization":

                        return normalize_company(
                            clean(data["name"]),
                            domain
                        )

            except:

                pass

        if soup.title:

            title = clean(soup.title.text)

            parts = re.split(r"\||-|–|:", title)

            longest = max(parts, key=len)

            return normalize_company(
                longest,
                domain
            )

    except Exception:

        pass

    return fallback_name(domain)


def search_linkedin(domain, company):

    queries = [

        f'"{domain}" linkedin',

        f'"{domain}" site:linkedin.com/company',

        f'{company} linkedin',

        f'{company} site:linkedin.com/company',

    ]

    with DDGS() as ddgs:

        for q in queries:

            try:

                results = ddgs.text(
                    q,
                    max_results=10
                )

                for r in results:

                    url = r.get("href", "")

                    if "linkedin.com/company/" in url:

                        return url.split("?")[0]

            except:

                continue

    return ""


def enrich(domain):

    company = get_company_name(domain)

    linkedin = search_linkedin(
        domain,
        company
    )

    return {

        "Company Name": company,

        "Company Domain": domain,

        "LinkedIn": linkedin

    }


domains = []

with open(
    "domains.csv",
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        domain = row.get(
            "Company Domain",
            ""
        ).strip().lower()

        if domain:

            domains.append(domain)

domains = list(dict.fromkeys(domains))

processed_domains = set()

if RESULTS_FILE.exists():

    with open(
        RESULTS_FILE,
        newline="",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:

            processed_domains.add(
                row["Company Domain"].lower()
            )

domains = [

    d for d in domains

    if d not in processed_domains

]

print(f"Remaining domains: {len(domains)}")

print(f"Loaded {len(domains)} unique domains")

print()

processed = len(processed_domains)

for domain in domains:

    print("=" * 70)

    print(domain)

    try:

        row = enrich(domain)

        status = "Completed"

        print(row)

        with open(
            RESULTS_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([

                row["Company Domain"],

                row["Company Name"],

                row["LinkedIn"],

                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

                status

            ])

    except Exception as e:

        with open(
            FAILED_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([

                domain,

                str(e)

            ])

    processed += 1

    with open(
        CHECKPOINT_FILE,
        "w"
    ) as f:

        json.dump(

            {

                "processed": processed,

                "last_domain": domain,

                "updated": datetime.now().isoformat()

            },

            f,

            indent=4

        )

    time.sleep(0.5)

print()

print("Enrichment completed.")

print(f"Processed: {processed}")

print(f"Results: {RESULTS_FILE}")

print(f"Failed: {FAILED_FILE}")
