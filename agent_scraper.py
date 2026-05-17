import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

def crawl_image_links(target_url, output_csv_path):
    print(f"🕵️ Agent đang thâm nhập vào trang: {target_url} ...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        print(f"🔍 Agent phát hiện tổng cộng {len(img_tags)} hình ảnh.")

        image_links = []
        for img in img_tags:
            img_url = img.get('src') or img.get('data-src')
            if img_url:
                full_url = urljoin(target_url, img_url)
                if not full_url.startswith('data:image'):
                    image_links.append([full_url])

        with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['URL'])
            writer.writerows(image_links)

        print(f"✅ HOÀN TẤT! Đã lưu {len(image_links)} đường link vào file '{output_csv_path}'")

    except Exception as e:
        print(f"❌ Lỗi: Agent không thể truy cập trang web này. Chi tiết: {e}")