import os
import shutil
import json
import time
import hashlib  # Công cụ tạo mã hash chống trùng tên file
from google import genai
from google.genai import types
from dotenv import load_dotenv

import config
from auto_sync import sync

# Nạp các biến môi trường từ file .env bí mật
load_dotenv()


def generate_short_hash(file_path):
    """Tính toán dữ liệu pixel của ảnh để tạo ra 4 ký tự ngẫu nhiên chống trùng lặp"""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read(1024)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(1024)
    return hasher.hexdigest()[:4]


def sort_images(input_dir, base_output_dir, target_topic):
    # Khởi tạo Client an toàn bên trong hàm để chắc chắn nhận được API_KEY từ file .env
    API_KEY = os.environ.get("GEMINI_API_KEY")
    if not API_KEY:
        print("❌ Lỗi: Không tìm thấy GEMINI_API_KEY trong file .env. Vui lòng kiểm tra lại két sắt!")
        return

    client = genai.Client(api_key=API_KEY)
    print(f"🤖 AI Agent khởi động. Đang tiến hành lọc theo chủ đề: '{target_topic}'...\n")

    if not os.path.exists(input_dir): return

    # Khu vực cách ly cho các file lỗi hoặc không khớp chủ đề
    quarantine_dir = os.path.join(base_output_dir, 'unprocessed')
    if not os.path.exists(quarantine_dir): os.makedirs(quarantine_dir)

    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        if not os.path.isfile(file_path): continue

        ext = os.path.splitext(filename)[1].lower()
        file_size_kb = os.path.getsize(file_path) / 1024

        # KIỂM TRA LUẬT 2: LỌC RÁC DUNG LƯỢNG THẤP
        if file_size_kb < config.MIN_FILE_SIZE_KB:
            print(f"🗑️ Đang xóa rác: {filename} (Chỉ nặng {file_size_kb:.1f} KB)")
            os.remove(file_path)
            continue

        # KIỂM TRA LUẬT 3: LUỒNG CAO TỐC CHO SVG
        if ext in config.VECTOR_EXTENSIONS:
            print(f"⚡ Đẩy thẳng file Vector: {filename} vào kho (Bypass AI)")
            target_dir = os.path.join(base_output_dir, config.VECTOR_DEFAULT_DIR)
            if not os.path.exists(target_dir): os.makedirs(target_dir)
            shutil.move(file_path, os.path.join(target_dir, filename))
            continue

        # KIỂM TRA LUẬT 1: CHẶN ĐUÔI FILE LẠ KHÔNG HỖ TRỢ
        if ext not in config.SUPPORTED_EXTENSIONS:
            print(f"⏩ Đưa vào khu cách ly: {filename} (Định dạng {ext} không hỗ trợ)")
            shutil.move(file_path, os.path.join(quarantine_dir, filename))
            continue

        print(f"👀 Đang đưa cho AI phân tích sâu: {filename}...")

        try:
            sample_file = client.files.upload(file=file_path)
            categories_str = ", ".join(config.ALLOWED_CATEGORIES)

            # Đưa chủ đề bạn nhập từ bàn phím vào Prompt gửi cho Gemini
            prompt = config.AGENT_PROMPT_TEMPLATE.format(
                target_topic=target_topic,
                categories=categories_str
            )

            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[sample_file, prompt],
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )

            result = json.loads(response.text)

            # KIỂM TRA XEM AI CÓ ĐÁNH GIÁ LÀ KHỚP CHỦ ĐỀ KHÔNG
            is_matched = result.get("is_matched", False)

            if not is_matched:
                print(f"   ❌ Không khớp chủ đề [{target_topic}] -> Đẩy vào unprocessed.")
                shutil.move(file_path, os.path.join(quarantine_dir, filename))
                client.files.delete(name=sample_file.name)
                continue

            # Ép danh mục chuẩn hóa
            category = result.get("category", "others")
            if category not in config.ALLOWED_CATEGORIES:
                category = "others"

            # TRÍCH XUẤT ĐẶC TÍNH ĐỂ ĐẶT TÊN FILE THEO ĐỊNH DẠNG MỚI (V2)
            main_color = result.get("main_color", "unknown").lower().replace(" ", "")
            keywords = result.get("keywords", "asset").lower().replace(" ", "_")
            short_hash = generate_short_hash(file_path)

            # Làm sạch chuỗi tên chủ đề (bỏ dấu cách/ký tự lạ) để đưa vào tên file
            safe_topic = "".join([c for c in target_topic if c.isalnum()]).lower()

            # Công thức ráp tên mới cực đẹp: cauthu_red_messi_ghi_ban_8a3f.jpg
            new_filename = f"{safe_topic}_{main_color}_{keywords}_{short_hash}{ext}"

            print(f"   -> Khớp! Đưa vào [{category}] | Tên mới nâng cấp: {new_filename}")

            target_dir = os.path.join(base_output_dir, category)
            if not os.path.exists(target_dir): os.makedirs(target_dir)

            # Di chuyển và đổi tên file
            shutil.move(file_path, os.path.join(target_dir, new_filename))
            client.files.delete(name=sample_file.name)

            # Đọc luật nhịp độ tránh lỗi Too Many Requests
            print(f"   ⏳ Nghỉ {config.RATE_LIMIT_SLEEP} giây để tránh quá tải API...")
            time.sleep(config.RATE_LIMIT_SLEEP)

        except Exception as e:
            print(f"   ❌ Lỗi khi phân tích {filename}: {e}")
            shutil.move(file_path, os.path.join(quarantine_dir, filename))

    print("\n🎉 HOÀN TẤT PHÂN LOẠI!")
    sync()


def run_sorter(target_topic="logo"):
    sort_images('temp_images', 'resource', target_topic)