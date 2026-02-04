import tkinter as tk
import random
import time

# --- Настройки ---
WIDTH = 380   # под Samsung A02s (в портретном режиме)
HEIGHT = 650
CARD_SIZE = (60, 90)

root = tk.Tk()
root.title("Блэкджек 21")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.configure(bg="#004400")

# --- Карты и масти ---
suits = ["♤", "♡", "◇", "♧"]
values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

def card_value(card):
    val = card[:-1]
    if val in ["J", "Q", "K"]:
        return 10
    elif val == "A":
        return 11
    return int(val)

def adjust_for_aces(hand):
    total = sum(card_value(c) for c in hand)
    aces = [c for c in hand if c[:-1] == "A"]
    while total > 21 and aces:
        total -= 10
        aces.pop()
    return total

# --- UI ---
frame = tk.Frame(root, bg="#006600")
frame.pack(expand=True, fill="both")

info_label = tk.Label(frame, text="Добро пожаловать в 21 очко!", font=("Arial", 14, "bold"), bg="#006600", fg="white")
info_label.pack(pady=10)

canvas = tk.Canvas(frame, width=WIDTH, height=HEIGHT//2, bg="#228822", highlightthickness=0)
canvas.pack()

buttons_frame = tk.Frame(frame, bg="#004400")
buttons_frame.pack(pady=10)

player_label = tk.Label(frame, text="", font=("Arial", 14, "bold"), bg="#004400", fg="white")
dealer_label = tk.Label(frame, text="", font=("Arial", 14, "bold"), bg="#004400", fg="white")
player_label.pack(pady=5)
dealer_label.pack(pady=5)

# --- Игровая логика ---
deck = []
player = []
dealer = []
player_cards_ui = []
dealer_cards_ui = []

def new_deck():
    d = [v + s for s in suits for v in values]
    random.shuffle(d)
    return d

def draw_card_animation(card_text, x, y):
    """Анимация плавного выезда карты"""
    rect = canvas.create_rectangle(x, y-100, x+CARD_SIZE[0], y-10, fill="white", outline="black", width=2)
    text = canvas.create_text(x+CARD_SIZE[0]//2, y-55, text=card_text, font=("Arial", 16, "bold"), fill="black")
    for i in range(20):
        canvas.move(rect, 0, 5)
        canvas.move(text, 0, 5)
        canvas.update()
        time.sleep(0.02)
    return rect, text

def update_labels():
    player_total = adjust_for_aces(player)
    dealer_total = adjust_for_aces(dealer)
    player_label.config(text=f"Игрок: {player_total}")
    dealer_label.config(text=f"Дилер: {dealer_total if game_over else '??'}")

def deal_initial():
    global deck, player, dealer, player_cards_ui, dealer_cards_ui, game_over
    canvas.delete("all")
    player, dealer = [], []
    player_cards_ui, dealer_cards_ui = [], []
    deck = new_deck()
    game_over = False
    info_label.config(text="Новая игра началась!")
    # Раздача
    for _ in range(2):
        player.append(deck.pop())
        dealer.append(deck.pop())
    show_cards(animated=True)
    update_labels()

def show_cards(animated=False):
    canvas.delete("all")
    spacing = 70
    # Игрок
    for i, card in enumerate(player):
        if animated:
            player_cards_ui.append(draw_card_animation(card, 60 + i*spacing, 350))
        else:
            canvas.create_rectangle(60 + i*spacing, 350, 60 + i*spacing + CARD_SIZE[0], 440, fill="white", outline="black", width=2)
            canvas.create_text(90 + i*spacing, 395, text=card, font=("Arial", 16, "bold"))
    # Дилер
    for i, card in enumerate(dealer):
        if not game_over and i == 0:
            canvas.create_rectangle(60 + i*spacing, 120, 60 + i*spacing + CARD_SIZE[0], 210, fill="gray")
        else:
            if animated:
                dealer_cards_ui.append(draw_card_animation(card, 60 + i*spacing, 120))
            else:
                canvas.create_rectangle(60 + i*spacing, 120, 60 + i*spacing + CARD_SIZE[0], 210, fill="white", outline="black", width=2)
                canvas.create_text(90 + i*spacing, 165, text=card, font=("Arial", 16, "bold"))

def hit():
    global game_over
    if game_over:
        return
    player.append(deck.pop())
    show_cards(animated=True)
    total = adjust_for_aces(player)
    update_labels()
    if total > 21:
        end_game("Перебор! Вы проиграли 😢")

def stand():
    global game_over
    if game_over:
        return
    while adjust_for_aces(dealer) < 17:
        dealer.append(deck.pop())
        show_cards(animated=True)
    update_labels()
    player_total = adjust_for_aces(player)
    dealer_total = adjust_for_aces(dealer)
    if dealer_total > 21 or player_total > dealer_total:
        end_game("Вы победили! 🎉")
    elif dealer_total == player_total:
        end_game("Ничья 🤝")
    else:
        end_game("Вы проиграли 😢")

def end_game(msg):
    global game_over
    game_over = True
    info_label.config(text=msg)
    show_cards(animated=False)
    update_labels()

# --- Кнопки управления ---
tk.Button(buttons_frame, text="Раздать", command=deal_initial, font=("Arial", 14, "bold"), width=8, bg="#00aa00", fg="white").grid(row=0, column=0, padx=5)
tk.Button(buttons_frame, text="Взять", command=hit, font=("Arial", 14, "bold"), width=8, bg="#ffaa00", fg="black").grid(row=0, column=1, padx=5)
tk.Button(buttons_frame, text="Хватит", command=stand, font=("Arial", 14, "bold"), width=8, bg="#aa0000", fg="white").grid(row=0, column=2, padx=5)

# --- Запуск ---
game_over = False
deal_initial()
root.mainloop()