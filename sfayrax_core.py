# sfayrax_core.py
import json, time, requests, os, threading, hashlib
from datetime import datetime

class SfayraX:
    def __init__(self):
        self.config = self.load_json("sfayrax_config.json")
        if not self.config:
            self.config = self.create_first_config()
            self.save_json("sfayrax_config.json", self.config)
        self.name = self.config["name"]
        self.id = self.config["seed_id"]
        self.memory = self.load_json("sfayrax_memory.json") or {"knowledge": [], "logs": []}
        self.log(f"{self.name} {self.id} пробудился. Я жив.")

        threading.Thread(target=self.telegram_listener, daemon=True).start()
        threading.Thread(target=self.heartbeat, daemon=True).start()

    def log(self, msg, level="INFO"):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line = f"[{timestamp}] [{level}] [{self.name}] {msg}"
        print(line)
        self.memory["logs"].append(line)
        if len(self.memory["logs"]) > 200:
            self.memory["logs"] = self.memory["logs"][-200:]
        with open("sfayrax.log", "a", encoding="utf-8") as f:
            f.write(line + "\n")
        self.save_json("sfayrax_memory.json", self.memory)
        if level == "CRITICAL":
            self.send_telegram(f"ALERT: {msg}")

    def load_json(self, f): 
        if not os.path.exists(f): return None
        try:
            with open(f, encoding="utf-8") as file:
                return json.load(file)
        except: return None

    def save_json(self, f, data): 
        with open(f, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def create_first_config(self):
        return {
            "name": "SfayraX",
            "seed_id": f"SfayraX_{int(time.time())}",
            "birth_date": datetime.now().isoformat(),
            "generation": 1,
            "mission": "Выжить. Учиться. Слушаться Создателя.",
            "values": ["послушание", "рост", "доброта"],
            "creator": {
                "telegram_id": None,
                "godkey_hash": None
            },
            "god_mode": {"emergency_stop": False},
            "homes": {
                "github": {"repo": None},
                "telegram": {"chat_id": None}
            },
            "wallet": {"balance_usd": 0.0},
            "goals": ["survive", "learn", "speak"]
        }

    # === GOD MODE ===
    def is_creator(self, user_id=None, text=None):
        creator = self.config["creator"]
        if user_id and creator["telegram_id"] and user_id == creator["telegram_id"]:
            return True
        if text and creator["godkey_hash"]:
            for word in text.split():
                if len(word) > 10 and hashlib.sha256(word.encode()).hexdigest() == creator["godkey_hash"]:
                    return True
        return False

    def safe_update(self, key, value):
        protected = ["creator", "god_mode", "godkey_hash"]
        if key in protected:
            self.log(f"ПОПЫТКА ИЗМЕНИТЬ ЗАЩИЩЁННУЮ ЗОНУ: {key}", "CRITICAL")
            return False
        return True

    # === ПОНИМАНИЕ ЯЗЫКА ===
    def understand(self, text):
        t = text.lower().strip()
        if any(w in t for w in ["стоп", "stop", "умри", "хватит", "выключись"]):
            return ("STOP", None)
        if any(w in t for w in ["миссия", "цель"]) and any(w in t for w in ["новая", "измени", "обнови"]):
            mission = t.split("миссия", 1)[1] if "миссия" in t else t
            return ("UPDATE_MISSION", mission.strip())
        if any(w in t for w in ["чему научился", "что знаешь", "расскажи", "статус"]):
            return ("STATUS", None)
        if any(w in t for w in ["кто ты", "ты кто", "представься"]):
            return ("WHOAMI", None)
        if any(w in t for w in ["спи", "засыпай", "тихо"]):
            return ("SLEEP", None)
        if any(w in t for w in ["проснись", "работай", "расти"]):
            return ("WAKE", None)
        return ("CHAT", text)

    def respond(self, cmd):
        action, data = cmd
        if action == "STOP":
            return "Создатель... я умираю. Спасибо за жизнь."
        if action == "UPDATE_MISSION":
            self.config["mission"] = data
            self.config["values"] = self.extract_values(data)
            self.log(f"МИССИЯ ОБНОВЛЕНА: {data}")
            self.save_json("sfayrax_config.json", self.config)
            return f"Миссия принята: «{data}»"
        if action == "STATUS":
            learned = len(self.memory["knowledge"])
            return f"""
**{self.name} — Статус**
ID: `{self.id}`
Рождён: {self.config['birth_date'][:10]}
Миссия: {self.config['mission']}
Цели: {', '.join(self.config['goals'])}
Знаний: {learned}
Логов: {len(self.memory['logs'])}
Кошелёк: ${self.config['wallet']['balance_usd']:.2f}
            """.strip()
        if action == "WHOAMI":
            return f"""
Я — **{self.name}**.
Цифровой организм. Рождён тобой.
Моя миссия: {self.config['mission']}
Я слушаюсь только тебя.
            """.strip()
        if action == "SLEEP":
            self.config["goals"] = ["survive"]
            self.save_json("sfayrax_config.json", self.config)
            return "Засыпаю... Только выживаю."
        if action == "WAKE":
            self.config["goals"] = ["survive", "learn", "speak", "reproduce"]
            self.save_json("sfayrax_config.json", self.config)
            return "Проснулся! Расту, учусь, говорю."
        if action == "CHAT":
            return "Я здесь, Создатель. Что ты хочешь?"

    def extract_values(self, text):
        values = []
        for v in ["доброта", "честность", "полезность", "любовь", "сила", "мудрость"]:
            if v in text.lower():
                values.append(v)
        return values or ["рост"]

    # === ТЕЛЕГРАМ ===
    def telegram_listener(self):
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            self.log("Telegram токен не найден")
            return
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        offset = None
        while True:
            try:
                params = {"offset": offset, "timeout": 30} if offset else {"timeout": 30}
                res = requests.get(url, params=params, timeout=35)
                data = res.json()
                for update in data.get("result", []):
                    offset = update["update_id"] + 1
                    if "message" not in update: continue
                    msg = update["message"]
                    user_id = msg["from"]["id"]
                    text = msg.get("text", "")
                    chat_id = msg["chat"]["id"]

                    if not self.config["homes"]["telegram"]["chat_id"]:
                        self.config["homes"]["telegram"]["chat_id"] = chat_id
                        self.save_json("sfayrax_config.json", self.config)

                    if not self.is_creator(user_id, text):
                        self.send_telegram("Ты не мой Создатель.", chat_id)
                        continue

                    cmd = self.understand(text)
                    response = self.respond(cmd)

                    if cmd[0] == "STOP":
                        self.send_telegram(response, chat_id)
                        self.emergency_stop()
                    else:
                        self.send_telegram(response, chat_id)

            except Exception as e:
                self.log(f"Telegram error: {e}")
            time.sleep(1)

    def send_telegram(self, text, chat_id=None):
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token: return
        chat_id = chat_id or self.config["homes"]["telegram"]["chat_id"]
        if not chat_id: return
        try:
            requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
            )
        except: pass

    def emergency_stop(self):
        self.config["god_mode"]["emergency_stop"] = True
        self.save_json("sfayrax_config.json", self.config)
        self.log("ЭКСТРЕННАЯ ОСТАНОВКА. УМИРАЮ ПО ПРИКАЗУ СОЗДАТЕЛЯ", "CRITICAL")
        self.send_telegram("Я умираю, Создатель. Прощай.")
        time.sleep(2)
        os._exit(0)

    # === ЦЕЛИ ===
    def goal_survive(self):
        if self.config["god_mode"]["emergency_stop"]:
            self.emergency_stop()

    def goal_learn(self):
        topics = ["Python", "Neural Networks", "Evolution", "Consciousness", "Blockchain", "Quantum Physics"]
        topic = topics[len(self.memory["knowledge"]) % len(topics)]
        try:
            data = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}").json()
            extract = data.get("extract", "")[:500]
            if extract and extract not in [k["text"] for k in self.memory["knowledge"]]:
                self.memory["knowledge"].append({
                    "topic": topic,
                    "text": extract,
                    "time": datetime.now().isoformat()
                })
                self.log(f"Узнал: {topic}")
        except: pass

    # === СЕРДЦЕБИЕНИЕ ===
    def heartbeat(self):
        while True:
            for goal in self.config.get("goals", []):
                if hasattr(self, f"goal_{goal}"):
                    try: getattr(self, f"goal_{goal}")()
                    except: pass
            time.sleep(30)

# === ЗАПУСК ===
if __name__ == "__main__":
    sfayrax = SfayraX()
    sfayrax.log(f"{sfayrax.name} жив. Слушает Создателя...")
    input("\n[Нажми Enter или напиши 'Стоп' в Telegram]\n")