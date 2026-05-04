import tkinter as tk
import subprocess
import os
import threading


def download():
    return None


# 主視窗
win = tk.Tk()
win.geometry("")
win.title("yt-dlp GUI")

# YouTube網址輸入
URLLabel = tk.Label(win, text="請輸入你要下載的YouTube網址：")
URLLabel.pack(padx=20, pady=5)

URL = tk.StringVar()
URLentry = tk.Entry(win, width=50, textvariable=URL)
URLentry.pack(padx=20)

# 排版空行
tk.Label(win, text="").pack()

# yt-dlp設定選項
YTDLP_OPTIONS = {
    "儲存影片縮圖": "--embed-thumbnail",
    "儲存影片資訊 (Metadata)": "--add-metadata",
    "轉碼成MP4": "--merge-output-format mp4",
    "以H.264編碼": "-S vcodec:h264",
}

# checkbox
options_vars = {}

for label_text, ytdlp_command in YTDLP_OPTIONS.items():
    var = tk.BooleanVar()
    checkbox = tk.Checkbutton(win, text=label_text, variable=var)
    checkbox.pack(anchor="w", padx=20, pady=2)
    options_vars[label_text] = var

# 下載button
download_button = tk.Button(win, text="下載", command=download, width=10, height=2)
download_button.pack(pady=20)

win.mainloop()
