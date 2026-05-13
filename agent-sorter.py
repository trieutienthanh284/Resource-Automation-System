import os
import shutil
import json
import time
from google import genai
from google.genai import types

# Nhập khẩu bộ quy chuẩn từ file rules.py
import config
from auto_sync import sync

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

        # Lấy đuôi file và dung lượng
        ext = os.path.splitext(filename)[1].lower()
        file_size_kb = os.path.getsize(file_path) / 1024

        # KIỂM TRA LUẬT 2: LỌC RÁC
        if file_size_kb < config.MIN_FILE_SIZE_KB:
            print(f"🗑️ Đang xóa rác: {filename} (Chỉ nặng {file_size_kb:.1f} KB)")
            os.remove(file_path)  # Tiêu hủy luôn
            continue

        # KIỂM TRA LUẬT 3: LUỒNG CAO TỐC CHO SVG
        if ext in config.VECTOR_EXTENSIONS:
            print(f"⚡ Đẩy thẳng file Vector: {filename} vào kho (Bypass AI)")
            target_dir = os.path.join(base_output_dir, config.VECTOR_DEFAULT_DIR)
            if not os.path.exists(target_dir): os.makedirs(target_dir)
            shutil.move(file_path, os.path.join(target_dir, filename))
            continue

        # KIỂM TRA LUẬT 1: CHẶN ĐUÔI FILE LẠ
        if ext not in config.SUPPORTED_EXTENSIONS:
            print(f"⏩ Đưa vào khu cách ly: {filename} (Định dạng {ext} không hỗ trợ)")
            shutil.move(file_path, os.path.join(quarantine_dir, filename))
            continue

        print(f"👀 Đang đưa cho AI phân tích: {filename}...")

        # ... (Đoạn code try...except gọi genai.Client cũ giữ nguyên)

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
    sync()

if __name__ == "__main__":
    sort_images('temp_images', 'resource')