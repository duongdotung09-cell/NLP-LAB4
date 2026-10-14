# Reflection

## 1. Đối chiếu prediction với kết quả

| Prediction | Kết quả thực tế | Đúng/Sai |
|---|---|---|
| TF-IDF tốt hơn Average Word2Vec trên IMDb | TF-IDF + LR F1 = 0.900, Avg Word2Vec + LR F1 = 0.860 | Đúng |
| P1: TF-IDF + LR hoạt động tốt (F1 khoảng 0.88 - 0.90) | F1 = 0.900, accuracy = 0.899 | Đúng |
| P2: Avg Word2Vec không chắc chắn tốt hơn TF-IDF | Kém hơn khoảng 4 điểm F1 | Đúng |
| P3: Tăng vocabulary không chắc chắn tăng accuracy | Vocabulary tăng từ 57k lên 554k (thêm bigram) làm F1 tăng lên 0.920, nhưng đó là do bigram mang thông tin mới chứ không do kích thước; thời gian vectorize tăng khoảng 3 lần | Chưa kiểm chứng đầy đủ, chỉ có một trường hợp tăng |
| P4: Bỏ stopwords không chắc chắn tăng performance | Không chạy trong lab này | Chưa kiểm chứng |
| P5: Accuracy và F1 có thể cho kết luận khác nhau | Trên IMDb cân bằng, accuracy và F1 cho cùng thứ tự xếp hạng; khác biệt chỉ thấy rõ ở Bài 4 (imbalance) | Đúng như dự đoán |

## 2. Tại sao hai representation tạo ra kết quả khác nhau?

Cùng một classifier (Logistic Regression) nhưng TF-IDF đạt F1 0.900 còn Average Word2Vec chỉ 0.860.

TF-IDF là sparse, lexical, mỗi term là một chiều riêng nên Logistic Regression gán được weight riêng cho từng từ đặc trưng cảm xúc (great +11.3, worst -14.7, waste -10.9). Sentiment trên IMDb được quyết định phần lớn bởi những từ như vậy nên TF-IDF rất phù hợp.

Average Word2Vec là dense, semantic nhưng có ba vấn đề với task này. Thứ nhất, Word2Vec học từ ngữ cảnh nên good và bad là hàng xóm gần nhất của nhau (đã kiểm tra trong notebook), tức là vector không tách rõ cực cảm xúc. Thứ hai, averaging khoảng 230 từ làm các từ cảm xúc bị pha loãng bởi từ trung tính. Thứ ba, mất word order và mỗi từ chỉ có một vector bất kể ngữ cảnh. Hai model cũng sai ở những mẫu khác nhau (228 mẫu chỉ TF-IDF sai, 534 mẫu chỉ Word2Vec sai), cho thấy chúng dùng thông tin khác nhau.

Linear SVM trên cùng TF-IDF cho F1 0.901, gần như bằng LR, nên representation ảnh hưởng tới kết quả nhiều hơn việc chọn linear classifier.

## 3. Data leakage

Fit TF-IDF trên toàn bộ dataset rồi mới split là leakage vì vocabulary và IDF đã được tính từ cả document của test set. Model có cột feature cho những từ chỉ xuất hiện trong test và trọng số IDF bị ảnh hưởng bởi tần suất trong test, tức là thông tin của test đã đi vào quá trình train. Kết quả đánh giá vì vậy lạc quan hơn so với khi gặp dữ liệu thật sự mới. Trong lab này TF-IDF, Word2Vec và việc chọn C đều chỉ dùng train/validation, test chỉ được dùng một lần để báo cáo. Ngoài ra 422 review trùng lặp được loại bỏ trước khi split để tránh cùng một review nằm ở cả train và test.

## 4. Model interpretation

Top feature của TF-IDF unigram + LR:

| Positive | Weight | Negative | Weight |
|---|---|---|---|
| great | 11.31 | worst | -14.66 |
| excellent | 9.87 | awful | -11.48 |
| 7 | 9.41 | bad | -10.94 |
| perfect | 8.00 | waste | -10.90 |
| best | 7.89 | boring | -9.83 |
| wonderful | 7.25 | poor | -8.04 |
| favorite | 7.02 | nothing | -7.79 |
| amazing | 6.91 | horrible | -7.66 |

Phần lớn feature có ý nghĩa cảm xúc thật sự, nên model học đúng tín hiệu của task. Tuy nhiên "7", "8" là điểm số (7/10) chỉ có ý nghĩa trong domain review có chấm điểm; "nothing", "supposed" chỉ tiêu cực nhờ ngữ cảnh; "dvd", "well" là tương quan thống kê của dữ liệu. Các feature này hợp lệ trên IMDb nhưng là shortcut, dễ không tổng quát sang domain khác.

## 5. Giới hạn của representation và hướng sang neural NLP

Experiment 4 cho thấy avg("this movie is good") và avg("this movie is not good") có cosine khoảng 0.95, và "this movie is not bad" vẫn bị đoán negative với xác suất gần 1. Cả TF-IDF unigram và Average Word2Vec đều là bag-of-words, không hiểu phạm vi của "not". Bigram giúp được một phần ("not good" có weight -3.6) nhưng vẫn không lật được "not bad" vì weight của "bad" quá lớn, và feature space tăng gần 10 lần. Error analysis cũng cho thấy lỗi tập trung ở negation, mixed sentiment và sarcasm, đều cần thứ tự từ và ngữ cảnh. Đây là động lực cho sequence models (RNN/LSTM/GRU) ở LAB 05, nơi mỗi từ được xử lý theo thứ tự và trạng thái ẩn mang ngữ cảnh của các từ trước, rồi tới attention/Transformer với contextual embeddings (bank tài chính khác bank bờ sông).

## 6. Individual learning check

Tại sao accuracy 95% chưa chắc tốt? Vì khi dữ liệu imbalance (950 negative / 50 positive), model đoán toàn bộ là negative cũng đạt 95% nhưng recall và F1 của class positive bằng 0. Cần xem confusion matrix, precision, recall, F1 của từng class và macro-F1.

TF-IDF khác average Word2Vec ở điểm nào? TF-IDF là vector sparse, chiều bằng kích thước vocabulary, mỗi chiều là một term, giữ thông tin lexical. Average Word2Vec là vector dense chiều thấp, mang thông tin semantic (từ đồng nghĩa gần nhau) nhưng làm mất trọng số riêng của từ quan trọng và mỗi từ chỉ có một vector. Cả hai đều mất word order.

Tại sao "not good" có thể gây lỗi? Vì bag-of-words tách thành hai feature độc lập "not" và "good"; "good" có weight positive lớn nên câu phủ định vẫn có thể bị đoán positive. Với average embedding, vector của "not" chỉ được cộng vào trung bình chứ không đảo nghĩa của "good".

Data leakage xảy ra ở đâu nếu fit TF-IDF trước khi split? Ở bước tính vocabulary và IDF: các thống kê này đã dùng document của test set, nên test không còn là dữ liệu chưa thấy.

Precision và recall khác nhau thế nào? Precision = TP / (TP + FP), trong các mẫu model đoán positive có bao nhiêu đúng. Recall = TP / (TP + FN), trong các mẫu positive thật model tìm được bao nhiêu. Precision phạt false positive, recall phạt false negative.

Tại sao thêm bigram có thể cải thiện sentiment classification? Vì bigram như "not good", "highly recommend", "waste of" trở thành feature riêng với weight riêng, bắt được một phần negation và cụm từ cảm xúc mà unigram bỏ lỡ. Trên IMDb F1 tăng từ 0.900 lên 0.920, đổi lại vocabulary tăng từ 57k lên 554k.
