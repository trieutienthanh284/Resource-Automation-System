import os
import shutil
import json
import time
from google import genai
from google.genai import types

# Nhập khẩu bộ quy chuẩn từ file rules.py
import config

API_KEY = "AIzaSyATcPec9FiZSTuu4VlLo8TVwQtCTEe43YA"  # Dán Key của bạn vào đây
client = genai.Client(api_key=API_KEY)


def sort_images(input_dir, base_output_dir):
    print("🤖 Agent AI đang khởi động, đọc sổ tay quy chuẩn...\n")

    if not os.path.exists(input_dir): return
    quarantine_dir = os.path.join(base_output_dir, 'unprocessed')
    if not os.path.exists(quarantine_dir): os.makedirs(quarantine_dir)

    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        if not os.path.isfile(file_path): continue

        ext = os.path.splitext(filename)[1].lower()

        # 1. Đọc luật định dạng: Nếu file không hợp lệ -> Cách ly
        if ext not in config.SUPPORTED_EXTENSIONS:
            print(f"⏩ Bỏ qua {filename} (Định dạng {ext} không hỗ trợ)")
            shutil.move(file_path, os.path.join(quarantine_dir, filename))
            continue

        print(f"👀 Đang phân tích: {filename}...")

        try:
            sample_file = client.files.upload(file=file_path)

            # 2. Đọc luật tư duy: Bơm danh mục và đuôi file vào Prompt
            categories_str = ", ".join(config.ALLOWED_CATEGORIES)
            prompt = config.AGENT_PROMPT_TEMPLATE.format(categories=categories_str, ext=ext)

            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[sample_file, prompt],
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )

            result = json.loads(response.text)

            # Nếu AI tự bịa ra thư mục lạ, ép nó về 'others'
            category = result.get("category", "others")
            if category not in config.ALLOWED_CATEGORIES:
                category = "others"

            new_filename = result.get("filename", filename)

            print(f"   -> Đưa vào [{category}] | Đổi tên: {new_filename}")

            target_dir = os.path.join(base_output_dir, category)
            if not os.path.exists(target_dir): os.makedirs(target_dir)

            shutil.move(file_path, os.path.join(target_dir, new_filename))
            client.files.delete(name=sample_file.name)

            # 3. Đọc luật nhịp độ: Nghỉ ngơi theo số giây đã quy định
            print(f"   ⏳ Nghỉ {config.RATE_LIMIT_SLEEP} giây để tránh quá tải API...")
            time.sleep(config.RATE_LIMIT_SLEEP)

        except Exception as e:
            print(f"   ❌ Lỗi khi phân tích {filename}: {e}")
            shutil.move(file_path, os.path.join(quarantine_dir, filename))

    print("\n🎉 HOÀN TẤT PHÂN LOẠI!")


if __name__ == "__main__":
    sort_images('temp_images', 'resource')