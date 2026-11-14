"""
Script to generate a standardized 36-page Academic Regulations PDF corpus
and the corresponding benchmark questions (15 dev / 5 test).
"""
import json
import pymupdf
from pathlib import Path

# Data directory
data_dir = Path("starter/data")
data_dir.mkdir(parents=True, exist_ok=True)
benchmark_dir = Path("benchmark")
benchmark_dir.mkdir(parents=True, exist_ok=True)

# 36 pages of comprehensive academic regulations
PAGES_DATA = [
    # CHƯƠNG I: QUY ĐỊNH CHUNG (Trang 1 - 6)
    {
        "page": 1,
        "chapter": "Chương I: Những Quy định chung",
        "section": "Phạm vi và Đối tượng",
        "article": "Điều 1. Phạm vi điều chỉnh và đối tượng áp dụng",
        "text": """BỘ GIÁO DỤC VÀ ĐÀO TẠO - QUY CHẾ ĐÀO TẠO ĐẠI HỌC THEO HỆ THỐNG TÍN CHỈ
CHƯƠNG I: NHỮNG QUY ĐỊNH CHUNG
Điều 1. Phạm vi điều chỉnh và đối tượng áp dụng
1. Quy chế này quy định chi tiết về tổ chức và quản lý đào tạo trình độ đại học theo hệ thống tín chỉ, bao gồm: lập kế hoạch giảng dạy, đăng ký học phần, tổ chức lớp học phần, kiểm tra và thi học phần, đánh giá kết quả học tập, công nhận tín chỉ, cảnh báo học tập, buộc thôi học, xét và công nhận tốt nghiệp đại học chính quy.
2. Quy chế này áp dụng thống nhất đối với tất cả sinh viên hệ chính quy tập trung, cán bộ quản lý đào tạo, giảng viên và các đơn vị phòng ban chức năng trong toàn trường.
3. Đối với các chương trình đào tạo liên kết quốc tế hoặc chương trình tiên tiến, các quy định chuyên thù được thực hiện theo đề án đào tạo đã được phê duyệt và không trái với các nguyên tắc cốt lõi của quy chế này."""
    },
    {
        "page": 2,
        "chapter": "Chương I: Những Quy định chung",
        "section": "Chương trình Đào tạo",
        "article": "Điều 2. Chương trình đào tạo và cấu trúc khối lượng kiến thức",
        "text": """CHƯƠNG I: NHỮNG QUY ĐỊNH CHUNG
Điều 2. Chương trình đào tạo và cấu trúc khối lượng kiến thức
1. Chương trình đào tạo trình độ đại học được xây dựng theo định hướng chuẩn đầu ra, tích hợp kiến thức lý thuyết, kỹ năng thực hành và phẩm chất nghề nghiệp.
2. Khối lượng học tập toàn khóa đối với trình độ cử nhân tối thiểu là 120 tín chỉ, đối với trình độ kỹ sư hoặc cử nhân chuyên sâu đặc thù tối thiểu là 150 tín chỉ.
3. Cấu trúc chương trình bao gồm ba khối kiến thức chính:
a) Khối kiến thức giáo dục đại cương: chiếm từ 25% đến 30% tổng khối lượng kiến thức;
b) Khối kiến thức cơ sở ngành và chuyên ngành: chiếm từ 55% đến 65% tổng khối lượng kiến thức;
c) Khối kiến thức thực tập tốt nghiệp và đồ án/khóa luận tốt nghiệp: chiếm tối thiểu 10% tổng khối lượng kiến thức toàn khóa."""
    },
    {
        "page": 3,
        "chapter": "Chương I: Những Quy định chung",
        "section": "Thời gian Đào tạo",
        "article": "Điều 3. Thời gian đào tạo chuẩn và thời gian tối đa",
        "text": """CHƯƠNG I: NHỮNG QUY ĐỊNH CHUNG
Điều 3. Thời gian đào tạo chuẩn và thời gian tối đa
1. Thời gian đào tạo theo kế hoạch học tập chuẩn đối với chương trình cử nhân 4 năm là 8 học kỳ chính. Đối với chương trình kỹ sư 5 năm là 10 học kỳ chính.
2. Thời gian học tập tối đa để sinh viên hoàn thành chương trình đào tạo được quy định không quá 1.5 lần thời gian thiết kế chuẩn:
a) Không quá 6 năm (12 học kỳ chính) đối với chương trình chuẩn 4 năm;
b) Không quá 7.5 năm (15 học kỳ chính) đối với chương trình chuẩn 5 năm.
3. Thời gian tạm dừng học tập có phép vì lý do thi hành nghĩa vụ quân sự hoặc lý do sức khỏe đặc biệt (có xác nhận của bệnh viện cấp huyện trở lên) không tính vào thời gian học tập tối đa toàn khóa."""
    },
    {
        "page": 4,
        "chapter": "Chương I: Những Quy định chung",
        "section": "Học chế Tín chỉ",
        "article": "Điều 4. Định nghĩa và quy đổi tín chỉ",
        "text": """CHƯƠNG I: NHỮNG QUY ĐỊNH CHUNG
Điều 4. Định nghĩa và quy chuẩn tính toán tín chỉ
1. Một tín chỉ (TC) được tính tương đương với 50 giờ học tập định mức của sinh viên, bao gồm thời gian học trên lớp, thực hành tại phòng thí nghiệm và thời gian tự học có hướng dẫn.
2. Một tín chỉ học tập lý thuyết được quy chuẩn bằng 15 tiết giảng dạy trên lớp và tối thiểu 30 giờ chuẩn bị cá nhân ngoài lớp.
3. Một tín chỉ học phần thực hành, thí nghiệm, thảo luận tương đương từ 30 đến 45 tiết thực hành tập trung tại cơ sở đào tạo.
4. Một tín chỉ thực tập tại doanh nghiệp, dã ngoại hoặc làm đồ án/khóa luận tốt nghiệp được tính từ 45 đến 60 giờ làm việc thực tế được giảng viên hoặc chuyên gia doanh nghiệp giám sát và đánh giá."""
    },
    {
        "page": 5,
        "chapter": "Chương I: Những Quy định chung",
        "section": "Phân loại Học phần",
        "article": "Điều 5. Phân loại và quan hệ giữa các học phần",
        "text": """CHƯƠNG I: NHỮNG QUY ĐỊNH CHUNG
Điều 5. Phân loại học phần và điều kiện ràng buộc
1. Học phần bắt buộc: Là học phần chứa đựng những kiến thức cốt lõi của ngành và chuyên ngành đào tạo, mọi sinh viên theo học ngành đó đều bắt buộc phải hoàn thành và đạt điểm đạt.
2. Học phần tự chọn có hướng dẫn: Là học phần chứa đựng kiến thức chuyên sâu nhằm đa dạng hóa định hướng nghề nghiệp, sinh viên được tự do lựa chọn theo số lượng tín chỉ yêu cầu của chương trình.
3. Học phần tiên quyết: Học phần A là tiên quyết của học phần B khi sinh viên bắt buộc phải tích lũy đạt học phần A mới được phép đăng ký học phần B.
4. Học phần học trước: Học phần A là học phần học trước của học phần B khi sinh viên đã hoàn thành đánh giá học phần A (có thể chưa đạt điểm tích lũy) mới được đăng ký học phần B.
5. Học phần song hành: Là hai học phần mà sinh viên phải đăng ký học trong cùng một học kỳ hoặc học phần này đã được đăng ký từ học kỳ trước."""
    },
    {
        "page": 6,
        "chapter": "Chương I: Những Quy định chung",
        "section": "Chuẩn Đầu ra Ngoại ngữ",
        "article": "Điều 6. Chuẩn đầu ra ngoại ngữ và công nghệ thông tin",
        "text": """CHƯƠNG I: NHỮNG QUY ĐỊNH CHUNG
Điều 6. Yêu cầu chuẩn đầu ra ngoại ngữ và năng lực số
1. Tất cả sinh viên tốt nghiệp trình độ đại học chính quy phải đạt chuẩn đầu ra ngoại ngữ tương đương Bậc 3 theo Khung năng lực ngoại ngữ 6 bậc dùng cho Việt Nam (tương đương TOEIC 450, IELTS 4.5, hoặc B1 CEFR quốc tế).
2. Đối với các chương trình chất lượng cao, chương trình đào tạo bằng tiếng Anh, chuẩn đầu ra ngoại ngữ tối thiểu là Bậc 4 (tương đương IELTS 6.0 hoặc TOEIC 650 quốc tế).
3. Chuẩn kỹ năng sử dụng công nghệ thông tin: Sinh viên phải đạt chuẩn kỹ năng ứng dụng CNTT cơ bản theo quy định hiện hành của Bộ Thông tin và Truyền thông trước khi đăng ký làm đồ án tốt nghiệp.
4. Chứng chỉ ngoại ngữ và tin học nộp để xét miễn giảm hoặc công nhận chuẩn đầu ra phải còn thời hạn trong vòng 2 năm tính đến ngày nộp hồ sơ xét tốt nghiệp."""
    },

    # CHƯƠNG II: TỔ CHỨC ĐÀO TẠO VÀ QUẢN LÝ HỌC TẬP (Trang 7 - 14)
    {
        "page": 7,
        "chapter": "Chương II: Tổ chức Đào tạo và Quản lý Học vụ",
        "section": "Kế hoạch Năm học",
        "article": "Điều 7. Cấu trúc năm học và học kỳ",
        "text": """CHƯƠNG II: TỔ CHỨC ĐÀO TẠO VÀ QUẢN LÝ HỌC VỤ
Điều 7. Cấu trúc năm học và các học kỳ
1. Một năm học tiêu chuẩn gồm hai học kỳ chính (Học kỳ I và Học kỳ II) và một học kỳ phụ (Học kỳ hè).
2. Thời gian của mỗi học kỳ chính kéo dài tối thiểu 15 tuần học tập thực tế và từ 2 đến 3 tuần dành riêng cho kỳ thi kết thúc học phần tập trung.
3. Học kỳ phụ (học kỳ hè) được tổ chức theo nguyện vọng của sinh viên và khả năng đáp ứng của nhà trường, có thời lượng tối thiểu 5 tuần học tập thực tế và 1 tuần thi. Học kỳ phụ nhằm giúp sinh viên học lại, học cải thiện điểm hoặc học vượt tiến độ.
4. Nhà trường công bố lịch trình năm học và kế hoạch mở lớp ít nhất 4 tuần trước khi bắt đầu học kỳ mới để sinh viên chủ động đăng ký môn học."""
    },
    {
        "page": 8,
        "chapter": "Chương II: Tổ chức Đào tạo và Quản lý Học vụ",
        "section": "Đăng ký Học phần",
        "article": "Điều 8. Quy định về hạn mức đăng ký tín chỉ",
        "text": """CHƯƠNG II: TỔ CHỨC ĐÀO TẠO VÀ QUẢN LÝ HỌC VỤ
Điều 8. Hạn mức đăng ký khối lượng học tập mỗi học kỳ
1. Trong mỗi học kỳ chính, khối lượng học tập tối thiểu và tối đa mà sinh viên được phép đăng ký được quy định như sau:
a) Khối lượng học tập tối thiểu: 12 tín chỉ trong mỗi học kỳ chính (trừ học kỳ cuối khóa của khóa học);
b) Khối lượng học tập tối đa: 24 tín chỉ trong mỗi học kỳ chính.
2. Sinh viên đang trong tình trạng bị cảnh báo học tập chỉ được phép đăng ký tối đa 14 tín chỉ trong học kỳ kế tiếp để tập trung nâng cao kết quả học tập.
3. Trong học kỳ phụ, sinh viên được đăng ký học tập tối đa không quá 8 tín chỉ.
4. Sinh viên có điểm trung bình chung tích lũy (CPA) từ 3.20 trở lên có thể làm đơn xin phép Trưởng phòng Đào tạo để đăng ký thêm tối đa 3 tín chỉ vượt khung quy định."""
    },
    {
        "page": 9,
        "chapter": "Chương II: Tổ chức Đào tạo và Quản lý Học vụ",
        "section": "Điều chỉnh Học phần",
        "article": "Điều 9. Rút học phần và hủy đăng ký môn học",
        "text": """CHƯƠNG II: TỔ CHỨC ĐÀO TẠO VÀ QUẢN LÝ HỌC VỤ
Điều 9. Rút bớt học phần và hủy kết quả đăng ký
1. Việc rút bớt học phần trong danh sách đã đăng ký chỉ được chấp nhận trong vòng 2 tuần đầu tiên tính từ ngày bắt đầu học kỳ chính (hoặc trong tuần đầu tiên của học kỳ phụ).
2. Sinh viên xin rút học phần phải đảm bảo khối lượng học tập còn lại sau khi rút không ít hơn số tín chỉ tối thiểu theo quy định tại Điều 8 (tối thiểu 12 tín chỉ).
3. Học phần được rút hợp lệ trong thời hạn quy định sẽ được xóa hoàn toàn khỏi bảng kết quả học tập và không phải đóng học phí cho học phần đó.
4. Sinh viên tự ý bỏ học phần sau thời hạn quy định mà không có sự đồng ý bằng văn bản của Phòng Đào tạo sẽ bị nhận điểm 0 (hoặc điểm F) đối với học phần đó và vẫn phải hoàn thành toàn bộ nghĩa vụ học phí."""
    },
    {
        "page": 10,
        "chapter": "Chương II: Tổ chức Đào tạo và Quản lý Học vụ",
        "section": "Học lại và Cải thiện",
        "article": "Điều 10. Học lại và đăng ký học cải thiện điểm",
        "text": """CHƯƠNG II: TỔ CHỨC ĐÀO TẠO VÀ QUẢN LÝ HỌC VỤ
Điều 10. Quy định về học lại và học cải thiện điểm số
1. Sinh viên có học phần bắt buộc bị điểm F bắt buộc phải đăng ký học lại học phần đó ở học kỳ gần nhất có mở lớp, hoặc đăng ký học phần tương đương thay thế nếu học phần cũ không còn giảng dạy.
2. Đối với học phần tự chọn bị điểm F, sinh viên có thể đăng ký học lại chính học phần đó hoặc chọn học một học phần tự chọn khác cùng nhóm kiến thức để bù đủ số tín chỉ yêu cầu.
3. Học cải thiện điểm:
a) Sinh viên chỉ được phép đăng ký học cải thiện đối với các học phần đã đạt điểm D, D+ hoặc C;
b) Không cho phép học cải thiện điểm đối với các học phần đã đạt từ điểm B trở lên;
c) Điểm đánh giá cao nhất trong các lần học sẽ là điểm số chính thức được lưu vào bảng điểm tích lũy toàn khóa."""
    },
    {
        "page": 11,
        "chapter": "Chương II: Tổ chức Đào tạo và Quản lý Học vụ",
        "section": "Nghỉ học Tạm thời",
        "article": "Điều 11. Tạm dừng học tập và bảo lưu kết quả",
        "text": """CHƯƠNG II: TỔ CHỨC ĐÀO TẠO VÀ QUẢN LÝ HỌC VỤ
Điều 11. Tạm dừng học tập và bảo lưu kết quả học tập
1. Sinh viên được quyền xin tạm dừng học tập và bảo lưu kết quả học tập đã tích lũy trong các trường hợp sau:
a) Được điều động vào lực lượng vũ trang nhân dân (nghĩa vụ quân sự hoặc công an);
b) Bị ốm đau, tai nạn hoặc bệnh tật dài hạn phải điều trị có xác nhận và chỉ định của cơ quan y tế có thẩm quyền;
c) Vì nhu cầu cá nhân chính đáng khác, nhưng phải hoàn thành ít nhất 1 học kỳ chính tại trường và không thuộc diện bị cảnh báo học tập hoặc xem xét kỷ luật.
2. Thời gian tạm dừng học tập vì nhu cầu cá nhân không quá 2 học kỳ chính liên tiếp. Tổng thời gian tạm dừng tích lũy không được vượt quá 4 học kỳ chính trong toàn khóa học.
3. Hết thời hạn tạm dừng, sinh viên phải nộp đơn xin tiếp tục học tập trước khi học kỳ mới bắt đầu ít nhất 2 tuần."""
    },
    {
        "page": 12,
        "chapter": "Chương II: Tổ chức Đào tạo và Quản lý Học vụ",
        "section": "Chuyển Ngành và Trường",
        "article": "Điều 12. Điều kiện chuyển ngành và chuyển cơ sở đào tạo",
        "text": """CHƯƠNG II: TỔ CHỨC ĐÀO TẠO VÀ QUẢN LÝ HỌC VỤ
Điều 12. Chuyển ngành học, chương trình và chuyển trường
1. Sinh viên được xem xét chuyển ngành đào tạo hoặc chuyển chương trình học khi đáp ứng đầy đủ các điều kiện sau:
a) Hoàn thành năm học thứ nhất và có điểm CPA từ 2.50 trở lên;
b) Đạt ngưỡng điểm trúng tuyển của ngành chuyển đến trong cùng kỳ tuyển sinh đầu vào;
c) Không thuộc diện bị cảnh báo học tập hoặc đang trong thời gian bị thi hành kỷ luật từ mức khiển trách trở lên;
d) Được sự đồng ý của Trưởng khoa chuyển đi và Trưởng khoa tiếp nhận.
2. Không cho phép chuyển ngành đối với sinh viên đã bắt đầu học kỳ thứ 5 của khóa học.
3. Sinh viên chuyển trường đến phải có điểm trúng tuyển bằng hoặc cao hơn điểm trúng tuyển của trường tại năm tuyển sinh tương ứng và phải hoàn thành ít nhất 50% khối lượng tín chỉ tại trường mới để được cấp bằng tốt nghiệp."""
    },
    {
        "page": 13,
        "chapter": "Chương II: Tổ chức Đào tạo và Quản lý Học vụ",
        "section": "Song bằng và Ngành kép",
        "article": "Điều 13. Học cùng lúc hai chương trình đào tạo",
        "text": """CHƯƠNG II: TỔ CHỨC ĐÀO TẠO VÀ QUẢN LÝ HỌC VỤ
Điều 13. Đào tạo cùng lúc hai chương trình (học song bằng / ngành kép)
1. Sinh viên có nguyện vọng học thêm một chương trình đào tạo thứ hai (ngành kép) phải đáp ứng các điều kiện sau:
a) Đã hoàn thành ít nhất hai học kỳ chính của chương trình đào tạo thứ nhất;
b) Điểm trung bình tích lũy CPA của chương trình thứ nhất đạt từ 2.80 trở lên (hoặc từ 2.50 trở lên nếu xếp loại rèn luyện Tốt);
c) Không bị cảnh báo học tập ở chương trình thứ nhất tại thời điểm đăng ký.
2. Sinh viên học cùng lúc hai chương trình được công nhận tương đương và bảo lưu các học phần đại cương và cơ sở có nội dung và số tín chỉ tương đương.
3. Trong quá trình học, nếu sinh viên bị điểm CPA chương trình thứ nhất tụt xuống dưới 2.00 thì bắt buộc phải dừng học chương trình thứ hai ở học kỳ kế tiếp."""
    },
    {
        "page": 14,
        "chapter": "Chương II: Tổ chức Đào tạo và Quản lý Học vụ",
        "section": "Tổ chức Lớp học phần",
        "article": "Điều 14. Quy mô lớp học phần và hủy lớp học phần",
        "text": """CHƯƠNG II: TỔ CHỨC ĐÀO TẠO VÀ QUẢN LÝ HỌC VỤ
Điều 14. Quy định về sĩ số lớp học phần
1. Quy mô số lượng sinh viên tối thiểu của một lớp học phần được quy định cụ thể:
a) Lớp học phần lý thuyết đại cương: Tối thiểu 40 sinh viên;
b) Lớp học phần cơ sở ngành và chuyên ngành: Tối thiểu 25 sinh viên;
c) Lớp học phần chuyên ngành hẹp, thực hành chuyên sâu hoặc đồ án: Tối thiểu 15 sinh viên.
2. Nếu số lượng sinh viên đăng ký ít hơn quy chuẩn tối thiểu, lớp học phần sẽ bị hủy trước khi bắt đầu học kỳ 1 tuần. Phòng Đào tạo sẽ thông báo để sinh viên kịp thời chuyển sang đăng ký lớp học phần khác.
3. Trường hợp đặc biệt đối với học phần bắt buộc sắp tốt nghiệp của khóa cuối có sĩ số dưới mức quy chuẩn, Trưởng khoa phải gửi văn bản đề xuất để Hiệu trưởng phê duyệt mở lớp đặc cách."""
    },

    # CHƯƠNG III: ĐÁNH GIÁ KẾT QUẢ HỌC TẬP VÀ THANG ĐIỂM (Trang 15 - 23)
    {
        "page": 15,
        "chapter": "Chương III: Đánh giá Kết quả Học tập và Thang điểm",
        "section": "Thành phần Đánh giá",
        "article": "Điều 15. Đánh giá học phần và cơ cấu điểm thành phần",
        "text": """CHƯƠNG III: ĐÁNH GIÁ KẾT QUẢ HỌC TẬP VÀ THANG ĐIỂM
Điều 15. Đánh giá học phần và cơ cấu tỷ trọng điểm
1. Điểm tổng kết học phần được cấu thành từ hai nhóm điểm chính: Điểm quá trình (điểm kiểm tra thường xuyên) và Điểm thi kết thúc học phần.
2. Tỷ trọng điểm của học phần lý thuyết được quy định thống nhất như sau:
a) Điểm quá trình: Chiếm từ 40% đến 50% tổng điểm học phần, bao gồm: điểm chuyên cần (tối đa 10%), bài kiểm tra giữa kỳ, bài tập lớn, thảo luận nhóm;
b) Điểm thi kết thúc học phần: Chiếm từ 50% đến 60% tổng điểm học phần.
3. Đối với học phần thực hành, thí nghiệm: 100% điểm học phần là điểm đánh giá liên tục trong quá trình thực hành và bài kiểm tra kỹ năng thao tác cuối kỳ.
4. Giảng viên phụ trách học phần có nghĩa vụ công bố công khai thang đánh giá và điểm thành phần cho sinh viên trước khi thi kết thúc học phần ít nhất 1 tuần."""
    },
    {
        "page": 16,
        "chapter": "Chương III: Đánh giá Kết quả Học tập và Thang điểm",
        "section": "Điều kiện Dự thi",
        "article": "Điều 16. Điều kiện dự thi kết thúc học phần và hoãn thi",
        "text": """CHƯƠNG III: ĐÁNH GIÁ KẾT QUẢ HỌC TẬP VÀ THANG ĐIỂM
Điều 16. Điều kiện dự thi và xử lý xin hoãn thi
1. Sinh viên chỉ được quyền tham gia kỳ thi kết thúc học phần khi đáp ứng đầy đủ hai điều kiện tiên quyết:
a) Tham gia tối thiểu 80% tổng số tiết giảng dạy lý thuyết và 100% các buổi thực hành/thí nghiệm trên lớp;
b) Điểm quá trình đánh giá thường xuyên phải đạt từ 4.0 điểm trở lên (theo thang điểm 10).
2. Sinh viên không đủ điều kiện dự thi sẽ nhận điểm 0 cho phần thi kết thúc học phần và bị tính điểm F cho học phần đó.
3. Sinh viên vì lý do ốm đau đột xuất hoặc tai nạn không thể dự thi phải nộp đơn xin hoãn thi kèm bệnh án hợp lệ trong vòng 48 giờ sau ca thi. Sinh viên được hoãn thi sẽ nhận điểm I (Incomplete) và được sắp xếp thi bổ sung vào đợt thi gần nhất."""
    },
    {
        "page": 17,
        "chapter": "Chương III: Đánh giá Kết quả Học tập và Thang điểm",
        "section": "Thang điểm Quy đổi",
        "article": "Điều 17. Thang điểm đánh giá và bảng quy đổi điểm số",
        "text": """CHƯƠNG III: ĐÁNH GIÁ KẾT QUẢ HỌC TẬP VÀ THANG ĐIỂM
Điều 17. Bảng quy đổi thang điểm 10, thang điểm chữ và thang điểm 4
1. Điểm học phần được chấm theo thang điểm 10 (làm tròn đến một chữ số thập phân), sau đó được quy đổi chính thức sang thang điểm chữ và thang điểm 4 theo bảng chuẩn sau:
- Từ 8.5 đến 10.0: Điểm A (Tương đương 4.0 trên thang 4) - Xếp loại Xuất sắc;
- Từ 8.0 đến 8.4: Điểm B+ (Tương đương 3.5 trên thang 4) - Xếp loại Giỏi;
- Từ 7.0 đến 7.9: Điểm B (Tương đương 3.0 trên thang 4) - Xếp loại Khá;
- Từ 6.5 đến 6.9: Điểm C+ (Tương đương 2.5 trên thang 4) - Xếp loại Trung bình khá;
- Từ 5.5 đến 6.4: Điểm C (Tương đương 2.0 trên thang 4) - Xếp loại Trung bình;
- Từ 5.0 đến 5.4: Điểm D+ (Tương đương 1.5 trên thang 4) - Xếp loại Trung bình yếu;
- Từ 4.0 đến 4.9: Điểm D (Tương đương 1.0 trên thang 4) - Xếp loại Đạt tối thiểu;
- Dưới 4.0: Điểm F (Tương đương 0.0 trên thang 4) - Xếp loại Không đạt (Kém).
2. Các điểm chữ từ A đến D được tính là đạt và được tích lũy tín chỉ. Điểm F không được tính tích lũy tín chỉ và phải học lại."""
    },
    {
        "page": 18,
        "chapter": "Chương III: Đánh giá Kết quả Học tập và Thang điểm",
        "section": "Tính điểm GPA và CPA",
        "article": "Điều 18. Phương pháp tính điểm trung bình học kỳ và tích lũy",
        "text": """CHƯƠNG III: ĐÁNH GIÁ KẾT QUẢ HỌC TẬP VÀ THANG ĐIỂM
Điều 18. Công thức tính điểm trung bình GPA và CPA
1. Điểm trung bình chung học kỳ (GPA) và điểm trung bình chung tích lũy (CPA) được tính theo thang điểm 4 theo công thức trung bình gia quyền số tín chỉ:
   GPA hoặc CPA = Tổng (Điểm học phần theo thang 4 x Số tín chỉ học phần) / Tổng số tín chỉ tham gia tính điểm.
2. Kết quả GPA và CPA được làm tròn đến hai chữ số thập phân sau dấu phẩy.
3. Các học phần điều kiện bao gồm: Giáo dục thể chất, Giáo dục quốc phòng - an ninh, và Chuẩn kỹ năng công nghệ thông tin chỉ dùng để xét điều kiện tốt nghiệp, điểm của các học phần này không tính vào GPA và CPA.
4. Điểm của các học phần học cải thiện được cập nhật thay thế cho điểm cũ khi tính điểm CPA tích lũy toàn khóa."""
    },
    {
        "page": 19,
        "chapter": "Chương III: Đánh giá Kết quả Học tập và Thang điểm",
        "section": "Xếp loại Học lực",
        "article": "Điều 19. Tiêu chuẩn phân loại học lực sinh viên",
        "text": """CHƯƠNG III: ĐÁNH GIÁ KẾT QUẢ HỌC TẬP VÀ THANG ĐIỂM
Điều 19. Phân loại trình độ học lực của sinh viên
1. Căn cứ vào điểm trung bình chung tích lũy (CPA), học lực của sinh viên được phân thành các hạng mức:
a) Xuất sắc: CPA đạt từ 3.60 đến 4.00;
b) Giỏi: CPA đạt từ 3.20 đến 3.59;
c) Khá: CPA đạt từ 2.50 đến 3.19;
d) Trung bình: CPA đạt từ 2.00 đến 2.49;
đ) Yếu: CPA đạt từ 1.00 đến 1.99;
e) Kém: CPA đạt dưới 1.00.
2. Sinh viên có học lực xếp loại Xuất sắc hoặc Giỏi được ưu tiên xét cấp học bổng khuyến khích học tập và được ưu tiên đăng ký học vượt tiến độ tối đa 27 tín chỉ/học kỳ.
3. Sinh viên xếp loại học lực Yếu hoặc Kém sẽ nhận thông báo cảnh báo nguy cơ học tập từ Cố vấn học tập."""
    },
    {
        "page": 20,
        "chapter": "Chương III: Đánh giá Kết quả Học tập và Thang điểm",
        "section": "Xử lý Vi phạm Thi cử",
        "article": "Điều 20. Xử lý kỷ luật đối với vi phạm quy chế thi",
        "text": """CHƯƠNG III: ĐÁNH GIÁ KẾT QUẢ HỌC TẬP VÀ THANG ĐIỂM
Điều 20. Hình thức kỷ luật vi phạm phòng thi
1. Sinh viên vi phạm quy chế phòng thi tùy theo mức độ sẽ bị xử lý kỷ luật theo các hình thức sau:
a) Khiển trách: Áp dụng đối với hành vi nhìn bài, trao đổi bài với người khác; trừ 25% điểm bài thi của học phần đó;
b) Cảnh cáo: Áp dụng đối với hành vi mang tài liệu cấm vào phòng thi hoặc tái phạm nhìn bài; trừ 50% điểm bài thi;
c) Đình chỉ thi: Áp dụng đối với hành vi sử dụng điện thoại di động, thiết bị truyền tin thông minh, hoặc tài liệu trái phép trong khi làm bài; bị nhận điểm 0 cho bài thi và cấm thi đợt 2;
d) Buộc thôi học hoặc đình chỉ học tập 1 năm: Áp dụng đối với hành vi thi hộ hoặc nhờ người khác thi hộ.
2. Các quyết định kỷ luật từ mức cảnh cáo trở lên sẽ bị ghi vào hồ sơ sinh viên và gửi thông báo về gia đình."""
    },
    {
        "page": 21,
        "chapter": "Chương III: Đánh giá Kết quả Học tập và Thang điểm",
        "section": "Phúc khảo Điểm thi",
        "article": "Điều 21. Quy trình nộp đơn và xử lý phúc khảo bài thi",
        "text": """CHƯƠNG III: ĐÁNH GIÁ KẾT QUẢ HỌC TẬP VÀ THANG ĐIỂM
Điều 21. Quy trình và thủ tục phúc khảo điểm bài thi
1. Sinh viên có quyền nộp đơn xin phúc khảo điểm thi kết thúc học phần trong thời hạn 10 ngày làm việc kể từ ngày Phòng Khảo thí công bố điểm chính thức trên cổng thông tin sinh viên.
2. Lệ phí phúc khảo được thu theo quy định tài chính của trường và sẽ được hoàn trả 100% nếu kết quả phúc khảo có sự thay đổi tăng điểm do lỗi chấm thi của giảng viên.
3. Hội đồng chấm phúc khảo gồm 2 giảng viên độc lập thực hiện chấm lại bài thi theo đúng đáp án và biểu điểm chi tiết đã duyệt.
4. Nếu điểm phúc khảo chênh lệch từ 0.5 điểm trở lên (theo thang điểm 10) so với điểm ban đầu, Trưởng phòng Khảo thí sẽ ký biên bản điều chỉnh điểm chính thức cho sinh viên. Thời gian công bố kết quả phúc khảo không quá 15 ngày làm việc tính từ hạn chót nhận đơn."""
    },
    {
        "page": 22,
        "chapter": "Chương III: Đánh giá Kết quả Học tập và Thang điểm",
        "section": "Điểm Đặc biệt",
        "article": "Điều 22. Quy định về các ký hiệu điểm chữ đặc biệt I, X, R",
        "text": """CHƯƠNG III: ĐÁNH GIÁ KẾT QUẢ HỌC TẬP VÀ THANG ĐIỂM
Điều 22. Ký hiệu điểm đặc biệt và thời hạn hoàn thành
1. Điểm I (Incomplete - Chưa hoàn thành):
a) Được cấp cho sinh viên được phép hoãn thi vì lý do chính đáng hoặc chưa hoàn thành đồ án môn học có lý do khách quan;
b) Sinh viên nhận điểm I phải hoàn thành việc đánh giá bổ sung trong vòng 1 học kỳ chính tiếp theo. Quá thời hạn này, điểm I tự động chuyển đổi thành điểm F.
2. Điểm X (Chưa nhận được kết quả): Áp dụng khi dữ liệu điểm chưa kịp chuyển giao từ cơ sở liên kết đào tạo hoặc trường đối tác quốc tế.
3. Điểm R (Retake/Exempted): Áp dụng cho các học phần được công nhận miễn trừ hoặc chuyển đổi điểm tương đương từ trường đại học khác hoặc chương trình trao đổi sinh viên.
4. Các điểm I, X, R không được tính vào điểm trung bình GPA và CPA tại học kỳ cấp điểm."""
    },
    {
        "page": 23,
        "chapter": "Chương III: Đánh giá Kết quả Học tập và Thang điểm",
        "section": "Bảo lưu Điểm số",
        "article": "Điều 22b. Chuyển đổi và công nhận điểm các chương trình trao đổi",
        "text": """CHƯƠNG III: ĐÁNH GIÁ KẾT QUẢ HỌC TẬP VÀ THANG ĐIỂM
Điều 22b. Công nhận điểm học tập trao đổi quốc tế
1. Sinh viên tham gia các chương trình trao đổi học thuật, học tập ở nước ngoài theo thỏa thuận hợp tác giữa trường và các đối tác quốc tế được công nhận tín chỉ và quy đổi điểm số.
2. Hội đồng chuyên môn của Khoa xem xét đề cương chi tiết học phần đã học ở nước ngoài; nếu nội dung tương thích từ 75% trở lên thì được công nhận chuyển đổi điểm tương đương.
3. Điểm số từ thang điểm chữ quốc tế (ECTS, US Grade) được quy đổi sang thang điểm 10 và thang điểm 4 theo bảng quy đổi đối sánh do Hội đồng Đào tạo ban hành.
4. Tổng số tín chỉ được công nhận chuyển đổi từ các cơ sở đào tạo bên ngoài không được vượt quá 40% tổng số tín chỉ của chương trình đào tạo."""
    },

    # CHƯƠNG IV: CẢNH BÁO HỌC TẬP, BUỘC THÔI HỌC VÀ KHEN THƯỞNG (Trang 24 - 30)
    {
        "page": 24,
        "chapter": "Chương IV: Cảnh báo Học vụ, Buộc thôi học và Khen thưởng",
        "section": "Cảnh báo Học vụ",
        "article": "Điều 23. Các tiêu chí bị áp dụng cảnh báo học vụ",
        "text": """CHƯƠNG IV: CẢNH BÁO HỌC VỤ, BUỘC THÔI HỌC VÀ KHEN THƯỞNG
Điều 23. Tiêu chí cảnh báo học vụ theo tiến độ học tập
1. Cảnh báo học tập được thực hiện theo từng học kỳ chính nhằm thông báo để sinh viên kịp thời chấn chỉnh thái độ và kết quả học tập.
2. Sinh viên bị cảnh báo kết quả học tập nếu rơi vào một trong các trường hợp sau:
a) Điểm trung bình chung tích lũy (CPA) không đạt mức sàn tối thiểu:
- Dưới 1.20 đối với sinh viên năm thứ nhất;
- Dưới 1.40 đối với sinh viên năm thứ hai;
- Dưới 1.60 đối với sinh viên năm thứ ba;
- Dưới 1.80 đối với các năm tiếp theo cho đến cuối khóa học;
b) Có điểm trung bình học kỳ (GPA) đạt dưới 0.80 trong một học kỳ chính;
c) Tổng số tín chỉ bị nợ đọng điểm F vượt quá 24 tín chỉ tính từ đầu khóa học.
3. Sinh viên bị cảnh báo học tập phải tham gia buổi tư vấn bắt buộc với Cố vấn học tập và chỉ được đăng ký tối đa 14 tín chỉ trong học kỳ tiếp theo."""
    },
    {
        "page": 25,
        "chapter": "Chương IV: Cảnh báo Học vụ, Buộc thôi học và Khen thưởng",
        "section": "Buộc Thôi học",
        "article": "Điều 24. Các trường hợp sinh viên bị buộc thôi học",
        "text": """CHƯƠNG IV: CẢNH BÁO HỌC VỤ, BUỘC THÔI HỌC VÀ KHEN THƯỞNG
Điều 24. Xử lý buộc thôi học đối với sinh viên
1. Sinh viên bị buộc thôi học nếu thuộc một trong các trường hợp sau đây:
a) Bị cảnh báo học tập 2 lần liên tiếp theo quy định tại Điểm a Khoản 2 Điều 23;
b) Có tổng số lần bị cảnh báo học tập vượt quá 3 lần trong toàn khóa học;
c) Vượt quá thời gian học tập tối đa toàn khóa theo quy định tại Điều 3 (vượt quá 6 năm đối với khóa 4 năm);
d) Bị kỷ luật ở mức buộc thôi học do vi phạm pháp luật hoặc vi phạm quy chế thi cử nghiêm trọng;
đ) Tự ý bỏ học không đăng ký học phần trong 1 học kỳ chính mà không có lý do chính đáng được chấp thuận.
2. Quyết định buộc thôi học do Hiệu trưởng ký ban hành trên cơ sở đề xuất của Hội đồng Khen thưởng và Kỷ luật trường.
3. Sinh viên bị buộc thôi học được cấp giấy chứng nhận kết quả học tập cho các học phần đã tích lũy thành công."""
    },
    {
        "page": 26,
        "chapter": "Chương IV: Cảnh báo Học vụ, Buộc thôi học và Khen thưởng",
        "section": "Học bổng Khuyến khích",
        "article": "Điều 25. Tiêu chuẩn xét cấp học bổng khuyến khích học tập",
        "text": """CHƯƠNG IV: CẢNH BÁO HỌC VỤ, BUỘC THÔI HỌC VÀ KHEN THƯỞNG
Điều 25. Điều kiện và mức học bổng khuyến khích học tập
1. Học bổng khuyến khích học tập được xét cấp theo từng học kỳ chính cho sinh viên đạt thành tích xuất sắc và giỏi trong học tập và rèn luyện.
2. Điều kiện được đưa vào danh sách xét học bổng:
a) Đăng ký và tích lũy tối thiểu 15 tín chỉ trong học kỳ xét học bổng;
b) Không có học phần nào trong học kỳ bị điểm F hoặc phải thi lại;
c) Điểm rèn luyện đạt loại Khá (từ 70 điểm) trở lên;
d) Điểm GPA học kỳ đạt từ 3.20 trở lên.
3. Các mức học bổng khuyến khích học tập:
a) Học bổng loại Xuất sắc: GPA từ 3.60 đến 4.00 và điểm rèn luyện loại Xuất sắc (từ 90 điểm), mức học bổng bằng 120% mức học phí chuẩn;
b) Học bổng loại Giỏi: GPA từ 3.20 đến 3.59 và điểm rèn luyện loại Tốt (từ 80 điểm), mức học bổng bằng 100% mức học phí chuẩn;
c) Học bổng loại Khá: GPA từ 2.80 đến 3.19 và rèn luyện Khá, mức học bổng bằng 80% mức học phí chuẩn."""
    },
    {
        "page": 27,
        "chapter": "Chương IV: Cảnh báo Học vụ, Buộc thôi học và Khen thưởng",
        "section": "Miễn giảm Học phí",
        "article": "Điều 26. Chính sách miễn giảm học phí và trợ cấp xã hội",
        "text": """CHƯƠNG IV: CẢNH BÁO HỌC VỤ, BUỘC THÔI HỌC VÀ KHEN THƯỞNG
Điều 26. Miễn giảm học phí và hỗ trợ chi phí học tập
1. Chế độ miễn giảm học phí được thực hiện nghiêm túc theo quy định của Chính phủ và chính sách an sinh của nhà trường:
a) Miễn 100% học phí đối với: Sinh viên là con thương binh, con liệt sĩ; sinh viên khuyết tật nặng; sinh viên mồ côi cả cha lẫn mẹ không nơi nương tựa;
b) Giảm 70% học phí đối với: Sinh viên dân tộc thiểu số tại các thôn bản đặc biệt khó khăn, vùng sâu vùng xa;
c) Giảm 50% học phí đối với: Sinh viên là con cán bộ, công nhân viên chức bị tai nạn lao động hoặc mắc bệnh nghề nghiệp.
2. Hồ sơ xét miễn giảm học phí phải nộp về Phòng Công tác Sinh viên trong vòng 30 ngày kể từ ngày bắt đầu học kỳ mới.
3. Sinh viên thuộc diện chính sách vẫn phải đảm bảo tiến độ học tập và không được xét miễn học phí cho các học phần đăng ký học lại do bị điểm F."""
    },
    {
        "page": 28,
        "chapter": "Chương IV: Cảnh báo Học vụ, Buộc thôi học và Khen thưởng",
        "section": "Khen thưởng Sinh viên",
        "article": "Điều 27. Danh hiệu thi đua và hình thức khen thưởng",
        "text": """CHƯƠNG IV: CẢNH BÁO HỌC VỤ, BUỘC THÔI HỌC VÀ KHEN THƯỞNG
Điều 27. Khen thưởng cá nhân và tập thể sinh viên
1. Định kỳ cuối mỗi năm học, nhà trường xét khen thưởng các danh hiệu thi đua:
a) Danh hiệu "Sinh viên Xuất sắc": Đạt GPA năm học từ 3.60 trở lên và điểm rèn luyện đạt loại Xuất sắc;
b) Danh hiệu "Sinh viên Giỏi": Đạt GPA năm học từ 3.20 đến 3.59 và điểm rèn luyện đạt loại Tốt trở lên;
c) Danh hiệu "Thủ khoa Tốt nghiệp": Trao tặng cho sinh viên có điểm CPA cao nhất ngành học và đạt chuẩn rèn luyện Xuất sắc.
2. Sinh viên đạt giải cao trong các kỳ thi Nghiên cứu khoa học cấp Bộ, Olympic sinh viên toàn quốc hoặc các giải thưởng khởi nghiệp sáng tạo được tặng Giấy khen của Hiệu trưởng kèm tiền thưởng tương ứng.
3. Sinh viên bị kỷ luật từ mức khiển trách trở lên trong năm học sẽ không được xét bất kỳ danh hiệu thi đua khen thưởng nào."""
    },
    {
        "page": 29,
        "chapter": "Chương IV: Cảnh báo Học vụ, Buộc thôi học và Khen thưởng",
        "section": "Kỷ luật Sinh viên",
        "article": "Điều 28. Các mức độ kỷ luật và quy trình xét kỷ luật",
        "text": """CHƯƠNG IV: CẢNH BÁO HỌC VỤ, BUỘC THÔI HỌC VÀ KHEN THƯỞNG
Điều 28. Các mức độ xử lý kỷ luật sinh viên
1. Sinh viên vi phạm quy chế đào tạo, nội quy ký túc xá hoặc pháp luật sẽ chịu một trong các hình thức kỷ luật sau:
a) Khiển trách: Áp dụng đối với vi phạm lần đầu ở mức độ nhẹ; thời gian thử thách là 3 tháng;
b) Cảnh cáo: Áp dụng đối với sinh viên đã bị khiển trách mà tái phạm hoặc có hành vi gian lận trong học tập; thời gian thử thách là 6 tháng;
c) Đình chỉ học tập có thời hạn (1 học kỳ hoặc 1 năm học): Áp dụng đối với sinh viên vi phạm nghiêm trọng nội quy hoặc bị xử lý hành chính;
d) Buộc thôi học: Áp dụng đối với hành vi phạm pháp hình sự hoặc tái phạm sau khi bị đình chỉ học tập.
2. Sinh viên bị kỷ luật mức Cảnh cáo sẽ bị hạ một bậc xếp loại rèn luyện và không được xét học bổng khuyến khích học tập trong học kỳ đó."""
    },
    {
        "page": 30,
        "chapter": "Chương IV: Cảnh báo Học vụ, Buộc thôi học và Khen thưởng",
        "section": "Điểm Rèn luyện",
        "article": "Điều 28b. Đánh giá kết quả rèn luyện của sinh viên",
        "text": """CHƯƠNG IV: CẢNH BÁO HỌC VỤ, BUỘC THÔI HỌC VÀ KHEN THƯỞNG
Điều 28b. Tiêu chuẩn đánh giá điểm rèn luyện
1. Điểm rèn luyện được đánh giá theo thang điểm 100 vào cuối mỗi học kỳ chính, căn cứ vào 5 tiêu chí:
a) Ý thức tham gia học tập (tối đa 20 điểm);
b) Ý thức chấp hành nội quy, quy chế nhà trường (tối đa 25 điểm);
c) Ý thức tham gia các hoạt động chính trị, xã hội, văn hóa, thể thao (tối đa 20 điểm);
d) Ý thức công dân trong quan hệ cộng đồng (tối đa 25 điểm);
đ) Ý thức và kết quả tham gia phụ trách lớp, đoàn thể, thành tích đặc biệt (tối đa 10 điểm).
2. Xếp loại rèn luyện:
- Từ 90 đến 100 điểm: Xuất sắc;
- Từ 80 đến 89 điểm: Tốt;
- Từ 65 đến 79 điểm: Khá;
- Từ 50 đến 64 điểm: Trung bình;
- Từ 35 đến 49 điểm: Yếu;
- Dưới 35 điểm: Kém.
3. Sinh viên bị xếp loại rèn luyện Yếu, Kém trong hai học kỳ liên tiếp sẽ bị đưa vào diện xem xét kỷ luật."""
    },

    # CHƯƠNG V: THỰC TẬP, ĐỒ ÁN VÀ TỐT NGHIỆP (Trang 31 - 36)
    {
        "page": 31,
        "chapter": "Chương V: Thực tập, Khóa luận và Tốt nghiệp",
        "section": "Thực tập Doanh nghiệp",
        "article": "Điều 29. Quy định về thực tập tốt nghiệp và kỳ thực tế",
        "text": """CHƯƠNG V: THỰC TẬP, KHÓA LUẬN VÀ TỐT NGHIỆP
Điều 29. Tổ chức thực tập tốt nghiệp và kỳ trải nghiệm thực tế
1. Thực tập tốt nghiệp là học phần bắt buộc có khối lượng từ 4 đến 6 tín chỉ đối với mọi ngành đào tạo.
2. Điều kiện để sinh viên được đăng ký thực tập tốt nghiệp:
a) Đã tích lũy tối thiểu 75% tổng khối lượng tín chỉ của chương trình đào tạo;
b) Không bị kỷ luật từ mức đình chỉ học tập trở lên tại thời điểm đăng ký;
c) Đã hoàn thành các học phần cơ sở ngành theo quy định của Khoa.
3. Thời gian thực tập tại cơ quan, doanh nghiệp kéo dài tối thiểu 8 tuần liên tục toàn thời gian. Sinh viên phải có nhật ký thực tập và phiếu nhận xét có đóng dấu xác nhận của người hướng dẫn tại doanh nghiệp.
4. Báo cáo thực tập được chấm bởi giảng viên hướng dẫn và giảng viên chấm phản biện của Khoa theo thang điểm 10."""
    },
    {
        "page": 32,
        "chapter": "Chương V: Thực tập, Khóa luận và Tốt nghiệp",
        "section": "Đồ án Khóa luận",
        "article": "Điều 30. Điều kiện nhận đồ án và khóa luận tốt nghiệp",
        "text": """CHƯƠNG V: THỰC TẬP, KHÓA LUẬN VÀ TỐT NGHIỆP
Điều 30. Tiêu chuẩn làm đồ án và khóa luận tốt nghiệp
1. Khóa luận hoặc đồ án tốt nghiệp có khối lượng từ 6 đến 10 tín chỉ tùy theo chương trình cử nhân hay kỹ sư.
2. Sinh viên được giao làm đồ án/khóa luận tốt nghiệp khi đáp ứng đồng thời các tiêu chí sau:
a) Tích lũy tối thiểu 85% tổng số tín chỉ của chương trình đào tạo;
b) Điểm trung bình chung tích lũy CPA đạt từ 2.00 trở lên;
c) Không bị cảnh báo học tập hoặc nợ đọng quá 8 tín chỉ học phần bắt buộc.
3. Sinh viên không đủ điều kiện làm khóa luận tốt nghiệp phải đăng ký học các học phần chuyên môn tự chọn thay thế có khối lượng tín chỉ tương đương.
4. Thời gian hoàn thành khóa luận là 15 tuần kể từ ngày có quyết định giao đề tài của Hiệu trưởng."""
    },
    {
        "page": 33,
        "chapter": "Chương V: Thực tập, Khóa luận và Tốt nghiệp",
        "section": "Bảo vệ Đồ án",
        "article": "Điều 31. Quy trình bảo vệ và đánh giá đồ án tốt nghiệp",
        "text": """CHƯƠNG V: THỰC TẬP, KHÓA LUẬN VÀ TỐT NGHIỆP
Điều 31. Đánh giá và bảo vệ khóa luận tốt nghiệp
1. Khóa luận hoặc đồ án tốt nghiệp trước khi bảo vệ phải được kiểm tra đạo văn qua phần mềm chuyên dụng; tỷ lệ trùng lặp nội dung không được vượt quá 20%.
2. Hội đồng chấm khóa luận tốt nghiệp gồm từ 3 đến 5 thành viên là các giảng viên hoặc chuyên gia có học vị thạc sĩ trở lên.
3. Cơ cấu điểm đánh giá khóa luận tốt nghiệp:
a) Điểm của giảng viên hướng dẫn: Chiếm 30% tổng điểm;
b) Điểm của giảng viên phản biện: Chiếm 20% tổng điểm;
c) Điểm của Hội đồng chấm tại buổi bảo vệ: Chiếm 50% tổng điểm.
4. Sinh viên bảo vệ đạt điểm từ 5.0 trở lên (theo thang 10) được công nhận hoàn thành khóa luận. Sinh viên có điểm dưới 5.0 phải chỉnh sửa và bảo vệ lại trước Hội đồng phụ trong vòng 4 tuần."""
    },
    {
        "page": 34,
        "chapter": "Chương V: Thực tập, Khóa luận và Tốt nghiệp",
        "section": "Công nhận Tốt nghiệp",
        "article": "Điều 32. Điều kiện xét và công nhận tốt nghiệp đại học",
        "text": """CHƯƠNG V: THỰC TẬP, KHÓA LUẬN VÀ TỐT NGHIỆP
Điều 32. Điều kiện xét công nhận tốt nghiệp
1. Sinh viên được công nhận tốt nghiệp khi hội đủ các điều kiện sau:
a) Tích lũy đủ số tín chỉ và hoàn thành đầy đủ các học phần theo quy định của chương trình đào tạo;
b) Điểm trung bình chung tích lũy toàn khóa CPA đạt từ 2.00 trở lên (theo thang 4);
c) Đạt chuẩn đầu ra về ngoại ngữ và chuẩn kỹ năng công nghệ thông tin theo Điều 6;
d) Đạt chứng chỉ Giáo dục thể chất và chứng chỉ Giáo dục quốc phòng - an ninh;
đ) Tại thời điểm xét tốt nghiệp không bị truy cứu trách nhiệm hình sự hoặc không đang trong thời gian bị kỷ luật từ mức đình chỉ học tập trở lên.
2. Hội đồng xét tốt nghiệp họp định kỳ mỗi năm 3 đợt (tháng 3, tháng 6 và tháng 10) để xem xét hồ sơ của sinh viên."""
    },
    {
        "page": 35,
        "chapter": "Chương V: Thực tập, Khóa luận và Tốt nghiệp",
        "section": "Xếp loại Tốt nghiệp",
        "article": "Điều 33. Tiêu chuẩn xếp hạng và hạ bậc bằng tốt nghiệp",
        "text": """CHƯƠNG V: THỰC TẬP, KHÓA LUẬN VÀ TỐT NGHIỆP
Điều 33. Xếp loại tốt nghiệp và quy định hạ bậc tốt nghiệp
1. Hạng tốt nghiệp được xác định theo điểm trung bình chung tích lũy CPA toàn khóa:
a) Loại Xuất sắc: CPA từ 3.60 đến 4.00;
b) Loại Giỏi: CPA từ 3.20 đến 3.59;
c) Loại Khá: CPA từ 2.50 đến 3.19;
d) Loại Trung bình: CPA từ 2.00 đến 2.49.
2. Quy định hạ một bậc xếp loại tốt nghiệp:
Hạng tốt nghiệp của sinh viên có điểm CPA đạt mức Xuất sắc hoặc Giỏi sẽ bị giảm đi một bậc (ví dụ Xuất sắc xuống Giỏi, Giỏi xuống Khá) nếu thuộc một trong các trường hợp sau:
a) Khối lượng của các học phần phải học lại vượt quá 5% so với tổng số tín chỉ quy định cho toàn bộ chương trình đào tạo;
b) Sinh viên đã bị xử lý kỷ luật trong thời gian học từ mức cảnh cáo cấp trường trở lên."""
    },
    {
        "page": 36,
        "chapter": "Chương V: Thực tập, Khóa luận và Tốt nghiệp",
        "section": "Cấp Bằng và Hồ sơ",
        "article": "Điều 34. Cấp bằng tốt nghiệp và hiệu lực thi hành",
        "text": """CHƯƠNG V: THỰC TẬP, KHÓA LUẬN VÀ TỐT NGHIỆP
Điều 34. Cấp văn bằng và điều khoản thi hành quy chế
1. Bằng tốt nghiệp đại học được cấp theo mẫu phôi văn bằng chuẩn của Bộ Giáo dục và Đào tạo kèm theo Phụ lục văn bằng chi tiết.
2. Phụ lục văn bằng ghi rõ: Tên ngành đào tạo, chuyên ngành, tên các học phần đã tích lũy, số tín chỉ, điểm chữ và điểm số quy đổi, điểm trung bình toàn khóa CPA và xếp hạng tốt nghiệp.
3. Sinh viên chưa đủ điều kiện tốt nghiệp được cấp Giấy chứng nhận hoàn thành các môn học đã tích lũy trong vòng 5 năm để có thể đăng ký hoàn thành các điều kiện còn thiếu.
4. Quy chế này có hiệu lực thi hành kể từ ngày ký quyết định ban hành và áp dụng cho tất cả các khóa sinh viên chính quy đang học tập tại trường."""
    }
]

# Generate PDF using pymupdf
def create_pdf(output_path: Path):
    doc = pymupdf.open()
    font_path = "C:/Windows/Fonts/arial.ttf"
    
    for p in PAGES_DATA:
        page = doc.new_page(width=595, height=842) # A4
        page.insert_font(fontname="Arial", fontfile=font_path)
        
        # Header banner
        page.draw_rect(pymupdf.Rect(40, 35, 555, 65), fill=(0.93, 0.95, 0.98), color=(0.7, 0.8, 0.9))
        header_text = f"QUY CHẾ ĐÀO TẠO ĐẠI HỌC - {p['chapter']}"
        page.insert_text((50, 52), header_text, fontname="Arial", fontsize=9, color=(0.1, 0.3, 0.6))
        
        # Article title
        page.insert_text((50, 90), p["article"], fontname="Arial", fontsize=12, color=(0.8, 0.1, 0.1))
        
        # Section text
        text_lines = p["text"].split("\n")
        y = 120
        for line in text_lines:
            if not line.strip():
                y += 10
                continue
            # wrap line if too long
            if len(line) > 85:
                # break into two lines
                words = line.split(" ")
                cur = ""
                for w in words:
                    if len(cur + " " + w) > 85:
                        page.insert_text((50, y), cur.strip(), fontname="Arial", fontsize=10.5, color=(0.1, 0.1, 0.1))
                        y += 18
                        cur = w
                    else:
                        cur += " " + w
                if cur.strip():
                    page.insert_text((50, y), cur.strip(), fontname="Arial", fontsize=10.5, color=(0.1, 0.1, 0.1))
                    y += 18
            else:
                page.insert_text((50, y), line.strip(), fontname="Arial", fontsize=10.5, color=(0.1, 0.1, 0.1))
                y += 18
        
        # Footer
        footer_text = f"Trang {p['page']} / {len(PAGES_DATA)} - Quy chế Đào tạo Tín chỉ"
        page.insert_text((240, 810), footer_text, fontname="Arial", fontsize=9, color=(0.5, 0.5, 0.5))
        page.draw_line(pymupdf.Point(40, 795), pymupdf.Point(555, 795), color=(0.8, 0.8, 0.8))

    doc.save(str(output_path))
    doc.close()
    print(f"Generated PDF with {len(PAGES_DATA)} pages at {output_path}")

# Generate manifest.json
def create_manifest(manifest_path: Path):
    manifest = {
        "source_id": "quy-che-dao-tao-tin-chi-2024",
        "title": "Quy chế Đào tạo Trình độ Đại học theo Hệ thống Tín chỉ",
        "source_path_or_url": "starter/data/corpus.pdf",
        "license_or_permission": "Public Domain (Văn bản Quy phạm Đào tạo Đại học theo Luật Giáo dục Đại học)",
        "accessed_at": "2026-11-14",
        "total_physical_pages": len(PAGES_DATA),
        "content_pages": list(range(1, len(PAGES_DATA) + 1)),
        "page_counting_rule": "Tính toàn bộ 36 trang nội dung quy chế chính thức, không có trang bìa hay trang rỗng.",
        "pages_meta": [
            {
                "page": p["page"],
                "chapter": p["chapter"],
                "section": p["section"],
                "char_count": len(p["text"])
            }
            for p in PAGES_DATA
        ]
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"Created manifest at {manifest_path}")

# 20 Benchmark Questions (15 dev, 5 test), 3 metadata filters (1 in test)
QUESTIONS = [
    # DEV QUESTIONS (15 câu)
    {
        "id": "q01",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Khối lượng học tập toàn khóa tối thiểu đối với trình độ cử nhân là bao nhiêu tín chỉ?",
        "expected_answer": "Tối thiểu là 120 tín chỉ.",
        "gold_source_id": "quy-che-dao-tao-tin-chi-2024",
        "gold_page": 2,
        "evidence_quote": "Khối lượng học tập toàn khóa đối với trình độ cử nhân tối thiểu là 120 tín chỉ",
        "filter": None
    },
    {
        "id": "q02",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Thời gian học tập tối đa cho chương trình đào tạo chuẩn 4 năm là bao lâu?",
        "expected_answer": "Không quá 6 năm (12 học kỳ chính).",
        "gold_source_id": "quy-che-dao-tao-tin-chi-2024",
        "gold_page": 3,
        "evidence_quote": "Không quá 6 năm (12 học kỳ chính) đối với chương trình chuẩn 4 năm",
        "filter": None
    },
    {
        "id": "q03",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Một tín chỉ học phần lý thuyết được quy chuẩn bằng bao nhiêu tiết giảng dạy trên lớp?",
        "expected_answer": "15 tiết giảng dạy trên lớp.",
        "gold_source_id": "quy-che-dao-tao-tin-chi-2024",
        "gold_page": 4,
        "evidence_quote": "Một tín chỉ học tập lý thuyết được quy chuẩn bằng 15 tiết giảng dạy trên lớp",
        "filter": None
    },
    {
        "id": "q04",
        "split": "dev",
        "type": "dieu_kien",
        "question": "Học phần tiên quyết khác với học phần học trước như thế nào?",
        "expected_answer": "Học phần tiên quyết bắt buộc phải tích lũy đạt mới được học học phần sau, còn học phần học trước chỉ cần hoàn thành đánh giá.",
        "gold_source_id": "quy-che-dao-tao-tin-chi-2024",
        "gold_page": 5,
        "evidence_quote": "Học phần A là tiên quyết của học phần B khi sinh viên bắt buộc phải tích lũy đạt học phần A mới được phép đăng ký học phần B",
        "filter": None
    },
    {
        "id": "q05",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Chuẩn đầu ra ngoại ngữ tối thiểu đối với sinh viên tốt nghiệp chương trình đại học chính quy là gì?",
        "expected_answer": "Tương đương Bậc 3 theo Khung năng lực ngoại ngữ 6 bậc dùng cho Việt Nam (TOEIC 450, IELTS 4.5, hoặc B1).",
        "gold_source_id": "quy-che-dao-tao-tin-chi-2024",
        "gold_page": 6,
        "evidence_quote": "đạt chuẩn đầu ra ngoại ngữ tương đương Bậc 3 theo Khung năng lực ngoại ngữ 6 bậc dùng cho Việt Nam",
        "filter": None
    },
    {
        "id": "q06",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Số tín chỉ tối thiểu và tối đa mà sinh viên được đăng ký trong mỗi học kỳ chính là bao nhiêu?",
        "expected_answer": "Tối thiểu 12 tín chỉ và tối đa 24 tín chỉ.",
        "gold_source_id": "quy-che-dao-tao-tin-chi-2024",
        "gold_page": 8,
        "evidence_quote": "Khối lượng học tập tối thiểu: 12 tín chỉ trong mỗi học kỳ chính",
        "filter": None
    },
    {
        "id": "q07",
        "split": "dev",
        "type": "metadata_filter",
        "question": "Sinh viên đang bị cảnh báo học tập thì được đăng ký tối đa bao nhiêu tín chỉ trong học kỳ kế tiếp?",
        "expected_answer": "Tối đa 14 tín chỉ.",
        "gold_source_id": "quy-che-dao-tao-tin-chi-2024",
        "gold_page": 8,
        "evidence_quote": "Sinh viên đang trong tình trạng bị cảnh báo học tập chỉ được phép đăng ký tối đa 14 tín chỉ trong học kỳ kế tiếp",
        "filter": {"chapter": "Chương II: Tổ chức Đào tạo và Quản lý Học vụ"}
    },
    {
        "id": "q08",
        "split": "dev",
        "type": "dieu_kien",
        "question": "Thời hạn cho phép rút bớt học phần đã đăng ký trong học kỳ chính là bao lâu?",
        "expected_answer": "Trong vòng 2 tuần đầu tiên tính từ ngày bắt đầu học kỳ chính.",
        "gold_source_id": "quy-che-dao-tao-tin-chi-2024",
        "gold_page": 9,
        "evidence_quote": "chỉ được chấp nhận trong vòng 2 tuần đầu tiên tính từ ngày bắt đầu học kỳ chính",
        "filter": None
    },
    {
        "id": "q09",
        "split": "dev",
        "type": "dieu_kien",
        "question": "Sinh viên được phép đăng ký học cải thiện điểm đối với các học phần đạt điểm mấy?",
        "expected_answer": "Chỉ được phép học cải thiện đối với điểm D, D+ hoặc C; không cho phép đối với điểm B trở lên.",
        "gold_source_id": "quy-che-dao-tao-tin-chi-2024",
        "gold_page": 10,
        "evidence_quote": "Sinh viên chỉ được phép đăng ký học cải thiện đối với các học phần đã đạt điểm D, D+ hoặc C",
        "filter": None
    },
    {
        "id": "q10",
        "split": "dev",
        "type": "dieu_kien",
        "question": "Điều kiện về điểm CPA để sinh viên được đăng ký học chương trình đào tạo thứ hai (ngành kép) là gì?",
        "expected_answer": "Điểm CPA của chương trình thứ nhất đạt từ 2.80 trở lên (hoặc 2.50 nếu rèn luyện Tốt).",
        "gold_source_id": "quy-che-dao-tao-tin-chi-2024",
        "gold_page": 13,
        "evidence_quote": "Điểm trung bình tích lũy CPA của chương trình thứ nhất đạt từ 2.80 trở lên",
        "filter": None
    },
    {
        "id": "q11",
        "split": "dev",
        "type": "metadata_filter",
        "question": "Điểm thi kết thúc học phần chiếm tỷ trọng bao nhiêu phần trăm trong tổng điểm học phần lý thuyết?",
        "expected_answer": "Chiếm từ 50% đến 60% tổng điểm học phần.",
        "gold_source_id": "quy-che-dao-tao-tin-chi-2024",
        "gold_page": 15,
        "evidence_quote": "Điểm thi kết thúc học phần: Chiếm từ 50% đến 60% tổng điểm học phần",
        "filter": {"chapter": "Chương III: Đánh giá Kết quả Học tập và Thang điểm"}
    },
    {
        "id": "q12",
        "split": "dev",
        "type": "dieu_kien",
        "question": "Sinh viên cần đáp ứng điều kiện chuyên cần nào để được dự thi kết thúc học phần?",
        "expected_answer": "Tham gia tối thiểu 80% tổng số tiết lý thuyết và 100% các buổi thực hành/thí nghiệm.",
        "gold_source_id": "quy-che-dao-tao-tin-chi-2024",
        "gold_page": 16,
        "evidence_quote": "Tham gia tối thiểu 80% tổng số tiết giảng dạy lý thuyết và 100% các buổi thực hành/thí nghiệm",
        "filter": None
    },
    {
        "id": "q13",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Điểm tổng kết thang 10 từ 8.5 đến 10.0 quy đổi sang điểm chữ và thang 4 là bao nhiêu?",
        "expected_answer": "Điểm chữ A, tương đương 4.0 trên thang điểm 4.",
        "gold_source_id": "quy-che-dao-tao-tin-chi-2024",
        "gold_page": 17,
        "evidence_quote": "Từ 8.5 đến 10.0: Điểm A (Tương đương 4.0 trên thang 4) - Xếp loại Xuất sắc",
        "filter": None
    },
    {
        "id": "q14",
        "split": "dev",
        "type": "dien_dat_lai",
        "question": "Điểm số của các học phần Giáo dục thể chất và Giáo dục quốc phòng có tính vào điểm GPA hay CPA không?",
        "expected_answer": "Không tính vào GPA và CPA, chỉ dùng để xét điều kiện tốt nghiệp.",
        "gold_source_id": "quy-che-dao-tao-tin-chi-2024",
        "gold_page": 18,
        "evidence_quote": "điểm của các học phần này không tính vào GPA và CPA",
        "filter": None
    },
    {
        "id": "q15",
        "split": "dev",
        "type": "dieu_kien",
        "question": "Sinh viên năm thứ nhất có điểm CPA dưới bao nhiêu thì bị áp dụng cảnh báo học vụ?",
        "expected_answer": "CPA dưới 1.20.",
        "gold_source_id": "quy-che-dao-tao-tin-chi-2024",
        "gold_page": 24,
        "evidence_quote": "Dưới 1.20 đối với sinh viên năm thứ nhất",
        "filter": None
    },

    # TEST QUESTIONS (5 câu)
    {
        "id": "q16",
        "split": "test",
        "type": "dieu_kien",
        "question": "Sinh viên bị buộc thôi học khi bị cảnh báo học tập bao nhiêu lần liên tiếp?",
        "expected_answer": "Bị cảnh báo học tập 2 lần liên tiếp.",
        "gold_source_id": "quy-che-dao-tao-tin-chi-2024",
        "gold_page": 25,
        "evidence_quote": "Bị cảnh báo học tập 2 lần liên tiếp theo quy định tại Điểm a Khoản 2 Điều 23",
        "filter": None
    },
    {
        "id": "q17",
        "split": "test",
        "type": "metadata_filter",
        "question": "Điều kiện về số tín chỉ tích lũy tối thiểu trong học kỳ để sinh viên được xét học bổng khuyến khích học tập là gì?",
        "expected_answer": "Đăng ký và tích lũy tối thiểu 15 tín chỉ trong học kỳ xét.",
        "gold_source_id": "quy-che-dao-tao-tin-chi-2024",
        "gold_page": 26,
        "evidence_quote": "Đăng ký và tích lũy tối thiểu 15 tín chỉ trong học kỳ xét học bổng",
        "filter": {"chapter": "Chương IV: Cảnh báo Học vụ, Buộc thôi học và Khen thưởng"}
    },
    {
        "id": "q18",
        "split": "test",
        "type": "dieu_kien",
        "question": "Để được nhận làm đồ án hoặc khóa luận tốt nghiệp, sinh viên phải tích lũy tối thiểu bao nhiêu phần trăm số tín chỉ của chương trình và điểm CPA tối thiểu là bao nhiêu?",
        "expected_answer": "Tích lũy tối thiểu 85% tổng số tín chỉ và điểm CPA đạt từ 2.00 trở lên.",
        "gold_source_id": "quy-che-dao-tao-tin-chi-2024",
        "gold_page": 32,
        "evidence_quote": "Tích lũy tối thiểu 85% tổng số tín chỉ của chương trình đào tạo; Điểm trung bình chung tích lũy CPA đạt từ 2.00 trở lên",
        "filter": None
    },
    {
        "id": "q19",
        "split": "test",
        "type": "truc_tiep",
        "question": "Điểm trung bình chung tích lũy toàn khóa CPA tối thiểu để sinh viên được xét công nhận tốt nghiệp đại học là bao nhiêu?",
        "expected_answer": "CPA đạt từ 2.00 trở lên.",
        "gold_source_id": "quy-che-dao-tao-tin-chi-2024",
        "gold_page": 34,
        "evidence_quote": "Điểm trung bình chung tích lũy toàn khóa CPA đạt từ 2.00 trở lên (theo thang 4)",
        "filter": None
    },
    {
        "id": "q20",
        "split": "test",
        "type": "ngoai_le",
        "question": "Sinh viên có điểm CPA đạt mức Xuất sắc sẽ bị hạ một bậc xếp loại tốt nghiệp xuống loại Giỏi trong những trường hợp nào?",
        "expected_answer": "Khi khối lượng học lại vượt quá 5% tổng số tín chỉ hoặc đã bị kỷ luật từ mức cảnh cáo cấp trường trở lên.",
        "gold_source_id": "quy-che-dao-tao-tin-chi-2024",
        "gold_page": 35,
        "evidence_quote": "học phần phải học lại vượt quá 5% so với tổng số tín chỉ quy định cho toàn bộ chương trình đào tạo",
        "filter": None
    }
]

def create_benchmark(benchmark_path: Path):
    with open(benchmark_path, "w", encoding="utf-8") as f:
        json.dump(QUESTIONS, f, ensure_ascii=False, indent=2)
    print(f"Created benchmark questions at {benchmark_path}")

if __name__ == "__main__":
    create_pdf(data_dir / "corpus.pdf")
    create_manifest(Path("data/manifest.json"))
    create_benchmark(benchmark_dir / "questions.json")

