from flask import Flask, request, jsonify
import subprocess
import time

app = Flask(__name__)

@app.route('/')
def home():
    #Homepage

    return "Welcome to the Midland Bot."

@app.route('/run_bot', methods=['GET'])
def run_bot():
    # Set environment variables for user credentials
    env_vars = {
        'TEST': True, 
        'MH_USERNAME': "eoadepoju10@gmail.com",
        'MH_PASSWORD': "okechukwu",
        'MH_ID': 3324,
        'BOT_TOKEN': '6381387820:AAEwsEYPCifq3WKX-atUx-B7-fy7CKKyC90',
        'BOT_USERNAME': '@midland_monitor'
    }

    # docker run -it --rm -e "MH_USERNAME=eoadepoju10@gmail.com" -e "MH_PASSWORD=okechukwu" -e "MH_ID=3324" -e "BOT_TOKEN=6381387820:AAEwsEYPCifq3WKX-atUx-B7-fy7CKKyC90" -e "BOT_USERNAME=@midland_monitor" -e "TEST"=True -m 2G -v $(pwd):/app  bot
    # python3 main.py eoadepoju10@gmail.com okechukwu 3357 JB321623C 9 12
    # docker run -it --rm -e "MH_USERNAME=eoadepoju10@gmail.com" -e "MH_PASSWORD=okechukwu" -e "MH_ID=3355" -e "BOT_TOKEN=6381387820:AAEwsEYPCifq3WKX-atUx-B7-fy7CKKyC90" -e "BOT_USERNAME=@midland_monitor" -m 2G -v $(pwd):/app  bot-instance
    # docker run -it --rm -e "MH_USERNAME=eoadepoju10@gmail.com" -e "okechukwu" -e "MH_ID=3355" -e "BOT_TOKEN=6381387820:AAEwsEYPCifq3WKX-atUx-B7-fy7CKKyC90" -e "BOT_USERNAME=@midland_monitor" bot-instance
    
    # Run the bot instance container and capture the logs
    bot_container_id = subprocess.run(['docker', 'run', '-d'] + [f'-e {k}={v}' for k, v in env_vars.items()] + ['-m', '2G', 'bot'], capture_output=True, text=True)
    print(bot_container_id.returncode)
    time.sleep(5)
    print(bot_container_id.stdout)
    print(bot_container_id.stderr)
    
    # Stream the logs of the bot instance
    # bot_logs = subprocess.run(['docker', 'logs', '-f', bot_container_id], capture_output=True, text=True, check=True).stdout
    
    return jsonify({'message': 'Bot instance started', 'id': bot_container_id.stdout.strip()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
