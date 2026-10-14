# Error analysis

Model được phân tích: TF-IDF (unigram + bigram) + Logistic Regression, model tốt nhất trên test (F1 = 0.920). Chỉ số [id] là index của mẫu trong tập test ở notebook (mục 8).

Tổng quan: 603 / 7437 mẫu test bị sai (8.1%), gồm 339 FP (negative bị đoán positive) và 264 FN (positive bị đoán negative). Độ dài trung bình của mẫu sai (223 từ) xấp xỉ mẫu đúng (229 từ), nên lỗi không chủ yếu do độ dài mà do nội dung review.

## Correctly classified

| id | Text (trích) | True | Predicted | P(pos) | Analysis |
|---|---|---|---|---|---|
| 6797 | "one of bruce's most underrated films ... an awesome heartwarming film ... an amazing performance" | positive | positive | 1.000 | Dày đặc từ cảm xúc tích cực có weight lớn (awesome, amazing, great, best), không có từ trái chiều. |
| 4452 | "it is my favorite. the artwork is amazing ... i gave the animatrix a "7", but this particular segment deserves a "10."" | positive | positive | 1.000 | Văn bản ngắn nhưng có favorite, amazing, perfectly và điểm số 7, 10, đều là feature positive mạnh. |
| 4520 | "a very disappointing movie ... the worst movie of all time ... just plain awful. avoid this wretched piece of garbage" | negative | negative | 0.000 | Các từ negative mạnh nhất của model (worst, awful, disappointing, avoid, stupid) cùng xuất hiện. |

## Incorrectly classified

| id | Text (trích) | True | Predicted | P(pos) | Loại lỗi | Analysis |
|---|---|---|---|---|---|---|
| 2402 | "this is a great movie. i love the series on tv and so i loved the movie ... it's a great movie! doy!!!" | negative | positive | 1.000 | data noise | Nội dung hoàn toàn tích cực, nhãn negative gần như chắc chắn là nhãn sai. Model đúng về mặt ngôn ngữ. |
| 2529 | "you can't make a film this bad, so good, on purpose ... the dubbing is horrible, the acting is stiff ... a terrific cult classic" | negative | positive | 0.987 | lexical ambiguity, data noise | Review kiểu "so bad it's good": người viết khen phim dở theo nghĩa cult, rất nhiều excellent, terrific, great. Nhãn negative mâu thuẫn với lời khen, nhưng bad/horrible ở đây lại mang nghĩa tích cực, bag-of-words không phân biệt được. |
| 4203 | "a poor script based on a lackluster novel ... the biggest travesty ... downright painful ... "comanche moon" is almost a brilliant production" | positive | negative | 0.005 | lexical ambiguity (mixed sentiment) | Review dài, phần lớn là chê (poor, lackluster, travesty, painful, dull, tedious), kết luận tích cực chỉ nằm ở vài câu cuối. Bag-of-words cộng dồn mọi từ như nhau nên phần chê áp đảo, không biết câu kết luận quan trọng hơn. |
| 2707 | "the acting/dialog is pretty weak ... the worst irish accent ever ... not bad for the first 5 minutes ... not nearly as bad as i expected ... 7.5/10" | positive | negative | 0.017 | negation | Ý tích cực được diễn đạt bằng phủ định của từ tiêu cực (not bad, not nearly as bad, don't really have too much time to be bored). Model vẫn bị kéo về negative bởi bad, worst, weak, bored. Điểm 7.5/10 bị tokenizer tách thành 7, 5, 10 nên tín hiệu điểm số cũng yếu đi. |
| 7021 | "this is the definitive movie version of hamlet. branagh cuts nothing, but there are no wasted moments." | positive | negative | 0.059 | short text, negation | Câu ngắn (17 từ) gần như không có từ khen trực tiếp. "nothing" và "wasted" là feature negative mạnh (waste, nothing nằm trong top negative), trong khi "no wasted moments" thực ra là lời khen. |
| 1291 | "more suspenseful, more subtle, much, much more disturbing...." | negative | positive | 0.924 | short text, domain-specific term | Chỉ có 8 từ. Với phim kinh dị, suspenseful/subtle/disturbing thường là lời khen nên model đoán positive. Câu này có thể là đoạn so sánh với bản phim khác (bản kia hay hơn), thiếu ngữ cảnh để kết luận, nên với văn bản quá ngắn cả model lẫn người đọc đều khó xác định. |
| 3315 | "it's not citizen kane, but it does deliver. cleavage, and lots of it. badly acted and directed, poorly scripted. who cares?" | positive | negative | 0.418 | sarcasm, negation | Người viết thừa nhận phim dở (badly, poorly) nhưng vẫn thích theo kiểu mỉa mai ("who cares?"). Ý tích cực nằm ở cấu trúc câu chứ không ở từ vựng, model chỉ thấy các từ negative. |

## Kết luận

- Nhóm lỗi nhiều nhất là review có cảm xúc trộn lẫn (khen một phần, chê một phần) và negation (not bad, no wasted moments), là giới hạn trực tiếp của bag-of-words: không biết thứ tự, không biết phạm vi của phủ định, không biết câu nào là kết luận.
- Một phần lỗi FP có P(pos) gần 1 là do data noise (nhãn sai), các lỗi này không thể và không nên được model "sửa".
- Văn bản rất ngắn thiếu tín hiệu từ vựng nên xác suất dự đoán gần ngưỡng hoặc phụ thuộc vào vài từ đơn lẻ.
- Class imbalance không phải nguyên nhân lỗi ở đây vì IMDb cân bằng 50/50.
