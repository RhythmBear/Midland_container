from bot import MidlandBot
from dotenv import load_dotenv
import os
import time

load_dotenv()

monitored_listings = []
monitoring_id = os.getenv('MH_ID')
print("Starting bot")
# Create the bot class

trials = 0
application_successful = False

while not application_successful:
    # Create Bot Instance 
    try:
        bot_instance = MidlandBot(test=os.getenv('TEST'),
                        user_name=os.getenv('MH_USERNAME'),
                        password=os.getenv('MH_PASSWORD'),
                        monitoring_id= monitoring_id,
                        ni_number="JB321613C",
                        start=0,
                        end=23
                        )

        trials += 1
        bot_instance.send_message_to_telegram(f"Attempt: {trials} \nTesting : {bot_instance.testing} \nStarting Bot to monitor for lisitng_id = {bot_instance.listing_id} using {bot_instance.username}'s account.")
        
        bot_instance.start_bot()
        application_successful = bot_instance.application_success
        
    except Exception as err:
        bot_instance.logger.info(f"An {err} Error occured while trying to start bot...") 
        bot_instance.send_message_to_telegram(f"An {err} Error occured while trying to start bot for User: {bot_instance.username} and listing {bot_instance.listing_id}...") 
        if trials >= 3: 
            bot_instance.logger.info(f"Failed to start the bot application after {trials} trials... Stopping Bot.")
            bot_instance.send_message_to_telegram(f"Failed to start the bot win application after {trials} trials... \nUser: {bot_instance.username} and listing {bot_instance.listing_id}...")
            break  
        
        else:
            bot_instance.logger.info(f"Restarting Bot... Attempt: {trials}")
    else:
        # Check if the bot successfully submitted the listing and send a message once the Bot instance has been stopped 
        bot_instance.send_message_to_telegram(f"Bot has stopped running... \nJust Completed {bot_instance.username}'s apllication for listing_id = {bot_instance.listing_id}  ")

   
    