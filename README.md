5mins reading....

# Company LinkedIn Enricher

A lightweight Python utility for enriching company domains with their official company name and LinkedIn company page.

---

# Features

* Extracts company names from:

  * `og:site_name`
  * `application-name`
  * `schema.org Organization`
  * HTML `<title>`
  * Domain fallback

* Searches public indexes for LinkedIn company pages

* Automatically filters common marketing phrases

* Exports results to CSV

* No Selenium required

* No ChromeDriver required

* No Playwright required

* Works on Ubuntu, Debian, and most Linux VPS providers

---

# System Requirements

* Ubuntu 22.04 or newer
* Debian 12 or newer
* Python 3.10+
* Internet connection

Recommended RAM:

* 1 GB minimum
* 2 GB recommended

---

# Installation

## Update your server

bash
sudo apt update
sudo apt upgrade -y


---

## Install required packages

bash
sudo apt install -y \
git \
python3 \
python3-pip \
python3-venv


Verify Python:

bash
python3 --version


Example:


Python 3.12.3


---

# Clone the repository

bash
git clone https://github.com/YOUR_USERNAME/company-linkedin-enricher.git

cd company-linkedin-enricher


Replace `YOUR_USERNAME` with your GitHub username.

---

# Create a virtual environment

bash
python3 -m venv venv


Activate it:

bash
source venv/bin/activate


Your shell should now show:


(venv)


---

# Upgrade pip

bash
pip install --upgrade pip


---

# Install Python dependencies

bash
pip install \
requests \
beautifulsoup4 \
lxml \
ddgs


Or install from a `requirements.txt` file:

bash
pip install -r requirements.txt


---

# Recommended requirements.txt

Create a file named `requirements.txt`:

text
requests>=2.32.0
beautifulsoup4>=4.13.0
lxml>=5.2.0
ddgs>=9.0.0


Then install with:

bash
pip install -r requirements.txt


---

# Running the script

bash
python linkedin.py


The script will process the configured domains and create:


linkedin_results.csv


---

# Example Output


============================================================

{
  'Company Name': 'Tiger Pistol',
  'Company Domain': 'tigerpistol.com',
  'LinkedIn': 'https://www.linkedin.com/company/tiger-pistol/'
}

============================================================


---

# CSV Output


Company Name,Company Domain,LinkedIn

Tiger Pistol,tigerpistol.com,https://www.linkedin.com/company/tiger-pistol/

Sedgwick,sedgwick.com,https://www.linkedin.com/company/sedgwick/


---

# Adding Domains

Edit the `domains` list inside `linkedin.py`:

python
domains = [

    "google.com",

    "microsoft.com",

    "apple.com",

    "amazon.com",

]


Then run:

bash
python linkedin.py


---

# Recommended Bulk Processing

Instead of hardcoding domains, store them in a file:


domains.csv


Example:

csv
Company Domain
google.com
apple.com
microsoft.com
amazon.com


Future versions can read directly from CSV for processing thousands of domains.

---

# Project Structure


company-linkedin-enricher/

├── linkedin.py
├── requirements.txt
├── README.md
├── domains.csv
├── linkedin_results.csv
└── venv/


---

# Updating the Project

bash
cd company-linkedin-enricher

git pull

source venv/bin/activate

pip install -r requirements.txt --upgrade


---

# Deactivating the Virtual Environment

bash
deactivate


---

# Reactivating Later

bash
cd company-linkedin-enricher

source venv/bin/activate

python linkedin.py


---

# Troubleshooting

## ModuleNotFoundError

Example:


ModuleNotFoundError: No module named 'bs4'


Install dependencies:

bash
pip install -r requirements.txt


---

## Virtual environment not active

Check:

bash
which python


Expected output:


.../company-linkedin-enricher/venv/bin/python


If it points to `/usr/bin/python3`, activate the virtual environment:

bash
source venv/bin/activate


---

## Permission denied

Grant execute permission:

bash
chmod +x linkedin.py


Run:

bash
./linkedin.py


or

bash
python linkedin.py


---

## Update Python packages

bash
pip install --upgrade requests beautifulsoup4 lxml ddgs


---

# License

This project is provided as-is for educational and business enrichment workflows.

Users are responsible for complying with the terms of service and applicable laws governing any websites or services they query.

---

# Contributing

Pull requests and improvements are welcome.

Suggestions for improving company name extraction, search quality, CSV handling, concurrency, and enrichment accuracy are encouraged.

---
# Automatic Directory Creation

The application automatically creates all required directories and files on startup.

No manual setup is required.

When `linkedin.py` starts, it will create the following structure if it does not already exist:
text
company-linkedin-enricher/

├── linkedin.py
├── README.md
├── requirements.txt
├── .gitignore
├── domains.csv

├── output/
│   ├── linkedin_results.csv
│   └── failed.csv

├── logs/
│   └── app.log

├── checkpoints/
│   └── progress.json

└── cache/

If any directory or file is missing, it will be created automatically.

This allows the application to resume interrupted jobs and maintain organized output without requiring manual preparation.

## First Run

Simply execute:
bash
source venv/bin/activate

python linkedin.py

The application will initialize the project structure automatically.

No additional configuration is necessary.
-----------------
# Version

Current Version: **1.0.0**


Company LinkedIn Enricher
Author: SCRIPTKID
Python 3 Compatible
Ubuntu / Debian Compatible

