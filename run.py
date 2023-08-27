from bot import MidlandBot
from dotenv import load_dotenv
import os
import time

load_dotenv()

monitored_listings = []
monitoring_id = os.getenv('MH_ID')
print("Starting bot")
# Create the bot class
test_bot = MidlandBot(user_name=os.getenv('MH_USERNAME'),
                      password=os.getenv('MH_PASSWORD'),
                      monitoring_id= monitoring_id,
                      ni_number="JB321613C",
                      start=0,
                      end=23
                      )
test_bot.start_bot()
