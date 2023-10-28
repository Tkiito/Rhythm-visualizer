import os
import threading
import time
import pygame
from pygame.locals import *

# Pygameの初期化
pygame.init()

# ウィンドウの幅と高さ
window_width = 400
window_height = 200

# ウィンドウの作成
window = pygame.display.set_mode((window_width, window_height))

# メトロノームの初期設定
bpm = 60
count = 1
max_count = 4
background_color = (255, 0, 0)  # 赤色 (R, G, B)
reset_pressed = False
running = False
thread = None
hihat = False

# 音声ファイルの読み込み
current_path = os.getcwd()
Soundtakt = pygame.mixer.Sound(
    os.path.join(current_path, "Rhythm visualizer/Sounds/Takt.wav")
)
Soundtin = pygame.mixer.Sound(
    os.path.join(current_path, "Rhythm visualizer/Sounds/Tin.wav")
)
Soundhihat = pygame.mixer.Sound(
    os.path.join(current_path, "Rhythm visualizer/Sounds/Hihat.wav")
)

# Pygameのクロック
clock = pygame.time.Clock()


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
    label_text = font.render(str(count), True, (255, 255, 255))
    label_rect = label_text.get_rect(center=(window_width - 50, window_height // 2))
    window.blit(label_text, label_rect)
    pygame.display.flip()
    global thread
    if thread is None or not thread.is_alive():
        thread = threading.Thread(target=metronome_thread)
        thread.start()


def hihat_switch():
    global hihat
    hihat = not hihat


def reset_metronome():
    global running
    global count
    reset_pressed = True
    running = False
    count = 1
    label_text = font.render(str(count), True, (255, 255, 255))
    label_rect = label_text.get_rect(center=(window_width - 50, window_height // 2))
    window.blit(label_text, label_rect)


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
            change_background_color()
        label_text = font.render(str(count), True, (255, 255, 255))
        label_rect = label_text.get_rect(center=(window_width - 50, window_height // 2))
        window.blit(label_text, label_rect)
        if count == 1:
            Soundtin.play()
        else:
            Soundtakt.play()
        if hihat:
            Soundhihat.play()
        time.sleep(60 / bpm / 2)
        if hihat:
            Soundhihat.play()
        time.sleep(60 / bpm / 2)
        pygame.display.flip()


def change_background_color():
    global background_color
    if background_color == (255, 0, 0):
        background_color = (0, 255, 0)  # 緑色 (R, G, B)
    else:
        background_color = (255, 0, 0)  # 赤色 (R, G, B)
    window.fill(background_color)
    pygame.display.flip()


# フォントとテキスト
font = pygame.font.Font(None, 36)
label_text = font.render(str(count), True, (255, 255, 255))
label_rect = label_text.get_rect(center=(window_width - 50, window_height // 2))
window.blit(label_text, label_rect)

# メトロノームの表示用ラベル
label = pygame.font.Font(None, 36).render(str(count), True, (255, 255, 255))
label_rect = label.get_rect(center=(window_width - 50, window_height // 2))
window.blit(label, label_rect)

# ハイハットのトグルスイッチ
hihat_button = pygame.Rect(20, 110, 50, 30)

# Countの入力欄
count_entry = pygame.Rect(120, 30, 50, 30)

# BPMの入力欄
bpm_entry = pygame.Rect(120, 80, 50, 30)

# メインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if hihat_button.collidepoint(event.pos):
                hihat_switch()
        elif event.type == KEYDOWN:
            if event.key == K_s:
                start_metronome()
            elif event.key == K_r:
                reset_metronome()
            elif event.key == K_UP:
                change_count()
            elif event.key == K_DOWN:
                change_bpm()

    clock.tick(bpm)
    pygame.display.flip()

pygame.quit()
