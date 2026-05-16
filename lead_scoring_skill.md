# Skill: Lead Scoring for Real Estate

## Description
This skill analyzes customer lead data from the "nhu_cau_mo_ta" (Description of Need) field to evaluate potential and assign a priority score. The goal is to identify VIP/High-Potential leads versus Trash/No-Potential leads to optimize the sales team's efforts.

## Input Parameters
- `id`: Unique identifier of the lead.
- `ten_khach`: Customer name.
- `sdt`: Phone number.
- `nhu_cau_mo_ta`: The primary text field containing the customer's requirements, budget, and context.

## Scoring Logic

### 1. Starting Score
- All leads start with a base score of **0**.

### 2. Add 50 Points (VIP / Super Potential)
Assign +50 points if the `nhu_cau_mo_ta` contains any of the following:
- **High Budget:** Mentions of 20 billion VND or more, "tài chính mạnh" (strong finance), "không thành vấn đề" (no problem).
- **Premium Properties:** "Biệt thự đơn lập" (Detached Villa), "Penthouse", "Shophouse mặt đường lớn", "Quỹ đất công nghiệp" (Industrial land), "Sàn văn phòng diện tích lớn".
- **Prime Locations:** "Quận 1", "Ven sông" (Riverside), "Vinhomes Ocean Park", "Phú Mỹ Hưng".
- **Client Profile:** "Chủ doanh nghiệp" (Business owner), "Nhà đầu tư chuyên nghiệp", "Mua sỉ" (Wholesale), "Mua số lượng lớn".
- **Urgency & Transparency:** "Pháp lý chuẩn 100%", "Sổ hồng riêng", "Muốn gặp trực tiếp chủ đầu tư để đàm phán".

### 3. Subtract 50 Points (Trash / No Potential)
Subtract 50 points if the `nhu_cau_mo_ta` contains any of the following:
- **Unrealistic Expectations:** Budget is significantly lower than market price (e.g., District 1 house for 1-2 billion VND).
- **No Demand:** "Nhầm số" (Wrong number), "Không có nhu cầu", "Dữ liệu cũ", "Nhầm ngành".
- **Uninterested/Uncooperative:** "Hỏi giá cho vui", "Chưa có ý định mua", "Thái độ không hợp tác".
- **Spam/Ads:** Content about "Bảo hiểm" (Insurance), "Vay vốn" (Loans), or other service offerings.
- **Contact Issues:** "Thuê bao", "Gọi nhiều lần không bắt máy", "Không phản hồi Zalo".

### 4. Neutral / Low Bonus (0 - 10 Points)
Maintain the score or add minimal points for:
- Apartments or townhouses in the 3-10 billion VND range.
- Leads needing bank loans or weighing policies.
- Real demand but requires further consultation on legal or location aspects.

## Output Format
The skill should return a structured JSON response for each lead:
```json
{
  "id": number,
  "score": number,
  "category": "VIP" | "Potential" | "Neutral" | "Trash",
  "reasoning": "Brief explanation of why this score was given based on keywords found."
}
```

## Categorization Guidelines
- **Score >= 50:** VIP
- **Score 1 to 49:** Potential
- **Score 0:** Neutral
- **Score < 0:** Trash
