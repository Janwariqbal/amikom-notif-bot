import requests
from bs4 import BeautifulSoup
import os

LOGIN_URL = "https://student.amikompurwokerto.ac.id/login"
NOTIF_URL = "https://student.amikompurwokerto.ac.id/notifikasi"

USERNAME = os.environ['USERNAME_PORTAL']
PASSWORD = os.environ['PASSWORD_PORTAL']
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

session = requests.Session()

# LOGIN
login_data = {
    "username": USERNAME,
    "password": PASSWORD
}

session.post(LOGIN_URL, data=login_data)

# AMBIL HALAMAN NOTIFIKASI
response = session.get(NOTIF_URL)
soup = BeautifulSoup(response.text, "html.parser")

# AMBIL NOTIFIKASI PERTAMA
first_td = soup.find("td")

if not first_td:
    exit()

latest_notif = first_td.text.strip()

# CEK FILE TERAKHIR
if os.path.exists("last.txt"):
    with open("last.txt", "r") as f:
        last_notif = f.read().strip()
else:
    last_notif = ""

# KIRIM KE TELEGRAM JIKA BERBEDA
if latest_notif != last_notif:
    with open("last.txt", "w") as f:
        f.write(latest_notif)

    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(send_url, data={
        "chat_id": CHAT_ID,
        "text": f"🔔 Notifikasi Baru:\n\n{latest_notif}"
    })
