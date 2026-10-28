# Báo cáo tổng hợp paper, hội nghị và tái lập thực nghiệm

> Paper #366956 · Cập nhật 13/10/2026, giờ Việt Nam · Tài liệu dành cho thành viên nhóm đã biết Python và ML cơ bản.

## 1. Nghiên cứu này là gì và nhóm đã làm đến đâu?

Paper nghiên cứu dự đoán khách hàng ngừng mua trong bán lẻ không có hợp đồng. Tiêu đề đầy đủ là “When Graph-Derived Neighbourhood Features Do Not Help: A Leakage-Controlled Evaluation of Behavioural-LRFM Churn Prediction in Non-Contractual Retail”. Một cửa hàng bán lẻ không nhận được thông báo hủy hợp đồng từ khách. Nhóm vì vậy dùng việc khách không phát sinh giao dịch trong một khoảng tương lai làm nhãn churn, rồi dùng hành vi trước khoảng đó để dự đoán.

Câu hỏi trung tâm là: ngoài ba đặc trưng RFM quen thuộc, thêm độ dài quan hệ, các đặc trưng mua hàng chi tiết, phân khúc và thông tin từ graph khách hàng giống nhau có giúp dự đoán tốt hơn không? Nhóm không chỉ xây một mô hình rồi báo AUC cao, mà tăng dần nhóm đặc trưng, giữ các fold đánh giá ghép cặp, lặp cross-validation và kiểm định mức khác biệt.

Mục tiêu là kiểm chứng giá trị bổ sung của độ phức tạp. Đóng góp hợp lý của paper là một đánh giá thực nghiệm có kiểm soát rò rỉ nhãn và kết quả âm: chưa phát hiện cải thiện có ý nghĩa của các tier đặc trưng so với RFM trên dữ liệu, họ graph, mô hình và cấu hình đã xét. Không có căn cứ gọi mọi thành phần thuật toán là phát minh mới, hoặc suy kết quả này sang mọi cửa hàng và mọi graph.

Phương pháp nghiên cứu là thực nghiệm định lượng trên dữ liệu giao dịch thứ cấp, kết hợp feature engineering, graph analysis, học có giám sát, so sánh loại bỏ/bổ sung nhóm đặc trưng và kiểm định thống kê ghép cặp. Đây không phải nghiên cứu khảo sát, EFA, CFA hay phỏng vấn người tiêu dùng.

Tiến độ hiện tại: paper đã được chấp nhận; code, dữ liệu local và các bảng thực nghiệm đã có; suite hiện hành đã chạy lại ngày 12/10/2026; bộ tài liệu tiếng Việt này phục vụ học và phối hợp nhóm. Camera-ready chưa được sửa/nộp trong phiên làm việc này; chưa xác minh thanh toán đã hoàn tất. Nguồn nghiên cứu: [paper gốc](../../paper/main.pdf), [source LaTeX](../../paper/main.tex), [code](../../src/significance_test.py), [bằng chứng chạy lại](evidence/reproduction-manifest.json).

### 1.1. Cách trả lời ngắn khi được hỏi về đề tài

“Nhóm kiểm tra xem việc xây graph giữa các khách hàng có hành vi mua giống nhau có giúp dự đoán ngừng mua tốt hơn RFM không. Nhóm dùng Online Retail II, tạo các tier đặc trưng và so hai mô hình trên 10 lần lặp 5-fold CV. Kết quả cho thấy chưa có cải thiện có ý nghĩa do thêm các tier. Code và bảng fold scores đã có, đã chạy lại thành công. Nhóm đang hoàn thiện diễn giải và các điểm paper-code cần làm rõ trước camera-ready.”

Đoạn này mô tả phạm vi bằng chứng, không nói “graph vô dụng” hay “mô hình phức tạp luôn kém hơn”. Một graph dựa trên tương tác thật, chẳng hạn giới thiệu khách hàng, có thể mang thông tin khác với graph dựng lại từ chính các đặc trưng mà classifier đã có.

## 2. Hồ sơ bài accepted và PDF đang đọc

Paper **#366956** được xác nhận Accepted bằng email EAI ngày 06/10/2026 và ảnh Confy do tác giả cung cấp. Bài image cropping #366800 là bài khác, có trạng thái Rejected. Preview của một email thread từng nhắc bài image cropping; điều đó không thay đổi quyết định của paper LRFM.

Bản PDF tác giả xác định là file đã nộp đã được so với `paper/main.pdf`. Hai file có cùng nội dung text, decoded page content và pixels render trên 12/12 trang. File supplied dài hơn đúng một byte CR ở cuối, nên SHA256 toàn file khác nhưng nội dung nghiên cứu không đổi. Nguồn gốc bản PDF nộp là xác nhận của tác giả; không coi đây là một lần tải độc lập mới từ Confy.

Hash của `paper/main.pdf` là `b3803266c2d3d0601b22d5a51ce7c11e7a05e33c7e27367b2839c2a301b6bbd2`. Tên tác giả trên bản này là Duc Nhat Vo, FPT University. Danh sách contributors GitHub và dòng tác giả README là các thông tin khác với author list xuất bản; muốn thêm đồng tác giả phải chốt đồng thuận và cập nhật hồ sơ hội nghị cùng PDF/source.

Trong bản dịch đi kèm, các phát biểu gốc được giữ trung thành, kể cả những điểm audit đề nghị sửa. Đọc bản dịch để hiểu tác giả đã viết gì; đọc sổ tay và báo cáo này để phân biệt điều đó với code thực thi và mức bằng chứng.

## 3. Hội nghị: phí, camera-ready và tham dự

### 3.1. Phí đang công bố

Kiểm tra website ngày 13/10/2026. Đơn vị USD; ưu đãi công bố đến 30/10.

| Gói | Early member | Early nonmember | Regular member | Regular nonmember |
|---|---:|---:|---:|---:|
| Author, một paper | 450 | 565 | 540 | 675 |
| Author, hai papers | 675 | 845 | 815 | 1015 |
| Audience | 315 | 395 | 385 | 475 |

Online và onsite cùng phí. Phụ phí: extra page 30 USD, đổi invoice 30 USD, vé dinner thêm 65 USD, xử lý refund 60 USD. Portal tác giả cung cấp từng hiện gói một bài 450 USD. Tổng cuối cần đối chiếu checkout/invoice. Nguồn: [Registration FISAT](https://fisat.eai-conferences.org/2026/registration/).

### 3.2. Registration và người trình bày

Ít nhất một full author registration mới mở camera-ready; student/audience không thay thế gói đăng ký bài. Một registration cho một người. Chưa tìm được quy định công khai xác nhận số đồng tác giả cùng chia nhau thuyết trình một paper. Tìm social public cũng chưa xác nhận được riêng FISAT; anecdote hội nghị khác không đủ để kết luận. Nguồn: [Camera-ready instructions](https://fisat.eai-conferences.org/2026/camera-ready-instructions/).

### 3.3. Hạn và loại file

| Track | Camera-ready công bố | Trạng thái áp dụng cho #366956 |
|---|---|---|
| Main | 15/10/2026 | Chưa xác minh paper thuộc track này |
| Final | 29/10/2026 | Ngày accept 06/10 khớp notification; vẫn là suy luận |
| Last | 30/10/2026 | Không tự dùng hạn này cho paper khác track |

Hội nghị công bố 25-27/11/2026 tại TP.HCM, hybrid. Cần xem track/hạn riêng trong Confy trước khi chốt. Nguồn: [lịch FISAT](https://fisat.eai-conferences.org/2026/). Nộp PDF theo template và archive PDF + LaTeX/Word source; sửa qua Edit trước hạn. Wire transfer có thể mất tới 5 business days để mở quyền upload. Nguồn: [quy trình camera-ready](https://fisat.eai-conferences.org/2026/camera-ready-instructions/).

### 3.4. Thêm tác giả và giới hạn sửa

EAI FAQ cho biết có thể thêm/xóa coauthor khi upload camera-ready sau registration: [EAI Add authors](https://help.eai-conferences.org/faq/what-are-my-duties-3-9/). Springer có hạn chế thay authorship sau acceptance: [Book policies](https://www.springernature.com/gp/policies/book-publishing-policies). Do mốc khóa khác nhau, cần Conference Manager xác nhận quy trình áp dụng; khả năng bấm sửa trên form chưa đủ giải quyết chuẩn xuất bản.

Email acceptance mà tác giả cung cấp giới hạn sửa sát reviewer comments, ngữ pháp/phong cách và thông tin tác giả/tài trợ. Không tự thay nghiên cứu đã được review bằng nghiên cứu khác. Nếu sửa code làm đổi cohort/labels/results, cần fit lại và trình bày tác động minh bạch với chair. Báo cáo này chưa gửi email, chưa thanh toán và chưa nộp hồ sơ.

## 4. GitHub, code ổ D và dữ liệu có giống nhau không?

### 4.1. File tracked và version

Đợt kiểm ngày 12/10 đối chiếu 43/43 tracked files với remote tree ở commit `fdbbccfc8c0ee91fcefb8f8f3a82f0ee7ada89a4`: tất cả Git blobs khớp. So với tag `v1.0-submission`, commit này chỉ thay dòng tác giả README. Paper/source/results gốc giữ nguyên sau rerun. Tài liệu mới được thêm trong đợt 13/10, vì vậy không tiếp tục dùng “43 file” như tổng số mọi file repo sau khi publish bộ tài liệu.

Sidebar contributors đã được refresh về tài khoản chủ repo; sau đó tên Nguyễn Công Minh trong dòng Authors README được gỡ theo yêu cầu. Không rewrite commit history để tạo một bản nghiên cứu khác.

Nguồn: remote Git tree đã đối chiếu và [manifest nguồn](evidence/source-identity.json). Kho công khai: [graph-neighbourhood-churn-fisat2026](https://github.com/VoDucNhatku/graph-neighbourhood-churn-fisat2026).

### 4.2. Raw data và feature cache

Raw `online_retail_II.xlsx` local có 45.622.278 bytes. File raw ở thư mục project cha và bản tải trực tiếp UCI cùng SHA256:

`bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980`

GitHub không chứa raw XLSX, nên không có một file raw khác trên GitHub để so. Khẳng định đúng là code/metadata tracked khớp remote, và dữ liệu local khớp nguồn UCI. Notebook tải lại từ nguồn rồi kiểm hash. Nguồn: [UCI Online Retail II](https://archive.ics.uci.edu/dataset/502/online%2Bretail%2Bii), DOI 10.24432/C5CG6D, Chen (2012), CC BY 4.0; [kiểm hash tải trực tiếp](evidence/uci-download-verification.json).

Cache đặc trưng xây mới từ raw hôm 12/10 có 5.038 khách, 3.285 churners, tỷ lệ 65,2044462088%. CSV cache mới khớp byte cache archived: cùng customer IDs, không đổi nhãn, không có chênh numeric sau đọc CSV. Đây là kết quả xây cache mới, không chỉ mở cache cũ rồi giả định nó đúng.

## 5. Thực nghiệm đã chạy lại thật

### 5.1. Máy và cấu hình

Chạy local Windows CPU, 8 logical cores, CPython 3.13.5; cả 14 dependency ghim đều khớp `requirements.txt`. Tổng 10 jobs mất **17 phút 42 giây**. Code được copy sang snapshot, outputs mới tách riêng; không sửa source hoặc data để khớp số. Source/dataset hashes trước và sau giống nhau. Chi tiết runtime và exit codes: [manifest](evidence/reproduction-manifest.json).

| Job | Thời gian | Nội dung |
|---|---:|---|
| Pipeline | 191,95 giây | Features, graph, classifier CV, profiles, SHAP |
| Clustering comparison | 150,26 giây | Các phương pháp phân cụm/segmentation |
| Auxiliary variants | 147,39 giây | Các nhánh thử nghiệm phụ |
| Repeated CV raw | 166,28 giây | 10 × 5-fold, features trong RAM |
| k5 | 98,75 giây | CV đọc cache mới, graph k5 |
| k10 | 100,04 giây | CV đọc cache mới, graph k10 |
| k15 | 92,39 giây | CV đọc cache mới, graph k15 |
| k20 | 93,54 giây | CV đọc cache mới, graph k20 |
| Seed42 | 16,61 giây | Một lần 5-fold, cache mới |
| Figure | 3,31 giây | Vẽ kết quả từ CSV mới |

Tất cả exit 0. Script audit được chạy ở một bản copy chỉ redirect đường dẫn; nó không kiểm hết mọi claim khoa học, nên exit 0 của audit chưa đủ thay thế kiểm tra phương pháp.

### 5.2. So kết quả chính với paper

| Tier | AUC paper | Raw/RAM mới | Cache k10 mới | pNB cache |
|---|---:|---:|---:|---:|
| RFM | 0,8066 | 0,806553 | 0,806552 | Không áp dụng |
| LRFM | 0,8074 | 0,807439 | 0,807439 | 0,755133 |
| B-LRFM | 0,8054 | 0,805329 | 0,805354 | 0,741649 |
| B-LRFM+Seg | 0,8044 | 0,804295 | 0,804371 | 0,561393 |
| Graph-Enhanced | 0,8044 | 0,804533 | 0,804422 | 0,590480 |

Graph ở lượt raw/RAM có ΔAUC −0,002020653, pNB 0,606128662. Lượt đọc cache k10 mới có ΔAUC −0,002129839, pNB 0,590479796. Chênh AUC Graph giữa hai lượt khoảng 0,000110661. Cả hai vẫn chưa phát hiện cải thiện có ý nghĩa so với RFM.

Mười sáu phép thử tier-vs-RFM của hai classifier và hai metrics ở main đều p≥0,05; p nhỏ nhất khoảng 0,144163. Điều này là failure to reject trong phạm vi các phép thử đó. Không suy thành “mọi hiệu ứng đúng bằng 0”, “hai pipelines tương đương”, hoặc “graph vô dụng trên mọi bài toán”.

### 5.3. Tại sao có hai đường chạy?

Khi không có cache, `significance_test.py` xây DataFrame đặc trưng, ghi CSV và tiếp tục fit trên DataFrame trong RAM. Khi có cache, script đọc CSV bằng `pd.read_csv` rồi fit. Output đầu được khởi tạo trống; các lượt k-sweep dùng cache vừa tạo mới. Hai đường cho kết quả hơi khác dù source/runtime/seeds giữ nguyên. Chưa thực hiện controlled experiment chỉ đổi CSV parser/float precision để xác định cơ chế sai khác; không quy ngay cho library drift hay sửa dữ liệu.

Mười lăm trong 17 CSV main so trực tiếp cùng filename archived khớp byte. Hai file khác là folds/summary của lượt RAM đầu. Tám CSV k-sweep khớp byte archived tương ứng. Đặc biệt cached k10 khớp byte cả main archived folds và summary, do đó các số main trong paper được tái lập theo đường cached này. Pipeline single-seed, comparison, auxiliary, profiles và hai SHAP CSV cũng khớp byte sau fit mới.

Hai CSV seed42 từ cache mới không byte-identical với bộ `results_rerun/seed42` cũ. Không trộn các artifact đó với single-seed pipeline đã khớp byte. Với lượt seed42 mới, Graph AUC khoảng 0,810250, delta khoảng +0,003340 và pNB khoảng 0,560752; dấu gain một split không thay thế kết quả repeated CV.

### 5.4. Graph degree và cross-model

| k | ΔAUC Graph − RFM | pNB |
|---:|---:|---:|
| 5 | −0,000640 | 0,879792 |
| 10 | −0,002130 | 0,590480 |
| 15 | +0,001686 | 0,666325 |
| 20 | −0,002676 | 0,499681 |

Các số này khớp rounding Table 3. Việc k15 đổi dấu không tự chứng minh nguyên nhân là noise; bằng chứng trực tiếp là chưa có p<0,05 ở bốn cấu hình đã thử.

Table 2 có hai cross-model comparison p<0,05 và một p≈0,068. LR/RFM vs LightGBM/Graph đổi cả mô hình và features; không tách riêng tác dụng graph. So feature tiers riêng cần giữ classifier như Table 1. Phát biểu “only significant comparison” cần thu hẹp hoặc sửa; figure gốc cũng có wording tương tự. Bản dịch giữ câu gốc, các tài liệu hướng dẫn giải thích giới hạn.

Năm bộ CV, mỗi bộ 500 rows = 50 folds × 5 tiers × 2 classifiers, đã kiểm không trùng FoldId/Tier/Model. Mean và corrected p-values tái tính khớp summary trong 1e−12. Bằng chứng số chi tiết: [comparison JSON](evidence/comparison.json), [paper-vs-rerun CSV](evidence/paper-vs-rerun.csv), [archive-vs-rerun CSV](evidence/archive-vs-rerun.csv).

## 6. Điểm nào lệch thật, điểm nào là diễn giải cần thận trọng?

### 6.1. Định nghĩa L: lệch có bằng chứng trực tiếp

Paper viết L là số ngày giữa lần mua đầu và cuối. Hai script churn tính `ANALYSIS_DATE - first_purchase`. Đây là hai đại lượng khác nhau. Nếu mục đích là tái lập code hiện hành, mô tả phải nói đúng relationship age tới analysis date. Nếu mục đích là dùng last-minus-first, phải sửa code và kiểm lại kết quả; không chỉ đổi công thức trong paper rồi giữ output không tương ứng. Nguồn: [paper, dòng 256](../../paper/main.tex#L256), [code, dòng 133](../../src/significance_test.py#L133).

### 6.2. Ngày kết thúc: lệch giữa ngày trọn vẹn và timestamp

`Timestamp("2011-06-30")` và `Timestamp("2011-09-30")` là 00:00. Giao dịch ban ngày 30/6 bị chuyển sang prediction và ban ngày 30/9 bị bỏ. Audit raw đếm 1.186 và 1.451 giao dịch hợp lệ bị ảnh hưởng ở hai ngày đó. Cửa sổ trọn ngày có 5.041 khách và 28 nhãn đổi trên nhóm khách shared; **chưa fit lại model với cửa sổ đã sửa**. Q3 trọn ngày là 92 ngày, không phải đúng 90 ngày. Nguồn: [code boundaries](../../src/significance_test.py#L119).

### 6.3. Neighbours và preprocessing

NCR lấy outgoing list kNN k10. Graph tổng là union vô hướng; một khách có thể nhận thêm cạnh từ khách khác nên undirected neighbours không luôn chỉ là 10. Công thức paper cần định nghĩa chính xác tập dùng cho NCR. Graph feature scaling, KMeans, communities và median IPT được tính trên toàn bộ covariates trước CV; scaler classifier là fold-local. Gọi mọi preprocessing là fold-local sẽ không đúng. Đây là thiết lập transductive ở covariates; không tự chứng minh validation labels đã vào NCR/CCR của main CV.

CCR trên training rows có thể chứa nhãn của chính row đó; inner cross-fitting/leave-one-out target encoding là bước kiểm tra tiếp được đề xuất, chưa có experiment riêng chứng minh tác động. Nguồn: [graph và folds](../../src/significance_test.py#L185).

### 6.4. SHAP: điều chỉnh cách diễn giải audit

Full-data SHAP không tự động sai. Code fit một final model trên toàn dữ liệu và giải thích các mẫu từ dữ liệu đó; đây là mô tả model đã fit. Paper không tuyên bố riêng phần SHAP là held-out. Cách diễn đạt trước đó gộp nó như một lỗi tính toán là quá mạnh; nhận xét đúng là nên ghi rõ phạm vi và không dùng attribution làm bằng chứng lợi ích dự báo out-of-sample.

Main CV có các NCR/CCR fold-local khác với aggregates toàn cục cho SHAP. Không gọi main AUC bị leakage chỉ vì final SHAP dùng full data. Tuy nhiên so Seg→Graph thêm cùng lúc bốn static graph features và hai aggregates; chưa cô lập NCR. Câu “removing it costs nothing” đối với riêng NCR vượt bằng chứng ablation hiện có. Nguồn: [final fit và SHAP](../../src/run_pipeline_v2.py#L468).

### 6.5. Leiden, baseline .398 và phạm vi kết luận

Louvain và Leiden đều thực sự có partition/log. Nhưng repeated predictive CV đang dùng Louvain, chưa có controlled detector comparison tương đương cho Leiden. Các auxiliary runs có cách tạo label aggregates khác, nên không thay thế được phép so đó.

Paper viết tái lập silhouette .398 của baseline. Local approximation trong comparison ra khoảng .4771 ở k4; .398 trong code là reference hằng số và manuscript project cha có báo số đó. Chưa tìm được numeric artifact đủ để độc lập chứng minh câu “we reproduce .398”. Không kết luận số published .398 bịa; cần sửa provenance hoặc thu hẹp câu local reproduction. Silhouette giữa scoring spaces khác nhau cũng không phải phép so clustering quality trực tiếp.

Những nhận xét “capacity spent on variance”, ngưỡng noise floor .005 hay causality do library drift chưa được kiểm bằng một experiment chỉ đổi đúng yếu tố tương ứng. Nên trình bày như giả thuyết/heuristic nếu giữ. Null tests hiện có chưa là equivalence test hay power study.

### 6.6. Kết luận audit đã hiệu chỉnh

Không có căn cứ kết luận toàn bộ paper sai hoặc cần bỏ nghiên cứu. Có ba mức thông tin: số chính có artifact và đã tái lập; một số mô tả paper-code lệch thực sự; một số diễn giải đi xa hơn bằng chứng. Cách sửa camera-ready phải phân biệt ba mức này, tránh cả giữ nguyên lỗi mô tả lẫn đổi nghiên cứu tùy ý sau acceptance.

## 7. Reviewer yêu cầu sửa và phương án camera-ready

Review 1 đề nghị mở rộng Discussion 9.2 về contractual churn trong telecom và inactivity-based churn trong retail. Khách hàng giống hành vi không đồng nghĩa họ tương tác hay ảnh hưởng nhau. Review 2 đề nghị giải thích đúng cross-model comparison Table 2 và nêu rõ trong abstract graph kNN xây từ chính features classifier đã dùng. Review 3 không có góp ý kỹ thuật thực hiện được.

Nhóm có thể bắt đầu bằng các thay đổi sát review: diễn giải bối cảnh, graph information source, phân biệt classifier effect và feature effect. Đối với sửa L/NCR/date windows ngoài comments, cần có danh sách before/after, bằng chứng code và tác động dự kiến để chair xác nhận phạm vi trước bản cuối.

| Việc cần làm | Có cần fit lại? | Tình trạng |
|---|---|---|
| Sửa diễn giải Table 2 theo reviewer | Không đổi experiment | Chưa sửa bản accepted |
| Bổ sung abstract/discussion theo review | Không đổi experiment | Chưa sửa bản accepted |
| Ghi rõ L, NCR, SHAP theo code | Không nếu chỉ mô tả đúng code hiện hành | Cần chốt phạm vi sửa |
| Đổi cửa sổ sang ngày trọn vẹn | Có, labels/cohort thay đổi | Chưa chạy model corrected-window |
| NCR-only ablation/cross-fitted encoding | Có, đây là kiểm tra bổ sung | Chưa thực nghiệm |
| Chốt authorship/track/presenter | Không phải model fit | Chưa có xác nhận riêng đầy đủ |

Không cần thay các bảng main chỉ vì raw/RAM lệch rất nhỏ trong một đường chạy, khi cached k10 đã tái lập exact archived folds. Nếu thật sự sửa phương pháp thì mọi bảng được giữ phải còn tương ứng với phương pháp mới; không giữ số cũ chỉ để tránh thay đổi.

## 8. Code train, epoch và Colab

Bộ source có khoảng 2.300 dòng trong sáu script. Phần repeated CV dùng LightGBM và Logistic Regression. LightGBM có 300 boosting rounds, learning rate .05, max depth 6; Logistic Regression tối đa 1.000 optimizer iterations. Đây không phải 300 epoch của neural network. Auxiliary có MLP/autoencoder tối đa 500 iterations và early stopping; không phải cơ sở của main negative-result comparison.

Một bộ repeated CV fit 10 repeats × 5 folds × 5 tiers × 2 classifiers = 500 models. Mỗi fold train khoảng 80% khách, đánh giá khoảng 20%. Do đó thời gian nằm ở nhiều lần fit, feature graph construction và đọc Excel, không phải một neural network lớn phải train nhiều ngày.

Notebook [366956-reproduce.ipynb](../../notebooks/366956-reproduce.ipynb) có 16 cells, 9 code cells; runner nằm trong notebook. Chọn `RUN_MODE="full"` cho 10 jobs hoặc `"main"` cho raw CV + cached k10 CV + figure, vẫn giữ 10×5 folds. Cài Python 3.13.5 riêng, pin commit, download UCI, kiểm hash, chạy source và so với paper.

Đã kiểm schema/cell syntax, data hash cell, actual download UCI, helper comparison trên outputs thật, plan jobs, refusal khi reuse output và ZIP export. **Chưa chạy toàn notebook trên Colab**, chưa đo thời gian Colab. Mốc 17m42 là local; phần main cộng các job đã đo khoảng 4m30, chưa tính cài/download. GPU runtime không tự làm code CPU dùng GPU: [Colab FAQ](https://research.google.com/colaboratory/faq.html).

## 9. Tiến độ và bàn giao cho thành viên

| Giai đoạn | Trạng thái xác minh | Bằng chứng |
|---|---|---|
| Xác định câu hỏi và viết manuscript | Có bản accepted 12 trang | PDF/TeX |
| Dữ liệu và feature engineering | Đã có raw/cache mới | Hash UCI, counts |
| Graph và cộng đồng | Đã chạy | Graph stats, logs/CSVs |
| Models, CV, corrected tests | Đã chạy lại 10 jobs | Fold files, summary, manifest |
| k-sensitivity/SHAP | Đã chạy, phạm vi cần phân biệt | k CSVs, SHAP outputs |
| Bộ tài liệu tiếng Việt | Bản học tập/diễn giải/dịch/báo cáo đi kèm | Bốn PDF + Markdown |
| Camera-ready theo review | Chưa sửa/nộp trong phiên này | Danh sách việc mục 7 |
| Corrected-window experiments | Chưa fit | Boundary audit không thay model run |
| Colab actual run | Chưa chạy | Notebook đã validate local |
| Business/causal/external validation | Chưa làm | Limitations trong paper |

Đề xuất bàn giao: một thành viên đọc và giải thích data/labels/features; một thành viên phụ trách graph/leakage; một thành viên đọc CV/statistics và tái tính p; một thành viên kiểm manuscript/reviewer/provenance. Đây là gợi ý tổ chức việc tiếp theo, không phải bằng chứng các thành viên mới đã có đóng góp tác giả.

Người nhận việc nên báo lại theo mẫu: câu hỏi đang kiểm; file/version dùng; thao tác thực hiện; kết quả định lượng; điều gì chưa biết; artifact lưu ở đâu. Trước khi đổi phương pháp hoặc publication metadata, chốt thống nhất với tác giả và phạm vi hội nghị.

## 10. Cách đọc bộ tài liệu và nguồn bằng chứng

Đọc sổ tay kiến thức trước để thống nhất thuật ngữ, đọc quy trình để biết nghiên cứu được tổ chức như thế nào, sau đó đọc bản dịch toàn bộ để đối chiếu từng lập luận với bài gốc. Báo cáo này là nơi cập nhật trạng thái, giải thích khác biệt và các quyết định cần chốt.

Bằng chứng máy nằm trong `docs/vietnamese/evidence`; aggregate outputs mới nằm trong `results/reproduction-20261012`. Raw XLSX và per-customer feature cache không được đóng gói vào bộ tài liệu này. Tài liệu có bản editable Markdown và script build PDF, font được embed để tiếng Việt hiển thị khi chuyển máy.

Các nguồn cần đọc:

- [Paper PDF gốc](../../paper/main.pdf) và [main.tex](../../paper/main.tex): nội dung manuscript được review.
- [significance_test.py](../../src/significance_test.py): repeated paired CV, folds, aggregates và statistics.
- [run_pipeline_v2.py](../../src/run_pipeline_v2.py): pipeline, final full-data reporting và SHAP.
- [compare_methods_v2.py](../../src/compare_methods_v2.py): clustering spaces và approximation baseline.
- [improvements_pipeline.py](../../src/improvements_pipeline.py): auxiliary scope khác main controlled CV.
- [requirements.txt](../../requirements.txt): dependency ghim.
- [Evidence index](evidence/README.md): nguồn/hash/runtime/coverage và giới hạn xác minh.
- [FISAT registration](https://fisat.eai-conferences.org/2026/registration/), [camera-ready](https://fisat.eai-conferences.org/2026/camera-ready-instructions/), [dates](https://fisat.eai-conferences.org/2026/): chính sách công khai kiểm lại ngày 13/10.

## Thuật ngữ (Glossary)

| English | Tiếng Việt | Ý nghĩa trong báo cáo |
|---|---|---|
| Camera-ready | Bản cuối để xuất bản | Hoàn thiện theo review và template, trước hạn |
| Accepted | Được chấp nhận | Quyết định hội nghị; chưa đồng nghĩa đã xuất bản |
| Raw data | Dữ liệu gốc | XLSX trước feature engineering |
| Feature tier | Nhóm/cấp đặc trưng | Một bước tăng độ phức tạp được so với baseline |
| Cache | Dữ liệu đặc trưng lưu tạm | CSV dùng lại, phải biết nguồn/version |
| Byte-identical | Khớp byte | Toàn bộ file giống nhau, mạnh hơn giống rounding |
| In-memory | Trong RAM | Fit trực tiếp DataFrame vừa tạo |
| Paired folds | Fold ghép cặp | Cùng khách train/validation giữa các tiers |
| pNB | Corrected p-value | p-value Nadeau-Bengio có hiệu chỉnh phụ thuộc CV |
| Failure to reject | Chưa bác bỏ giả thuyết không | Không phải chứng minh hiệu ứng bằng 0 |
| Provenance | Nguồn gốc bằng chứng | Số/claim được sinh từ file/run/version nào |
| Transductive | Dùng covariates cả nhóm trước đánh giá | Cần phân biệt với dùng validation labels |
