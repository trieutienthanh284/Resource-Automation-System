# ==========================================
# SỔ TAY QUY CHUẨN CHO HỆ THỐNG AGENT
# ==========================================

# 1. QUY CHUẨN ĐẦU VÀO (Dành cho Agent xử lý AI)
SUPPORTED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.webp']

# 2. QUY CHUẨN LỌC RÁC (Garbage Collection)
MIN_FILE_SIZE_KB = 10  # Dung lượng tối thiểu. File < 10KB sẽ bị xóa thẳng tay.

# 3. QUY CHUẨN XỬ LÝ NGOẠI LỆ (.SVG)
VECTOR_EXTENSIONS = ['.svg']      # Các file AI không đọc được
VECTOR_DEFAULT_DIR = 'icons'    # Thư mục mặc định chứa các file này (không qua AI)

# 4. QUY CHUẨN NHỊP ĐỘ (Tránh sập API)
RATE_LIMIT_SLEEP = 15  # Thời gian nghỉ bắt buộc giữa các lần gọi AI (giây)

# 5. QUY CHUẨN CẤU TRÚC KHO TÀI NGUYÊN (Dành cho AI)
ALLOWED_CATEGORIES = ['logos', 'icons', 'backgrounds', 'characters', 'others']

# 6. QUY CHUẨN NHẬN THỨC (Prompt cho AI)
AGENT_PROMPT_TEMPLATE = """
Bạn là chuyên gia quản lý tài nguyên thiết kế. Hãy phân loại bức ảnh này.
Trích xuất đuôi mở rộng của file gốc là '{ext}'.
Trả về đúng 1 file JSON chứa 2 trường:
- "category": Chọn 1 trong các phân loại sau ({categories}).
- "filename": Đặt tên mới ngắn gọn, mô tả nội dung ảnh, viết thường, không dấu, thay khoảng trắng bằng gạch dưới. BẮT BUỘC phải giữ lại đuôi mở rộng của file gốc (VD: bieu_tuong_the_thao.{ext}).
"""