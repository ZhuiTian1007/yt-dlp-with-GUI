import tkinter as tk
import tkinter.messagebox, tkinter.filedialog
import subprocess
import threading
import os

# 基本設定
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_SETTINGS = [
    "--force-ipv4",
    "--concurrent-fragments 8",
    "--part",
    "--continue",
    "--throttled-rate 200K",
    "--retries 10",
]

# yt-dlp設定選項
YTDLP_OPTIONS = {
    "儲存影片縮圖": "--embed-thumbnail",
    "儲存影片資訊 (Metadata)": "--add-metadata",
    "轉碼成MP4": "--merge-output-format mp4",
    "以H.264編碼": "-S vcodec:h264",
}


def download():

    URL = URL_var.get().strip()
    if not URL:
        tk.messagebox.showerror("錯誤", "請輸入YouTube網址！")
        return

    # 指定yt-dlp和ffmpeg的路徑
    yt_dlp_path = os.path.join(BASE_DIR, "yt-dlp_win", "yt-dlp.exe")
    ffmpeg_path = os.path.join(
        BASE_DIR, "ffmpeg-master-latest-win64-gpl-shared", "bin", "ffmpeg.exe"
    )

    # 最終執行指令
    cmd = [
        yt_dlp_path,
        "--ffmpeg-location",
        ffmpeg_path,
    ]

    for label_text, var in options_vars.items():
        if var.get():
            cmd.extend(YTDLP_OPTIONS[label_text].split())

    if download_location_var.get():
        cmd.extend(
            ["--output", os.path.join(download_location_var.get(), "%(title)s.%(ext)s")]
        )

    else:
        cmd.extend(["--output", os.path.join(BASE_DIR, "%(title)s.%(ext)s")])

    cmd.append(URL)

    print("執行指令：", " ".join(cmd))  # 偵錯用

    # 開始下載
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


# 瀏覽下載位置
def browse_location():
    download_location = tk.filedialog.askdirectory()
    download_location_var.set(download_location)


# 主視窗
win = tk.Tk()
win.geometry("")
win.title("yt-dlp GUI")

# YouTube網址輸入
URL_label = tk.Label(win, text="請輸入你要下載的YouTube影片網址：")
URL_label.pack(anchor="w", padx=20, pady=5)

URL_var = tk.StringVar()
URL_entry = tk.Entry(win, width=50, textvariable=URL_var)
URL_entry.pack(anchor="w", padx=20)

# 排版空行
tk.Label(win, text="").pack()

# checkbox
options_vars = {}

for label_text, ytdlp_command in YTDLP_OPTIONS.items():
    var = tk.BooleanVar()
    checkbox = tk.Checkbutton(win, text=label_text, variable=var)
    checkbox.pack(anchor="w", padx=20, pady=2)
    options_vars[label_text] = var

# 排版空行
tk.Label(win, text="").pack()

# 瀏覽下載檔案位址

download_location_label = tk.Label(win, text="下載檔案將儲存在：")
download_location_label.pack(anchor="w", padx=20)

download_location_var = tk.StringVar()
download_location_entry = tk.Entry(win, width=50, textvariable=download_location_var)
download_location_entry.pack(anchor="w", padx=20)

browse_location_button = tk.Button(win, text="瀏覽", command=browse_location)
browse_location_button.pack(anchor="w", padx=20, pady=5)

# 下載button
download_button = tk.Button(win, text="下載", command=download, width=10, height=2)
download_button.pack(pady=10)

win.mainloop()
