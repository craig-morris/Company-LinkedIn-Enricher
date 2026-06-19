python
#!/usr/bin/env python3

import csv
import json
import re
import time

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


domains = [

    "eclipse-results.com",
    "ohiofirstlandtitle.com",
    "arnoldprinting.com",
    "muohio.edu",
    "cblhdesign.com",
    "directoptions.com",
    "cityarch.com",
    "mraservices.com",
    "jewishtoledo.org",
    "rapidmailing.com",
    "gf-wealth.com",
    "everhard.com",
    "remax.net",
    "millsrunapts.com",
    "tartanagency.com",
    "brighton-science.com",
    "urbansites.com",
    "manningcontracting.com",
    "easternlakecountychamber.org",
    "gardnercorp.com",
    "sedgwick.com",
    "tigerpistol.com",

]

results = []

for domain in domains:

    print("=" * 60)

    row = enrich(domain)

    print(row)

    results.append(row)

    time.sleep(0.5)

with open(
    "linkedin_results.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "Company Name",
            "Company Domain",
            "LinkedIn"
        ]
    )

    writer.writeheader()

    writer.writerows(results)

print()
print("Saved linkedin_results.csv")
