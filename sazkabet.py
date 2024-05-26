from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import json
import consts
import time
 
service = Service(executable_path="chromedriver.exe")
browser = uc.Chrome(service=service)
browser.get("https://www.sazka.cz/kurzove-sazky/sports/matches")

time.sleep(2)

browser.find_element(By.XPATH, "/html/body/div[5]/div/div[2]/button").click()

time.sleep(5)

matches = browser.find_elements(By.XPATH, "//div/div/div/ul/li/div/div")
matchData = []

for match in matches:
    try:
        dataValue = "-"
        try:
            # Extract match date
            date = match.find_element(By.XPATH, "./div[3]/div[1]/div/span[2]")
            dateValue = date.get_attribute("textContent")
        except: pass
        
        # Check if the date text contains "dnes" (case-insensitive)
        # if "dnes" not in dateValue.lower():
        #     continue  # Skip this iteration if "dnes" is not found in the date text

        # Extract match title
        titles = match.find_elements(By.XPATH, ".//div[contains(@data-testid, 'event-card-team-name')]")

        if len(titles) != 2: continue
        firstTeam = titles[0].get_attribute("textContent").replace(" ", " ").strip()
        secondTeam = titles[1].get_attribute("textContent").replace(" ", " ").strip()

        oddsCells = match.find_elements(By.XPATH, ".//button[contains(@data-testid, 'outcome-button')]/span[contains(@data-testid, 'outcome-odds')]")

        oddsData = {}

        for oddsCell in oddsCells:
            try:
                desc = oddsCell.find_element(By.XPATH, "./span[1]")
                odd = oddsCell.find_element(By.XPATH, "./span[2]")
                oddsData[desc.get_attribute("textContent")] = odd.get_attribute("textContent")
            except: 
                print("Span element not found, skipping this iteration.")
                continue
            
        # Append match data to the list
        matchData.append({
            "title": "{} - {}".format(firstTeam, secondTeam),
            "date":  dateValue,
            "odds": oddsData
        })
    except: pass

# Create a dictionary with match data
data = {"matches": matchData}

# Write data to a JSON file
with open("sazkabet-matches.json", "w") as jsonFile:
    json.dump(data, jsonFile, indent=4)

browser.quit()
