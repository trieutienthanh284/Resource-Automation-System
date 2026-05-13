import os
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# ==========================================
# TỪ ĐIỂN QUY ĐỊNH LỜI NHẮN COMMIT
# ==========================================
COMMIT_MESSAGES = {
    "agent_scraper.py": "Agent thu thập dữ liệu",
    "agent_downloader.py": "Agent tải dữ liệu",
    "agent_sorter.py": "Agent phân loại và sắp xếp ảnh",
    "config.py": "Bộ quy tắc cho Agent",
    "auto_sync.py": "Agent tự động push lên Github",
    "resource/": "Update resource"  # Dành riêng cho thư mục ảnh
}


def run_git(args):
    return subprocess.run(["git"] + args, cwd=PROJECT_ROOT, capture_output=True, text=True)


def sync():
    print("🚚 Agent Giao Hàng đang kiểm tra kho...")

    # 1. Quét các file có sự thay đổi
    status = run_git(["status", "--porcelain"])
    if not status.stdout.strip():
        print("Mọi thứ đã đồng bộ. Không có dữ liệu mới.")
        return

    # Lấy danh sách đường dẫn các file bị thay đổi
    changed_paths = [line[3:] for line in status.stdout.splitlines()]
    commits_to_make = {}

    # 2. Phân loại file để chọn lời nhắn Commit tương ứng
    for path in changed_paths:
        path = path.strip('"')  # Xóa dấu ngoặc kép nếu đường dẫn có khoảng trắng

        # Nếu là file trong thư mục resource
        if path.startswith("resource/"):
            msg = COMMIT_MESSAGES["resource/"]
            commits_to_make.setdefault(msg, []).append(path)
        else:
            # Nếu là các file code
            matched = False
            for key, msg in COMMIT_MESSAGES.items():
                if path == key:
                    commits_to_make.setdefault(msg, []).append(path)
                    matched = True
                    break

            # Nếu có file lạ phát sinh chưa có trong từ điển
            if not matched:
                commits_to_make.setdefault(f"Cập nhật file: {path}", []).append(path)

    # 3. Tiến hành Add và Commit cho từng nhóm
    for msg, files in commits_to_make.items():
        print(f"📦 Đang đóng gói ({len(files)} file) với lời nhắn: '{msg}'")
        run_git(["add"] + files)
        run_git(["commit", "-m", msg])

    # 4. Đẩy toàn bộ các commit lên GitHub
    print("🚀 Đang đẩy dữ liệu lên GitHub...")
    result = run_git(["push", "origin", "HEAD"])

    if result.returncode == 0:
        print("🎉 Đã đồng bộ lên GitHub thành công với các commit chuyên nghiệp!")
    else:
        print(f"❌ Lỗi khi Push: {result.stderr}")


if __name__ == "__main__":
    sync()