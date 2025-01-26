import requests
import time
import schedule

game_id = "16732694052"  # ใส่ Game ID ของ Fisch
webhook_url = "YOUR_WEBHOOK_URL"  # ใส่ Webhook URL ของคุณ
url = f"https://games.roblox.com/v1/games/{game_id}/servers/Public?sortOrder=Asc&limit=100"

def fetch_all_servers():
    servers = []
    next_page = None

    while True:
        current_url = url if not next_page else f"{url}&cursor={next_page}"
        response = requests.get(current_url)

        if response.status_code == 200:
            data = response.json()
            servers.extend(data.get("data", []))  # รวมเซิร์ฟเวอร์เข้าไปใน list
            next_page = data.get("nextPageCursor", None)
            if not next_page:
                break  # ไม่มีหน้าถัดไปแล้ว
        else:
            print("Error:", response.status_code)
            break

    return servers

def job():
    all_servers = fetch_all_servers()
    print(f"จำนวนเซิร์ฟเวอร์ทั้งหมด: {len(all_servers)}")

    # แจ้งเตือนไปยัง Discord
    for server in all_servers:
        server_id = server.get("id", "Unknown")
        player_count = server.get("playing", 0)
        max_players = server.get("maxPlayers", 0)
        message = f"SEVERS: {server_id}\n# PLAYER {player_count}/{max_players}"
        requests.post(webhook_url, json={"content": message})

# ตั้งเวลาให้ฟังก์ชันทำงานทุก 30 วินาที
schedule.every(30).seconds.do(job)

while True:
    schedule.run_pending()  # รันงานที่กำหนดไว้
    time.sleep(1)  # รอ 1 วินาที
