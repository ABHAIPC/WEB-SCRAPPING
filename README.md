# SFC Ticket Show Scraper (Firefox + Selenium)

Scrape show-wise seat stats (Booked / Available / Blocked) and estimate revenue from **sfcticket.in** show pages.  
Outputs a timestamped Excel file with one row per show.

## ✨ What it does
- Opens a movie page, accepts T&C modal, and iterates through all showtime buttons
- Loads the seat layout for each show and classifies seats
- Calculates estimated revenue (`booked_seats * TICKET_PRICE`)
- Saves a summary to Excel: `movie_summary_YYYY-MM-DD_HHMMSS.xlsx`

## 🧰 Tech
- Python 3.8+
- Selenium (Firefox driver via `webdriver-manager`)
- BeautifulSoup4
- openpyxl (Excel export)

## 🔧 Prerequisites
- **Firefox** browser installed (required for geckodriver).
- Python 3.8+ (3.10+ recommended).

## 🚀 Quick Start

```bash
# 1) Clone
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# 2) (Optional) Create and activate a virtual environment
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Run
python main.py
