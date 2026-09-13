# Study Focus Guard

Một công cụ Python nhỏ giúp bạn tập trung học bài bằng cách kiểm tra các cửa sổ/tab trình duyệt đang mở, và tự động đóng bất kỳ thứ gì không liên quan đến việc học trong lúc bạn đang trong phiên tập trung.

## Cách hoạt động

1. **Khi bắt đầu** — quét tất cả cửa sổ/tab đang mở và so khớp với các từ khóa "tài liệu học tập" mà bạn tự định nghĩa. Bạn xác nhận hoặc dọn dẹp trước khi bắt đầu.
2. **Trong lúc chạy** — bất kỳ cửa sổ/tab mới nào không khớp từ khóa sẽ bị đóng (trên Windows) hoặc cảnh báo (trên macOS/Linux), kèm theo thông báo **"Bạn phải tập trung!"**.
3. **Quên thêm tài liệu học?** — gõ `add` trong console để thêm tab/cửa sổ vừa bị chặn vào danh sách cho phép.
4. **Để dừng** — gõ `stop` trong console bất cứ lúc nào.

## Cài đặt

```bash
pip install pygetwindow
```

## Chạy

```bash
python study_focus_guard.py
```

## Lưu ý

- Tính năng tự động đóng cửa sổ chỉ được hỗ trợ đầy đủ trên **Windows** (giới hạn của thư viện `pygetwindow`). Trên macOS/Linux, chương trình vẫn phát hiện và cảnh báo, nhưng không thể tự đóng cửa sổ.
- Việc nhận diện tab trình duyệt dựa trên tiêu đề của tab đang được chọn (tab đang hiển thị), không phải toàn bộ danh sách tab chạy nền.


Được hỗ trợ tạo bởi Claude
