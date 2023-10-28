import tkinter as tk
import threading, os, time, pygame

# メトロノームの初期設定
bpm = 60
count = 1
max_count = 4
background_color = "red"  # 背景色を初期化
background2 = "lightblue"
reset_pressed = False
running = False
thread = None
hihat = False
currentpath = os.getcwd()
pygame.init()
pygame.mixer.init()
# Rhythm visualizerはアップロード前に消す
# Takt
Soundtakt = pygame.mixer.Sound(currentpath + "\Rhythm visualizer\Sounds\Takt.wav")
# Tin
Soundtin = pygame.mixer.Sound(currentpath + "\Rhythm visualizer\Sounds\Tin.wav")
# Hihat
Soundhihat = pygame.mixer.Sound(currentpath + "\Rhythm visualizer\Sounds\Hihat.wav")
# Kickdrum
Soundkick = pygame.mixer.Sound(currentpath + "\Rhythm visualizer\Sounds\Bassdrum.wav")
# Snaredrum
Soundsnare = pygame.mixer.Sound(currentpath + "\Rhythm visualizer\Sounds\Snaredrum.wav")


def start_metronome():
    global running
    global reset_pressed
    global count
    running = True
    if reset_pressed:
        reset_pressed = False
        count = 1
    else:
        if count == max_count:
            count = 1
            change_background_color()
    label.config(text=str(count))
    global thread
    if thread is None or not thread.is_alive():
        thread = threading.Thread(target=metronome_thread)
        thread.start()


def hihat_switch():
    global hihat
    if button_hihat.get():
        hihat = True
    else:
        hihat = False


def reset_metronome():
    global running
    global count
    reset_pressed = True
    running = False
    count = 1
    label.config(text=str(count))


def change_count():
    global max_count
    max_count = int(count_entry.get())


def change_bpm():
    global bpm
    bpm = int(bpm_entry.get())


def metronome_thread():
    while running:
        global count
        count += 1
        if count > max_count:
            count = 1
            change_background_color()  # 背景色を変更
        label.config(text=str(count))
        if count == 1:
            Soundtin.play()
        else:
            Soundtakt.play()
        if hihat == True:
            Soundhihat.play()
        time.sleep(60 / bpm / 2)
        if hihat == True:
            Soundhihat.play()
        time.sleep(60 / bpm / 2)


def change_background_color():
    global background_color
    if background_color == "red":
        background_color = "green"
    else:
        background_color = "red"
    right_frame.config(bg=background_color)
    label.config(bg=background_color)


# GUIウィンドウの作成
root = tk.Tk()
root.title("Metronome")
root.geometry("400x200")

# 左側のフレーム
left_frame = tk.Frame(root, width=200, height=200, bg=background2)
left_frame.pack(side="left", fill="both", expand=True)

# 右側のフレーム（半透明の赤色の背景）
right_frame = tk.Frame(root, bg=background_color, width=120, height=200)
right_frame.pack(side="right", fill="both", expand=True)

# StartボタンとResetボタン
start_button = tk.Button(left_frame, text="Start", command=start_metronome)
reset_button = tk.Button(left_frame, text="Reset", command=reset_metronome)
start_button.place(x=20, y=150)
reset_button.place(x=120, y=150)

# Countの入力フィールドとボタン
count_label = tk.Label(left_frame, text="Max Count:", bg=background2)
count_label.place(x=20, y=30)
count_entry = tk.Entry(left_frame, width=5, bg=background2)
count_entry.place(x=120, y=30)
count_entry.insert(0, str(max_count))
update_count_button = tk.Button(left_frame, text="Update", command=change_count)
update_count_button.place(x=160, y=25)

# BPMの入力フィールドとボタン
bpm_label = tk.Label(left_frame, text="BPM:", bg=background2)
bpm_label.place(x=20, y=80)
bpm_entry = tk.Entry(left_frame, width=5, bg=background2)
bpm_entry.place(x=120, y=80)
bpm_entry.insert(0, str(bpm))
update_bpm_button = tk.Button(left_frame, text="Update", command=change_bpm)
update_bpm_button.place(x=160, y=75)

# ハイハットのトグルスイッチ
button_hihat = tk.BooleanVar()
button_hihat.set(False)
switch_hihat = tk.Checkbutton(
    root, text="Hihat", variable=button_hihat, command=hihat_switch, bg=background2
)
switch_hihat.place(x=20, y=110)

# メトロノームの表示用ラベル
label = tk.Label(root, text=str(count), font=("Helvetica", 48), fg="white", bg="red")
label.place(x=300, y=60)

root.mainloop()
