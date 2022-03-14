from datetime import datetime
from twilio.rest import Client
import gspread
import json
import os

#Twilio account info/creds
account_sid = os.environ['TWILIO_SID']
auth_token = os.environ['TWILIO_TOKEN']
twilio = Client(account_sid, auth_token)

#Google Sheets info/creds 
sa = gspread.service_account()
sh = sa.open("Plant Journal")
wks = sh.worksheet("Overview")

def main():
#Gets data from worksheet, adds items to list if today is their checkup day
  data = wks.get_all_values()
  todayPlants = []
  for row in data:
    if row[5] == datetime.today().strftime('%b %d'):
      todayPlants.append("{} ({}), Status: {} Last Watering: {}".format(row[0],row[1],row[2],row[4]))

#Checks if list is empty or not (to see if there are plants to check today) and if so, sends SMS
  if todayPlants:
    msg = "Check on these plants today!\n"
    for plant in todayPlants:
      msg += "- {}\n".format(plant)

    twilio.messages.create(
      to = os.environ['TWILIO_TO_NUM'],
      from_= os.environ['TWILIO_FROM_NUM'],
      body = msg 
    )
    print(msg)
  else:
    print("No plants to check today!")

main()
