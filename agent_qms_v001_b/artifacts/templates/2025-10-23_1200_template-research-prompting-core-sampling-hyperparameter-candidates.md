## Overview:
For effective grammar error correction in Korean using language models, the following hyperparameters are particularly relevant. These settings help balance fluency, accuracy, and diversity in the model's output while minimizing hallucinations:

### **Core Sampling Parameters**
1. **Temperature (0.1–0.3)**
   - Lower values (0.1–0.3) are recommended for Korean grammar correction to prioritize deterministic, high-confidence corrections.
   - Avoid temperatures >0.5, as they increase randomness and may introduce new errors.

2. **Top-k (30–50)**
   - Limits the next token selection to the top *k* most probable tokens.
   - For Korean, a moderate *k* (30–50) helps retain linguistic diversity while avoiding rare or incorrect particles/conjugations.

3. **Top-p (Nucleus Sampling, 0.7–0.9)**
   - A higher *p* (0.7–0.9) ensures the model considers a broader context, which is crucial for Korean morphology (e.g., honorifics, verb endings).
   - Too low (*<0.6*) may restrict the model’s ability to handle complex grammatical structures.

4. **Repetition Penalty (1.1–1.2)**
   - Slightly penalizes repeated tokens to avoid redundant corrections (e.g., over-correcting the same particle).

5. **Frequency Penalty (0.5–1.0)**
   - Helps prevent overuse of common but contextually incorrect forms (e.g., excessive use of 반말 in formal contexts).

### **Korean-Specific Considerations**
- **Context Length (2048+ tokens)**
  - Korean sentences often rely on context (e.g., topic markers `은/는`), so longer context windows improve accuracy.
- **Subword Tokenization**
  - Ensure the model uses a Korean-optimized tokenizer (e.g., SentencePiece) to handle agglutinative morphology (e.g., `먹었습니다` → `먹` + `었` + `습니다`).
- **Few-Shot Prompting**
  - Include 3–5 examples of Korean grammar errors/corrections in the prompt to guide the model (e.g., `잘못: 나는 학교에 갔어요 → 올바름: 저는 학교에 갔어요`).

### **Edge Case Handling**
- **Honorifics (존댓말 vs. 반말)**
  - Explicitly specify the desired formality level in the prompt (e.g., `반말로 수정하세요`).
- **Spelling vs. Grammar**
  - For spelling errors, use a lower temperature (0.1) and higher top-p (0.9) to prioritize exact matches.
  - For grammatical errors (e.g., tense, particles), a slightly higher temperature (0.2) may help with contextual adjustments.

### **Example Prompt Structure**
```text
"다음 한국어 문장의 문법 오류를 수정하세요. 존댓말로 답변하세요.
예시:
잘못: 어제 친구 집에 갔어. → 올바름: 어제 친구 집에 갔어요.
입력: [USER_TEXT]"
```

### **Testing Recommendations**
- Validate with datasets like **Korean Grammatical Error Correction (KGEC)** or **AI Hub’s Korean text corpus**.
- Measure **precision/recall** for particle corrections (은/는, 이/가) and verb conjugations.
