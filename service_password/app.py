from flask import Flask, request, jsonify
import requests
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app_port = int(os.getenv("PORT", 5000))
if not app_port:
    raise ValueError("Error: PORT pada environment variable belum di-set.")

PHP_SERVICE_URL = os.getenv("API_DATABASE_URL")
if not PHP_SERVICE_URL:
    raise ValueError("Error: API_DATABASE_URL pada environment variable belum di-set.")

KEY_FILE = "secret.key"
if not os.path.exists(KEY_FILE):
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(Fernet.generate_key())
with open(KEY_FILE, "rb") as key_file:
    cipher = Fernet(key_file.read())

@app.route('/python-service/passwords', methods=['POST'])
def add_password():
    data = request.json
    raw_password = data.get('password')
    
    encrypted_pw = cipher.encrypt(raw_password.encode()).decode()
    
    payload = {
        "service": data.get('service'),
        "username": data.get('username'),
        "password": encrypted_pw
    }
    
    try:
        response = requests.post(PHP_SERVICE_URL, json=payload)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"success": False, "message": "Service PHP tidak merespons"}), 500

@app.route('/python-service/passwords', methods=['GET'])
def get_passwords():
    response = requests.get(PHP_SERVICE_URL)
    if response.status_code != 200:
        return jsonify({
            "success": False,
            "message": f"Laravel menolak dengan status {response.status_code}",
            "detail": response.text
        }), response.status_code

    if response.status_code == 200:
        passwords = response.json()
        for pwd in passwords:
            try:
                pwd['decrypted_password'] = cipher.decrypt(pwd['password'].encode()).decode()
            except:
                pwd['decrypted_password'] = "ERROR_DECRYPT"
        return jsonify({"success": True, "message": "Password berhasil diambil.",  "data": passwords}), 200
    return jsonify({"success": False, "message": "Gagal mengambil data dari service PHP"}), response.status_code

@app.route('/python-service/passwords/<int:id>', methods=['PUT'])
def update_password(id):
    data = request.json
    payload = {}
    
    if 'service' in data:
        payload['service'] = data['service']
    if 'username' in data:
        payload['username'] = data['username']
    if 'password' in data:
        payload['encrypted_password'] = cipher.encrypt(data['password'].encode()).decode()
    
    try:
        response = requests.put(f"{PHP_SERVICE_URL}/{id}", json=payload)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"success": False, "message": "PHP Service tidak merespons"}), 500

@app.route('/python-service/passwords/<int:id>', methods=['DELETE'])
def delete_password(id):
    try:
        response = requests.delete(f"{PHP_SERVICE_URL}/{id}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"success": False, "message": "PHP Service tidak merespons"}), 500

if __name__ == '__main__':
    app.run(port=app_port, debug=True)