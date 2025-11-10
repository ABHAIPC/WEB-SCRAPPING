from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import time
from openpyxl import Workbook
import datetime
import os
# ---------- CONFIG ----------
MOVIE_URL = "https://sfcticket.in/book-ticket/15794"  # Example movie link
TICKET_PRICE = 150  # Set ticket price manually

# Setup Firefox
options = Options()
# options.add_argument("--headless")   # Uncomment if you want to run without opening browser
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

# Open movie page (contains all showtime buttons)
driver.get(MOVIE_URL)
time.sleep(5)


# ---------- HANDLE TERMS AND CONDITIONS MODAL ----------
try:
    # Wait for the Accept button and click it
    accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-acc"))
    )
    accept_button.click()
    print("✅ Terms and conditions accepted")
    time.sleep(2)
except Exception as e:
    print(f"❌ Could not find/click accept button: {e}")
    # Continue anyway in case the modal doesn't appear

# Find all showtime buttons
show_buttons = driver.find_elements(By.CSS_SELECTOR, "button.text-center.tibtn")

print(f"Found {len(show_buttons)} shows for this movie.")

# Excel setup
wb = Workbook()
ws = wb.active
ws.title = "Show Bookings"
ws.append(["Show Time", "Screen", "Booked Seats", "Available Seats", "Blocked Seats", "Revenue"])

# Loop through each showtime
for idx, btn in enumerate(show_buttons):
    # Extract text (example: "07:00 AM\nSAVITHA")
    show_text = btn.text.strip().split("\n")
    show_time = show_text[0] if len(show_text) > 0 else "Unknown"
    screen = show_text[1] if len(show_text) > 1 else "Unknown"

    # Click the button to open seat layout
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(5)

    # Wait for seats to load
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "seat-wrapper")))
    time.sleep(2)

    # Parse seat layout
    soup = BeautifulSoup(driver.page_source, "html.parser")
    seat_buttons = soup.find_all("button")

    available, booked, blocked = [], [], []
    for sb in seat_buttons:
        seat_num = sb.get_text(strip=True)
        if not seat_num.isdigit():
            continue
        cls = sb.get("class", [])
        if "btn-seatbook" in cls:   # Booked
            booked.append(seat_num)
        elif "btn-seat" in cls:     # Available
            available.append(seat_num)
        elif "fade" in cls:         # Blocked
            blocked.append(seat_num)

    total_booked = len(booked)
    revenue = total_booked * TICKET_PRICE

    print(f"\nShow: {show_time} ({screen})")
    print(f"✅ Available: {len(available)}")
    print(f"❌ Booked: {total_booked}")
    
    print(f"💰 Revenue: ₹{revenue}")

    # Save to Excel
    ws.append([show_time, screen, total_booked, len(available), len(blocked), revenue])

    # Go back to movie page for next show
    driver.back()
    time.sleep(4)
    show_buttons = driver.find_elements(By.CSS_SELECTOR, "button.text-center.tibtn")  # Refresh buttons list

# Save Excel file
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
excel_file = f"movie_summary_{timestamp}.xlsx"
wb.save(excel_file)
print(f"\n📊✅ Data saved to {excel_file}")
driver.quit()
