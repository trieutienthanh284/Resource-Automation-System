import os
from datetime import datetime

from agent_scraper import crawl_image_links
from agent_downloader import download_images
from agent_sorter import run_sorter
import config


def setup_environment():
    """Tự động xây dựng cấu trúc thư mục và file .gitkeep để chống lỗi GitHub xóa folder trống"""
    os.makedirs("temp_images", exist_ok=True)
    os.makedirs("resource/unprocessed", exist_ok=True)

    for category in config.ALLOWED_CATEGORIES:
        cat_path = os.path.join("resource", category)
        os.makedirs(cat_path, exist_ok=True)
        # Tạo file .gitkeep ẩn để giữ folder trên GitHub
        with open(os.path.join(cat_path, ".gitkeep"), "w") as f:
            pass


def main():
    print("============================================================")
    print("🚀 [HỆ THỐNG AGENT THÔNG MINH] Khởi động phòng điều hành...")
    print("============================================================")

    # Tự động setup thư mục an toàn
    setup_environment()

    URL_MUC_TIEU = input("🔗 Nhập URL trang web muốn cào ảnh: ").strip()
    if not URL_MUC_TIEU:
        URL_MUC_TIEU = "https://en.wikipedia.org/wiki/FC_Barcelona"

    CHU_DE_MUC_TIEU = input("🎯 Nhập chủ đề bạn muốn lọc (VD: cauthu, logo, caycoi...): ").strip()
    if not CHU_DE_MUC_TIEU:
        CHU_DE_MUC_TIEU = "logo"

    FILE_CSV = "image_links.csv"
    KHO_TAM = "temp_images"
    GIOI_HAN_TAI = 30

    start_time = datetime.now()
    print(f"\n⏰ Bắt đầu tiến trình lúc: {start_time.strftime('%H:%M:%S')}")
    print(f"🎯 Chủ đề cần săn tìm: [{CHU_DE_MUC_TIEU.upper()}]")
    print("-" * 60)

    try:
        print("\n🕵️ GIAI ĐOẠN 1: Agent Scraper đang thâm nhập...")
        crawl_image_links(URL_MUC_TIEU, FILE_CSV)

        print("\n📥 GIAI ĐOẠN 2: Agent Downloader đang tải ảnh nháp...")
        download_images(FILE_CSV, KHO_TAM, limit=GIOI_HAN_TAI)

        print("\n🤖 GIAI ĐOẠN 3: AI đang phân tích chuyên sâu theo chủ đề...")
        run_sorter(target_topic=CHU_DE_MUC_TIEU)

        end_time = datetime.now()
        duration = end_time - start_time
        print("\n" + "=" * 60)
        print(f"🎉 HOÀN TẤT THÀNH CÔNG! Đã lọc ảnh theo chủ đề '{CHU_DE_MUC_TIEU}' và đồng bộ GitHub.")
        print(f"⏱️ Tổng thời gian vận hành: {duration.seconds} giây.")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n🛑 Người dùng đã dừng hệ thống khẩn cấp.")
    except Exception as e:
        print(f"\n❌ LỖI HỆ THỐNG: {e}")


if __name__ == "__main__":
    main()