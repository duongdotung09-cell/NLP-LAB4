# LAB 04 - Text Classification

Bài toán: phân loại sentiment (positive/negative) của review phim IMDb (Option A - Sentiment classification), so sánh representation TF-IDF và Average Word2Vec với cùng classifier.

## Dataset

IMDb Dataset of 50K Movie Reviews (Kaggle), file imdb.zip đặt ở thư mục cha của lab04 (../imdb.zip). Code đọc trực tiếp file CSV trong zip, không cần giải nén.

- 50000 review, 2 class, 25000 positive / 25000 negative (không imbalance)
- Không có missing text / missing label
- 418 review trùng lặp nguyên văn và 4 review trùng sau khi bỏ thẻ HTML/lowercase, tổng cộng 422 review bị loại trước khi split (còn 49578)
- Split stratified 70/15/15: train 34704, validation 7437, test 7437 (seed 42)

## Cấu trúc

| File                 | Nội dung                                                                                                                                           |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| calculations.md      | Bài 1 - Bài 4 (logit, sigmoid, threshold, confusion matrix, accuracy trap)                                                                        |
| prediction.md        | Prediction trước experiment                                                                                                                       |
| classification.ipynb | Toàn bộ experiment: dataset inspection, split, baseline, representation comparison, word order, n-gram, evaluation, error analysis, model weights |
| preprocessing.py     | Đọc dữ liệu, thống kê, làm sạch text, tokenize, split, average Word2Vec                                                                     |
| results.csv          | Kết quả các model trên test set                                                                                                                 |
| confusion_matrix.png | Confusion matrix của 3 model trên test set                                                                                                        |
| error_analysis.md    | Phân tích 3 mẫu đúng và 7 mẫu sai                                                                                                            |
| reflection.md        | Đối chiếu prediction, so sánh representation, data leakage, interpretation, individual learning check                                           |

## Cách chạy

Yêu cầu: Python 3.10+, pandas, numpy, scikit-learn, gensim, matplotlib, jupyter.

```
pip install pandas numpy scikit-learn gensim matplotlib jupyter
cd lab04
jupyter nbconvert --to notebook --execute classification.ipynb
```

Notebook chạy khoảng 3 phút trên CPU, tự ghi lại results.csv và confusion_matrix.png.

## Pipeline

Raw text -> làm sạch (bỏ thẻ HTML, lowercase) -> loại trùng lặp -> split train/val/test -> fit TF-IDF hoặc Word2Vec chỉ trên train -> chọn C trên validation -> đánh giá một lần trên test.

## Kết quả trên test set

| Representation        | Classifier          | Vocabulary | Accuracy | Precision | Recall | F1     |
| --------------------- | ------------------- | ---------- | -------- | --------- | ------ | ------ |
| TF-IDF (unigram)      | Logistic Regression | 57229      | 0.8986   | 0.8884    | 0.9126 | 0.9003 |
| Avg Word2Vec (100d)   | Logistic Regression | 60788      | 0.8575   | 0.8468    | 0.8741 | 0.8602 |
| TF-IDF (unigram)      | Linear SVM          | 57229      | 0.8996   | 0.8896    | 0.9132 | 0.9012 |
| TF-IDF (uni + bigram) | Logistic Regression | 553663     | 0.9189   | 0.9110    | 0.9293 | 0.9200 |

Training time, thời gian vectorize và hyperparameter C xem trong results.csv. Metric precision/recall/F1 tính với positive là class 1.

## Ghi chú

- Word2Vec được train trên tập train với workers=4 nên kết quả của dòng Avg Word2Vec có thể dao động nhẹ (khoảng ±0.005) giữa các lần chạy; các model TF-IDF cho kết quả cố định.
- Thời gian train/vectorize phụ thuộc máy, chỉ dùng để so sánh tương đối.

## AI assistance statement

- Tool: Claude Code
- Purpose: hỗ trợ viết code, chạy các thí nghiệm và trình bày lại thành văn bản cho các file .md (các phần tính toán, dự đoán và phân tích đã tự làm trước)
- Generated content: preprocessing.py, classification.ipynb, results.csv, confusion_matrix.png và bản trình bày lại của calculations.md, prediction.md, error_analysis.md, reflection.md
- Modified content: các file .md được đọc lại, đối chiếu với phần đã tự làm trước, sửa những chỗ AI diễn đạt sai ý và chỉnh sửa trước khi nộp
- Verification: chạy notebook từ đầu đến cuối và đối chiếu các con số trong README.md, reflection.md, error_analysis.md với output của notebook và results.csv, kiểm tra kết quả tính tay ở calculations.md, kiểm tra không có review nào xuất hiện ở nhiều hơn một tập train/validation/test, và đọc lại các file .md để đảm bảo đúng yêu cầu từng mục trong W4.pdf
