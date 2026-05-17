import os
import csv
import requests

def download_images(csv_file, output_dir, limit=10):
    print(f"📥 Agent đang chuẩn bị tải {limit} ảnh đầu tiên từ {csv_file}...")

    os.makedirs(output_dir, exist_ok=True)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0

            for row in reader:
                if count >= limit:
                    break

                img_url = row.get('URL')
                if img_url:
                    try:
                        response = requests.get(img_url, headers=headers, timeout=10)
                        response.raise_for_status()

                        ext = img_url.split('.')[-1][:4]
                        if ext.lower() not in ['png', 'jpg', 'jpeg', 'svg', 'gif', 'webp']:
                            ext = 'png'

                        filename = f"image_temp_{count + 1}.{ext}"
                        filepath = os.path.join(output_dir, filename)

                        with open(filepath, 'wb') as f:
                            f.write(response.content)

                        print(f"✅ Đã tải thành công: {filename}")
                        count += 1

                    except Exception as e:
                        print(f"⚠️ Bỏ qua link bị lỗi. Chi tiết: {e}")

            print(f"🎉 HOÀN TẤT! Đã đưa {count} ảnh vào thư mục '{output_dir}'. Sẵn sàng cho AI phân tích!")

    except FileNotFoundError:
        print(f"❌ Lỗi: Không tìm thấy file {csv_file}.")