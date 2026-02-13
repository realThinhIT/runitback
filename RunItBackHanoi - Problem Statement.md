## **1\. Tóm tắt chung**

### 1.1. Vấn đề

Phần lớn trận bóng rổ tại Hà Nội bị hủy do thiếu người và không thể ghép đội hiệu quả giữa các người chơi (theo khảo sát thực tế của nhóm).

### 1.2. Giải pháp

AI Matchmaking Chatbot \- sử dụng GPT-4o-mini để đọc dữ liệu người chơi, sân, lịch trình và tự động ghép trận đấu theo trình độ, khu vực, thời gian.

### 1.3. Công nghệ AI áp dụng

**OpenAI API (GPT-4o-mini)** với kỹ thuật **RAG-lite**: truyền dữ liệu có cấu trúc từ Google Sheets vào system prompt để AI suy luận và ghép trận.

### 1.4. Sản phẩm

Website (HTML/CSS/JS) với AI chatbot tích hợp, kết nối trực tiếp với cơ sở dữ liệu Google Sheets.

### 1.5. Hiệu quả kỳ vọng

Giảm tỷ lệ hủy trận, rút ngắn thời gian sắp xếp từ hàng chục phút xuống dưới 5 phút.

## **2\. Mô tả vấn đề**

### 2.1. Bối cảnh

Bóng rổ (trận đấu tự phát, không thuộc giải đấu chính thức) là hình thức chơi phổ biến nhất trong cộng đồng bóng rổ nghiệp dư tại Hà Nội. Người chơi tự tập nhóm 5-10 người, chọn sân, hẹn giờ và thi đấu. Tuy nhiên, quá trình này gặp nhiều trở ngại khiến đa số trận đấu không diễn ra được.

### 2.2. Vấn đề cụ thể

Nhóm đã thực hiện khảo sát thực tế với người chơi bóng rổ tại Hà Nội (thông qua Google Forms) và ghi nhận các vấn đề sau:

1. **Tỷ lệ hủy trận cao:** Phần lớn các trận đấu được lên kế hoạch nhưng cuối cùng bị hủy, không phải vì thiếu sân mà vì thiếu người. Đây là vấn đề ghép đội, không phải vấn đề về cơ sở vật chất.  
2. **Quá trình sắp xếp không hiệu quả:** Người chơi thường sử dụng group chat (Messenger, Zalo) với 20+ thành viên nhưng phản hồi rất chậm. Mất 30-60 phút để hỏi và kết nối với từng người mà vẫn không đủ số lượng.  
3. **Chênh lệch trình độ:** Người chơi có trình độ cao hơn không muốn chơi với người mới bắt đầu (khác biệt trình độ), dẫn đến việc một số người bị từ chối hoặc tự bỏ không tham gia.  
4. **Thiếu thông tin về sân:** Không có nguồn thông tin tập trung về các sân bóng rổ (địa chỉ, giá thuê, giờ mở cửa), người chơi phải tự hỏi nhau hoặc tự tìm.

**Vấn đề cốt lõi:** Làm sao để tìm đủ người chơi phù hợp về trình độ, ở gần, vào đúng thời gian một cách nhanh chóng và tự động?

## **3\. Cách thức tiếp cận**

### 3.1. Tư tưởng thiết kế

Nhóm nhận diện rằng đây là bài toán matchmaking (ghép cặp), không phải bài toán tra cứu thông tin. Giải pháp cần có khả năng:

* **Thu thập thông tin người chơi:** trình độ, khu vực, thời gian rảnh.  
* **Đọc dữ liệu có sẵn:** danh sách sân, các trận đấu đang mở, số chỗ trống.  
* **Suy luận và gợi ý:** ghép người chơi vào trận phù hợp hoặc tạo trận mới.  
* **Giao tiếp tự nhiên:** người dùng chỉ cần nói chuyện bình thường, không cần học cách sử dụng.

AI chatbot là lựa chọn phù hợp nhất vì kết hợp được cả 4 yêu cầu trên trong một giao diện đơn giản.

### 3.2. Kiến trúc kỹ thuật: RAG-lite

Nhóm áp dụng mô hình RAG-lite (Retrieval-Augmented Generation phiên bản đơn giản hóa), hoạt động như sau:

| Bước | Mô tả | Công nghệ sử dụng |
| :---- | :---- | :---- |
| 1\. Lưu trữ dữ liệu | Thông tin sân bóng rổ, trận đấu đang mở, người chơi đã đăng ký được lưu trong Google Sheets. | Google Sheets |
| 2\. Truy xuất dữ liệu | Khi người dùng gửi tin nhắn, hệ thống đọc dữ liệu mới nhất từ Sheets và truyền vào system prompt. | Google Sheets API / Apps Script, Python |
| 3\. AI suy luận | GPT-4o-mini nhận dữ liệu \+ tin nhắn người dùng, suy luận để gợi ý trận đấu phù hợp, tạo trận mới, hoặc trả lời câu hỏi. | OpenAI API (GPT-4o-mini) |
| 4\. Cập nhật | Khi người dùng join trận, hệ thống ghi lại vào Sheets để cập nhật số chỗ trống. | Google Sheets API, Python |

**Điểm khác biệt của RAG-lite so với chatbot thông thường:** AI không chỉ trả lời câu hỏi chung chung mà đọc dữ liệu thực tế và đưa ra quyết định dựa trên dữ liệu đó. 

Đây là ứng dụng AI có ý nghĩa thực tiễn, không chỉ là chatbot hỏi và đáp.

## **4\. Mô tả sản phẩm**

### 4.1. Tổng quan sản phẩm

RunItBackHanoi là một website đơn giản với AI chatbot tích hợp, giúp người chơi bóng rổ tại Hà Nội:

* Tìm trận đấu phù hợp với trình độ và khu vực của mình.  
* Tham gia trận đấu chỉ bằng một cuộc hội thoại.  
* Tạo trận đấu mới và chia sẻ cho người khác.  
* Tra cứu thông tin sân bóng rổ (địa chỉ, giá, giờ mở cửa).

### 4.2. Công nghệ sử dụng

| Thành phần | Công nghệ | Vai trò |
| :---- | :---- | :---- |
| Giao diện (Frontend) | HTML/CSS/JS | Trang web chính và giao diện chat |
| AI Engine | OpenAI API (GPT-4o-mini) | Xử lý ngôn ngữ tự nhiên, suy luận ghép trận |
| Cơ sở dữ liệu | Google Sheets | Lưu trữ thông tin sân, trận đấu, người chơi |
| Backend | Python & FastAPI | Làm cầu nối xử lý dữ liệu và tích hợp giữa Frontend và AI/CSDL |
| Hosting | GitHub Pages | Host website để có thể truy cập từ internet |

### 4.3. Luồng hoạt động

Kịch bản khi một người chơi sử dụng RunItBackHanoi:

**Người dùng:** "Tối nay tôi muốn chơi bóng rổ, trình trung bình, gần khu vực Cầu Giấy"

**AI (đọc dữ liệu từ Sheets và trả lời):**   
"Hiện có 1 trận đấu phù hợp với bạn: 

* Trận \#12: Sân Lương Thế Vinh (55 P. Đinh Núp, Cầu Giấy), 19h00 tối nay, trình độ Trung bình, còn 2 chỗ trống.

Bạn muốn tham gia trận này không? Hoặc tôi có thể tạo trận mới cho bạn."

**Người dùng:** "Đăng kí cho tôi tham gia trận đó đi"

**AI:** "Đã ghi nhận. Bạn đã tham gia trận \#12. Hiện trận này còn 1 chỗ trống. Địa chỉ sân: 55 P. Đinh Núp, Nam Trung Yên, Cầu Giấy. Hẹn gặp bạn lúc 19h00\!"

### 4.3. System Prompt cho AI

Thành phần quan trọng nhất của sản phẩm là system prompt \- tập chỉ dẫn cho AI biết cách xử lý yêu cầu. 

**System prompt bao gồm:**

* **Vai trò và nhân cách:** AI được chỉ dẫn là trợ lý bóng rổ của RunItBackHanoi, giao tiếp bằng tiếng Việt, thân thiện và ngắn gọn.  
* **Dữ liệu sân bóng rổ:** Danh sách sân thật tại Hà Nội (tên, địa chỉ, giá, giờ mở cửa) được truyền trực tiếp vào prompt sau khi lấy dữ liệu từ Google Sheets.  
* **Dữ liệu trận đấu đang mở:** Thông tin các trận đấu hiện có (sân, giờ, trình độ, số chỗ trống) được cập nhật từ Google Sheets mỗi lần người dùng gửi tin nhắn.  
* **Quy tắc suy luận:** Hướng dẫn AI cách ghép trận: ưu tiên gần nhà, đúng trình độ, thời gian phù hợp. Nếu không có trận phù hợp, gợi ý tạo trận mới.

### 4.4. Dữ liệu sân bóng rổ

Nhóm đã tổng hợp danh sách các sân bóng rổ tại khu vực Hà Nội ***(bằng cách abcxyz tự điền)*** như sau để sử dụng trong demo.

|  |  |  |  |
| :---- | :---- | :---- | :---- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

Dữ liệu này được truyền vào một phần system prompt của AI, giúp chatbot gợi ý sân chính xác theo khu vực người chơi.

## 5\. Các điểm khác

### 5.1. Khả năng mở rộng

Nếu được phát triển tiếp, sản phẩm có thể mở rộng theo các hướng:

* **Tích hợp Zalo/Messenger:** Để người dùng không cần vào website riêng.  
* **Hệ thống đánh giá người chơi:** Sau mỗi trận, người chơi đánh giá nhau để cải thiện độ chính xác của matchmaking.  
* **Tự động tạo nhóm chat:** Khi đủ người, AI tự tạo group Zalo/Messenger cho các thành viên của trận.  
* **Mở rộng địa lý:** Áp dụng cho các thành phố khác ngoài Hà Nội.  
* **Mở rộng môn thể thao:** Bóng đá, cầu lông, tennis cũng có vấn đề tương tự.

