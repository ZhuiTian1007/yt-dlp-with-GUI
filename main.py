import tkinter as tk
import tkinter.messagebox
import subprocess
import threading
import os

# 基本設定
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# BASE_SETTINGS = ["--output 'D:\Videos\%(title)s.%(ext)s'", ]

# yt-dlp設定選項
YTDLP_OPTIONS = {
    "儲存影片縮圖": "--embed-thumbnail",
    "儲存影片資訊 (Metadata)": "--add-metadata",
    "轉碼成MP4": "--merge-output-format mp4",
    "以H.264編碼": "-S vcodec:h264",
}


def download():

    URL = URLvar.get().strip()
    if not URL:
        tk.messagebox.showerror("錯誤", "請輸入YouTube網址！")
        return

    yt_dlp_path = os.path.join(BASE_DIR, "yt-dlp_win", "yt-dlp.exe")
    ffmpeg_path = os.path.join(
        BASE_DIR, "ffmpeg-master-latest-win64-gpl-shared", "bin", "ffmpeg.exe"
    )
    cmd = [
        yt_dlp_path,
        "--ffmpeg-location",
        ffmpeg_path,
    ]

    for label_text, var in options_vars.items():
        if var.get():
            cmd.extend(YTDLP_OPTIONS[label_text].split())

    cmd.append(URL)
    print("執行指令：", " ".join(cmd))  # 偵錯用

    def run_download():

        try:
            download_button.config(state=tk.DISABLED, text="下載中...")
            result = subprocess.run(cmd, check=True, text=True)

        except subprocess.CalledProcessError as e:
            tk.messagebox.showerror("錯誤", f"下載失敗：{e}")

        except Exception as e:
            tk.messagebox.showerror("錯誤", f"發生意外錯誤：{e}")

        else:
            tk.messagebox.showinfo("完成", "下載完成！")

        finally:
            download_button.config(state=tk.NORMAL, text="下載")

    download_thread = threading.Thread(target=run_download)
    download_thread.start()


# 主視窗
win = tk.Tk()
win.geometry("")
win.title("yt-dlp GUI")

# YouTube網址輸入
URLLabel = tk.Label(win, text="請輸入你要下載的YouTube影片網址：")
URLLabel.pack(padx=20, pady=5)

URLvar = tk.StringVar()
URLentry = tk.Entry(win, width=50, textvariable=URLvar)
URLentry.pack(padx=20)

# 排版空行
tk.Label(win, text="").pack()

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
