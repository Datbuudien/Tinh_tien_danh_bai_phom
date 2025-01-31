import tkinter as tk
from tkinter import PhotoImage, Canvas, Button, Label, Frame
import configparser

key_map = {
    'nhi': 'Nhì',
    'ba': 'Ba',
    'bet': 'Bét',
    'chay': 'Cháy',
    'bi chan': 'Bị Chặn',
    'an chan': 'Ăn Chặn',
    'u den': 'Ù Đền',
    'u thuong': 'Ù Thường'
}

config = configparser.ConfigParser()
config.read('setting.ini', encoding='utf-8')

score_changes = {key_map.get(key, key): int(value) for key, value in config['ScoreChanges'].items()}
print(score_changes)
def load_scores():
    try:
        with open('scores.txt', 'r', encoding='utf-8') as file:
            for line in file:
                name, score = line.strip().split(": ")
                if name in scores:
                    scores[name].set(int(score))
    except FileNotFoundError:
        pass

def save_scores():
    with open('scores.txt', 'w', encoding='utf-8') as file:
        for name in player_names:
            file.write(f"{name}: {scores[name].get()}\n")
    print("Điểm đã được lưu vào file.")

root = tk.Tk()
root.title("Đánh bài ngày tết")
root.minsize(width=900, height=434)
root.resizable(width=False, height=False)

image_path = PhotoImage(file=r"GUI.png")
my_canvas = Canvas(root, width=900, height=434)
my_canvas.pack(fill="both", expand=True)
my_canvas.create_image(0, 0, image=image_path, anchor="nw")

main_frame = Frame(root, bg="white")
main_frame.place(relx=0.4, rely=0.5, anchor="center")

player_names = ["Lâm", "Tuấn", "Hùng", "Đạt"]
button_labels = ["Nhất", "Nhì", "Ba", "Bét", "Cháy", "Bị chặn", "Ăn chặn", "Ù đền", "Ù thường"]
# score_changes = {"Nhì": -5, "Ba": -10, "Bét": -15, "Cháy": -20, "Bị chặn": -5, "Ăn chặn": 5, "Ù đền": 60,
#                  "Ù thường": 45}

sub_frames = []

scores = {name: tk.IntVar(value=0) for name in player_names}
player_score_change = {name: 0 for name in player_names}

def update_score(player_index, action):
    player_name = player_names[player_index]

    if action == "Nhất":
        total_abs_penalty = sum(abs(player_score_change[p]) for p in player_names if p != player_name)
        scores[player_name].set(scores[player_name].get()+total_abs_penalty)
        for p in player_names:
            player_score_change[p]=0
    elif action== "Nhì" or action=="Ba" or action =="Bét" or action == "Cháy" :
        player_score_change[player_name] = score_changes[action]
        scores[player_name].set(scores[player_name].get() + score_changes[action])
    else:
        scores[player_name].set(scores[player_name].get()+ score_changes[action])
        minus_per_players=score_changes[action]//3
        for p in player_names:
            if p!=player_name:
                scores[p].set(scores[p].get()-minus_per_players)

for i in range(4):
    frame = Frame(main_frame, bg="lightgray", padx=10, pady=10, bd=2, relief="ridge")
    sub_frames.append(frame)

    label = Label(frame, text=player_names[i], font=("Arial", 10, "bold"), bg="lightgray")
    label.grid(row=0, column=0, columnspan=3, pady=5)

    for j, text in enumerate(button_labels):
        row, col = divmod(j, 3)
        btn = Button(frame, text=text, width=10, height=2, command=lambda p=i, a=text: update_score(p, a))
        btn.grid(row=row + 1, column=col, padx=2, pady=2)

sub_frames[0].grid(row=0, column=0, padx=10, pady=10)
sub_frames[1].grid(row=0, column=1, padx=10, pady=10)
sub_frames[2].grid(row=1, column=0, padx=10, pady=10)
sub_frames[3].grid(row=1, column=1, padx=10, pady=10)

load_scores()
score_frame = Frame(root, bg="white", bd=2, relief="ridge", padx=20, pady=20)
score_frame.place(relx=0.85, rely=0.5, anchor="center")

score_title = Label(score_frame, text="Điểm Số", font=("Arial", 12, "bold"), bg="white")
score_title.grid(row=0, column=0, columnspan=2, pady=10)

for i, name in enumerate(player_names):
    label = Label(score_frame, text=f"{name}:", font=("Arial", 10, "bold"), bg="white")
    label.grid(row=i + 1, column=0, sticky="w", padx=10, pady=5)

    score_label = Label(score_frame, textvariable=scores[name], font=("Arial", 10), bg="white")
    score_label.grid(row=i + 1, column=1, padx=10, pady=5)

save_button = Button(score_frame, text="Lưu điểm", font=("Arial", 10, "bold"), command=save_scores)
save_button.grid(row=5, column=0, columnspan=2, pady=20)

root.mainloop()
