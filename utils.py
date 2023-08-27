import requests


def send_message_to_private_channel(bot_token, channel_username, message):
    """
    Send a message to a private Telegram channel.

    Args:
        bot_token (str): The token of your Telegram bot.
        channel_username (str): The username of the private channel (including the "@" symbol).
        message (str): The message to send.
        recipient_user_id (str): The User ID of the recipient within the private channel.

    Returns:
        bool: True if the message was sent successfully, False otherwise.
    """
    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": channel_username,
        "text": message,
    }

    response = requests.post(api_url, data=data)

    if response.status_code == 200:
        return True
    else:
        print("Failed to send message:", response.text)
        return False

