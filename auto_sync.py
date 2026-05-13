import os
import subprocess
from datetime import datetime

# Xác định đúng tọa độ thư mục gốc của dự án
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def run_git(args):
    return subprocess.run(["git"] + args, cwd=PROJECT_ROOT, capture_output=True, text=True)


def sync():
    print("🚚 Agent Giao Hàng đang kiểm tra kho...")

    # 1. Quét xem có ảnh mới hoặc code mới không
    status = run_git(["status", "--porcelain"])
    if not status.stdout.strip():
        print(f"[{datetime.now()}] Mọi thứ đã đồng bộ. Không có dữ liệu mới để đẩy.")
        return

    print("📦 Đang đóng gói dữ liệu...")

    # 2. Gom tất cả các file (những file rác đã bị .gitignore chặn lại một cách an toàn)
    run_git(["add", "."])

    # 3. Ghi lời nhắn tự động
    msg = f"Auto-sync: Cập nhật tài nguyên lúc {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    run_git(["commit", "-m", msg])

    # 4. Đẩy thẳng lên nhánh hiện tại
    result = run_git(["push", "origin", "HEAD"])

    if result.returncode == 0:
        print(f"[{datetime.now()}] 🎉 Đã đẩy dữ liệu lên GitHub thành công!")
    else:
        print(f"❌ Lỗi khi Push: {result.stderr}")


if __name__ == "__main__":
    sync()