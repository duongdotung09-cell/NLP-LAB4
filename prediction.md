# Prediction trước experiment

Dataset được chọn: IMDb (sentiment, positive/negative), review phim dài trung bình khoảng 230 từ.

## Prediction 0 - TF-IDF vs Average Word2Vec trên IMDb

Prediction: TF-IDF + Logistic Regression sẽ tốt hơn Average Word2Vec + Logistic Regression.

Reason: Sentiment trên IMDb phụ thuộc mạnh vào một số từ/cụm từ đặc trưng (great, worst, waste, 7/10). TF-IDF giữ riêng trọng số của từng term nên classifier học trực tiếp được các từ này. Average Word2Vec lấy trung bình hàng trăm từ của một review dài nên tín hiệu cảm xúc bị pha loãng bởi từ trung tính, đồng thời good và bad thường có vector gần nhau vì xuất hiện trong ngữ cảnh giống nhau.

Confidence: 80%

## Prediction 1

TF-IDF + Logistic Regression có khả năng hoạt động tốt không?

Prediction: Có, F1 khoảng 0.88 - 0.90.

Reason: Dataset lớn (50k review), cân bằng, sentiment biểu hiện rõ qua từ vựng, và dữ liệu TF-IDF chiều cao gần như tách được tuyến tính nên một linear model là đủ mạnh.

Confidence: 85%

## Prediction 2

Average Word2Vec có chắc chắn tốt hơn TF-IDF không?

Prediction: Không, trên IMDb có thể còn kém hơn.

Reason: Word2Vec có thông tin semantic nhưng averaging làm mất word order và làm loãng các từ quan trọng; mỗi từ chỉ có một vector bất kể ngữ cảnh; chỉ có 100 chiều so với hàng chục nghìn feature của TF-IDF. Word2Vec có thể có lợi hơn khi dữ liệu ít hoặc văn bản ngắn và nhiều từ đồng nghĩa.

Confidence: 75%

## Prediction 3

Nếu tăng vocabulary size thì accuracy chắc chắn tăng không?

Prediction: Không chắc chắn.

Reason: Thêm feature có ích (ví dụ bigram như not good) có thể tăng accuracy, nhưng thêm nhiều từ hiếm, lỗi chính tả, tên riêng chỉ làm feature space lớn và sparse hơn, dễ overfit, tốn bộ nhớ và thời gian. Hiệu quả sẽ bão hòa hoặc giảm sau một ngưỡng.

Confidence: 80%

## Prediction 4

Nếu bỏ stopwords thì performance chắc chắn tăng không?

Prediction: Không, với sentiment có thể còn giảm.

Reason: Các danh sách stopwords chuẩn chứa not, no, nor, but, very, never, đây là những từ mang thông tin phủ định/nhấn mạnh rất quan trọng cho sentiment. TF-IDF vốn đã giảm trọng số của từ quá phổ biến qua IDF nên lợi ích của việc bỏ stopwords không lớn.

Confidence: 70%

## Prediction 5

Accuracy và F1 có thể cho kết luận khác nhau không?

Prediction: Có.

Reason: Khi dữ liệu imbalance, model nghiêng về class đa số có accuracy cao nhưng F1 của class thiểu số thấp (ví dụ Bài 4). Với IMDb cân bằng 50/50 thì hai metric sẽ gần nhau và cho cùng thứ tự xếp hạng model.

Confidence: 85%
