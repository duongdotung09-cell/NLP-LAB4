# Calculations

## Bài 1 - Binary classification

z = wᵀx + b = 0.5·1 + (-0.2)·2 + 0.4·0 + 0.1 = 0.5 - 0.4 + 0 + 0.1 = 0.2

P(y = 1 | x) = σ(0.2) = 1 / (1 + e^(-0.2)) = 1 / (1 + 0.8187) ≈ 0.5498

## Bài 2 - Prediction threshold

τ = 0.5: 0.72 ≥ 0.5 nên model dự đoán class 1 (positive).

τ = 0.8: 0.72 < 0.8 nên model dự đoán class 0 (negative).

Tăng threshold thì model chỉ dự đoán positive khi rất chắc chắn, số mẫu được dự đoán positive giảm: FP giảm nên precision thường tăng, nhưng FN tăng nên recall giảm. Giảm threshold thì ngược lại: recall tăng, precision giảm.

## Bài 3 - Confusion matrix

TP = 80, FN = 20, FP = 10, TN = 90.

Precision = TP / (TP + FP) = 80 / 90 ≈ 0.8889

Recall = TP / (TP + FN) = 80 / 100 = 0.8000

F1 = 2PR / (P + R) = 2 · 0.8889 · 0.8 / (0.8889 + 0.8) = 1.4222 / 1.6889 ≈ 0.8421

Với bài toán phát hiện spam (positive = spam):

- False positive: email bình thường bị đưa vào thư mục spam, người dùng có thể bỏ lỡ email quan trọng (thông báo, hợp đồng, OTP). Đây thường là lỗi nghiêm trọng hơn nên cần precision cao.
- False negative: email spam lọt vào inbox, gây phiền và có thể dẫn tới phishing/lừa đảo. Lỗi này ảnh hưởng tới recall.

## Bài 4 - Accuracy trap

Model dự đoán tất cả là negative: TP = 0, FN = 50, FP = 0, TN = 950.

- Accuracy = 950 / 1000 = 95%
- Recall (positive) = 0 / 50 = 0
- Precision (positive) = 0 / 0, không xác định (quy ước 0)
- F1 (positive) = 0
- F1 (negative) = 2 · 0.95 · 1 / (0.95 + 1) ≈ 0.9744, Macro-F1 = (0.9744 + 0) / 2 ≈ 0.487
- Balanced accuracy = (0 + 1) / 2 = 0.5

Model này không tốt: nó không phát hiện được bất kỳ mẫu positive nào, accuracy 95% chỉ phản ánh tỉ lệ class negative trong dữ liệu. Khi dữ liệu imbalance cần xem thêm confusion matrix, precision, recall, F1 của class thiểu số (positive), và macro-F1 hoặc balanced accuracy.
