# ==========================================
# SỔ TAY QUY CHUẨN CHO HỆ THỐNG AGENT (B.F.E ALLIANCE)
# ==========================================

# 1. QUY CHUẨN ĐẦU VÀO (Cho Agent Downloader & Sorter)
SUPPORTED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.webp']

# 2. QUY CHUẨN NHỊP ĐỘ (Tránh sập API)
RATE_LIMIT_SLEEP = 15  # Thời gian nghỉ bắt buộc giữa các lần gọi (giây)

# 3. QUY CHUẨN CẤU TRÚC KHO TÀI NGUYÊN
# Đây là các thư mục mà AI được phép sử dụng
ALLOWED_CATEGORIES = ['logos', 'icons', 'backgrounds', 'characters', 'others']

# 4. QUY CHUẨN NHẬN THỨC (Prompt cho AI)
# Dùng ngoặc nhọn {categories} và {ext} để code tự động điền dữ liệu vào
AGENT_PROMPT_TEMPLATE = """
Bạn là chuyên gia quản lý tài nguyên thiết kế. Hãy phân loại bức ảnh này.
Trích xuất đuôi mở rộng của file gốc là '{ext}'.
Trả về đúng 1 file JSON chứa 2 trường:
- "category": Chọn 1 trong các phân loại sau ({categories}).
- "filename": Đặt tên mới ngắn gọn, mô tả nội dung ảnh, viết thường, không dấu, thay khoảng trắng bằng gạch dưới. BẮT BUỘC phải giữ lại đuôi mở rộng của file gốc (VD: bieu_tuong_the_thao.{ext}).
"""