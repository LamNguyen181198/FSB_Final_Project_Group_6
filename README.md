# MSEK28_PPR501_Nhóm 6: Final Project
Đề bài:
Thiết kế hệ thống tạo, quản lý ngân hàng đề thi, thi
trắc nghiệm sử dụng Python & các framework dựa trên
Python có các yêu cầu:
- Người làm đề: tạo câu hỏi theo template dạng docx
(được cung cấp), ko làm việc trực tiếp với
CSDL/phần mềm.
- Người nhập đề: Sử dụng phần mềm import tự động file
docx vào csdl. Phần mềm có một vài cảnh báo như
check định dạng sai, ... (1)
- Người sửa ngân hàng đề: có quyền sửa được theo môn
được phân công, các chức năng cho phép: xem, thêm,
sửa, xóa trực tiếp từng câu. (2)
- Người sinh đề thi: tạo đề thi theo môn, trong đó
câu trả lời được xáo trộn thứ tự một cách ngẫu
nhiên. Thông số được thiết lập: mã đề thi, thời
gian thi (duration), số câu hỏi trong 1 đề. (3)
- Người thiết lập thời điểm thi thực tế: Cấu hình
thời điểm thi (ngày giờ phút bắt đầu -> kết thúc)
theo lịch thi. (4)
- Người dự thi: đăng nhập vào thời điểm thi hiệu lực.
Phần mềm cho phép làm bài, nộp bài. Khi kết thúc
biết được kết quả thi. (5)
Thiết kế có tính số lượng người dự thi lớn, tính bảo
mật.

MSEK28_PPR501_Nhóm 6: (1) + (2) + (3): Desktop app

---------------------------------------------------------------------------------------------------------------
CÁCH ĐỂ CHẠY: 

Trước khi làm mọi thứ, thì tạo 1 branch riêng của mình trước rồi hẵng merge vào main. 

**Module 1 (WIP - Cần phải thống nhất cách lưu trữ tài liệu sao cho dễ query để edit):**
- **Bước 0: Cài đặt hết các thư viện và ứng dụng cần thiết:**
  - Các ứng dụng cần thiết bao gồm: 
    - Python
    - DBeaver
    - PyCharm (hoặc IDE nào mọi người thích sử dụng)
 
- **Bước 1: Chạy thử desktop app**
  - App hiện tại vẫn đang WIP
  - Chạy lệnh uvicorn main:app --reload để chạy backend process
  - Mở 1 terminal mới và chạy lệnh python app.py 
  - Làm theo hướng dẫn con app hiện ra (document lấy ở trong sample_doc) 
    
