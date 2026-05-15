import os
from datetime import datetime

# Import các Agent "trưởng bộ phận"
from agent_scraper import crawl_image_links
from agent_downloader import download_images
from agent_sorter import run_sorter

def main():
    # --- CẤU HÌNH NHANH TẠI ĐÂY ---
    URL_MUC_TIEU = "https://en.wikipedia.org/wiki/2026_FIFA_World_Cup"
    FILE_CSV = "image_links.csv"
    KHO_TAM = "temp_images"
    KHO_THANH_PHAM = "resource"
    GIOI_HAN_TAI = 30
    # ------------------------------

    start_time = datetime.now()
    print(f"🚀 [HỆ THỐNG AGENT] Bắt đầu chu trình tự động hóa...")
    print(f"📅 Ngày chạy: {start_time.strftime('%d/%m/%Y')} | {start_time.strftime('%H:%M:%S')}")
    print("=" * 60)

    try:
        # BƯỚC 1: ĐI SĂN (SCRAPER)
        print("\n🕵️ GIAI ĐOẠN 1: Agent Scraper đang thâm nhập...")
        crawl_image_links(URL_MUC_TIEU, FILE_CSV)

        # BƯỚC 2: THU HOẠCH (DOWNLOADER)
        print("\n📥 GIAI ĐOẠN 2: Agent Downloader đang tải dữ liệu nháp...")
        download_images(FILE_CSV, KHO_TAM, limit=GIOI_HAN_TAI)

        # BƯỚC 3: XỬ LÝ & ĐỒNG BỘ (SORTER + SYNC)
        print("\n🤖 GIAI ĐOẠN 3: AI đang phân loại và Giao hàng (GitHub)...")
        run_sorter()

        end_time = datetime.now()
        duration = end_time - start_time
        print("\n" + "=" * 60)
        print(f"🎉 HOÀN TẤT! Toàn bộ tài nguyên đã được xử lý và đẩy lên GitHub.")
        print(f"⏱️ Tổng thời gian vận hành: {duration.seconds} giây.")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n🛑 Người dùng đã dừng hệ thống khẩn cấp.")
    except Exception as e:
        print(f"\n❌ LỖI HỆ THỐNG: {e}")


if __name__ == "__main__":
    main()