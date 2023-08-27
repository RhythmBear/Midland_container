from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run_bot', methods=['POST'])
def run_bot():
    # Set environment variables for user credentials
    env_vars = {
        'MH_USERNAME': 'user@example.com',
        'MH_PASSWORD': 'secretpassword',
        'MH_ID': 3355,
        'BOT_TOKEN': '6381387820:AAEwsEYPCifq3WKX-atUx-B7-fy7CKKyC90',
        'BOT_USERNAME': '@midland_monitor'

    }
    # python3 main.py eoadepoju10@gmail.com okechukwu 3357 JB321623C 9 12
    # docker run -it --rm -e "MH_USERNAME=eoadepoju10@gmail.com" -e "MH_PASSWORD=okechukwu" -e "MH_ID=3355" -e "BOT_TOKEN=6381387820:AAEwsEYPCifq3WKX-atUx-B7-fy7CKKyC90" -e "BOT_USERNAME=@midland_monitor" -m 2G -v $(pwd):/app  bot-instance
    # docker run -it --rm -e "MH_USERNAME=eoadepoju10@gmail.com" -e "okechukwu" -e "MH_ID=3355" -e "BOT_TOKEN=6381387820:AAEwsEYPCifq3WKX-atUx-B7-fy7CKKyC90" -e "BOT_USERNAME=@midland_monitor" bot-instance
    
    # Run the bot instance container and capture the logs
    bot_container_id = subprocess.run(['docker', 'run', '-d'] + ['--env={}={}'.format(k, v) for k, v in env_vars.items()] + ['your-bot-image'], capture_output=True, text=True).stdout.strip()
    
    # Stream the logs of the bot instance
    bot_logs = subprocess.run(['docker', 'logs', '-f', bot_container_id], capture_output=True, text=True, check=True).stdout
    
    return jsonify({'message': 'Bot instance started', 'logs': bot_logs})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
