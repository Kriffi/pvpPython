import tkinter as tk
from tkinter import scrolledtext
import random
import time
import threading


class Fighter:
    def __init__(self, name, level, health, damage):
        self.name = name
        self.level = level
        self.health = health * level
        self.damage = damage * level

    def attack(self, target):
        hit = random.randint(self.damage - 5, self.damage + 5)
        target.health -= hit
        return (
            f"{self.name} атакует {target.name} на {hit} урона! У {target.name} осталось {max(0, target.health)} здоровья.\n",
            hit,
            target.health,
        )


class BattleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Битва Орка и Мечника")
        self.root.geometry("500x400")

        tk.Label(root, text="Уровень Орка:").pack()
        self.ork_level = tk.IntVar(value=1)
        tk.Entry(root, textvariable=self.ork_level).pack()

        tk.Label(root, text="Уровень Мечника:").pack()
        self.barbarian_level = tk.IntVar(value=1)
        tk.Entry(root, textvariable=self.barbarian_level).pack()

        self.start_button = tk.Button(
            root, text="Начать бой", command=self.start_battle
        )
        self.start_button.pack(pady=10)

        self.text_area = scrolledtext.ScrolledText(root, height=15, width=50)
        self.text_area.pack()

        # Добавляем теги для цветов
        self.text_area.tag_config("damage", foreground="red")  # Урон - красный
        self.text_area.tag_config("health", foreground="green")  # Здоровье - зелёный

    def start_battle(self):
        ork = Fighter("Орк", self.ork_level.get(), health=100, damage=10)
        barbarian = Fighter("Мечник", self.barbarian_level.get(), health=50, damage=25)

        self.text_area.delete(1.0, tk.END)  # Очистка поля
        self.text_area.insert(tk.END, "🔥 Битва начинается! 🔥\n\n")

        def battle_loop():
            round_num = 1
            while ork.health > 0 and barbarian.health > 0:
                self.text_area.insert(tk.END, f"⚔️ Раунд {round_num}\n")

                # Атака мечника
                attack_text, hit, remaining_health = barbarian.attack(ork)
                self.insert_colored_text(attack_text, hit, remaining_health)

                if ork.health <= 0:
                    self.text_area.insert(tk.END, "✅ Мечник победил!\n")
                    break

                # Атака орка
                attack_text, hit, remaining_health = ork.attack(barbarian)
                self.insert_colored_text(attack_text, hit, remaining_health)

                if barbarian.health <= 0:
                    self.text_area.insert(tk.END, "❌ Орк победил!\n")
                    break

                round_num += 1
                time.sleep(1.5)
                self.text_area.see(tk.END)  # Прокрутка вниз

            self.text_area.insert(tk.END, "\n🏁 Бой окончен! 🏁")

        threading.Thread(
            target=battle_loop, daemon=True
        ).start()  # Запуск боя в отдельном потоке

    def insert_colored_text(self, text, damage_value, health_value):
        """Функция для вставки текста с цветными значениями урона и здоровья"""
        parts = text.split()
        for word in parts:
            if word.isdigit():
                if int(word) == damage_value:
                    self.text_area.insert(tk.END, word + " ", "damage")
                elif int(word) == health_value:
                    self.text_area.insert(tk.END, word + " ", "health")
                else:
                    self.text_area.insert(tk.END, word + " ")
            else:
                self.text_area.insert(tk.END, word + " ")
        self.text_area.insert(tk.END, "\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = BattleApp(root)
    root.mainloop()
