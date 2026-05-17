# ==========================================
# SỔ TAY QUY CHUẨN CHO HỆ THỐNG AGENT (V2)
# ==========================================

SUPPORTED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.webp']
MIN_FILE_SIZE_KB = 15
VECTOR_EXTENSIONS = ['.svg']
VECTOR_DEFAULT_DIR = 'icons'
RATE_LIMIT_SLEEP = 12  # Tối ưu lại thời gian nghỉ một chút

# BỘ PROMPT NÂNG CẤP ĐỂ TĂNG ĐỘ CHÍNH XÁC
AGENT_PROMPT_TEMPLATE = """
Bạn là chuyên gia phân tích và quản lý tài nguyên thiết kế hiệu năng cao.
Hãy phân tích bức ảnh được cung cấp dựa trên chủ đề mục tiêu: "{target_topic}".

Nhiệm vụ của bạn:
1. Kiểm tra xem bức ảnh này có liên quan hoặc chứa nội dung thuộc chủ đề "{target_topic}" hay không (Trả về True/False ở trường "is_matched").
2. Nếu "is_matched" là True, hãy phân loại nó vào một trong các thư mục sau: {categories}. Nếu không liên quan rõ ràng, hãy xếp vào 'others'.
3. Phân tích nội dung để trích xuất 2-3 từ khóa ngắn gọn (bằng tiếng Anh hoặc tiếng Việt không dấu, cách nhau bằng dấu gạch dưới).
4. Xác định 1 màu sắc chủ đạo nổi bật nhất của bức ảnh (ví dụ: red, blue, green, white, black...).

Trả về đúng 1 cấu trúc định dạng JSON duy nhất không kèm từ ngữ thừa:
{{
    "is_matched": true/false,
    "category": "tên_thư_mục_phù_hợp",
    "keywords": "tu_khoa_1_tu_khoa_2",
    "main_color": "mau_sac",
    "description": "mo_ta_ngan_gon_khong_dau_viet_thuong"
}}
"""