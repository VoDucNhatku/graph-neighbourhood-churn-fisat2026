# Chạy lại paper #366956 trên Colab

1. Mở [Google Colab](https://colab.research.google.com/), chọn **File → Upload notebook** và tải `366956-reproduce.ipynb`.
2. Chọn **Runtime → Change runtime type → Hardware accelerator: None**. Bộ code hiện tại chạy CPU.
3. Giữ `RUN_MODE = "full"` để chạy cả suite. Chọn `"main"` nếu chỉ cần hai lượt CV chính và figure; vẫn đủ 10×5 folds.
4. Chọn **Run all**. Notebook tự clone code, ghim commit, tải dữ liệu UCI, kiểm hash và cài Python 3.13.5 riêng.
5. Đọc bảng **Paper / Raw / Cached k10**. Mọi số được giữ đúng output; không tự chỉnh số để khớp paper.
6. Tải ZIP kết quả ở cell cuối trước khi ngắt runtime. Có logs, manifest, bảng so sánh và figure; raw XLSX và cache từng customer không nằm trong ZIP.

Notebook tự chứa runner; chỉ cần upload `.ipynb`, không cần upload file `.py`, ZIP code hoặc raw data. Khi dùng local Jupyter, các cell vẫn tạo môi trường riêng; cần Git và kết nối mạng.

Code chính thức: [graph-neighbourhood-churn-fisat2026](https://github.com/VoDucNhatku/graph-neighbourhood-churn-fisat2026), commit `fdbbccfc8c0ee91fcefb8f8f3a82f0ee7ada89a4`. Raw: [UCI Online Retail II](https://archive.ics.uci.edu/dataset/502/online%2Bretail%2Bii), Chen, D. (2012), DOI 10.24432/C5CG6D, CC BY 4.0. Dữ liệu tải về được kiểm SHA256 giống bản ổ D đã audit.

Thực đo trên máy Windows ngày 12/10/2026: full suite **17 phút 42 giây**, raw CV **166 giây**, cached k10 **100 giây**; chưa tính cài môi trường. Chưa đo thời gian trên Colab. Chọn GPU không tự làm code CPU nhanh hơn; nguồn CPU Colab và thời gian cài/download có thể khác.

Đã kiểm notebook schema, compile cells, hash dữ liệu và helper so số với outputs thật. **Chưa chạy toàn bộ notebook trên Colab**; package build Linux và Windows có thể tạo số khác. Lượt local raw CV lệch nhẹ; cached k10 mới khớp archived folds. Cả hai giữ nguyên kết luận chưa phát hiện cải thiện có ý nghĩa so với RFM.

Đây là tái lập nguyên trạng. Các điểm cần làm rõ về cửa sổ ngày, L, neighbours, scope SHAP/ablation và provenance baseline trong paper chưa được sửa bằng notebook này. Full-data SHAP là phân tích mô tả hợp lệ, không tự động sai. Xem [báo cáo đầy đủ](../docs/vietnamese/04-bao-cao-tong-hop.md).

File `reproduce_366956.py` là runner để chạy bằng interpreter đúng Python 3.13.5 với `requirements.txt`; truyền `--repo`, `--data`, `--out` (thư mục mới) và `--mode full`. `--repo` phải là Git checkout ở commit đã ghim. Notebook đã cung cấp các lệnh này theo đúng môi trường.
