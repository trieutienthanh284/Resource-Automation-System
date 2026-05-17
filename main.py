import os
from datetime import datetime

# Import các Agent trưởng bộ phận
from agent_scraper import crawl_image_links
from agent_downloader import download_images
from agent_sorter import run_sorter


def main():
    print("============================================================")
    print("🚀 [HỆ THỐNG AGENT THÔNG MINH] Khởi động phòng điều hành...")
    print("============================================================")

    # 1. Nhập cấu hình động từ bàn phím khi chạy
    URL_MUC_TIEU = input("🔗 Nhập URL trang web muốn cào ảnh: ").strip()
    if not URL_MUC_TIEU:
        URL_MUC_TIEU = "https://en.wikipedia.org/wiki/FC_Barcelona"  # Mặc định nếu bấm Enter luôn

    CHU_DE_MUC_TIEU = input("🎯 Nhập chủ đề bạn muốn lọc (VD: cauthu, logo, caycoi...): ").strip()
    if not CHU_DE_MUC_TIEU:
        CHU_DE_MUC_TIEU = "logo"  # Mặc định lọc logo để test độ chính xác

    # Các cấu hình kho bãi cố định
    FILE_CSV = "image_links.csv"
    KHO_TAM = "temp_images"
    KHO_THANH_PHAM = "resource"
    GIOI_HAN_TAI = 30

    start_time = datetime.now()
    print(f"\n⏰ Bắt đầu tiến trình lúc: {start_time.strftime('%H:%M:%S')}")
    print(f"🎯 Chủ đề cần săn tìm: [{CHU_DE_MUC_TIEU.upper()}]")
    print("-" * 60)

    try:
        # BƯỚC 1: CÀO WEB (SCRAPER)
        print("\n🕵️ GIAI ĐOẠN 1: Agent Scraper đang thâm nhập...")
        crawl_image_links(URL_MUC_TIEU, FILE_CSV)

        # BƯỚC 2: TẢI ẢNH NHÁP (DOWNLOADER)
        print("\n📥 GIAI ĐOẠN 2: Agent Downloader đang tải ảnh nháp...")
        download_images(FILE_CSV, KHO_TAM, limit=GIOI_HAN_TAI)

        # BƯỚC 3: AI PHÂN LOẠI & ĐỔI TÊN CHUẨN HOÁ (SORTER + SYNC)
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