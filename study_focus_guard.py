"""
Study Focus Guard (Bảo Vệ Sự Tập Trung Học Tập)
================================================
1. Khi bắt đầu: quét tất cả cửa sổ đang mở (tab trình duyệt sẽ hiện ra dưới
   dạng tiêu đề cửa sổ) và kiểm tra chúng theo các từ khóa BẠN định nghĩa là
   "tài liệu học tập". Bạn xác nhận/dọn dẹp trước khi phiên học bắt đầu.
2. Trong lúc chạy: liên tục kiểm tra xem có cửa sổ/tab MỚI nào không khớp
   với từ khóa học tập của bạn hay không, thử đóng nó lại, và hiện thông báo
   "Bạn phải tập trung!". Quên chưa thêm vào danh sách? Gõ 'add' để thêm
   tab/cửa sổ vừa bị chặn vào danh sách cho phép.
3. Để dừng: gõ `stop` (rồi nhấn Enter) trong console bất cứ lúc nào.

Cài đặt:
    pip install pygetwindow

Chạy:
    python study_focus_guard.py

Lưu ý:
- Tính năng tự động đóng cửa sổ chỉ được hỗ trợ trên Windows (do giới hạn
  của thư viện pygetwindow). Trên macOS/Linux, chương trình vẫn sẽ phát
  hiện và cảnh báo bạn, chỉ là không thể tự đóng cửa sổ giúp bạn.
- Việc nhận diện tab trình duyệt dựa vào tiêu đề cửa sổ trùng với tiêu đề
  của tab đang được chọn (cách hoạt động bình thường của Chrome/Edge/
  Firefox). Các tab chạy nền không được chọn sẽ không hiển thị riêng lẻ.
"""

import sys
import threading

try:
    import pygetwindow as gw
except ImportError:
    print("Thiếu thư viện cần thiết. Cài đặt bằng lệnh:\n    pip install pygetwindow")
    sys.exit(1)

import tkinter as tk

try:
    import winsound
    IS_WINDOWS = True
except ImportError:
    IS_WINDOWS = False

POLL_INTERVAL_MS = 1500
POPUP_TITLE_PREFIX = "Focus Guard"


def get_titles():
    """Trả về tất cả tiêu đề cửa sổ hiện tại (không rỗng)."""
    return [t for t in gw.getAllTitles() if t.strip()]


def matches_whitelist(title, whitelist_snapshot):
    low = title.lower()
    return any(keyword in low for keyword in whitelist_snapshot)


def try_close_window(title):
    """Thử đóng cửa sổ theo tiêu đề. Trả về True nếu đóng thành công."""
    try:
        windows = gw.getWindowsWithTitle(title)
        for w in windows:
            w.close()
        return True
    except Exception:
        return False


def show_focus_popup(root, offending_title, could_close):
    popup = tk.Toplevel(root)
    popup.title(f"{POPUP_TITLE_PREFIX} - Tập trung nào")
    popup.attributes("-topmost", True)
    popup.geometry("420x220+500+300")
    popup.configure(bg="#b00020")

    msg = "Bạn phải tập trung!"
    detail = f'Đã đóng: "{offending_title}"' if could_close else \
              f'Đã phát hiện (không thể tự đóng): "{offending_title}"'

    tk.Label(popup, text=msg, font=("Segoe UI", 22, "bold"),
              fg="white", bg="#b00020").pack(pady=(30, 10))
    tk.Label(popup, text=detail, font=("Segoe UI", 10),
              fg="white", bg="#b00020", wraplength=380).pack(pady=(0, 10))
    tk.Label(popup, text='Đây là tài liệu học tập mà bạn quên thêm vào? Gõ "add" trong console.',
              font=("Segoe UI", 9, "italic"), fg="white", bg="#b00020",
              wraplength=380).pack(pady=(0, 10))
    tk.Button(popup, text="Quay lại học bài", command=popup.destroy,
               font=("Segoe UI", 11)).pack()

    if IS_WINDOWS:
        try:
            winsound.MessageBeep()
        except Exception:
            pass

    # Tự động đóng sau vài giây kể cả khi bạn phớt lờ nó
    popup.after(4000, popup.destroy)


def run_setup():
    print("=" * 60)
    print("STUDY FOCUS GUARD - Thiết lập")
    print("=" * 60)
    raw = input(
        "Nhập các từ khóa để nhận diện tiêu đề cửa sổ/tab là TÀI LIỆU HỌC TẬP,\n"
        "cách nhau bằng dấu phẩy (vd: 'python docs, coursera, chuong 3, notion'):\n> "
    )
    whitelist = [w.strip().lower() for w in raw.split(",") if w.strip()]

    while True:
        titles = get_titles()
        allowed, blocked = [], []
        for t in titles:
            (allowed if matches_whitelist(t, whitelist) else blocked).append(t)

        print("\nCác cửa sổ/tab đang mở:")
        for t in allowed:
            print(f"  [OK]        {t}")
        for t in blocked:
            print(f"  [BỊ CHẶN]   {t}")

        if not blocked:
            print("\nMọi thứ đang mở đều liên quan đến học tập. Sẵn sàng bắt đầu.")
            break

        choice = input(
            "\nHãy đóng các cửa sổ/tab [BỊ CHẶN] ở trên, rồi nhấn Enter để\n"
            "kiểm tra lại. (Hoặc gõ 'ignore' để bắt đầu luôn): "
        ).strip().lower()
        if choice == "ignore":
            break

    return whitelist, set(get_titles())


def main():
    whitelist, known_titles = run_setup()
    lock = threading.Lock()
    state = {"last_flagged": None}

    print("\nPhiên học bắt đầu. Bất kỳ cửa sổ/tab mới nào mở ra mà không nằm")
    print("trong danh sách từ khóa học tập của bạn sẽ bị đóng và cảnh báo.")
    print("Các lệnh (gõ rồi nhấn Enter):")
    print("  add   -> thêm tab/cửa sổ vừa bị chặn vào danh sách cho phép (nếu bạn quên)")
    print("  stop  -> kết thúc phiên học\n")

    stop_event = threading.Event()

    def listen_for_commands():
        while True:
            cmd = input().strip()
            lc = cmd.lower()

            if lc == "stop":
                stop_event.set()
                break

            elif lc == "add":
                with lock:
                    target = state["last_flagged"]
                if target is None:
                    print("Chưa có cửa sổ/tab nào bị chặn.")
                    continue
                print(f'Vừa bị chặn: "{target}"')
                kw = input(
                    "Nhập từ khóa để thêm vào danh sách cho phép (nhấn Enter để dùng cả tiêu đề): "
                ).strip().lower()
                if not kw:
                    kw = target.lower()
                with lock:
                    whitelist.append(kw)
                    known_titles.add(target)
                print(f'Đã thêm "{kw}" vào danh sách từ khóa học tập. '
                      f'Hãy mở lại tab nếu nó đã bị đóng.')

            else:
                print("Lệnh không hợp lệ. Gõ 'add' hoặc 'stop'.")

    listener = threading.Thread(target=listen_for_commands, daemon=True)
    listener.start()

    root = tk.Tk()
    root.withdraw()  # ẩn cửa sổ gốc

    def poll():
        if stop_event.is_set():
            root.destroy()
            return

        current = get_titles()
        with lock:
            whitelist_snapshot = list(whitelist)

        for title in current:
            if title.startswith(POPUP_TITLE_PREFIX):
                continue  # bỏ qua thông báo của chính chương trình
            if title in known_titles:
                continue  # đã được xử lý trước đó
            if matches_whitelist(title, whitelist_snapshot):
                known_titles.add(title)
                continue

            # Phát hiện cửa sổ/tab mới, không phải tài liệu học tập
            closed = try_close_window(title)
            with lock:
                state["last_flagged"] = title
            show_focus_popup(root, title, closed)
            if not closed:
                # không thể tự đóng trên hệ điều hành này; ghi nhớ để
                # không hiện thông báo lặp lại mỗi vòng kiểm tra
                known_titles.add(title)

        root.after(POLL_INTERVAL_MS, poll)

    root.after(POLL_INTERVAL_MS, poll)
    root.mainloop()

    print("\nPhiên học đã kết thúc. Làm tốt lắm!")


if __name__ == "__main__":
    main()
