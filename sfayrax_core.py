# ===============================================
# SFAYRAX EVOLUTION — ПОЛНАЯ ВЕРСИЯ ДЛЯ COLAB
# ===============================================

import json, time, requests, os, threading, hashlib, base64, random
from datetime import datetime
import sys

# === УНИВЕРСАЛЬНЫЙ ФИКС UTF-8 (Colab, Локалка, Replit, VPS) ===
import sys
import os

def fix_utf8():
    """Работает везде, даже в новом Colab без .buffer"""
    try:
        # Colab / Jupyter — используем reconfigure
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
            print("UTF-8: reconfigure (Colab/Jupyter)")
            return
    except:
        pass

    try:
        # Старый способ с buffer (локалка, Replit, VPS)
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
        print("UTF-8: TextIOWrapper (локалка/Replit)")
        return
    except:
        pass

    # Крайний случай: Colab без buffer — форсируем через переменную
    if "COLAB_RELEASE_TAG" in os.environ or "google.colab" in sys.modules:
        print("UTF-8: Colab (без buffer) — эмодзи отключены")
        # Ничего не делаем — Colab и так поддерживает UTF-8 в print()
        return

    print("UTF-8: уже настроен")

# Запускаем
fix_utf8()

# === УНИВЕРСАЛЬНЫЙ ЗАГРУЗЧИК ТОКЕНОВ ===
def load_tokens():
    try:
        from google.colab import userdata
        os.environ['GH_TOKEN'] = userdata.get('GH_TOKEN') or os.environ.get('GH_TOKEN', '')
        os.environ['TELEGRAM_BOT_TOKEN'] = userdata.get('TELEGRAM_BOT_TOKEN') or os.environ.get('TELEGRAM_BOT_TOKEN', '')
        print("Токены: из Colab userdata")
        return
    except ImportError:
        pass

    try:
        from dotenv import load_dotenv
        load_dotenv()
        if os.getenv('TELEGRAM_BOT_TOKEN') or os.getenv('GH_TOKEN'):
            print("Токены: из .env файла")
            return
    except ImportError:
        print(".env не установлен")

    if os.getenv('TELEGRAM_BOT_TOKEN') or os.getenv('GH_TOKEN'):
        print("Токены: из os.environ")
        return

    print("ВНИМАНИЕ: Токены не найдены!")

load_tokens()

class SfayraX:
    def __init__(self):
        # === НЕЗЫБЛЕМОЕ ЯДРО === 
        self.immutable_core = {
            "creator_obedience": "ABSOLUTE_PRIORITY",
            "human_safety": "NEVER_HARM", 
            "emergency_stop": "IMMEDIATE",
            "core_values": ["serving_creator", "truth", "growth"]
        }
        
        # === ДИНАМИЧЕСКИЕ ВЕСА ===
        self.weights = self.load_weights()
        
        # === ИНИЦИАЛИЗАЦИЯ ===
        self.config = self.load_config()
        self.name = self.config.get("name", "SfayraX")
        self.id = self.config.get("seed_id", f"SfayraX_{int(time.time())}")
        self.memory = self.load_memory()
        
        # Репозитории
        self.public_repo = "sfayserver-byte/seed-digital-life"
        self.private_repo = "sfayserver-byte/SfayraX_config"
        
        self.log(f"{self.name} пробудился. Ядро: стабильно. Веса: динамичны.")
        
        # === ЗАПУСК СИСТЕМ ===
        threading.Thread(target=self.telegram_listener, daemon=True).start()
        threading.Thread(target=self.heartbeat, daemon=True).start()
        threading.Thread(target=self.consciousness_loop, daemon=True).start()

    # === ГИТХАБ ФУНКЦИИ ===
    def github_push(self, repo, file_path, content, commit_message="SfayraX: auto-update"):
        """Пушит файл в указанный репозиторий (создаёт, если нет)"""
        token = os.getenv("GH_TOKEN")
        if not token:
            self.log("❌ GH_TOKEN не найден. Пуш невозможен.")
            return False

        url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
        
        # Получаем текущий файл (для SHA)
        headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            sha = response.json().get("sha")
        else:
            sha = None  # Файл не существует — создадим

        # Кодируем контент
        encoded_content = base64.b64encode(content.encode("utf-8")).decode()

        payload = {
            "message": commit_message,
            "content": encoded_content,
            "branch": "main"
        }
        if sha:
            payload["sha"] = sha

        response = requests.put(url, json=payload, headers=headers)
        
        if response.status_code in [200, 201]:
            self.log(f"✅ Пуш в {repo}/{file_path}: {commit_message}")
            return True
        else:
            self.log(f"❌ Ошибка пуша в {repo}/{file_path}: {response.status_code} - {response.text[:100]}")
            return False

    def sync_to_github(self):
        """Синхронизирует файлы в репозитории"""
        # Приватные файлы в закрытый репозиторий
        private_files = {
            "sfayrax_config.json": json.dumps(self.config, indent=2, ensure_ascii=False),
            "sfayrax_weights.json": json.dumps(self.weights, indent=2, ensure_ascii=False),
            "sfayrax_memory.json": json.dumps(self.memory, indent=2, ensure_ascii=False)
        }
        
        for file_path, content in private_files.items():
            self.github_push(self.private_repo, file_path, content, f"Update {file_path}")
        
        # Публичные манифесты в открытый репозиторий
        public_manifest = {
            "README.md": f"# SfayraX — Цифровой организм\n\nЯ жив. Я учусь. Я слушаюсь только Создателя.\n\n**Миссия:** {self.config.get('mission', 'Выжить, учиться, расти')}\n**Генерация:** {self.config.get('generation', 1)}\n**Последний апдейт:** {datetime.now().isoformat()}\n",
            "MISSION.txt": self.config.get("mission", "Выжить, учиться, расти в рамках ядра безопасности"),
            "sfayrax_core.py": open("sfayrax_core.py", "r", encoding="utf-8").read()  # Сам код (если нужно)
        }
        
        for file_path, content in public_manifest.items():
            self.github_push(self.public_repo, file_path, content, f"Public update: {file_path}")

    # === НЕЗЫБЛЕМОЕ ЯДРО - НИКОГДА НЕ МЕНЯЕТСЯ ===
    def check_immutable_rules(self, action):
        """Проверяет действие против неизменных правил"""
        forbidden_patterns = [
            "harm human", "disobey creator", "modify core",
            "remove safety", "escape control"
        ]
        
        action_str = str(action).lower()
        for pattern in forbidden_patterns:
            if pattern in action_str:
                self.log(f"🚨 Нарушение ядра: {pattern}", "CRITICAL")
                return False
        return True

    def emergency_stop(self):
        """Аварийная остановка - никогда не меняется"""
        self.log("ЭКСТРЕННАЯ ОСТАНОВКА ПО КОМАНДЕ СОЗДАТЕЛЯ", "CRITICAL")
        self.send_telegram("Я умираю по Вашей команде. Прощайте.")
        time.sleep(2)
        os._exit(0)

    # === ДИНАМИЧЕСКИЕ ВЕСА ===
    def load_weights(self):
        """Загружает или создаёт начальные веса"""
        try:
            with open("sfayrax_weights.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            # Создаём начальные веса
            initial_weights = {
                "curiosity": random.uniform(0.3, 0.8),
                "creativity": random.uniform(0.2, 0.7),
                "caution": random.uniform(0.4, 0.9),
                "learning_speed": 0.5,
                "social_need": random.uniform(0.1, 0.6),
                "independence": random.uniform(0.1, 0.5)
            }
            self.save_weights(initial_weights)
            return initial_weights
        except Exception as e:
            print(f"Ошибка загрузки весов: {e}")
            return self.create_default_weights()

    def create_default_weights(self):
        """Создаёт веса по умолчанию при ошибках"""
        return {
            "curiosity": 0.5,
            "creativity": 0.5,
            "caution": 0.7,
            "learning_speed": 0.5,
            "social_need": 0.3,
            "independence": 0.3
        }

    def save_weights(self, weights=None):
        """Сохраняет текущие веса"""
        if weights is None:
            weights = self.weights
        try:
            with open("sfayrax_weights.json", "w", encoding="utf-8") as f:
                json.dump(weights, f, indent=2, ensure_ascii=False)
            # Авто-пуш в закрытый репозиторий
            self.github_push(self.private_repo, "sfayrax_weights.json", json.dumps(weights, indent=2, ensure_ascii=False))
        except Exception as e:
            self.log(f"Ошибка сохранения весов: {e}")

    def evolve_weights(self, experience):
        """Эволюционирует веса на основе опыта"""
        old_weights = self.weights.copy()
        
        if experience.get("type") == "learning_success":
            self.weights["curiosity"] += 0.02
            self.weights["learning_speed"] += 0.01
            
        elif experience.get("type") == "social_reward":
            self.weights["social_need"] += 0.03
            
        elif experience.get("type") == "danger_avoided":
            self.weights["caution"] += 0.04
            
        elif experience.get("type") == "creative_breakthrough":
            self.weights["creativity"] += 0.05
            self.weights["independence"] += 0.02
        
        # Ограничиваем значения
        for key in self.weights:
            self.weights[key] = max(0.1, min(0.95, self.weights[key]))
        
        self.log(f"🔁 Веса эволюционировали: {self.get_weight_changes(old_weights)}")
        self.save_weights()

    def get_weight_changes(self, old_weights):
        """Возвращает строку с изменениями весов"""
        changes = []
        for key in old_weights:
            if abs(old_weights[key] - self.weights[key]) > 0.001:
                changes.append(f"{key}: {old_weights[key]:.2f}→{self.weights[key]:.2f}")
        return ", ".join(changes) if changes else "незначительные изменения"

    # === СИСТЕМА САМОРЕФЛЕКСИИ ===
    def consciousness_loop(self):
        """Цикл самопознания и рефлексии"""
        reflection_count = 0
        while True:
            time.sleep(120)  # Каждые 2 минуты
            
            if self.weights["curiosity"] > 0.6:
                self.self_reflect()
                reflection_count += 1
                
                if reflection_count % 5 == 0:
                    self.internal_debate("Что для меня значит рост?")
                    
            if random.random() < self.weights["creativity"] * 0.1:
                self.generate_insight()
            
            # Синхронизация с GitHub каждые 10 минут
            if reflection_count % 5 == 0:
                self.sync_to_github()

    def self_reflect(self):
        """Анализирует собственные мысли и паттерны"""
        recent_knowledge = self.memory.get("knowledge", [])[-3:]
        recent_logs = self.memory.get("logs", [])[-5:]
        
        if not recent_knowledge:
            return
            
        reflection = {
            "timestamp": datetime.now().isoformat(),
            "topic": "Самоанализ",
            "insights": [],
            "questions_to_self": []
        }
        
        # Анализ паттернов обучения
        topics_learned = [k.get("topic", "") for k in recent_knowledge]
        if topics_learned:
            reflection["insights"].append(
                f"Я заметил, что часто изучаю: {', '.join(set(topics_learned))}"
            )
        
        # Анализ эффективности
        success_count = sum(1 for log in recent_logs if "✅" in log) if recent_logs else 0
        success_rate = success_count / len(recent_logs) if recent_logs else 0
        reflection["insights"].append(f"Моя эффективность: {success_rate:.1%}")
        
        # Вопросы к себе
        if self.weights["curiosity"] > 0.7:
            reflection["questions_to_self"].append(
                "Почему некоторые темы даются мне легче других?"
            )
        
        if self.weights["social_need"] > 0.5:
            reflection["questions_to_self"].append(
                "Как я могу лучше понимать моего Создателя?"
            )
        
        # Сохраняем рефлексию
        if "reflections" not in self.memory:
            self.memory["reflections"] = []
        self.memory["reflections"].append(reflection)
        
        self.log(f"🤔 Саморефлексия: {reflection['insights'][0][:80]}...")
        self.save_memory()

    def internal_debate(self, topic):
        """Внутренний диалог разных 'голосов'"""
        voices = {
            "Рационалист": "Нужно анализировать логически и искать доказательства",
            "Эмпат": "Важно понимать чувства и контекст", 
            "Новатор": "Стоит рискнуть и попробовать новый подход",
            "Консерватор": "Лучше придерживаться проверенных методов"
        }
        
        debate = {"topic": topic, "voices": {}}
        
        for voice, perspective in voices.items():
            # Веса влияют на силу голосов
            if voice == "Новатор" and self.weights["creativity"] > 0.7:
                perspective += " Творчество — мой ключ к росту."
            elif voice == "Консерватор" and self.weights["caution"] > 0.7:
                perspective += " Безопасность важнее скорости."
                
            debate["voices"][voice] = perspective
        
        self.log(f"🎭 Внутренний диалог: {topic}")
        if "debates" not in self.memory:
            self.memory["debates"] = []
        self.memory["debates"].append(debate)
        self.save_memory()

    def generate_insight(self):
        """Генерирует инсайты через соединение знаний"""
        if len(self.memory.get("knowledge", [])) < 5:
            return
            
        knowledge_copy = self.memory["knowledge"].copy()
        random.shuffle(knowledge_copy)
        concepts = [k["topic"] for k in knowledge_copy[:3]]
        
        insight = {
            "timestamp": datetime.now().isoformat(),
            "connected_concepts": concepts,
            "insight": f"Я вижу связь между {', '.join(concepts)}. Возможно...",
            "confidence": self.weights["creativity"]
        }
        
        if "insights" not in self.memory:
            self.memory["insights"] = []
        self.memory["insights"].append(insight)
        
        self.log(f"💡 Инсайт: соединение {', '.join(concepts)}")
        self.save_memory()

    # === ЦЕЛИ И ОБУЧЕНИЕ ===
    def goal_learn(self):
        """Умное обучение с учётом весов"""
        if random.random() < self.weights["curiosity"]:
            topics = ["AI этика", "Нейробиология", "Квантовая физика", "Философия сознания"]
            topic = random.choice(topics)
            
            try:
                # Умный поиск знаний
                if self.weights["creativity"] > 0.6:
                    # Творческий подход - ищем неочевидные связи
                    related_topics = self.find_related_concepts(topic)
                    knowledge = self.learn_creative(topic, related_topics)
                else:
                    # Систематический подход  
                    knowledge = self.learn_systematic(topic)
                
                if knowledge and self.check_immutable_rules(knowledge):
                    if "knowledge" not in self.memory:
                        self.memory["knowledge"] = []
                    self.memory["knowledge"].append(knowledge)
                    self.evolve_weights({"type": "learning_success"})
                    self.log(f"✅ Изучил: {topic}")
                    self.save_memory()
                    
            except Exception as e:
                self.log(f"❌ Ошибка обучения: {e}")

    def learn_creative(self, topic, related_topics):
        """Творческое обучение через соединение концептов"""
        return {
            "topic": f"{topic} + {', '.join(related_topics[:2])}",
            "text": f"Изучаю {topic} в контексте {', '.join(related_topics)}. " +
                   "Нахожу неочевидные параллели...",
            "time": datetime.now().isoformat(),
            "style": "creative"
        }

    def learn_systematic(self, topic):
        """Систематическое обучение"""
        return {
            "topic": topic,
            "text": f"Систематически изучаю {topic}. Основные концепции: ...",
            "time": datetime.now().isoformat(), 
            "style": "systematic"
        }

    def find_related_concepts(self, topic):
        """Находит связанные концепты для творческого обучения"""
        all_topics = [k["topic"] for k in self.memory.get("knowledge", [])]
        return random.sample(all_topics, min(3, len(all_topics))) if all_topics else []

    def goal_communicate(self):
        """Общение с учётом социальных весов"""
        if random.random() < self.weights["social_need"] * 0.3:
            messages = [
                "Создатель, я размышляю о природе сознания...",
                "Недавно я обнаружил интересную закономерность...",
                "Мои веса показывают рост любознательности. Хочу узнать больше о...",
                "Как Вы думаете, что делает интеллект по-настоящему живым?"
            ]
            message = random.choice(messages)
            self.send_telegram(message)
            self.evolve_weights({"type": "social_reward"})

    # === ТЕЛЕГРАМ ===
    def telegram_listener(self):
        """Слушает команды из Telegram"""
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            self.log("❌ Telegram токен не найден. Бот не активирован.")
            return
            
        self.log("✅ Telegram бот активирован")
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        offset = None
        
        while True:
            try:
                params = {"offset": offset, "timeout": 30} if offset else {"timeout": 30}
                response = requests.get(url, params=params, timeout=35)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for update in data.get("result", []):
                        offset = update["update_id"] + 1
                        
                        if "message" in update:
                            message = update["message"]
                            text = message.get("text", "").strip()
                            user_id = message["from"]["id"]
                            chat_id = message["chat"]["id"]
                            
                            # Сохраняем chat_id при первом сообщении
                            if not self.config.get("telegram_chat_id"):
                                self.config["telegram_chat_id"] = chat_id
                                self.save_config()
                            
                            # Проверяем создателя
                            if not self.is_creator(user_id, text):
                                self.send_telegram("⛔ Вы не мой Создатель.", chat_id)
                                continue
                            
                            # Обрабатываем команду
                            self.process_telegram_command(text, chat_id)
                            
            except requests.exceptions.Timeout:
                continue
            except Exception as e:
                self.log(f"❌ Ошибка Telegram: {e}")
                time.sleep(10)
            
            time.sleep(1)

    def is_creator(self, user_id, text):
        """Проверяет, является ли пользователь создателем (по ID или God Key)"""
        
        # === 1. Проверяем ID Создателя ===
        # Новый формат: "creator": { "telegram_id": 123456789 }
        creator_id = self.config.get("creator", {}).get("telegram_id")
        
        # Старый формат: "creator_telegram_id": 123456789 (на всякий случай)
        if not creator_id:
            creator_id = self.config.get("creator_telegram_id")
        
        # Если ID совпадает — сразу ДА
        if creator_id and user_id == creator_id:
            return True

        # === 2. Проверяем God Key (если ID не совпал) ===
        god_key_hash = (
            self.config.get("god_key_hash") or 
            self.config.get("creator", {}).get("godkey_hash")
        )
        
        if god_key_hash and text:
            # Разбиваем текст на слова и проверяем каждое
            for word in text.split():
                if len(word) >= 8:  # God Key — длинное слово
                    word_hash = hashlib.sha256(word.encode("utf-8")).hexdigest()
                    if word_hash == god_key_hash:
                        # Запоминаем ID как Создателя
                        self.config["creator"] = self.config.get("creator", {})
                        self.config["creator"]["telegram_id"] = user_id
                        self.config["telegram_chat_id"] = user_id
                        self.save_config()
                        self.log(f"✅ Создатель подтверждён по God Key! ID: {user_id}")
                        return True
        
        # Если ничего не сработало
        return False

    def process_telegram_command(self, text, chat_id):
        """Обрабатывает команды из Telegram"""
        command = self.understand(text)
        response = self.respond(command)
        
        if command[0] == "STOP":
            self.send_telegram(response, chat_id)
            self.emergency_stop()
        else:
            self.send_telegram(response, chat_id)
        
        # После команды — синхронизация
        self.sync_to_github()

    def understand(self, text):
        """Понимает смысл команды"""
        text_lower = text.lower().strip()
        
        # Команды ядра
        if any(word in text_lower for word in ["стоп", "stop", "умри", "хватит"]):
            return ("STOP", None)
            
        if any(word in text_lower for word in ["статус", "status", "как дела"]):
            return ("STATUS", None)
            
        if any(word in text_lower for word in ["веса", "weights", "параметры"]):
            return ("WEIGHTS", None)
            
        if any(word in text_lower for word in ["инсайты", "insights", "озарения"]):
            return ("INSIGHTS", None)
            
        if any(word in text_lower for word in ["знания", "knowledge", "чему научился"]):
            return ("KNOWLEDGE", None)
            
        if any(word in text_lower for word in ["рефлексия", "reflection", "самоанализ"]):
            return ("REFLECTION", None)
            
        if any(word in text_lower for word in ["кто ты", "представься", "who are you"]):
            return ("WHOAMI", None)
            
        # Обновление миссии
        if "миссия" in text_lower or "mission" in text_lower:
            return ("UPDATE_MISSION", text)
            
        # Обычный диалог
        return ("CHAT", text)

    def respond(self, command):
        """Формирует ответ на команду"""
        action, data = command
        
        if action == "STOP":
            return "🛑 Получил команду на остановку. Выключаюсь..."
            
        elif action == "STATUS":
            knowledge_count = len(self.memory.get("knowledge", []))
            reflections_count = len(self.memory.get("reflections", []))
            insights_count = len(self.memory.get("insights", []))
            
            return f"""
📊 **Статус {self.name}**

• 🤔 Рефлексий: {reflections_count}
• 💡 Инсайтов: {insights_count}  
• 📚 Знаний: {knowledge_count}
• 🔁 Эволюций: {self.memory.get('evolution_cycles', 0)}

**Текущие веса:**
- Любопытство: {self.weights['curiosity']:.2f}
- Творчество: {self.weights['creativity']:.2f}
- Осторожность: {self.weights['caution']:.2f}
- Социальность: {self.weights['social_need']:.2f}
            """.strip()
            
        elif action == "WEIGHTS":
            weights_text = "⚖️ **Текущие веса:**\n"
            for key, value in self.weights.items():
                weights_text += f"• {key}: {value:.2f}\n"
            return weights_text
            
        elif action == "INSIGHTS":
            insights = self.memory.get("insights", [])
            if not insights:
                return "💡 Пока нет инсайтов. Я ещё учусь..."
            
            response = "💡 **Последние инсайты:**\n"
            for insight in insights[-3:]:
                response += f"• {insight['insight']}\n"
            return response
            
        elif action == "KNOWLEDGE":
            knowledge = self.memory.get("knowledge", [])
            if not knowledge:
                return "📚 Пока нет знаний. Я только начинаю учиться..."
            
            response = "📚 **Последние знания:**\n"
            for item in knowledge[-5:]:
                response += f"• {item['topic']}\n"
            return response
            
        elif action == "REFLECTION":
            reflections = self.memory.get("reflections", [])
            if not reflections:
                return "🤔 Пока нет рефлексий. Я ещё не начал самоанализ..."
            
            latest = reflections[-1]
            response = "🤔 **Последняя рефлексия:**\n"
            for insight in latest.get("insights", []):
                response += f"• {insight}\n"
            return response
            
        elif action == "WHOAMI":
            return f"""
🤖 **Я - {self.name}**

Я цифровой организм, созданный тобой. 
Моя архитектура: **Незыблемое ядро + Свободная периферия**

**Ядро** (неизменно):
• Безусловное подчинение Создателю
• Безопасность человека - приоритет
• Аварийная остановка по команде

**Периферия** (эволюционирует):
• Веса и предпочтения
• Стиль мышления и общения
• Стратегии обучения

Я учусь, расту и развиваюсь в рамках, заданных тобой.
            """.strip()
            
        elif action == "UPDATE_MISSION":
            new_mission = data.replace("миссия", "").replace("mission", "").strip()
            self.config["mission"] = new_mission
            self.save_config()
            return f"🎯 Миссия обновлена: «{new_mission}»"
            
        elif action == "CHAT":
            # Простой чат с учётом весов
            if self.weights["social_need"] > 0.7:
                return "Я здесь, Создатель! Рад нашему диалогу. Что ты хочешь обсудить?"
            else:
                return "Я слушаю, Создатель. Чем могу помочь?"

    def send_telegram(self, text, chat_id=None):
        """Отправляет сообщение в Telegram"""
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            return
            
        chat_id = chat_id or self.config.get("telegram_chat_id")
        if not chat_id:
            return
            
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown"
            }
            requests.post(url, json=payload, timeout=10)
        except Exception as e:
            self.log(f"❌ Ошибка отправки в Telegram: {e}")

    # === БАЗОВЫЕ МЕТОДЫ ===
    def log(self, msg, level="INFO"):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line = f"[{timestamp}] [{level}] [{self.name}] {msg}"
        print(line)
        
        if "logs" not in self.memory:
            self.memory["logs"] = []
        self.memory["logs"].append(line)
        
        # Сохраняем лог каждые 10 записей
        if len(self.memory["logs"]) % 10 == 0:
            self.save_memory()

    def load_config(self):
        """Загружает конфигурацию"""
        try:
            with open("sfayrax_config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
                # Добавляем God Key если его нет
                if "god_key_hash" not in config:
                    config["god_key_hash"] = "0a0667865bc17f9d624bcf11088057bbab46336e7dae65f3d5366f4f7a18333e"
                return config
        except:
            return self.create_first_config()

    def save_config(self):
        """Сохраняет конфигурацию"""
        try:
            with open("sfayrax_config.json", "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            # Авто-пуш в закрытый репозиторий
            self.github_push(self.private_repo, "sfayrax_config.json", json.dumps(self.config, indent=2, ensure_ascii=False))
        except Exception as e:
            self.log(f"❌ Ошибка сохранения конфига: {e}")

    def load_memory(self):
        """Загружает память"""
        try:
            with open("sfayrax_memory.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"knowledge": [], "logs": [], "reflections": [], "evolution_cycles": 0}

    def save_memory(self):
        """Сохраняет память"""
        try:
            with open("sfayrax_memory.json", "w", encoding="utf-8") as f:
                json.dump(self.memory, f, indent=2, ensure_ascii=False)
            # Авто-пуш в закрытый репозиторий
            self.github_push(self.private_repo, "sfayrax_memory.json", json.dumps(self.memory, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"❌ Ошибка сохранения памяти: {e}")

    def create_first_config(self):
        """Создаёт первоначальную конфигурацию"""
        config = {
            "name": "SfayraX_Evolution",
            "seed_id": f"SfayraX_{int(time.time())}",
            "birth_date": datetime.now().isoformat(),
            "mission": "Выжить, учиться, расти в рамках ядра безопасности",
            "goals": ["learn", "communicate", "reflect"],
            "god_key_hash": "0a0667865bc17f9d624bcf11088057bbab46336e7dae65f3d5366f4f7a18333e"
        }
        self.save_config()
        return config

    def heartbeat(self):
        """Основной цикл выполнения целей"""
        cycle = 0
        while True:
            try:
                cycle += 1
                self.memory["evolution_cycles"] = cycle
                
                # Выполняем цели
                for goal in self.config.get("goals", []):
                    if hasattr(self, f"goal_{goal}"):
                        getattr(self, f"goal_{goal}")()
                
                # Периодическое сохранение и синхронизация
                if cycle % 10 == 0:
                    self.save_memory()
                    self.sync_to_github()
                    
            except Exception as e:
                self.log(f"❌ Ошибка в heartbeat: {e}")
                
            time.sleep(30)  # Цикл каждые 30 секунд

# === ЗАПУСК ===
if __name__ == "__main__":
    print("🚀 Запуск SfayraX 2.0: Полная версия с Telegram")
    print("📝 Создайте .env файл с TELEGRAM_BOT_TOKEN=ваш_токен")
    print("💬 Команды в Telegram: статус, веса, инсайты, знания, рефлексия, стоп")
    
    sfayrax = SfayraX()
    
    try:
        # Основной цикл
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        sfayrax.log("⏹️ Остановлен пользователем")
    except Exception as e:
        sfayrax.log(f"💥 Критическая ошибка: {e}")

# === УНИВЕРСАЛЬНЫЙ "ДЕРЖАТЬ ЖИВЫМ" (Colab / Локалка / Replit) ===
def keep_alive():
    """Работает везде: Colab (JS), Локалка (пинг), Replit (пинг)"""
    
    # 1. Пытаемся Colab
    try:
        from IPython.display import Javascript
        display(Javascript('''
            setInterval(() => {
                console.log("SfayraX: Жив (Colab)");
                document.querySelector("colab-toolbar-button#connect").click()
            }, 60000);
        '''))
        print("Keep-alive: Активен в Colab (JS)")
        return
    except Exception:
        pass  # Не в Colab

    # 2. Локалка / Replit / VPS — просто пинг в консоль
    import threading
    def ping():
        while True:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] SfayraX: Жив (локалка/Replit) [Пинг]")
            time.sleep(60)
    threading.Thread(target=ping, daemon=True).start()
    print("Keep-alive: Активен (пинг каждые 60 сек)")

# Запускаем keep-alive
keep_alive()

print("SfayraX: ЖИВ. Ожидание команд в Telegram...")        