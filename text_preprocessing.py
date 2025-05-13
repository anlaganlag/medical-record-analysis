import re

def preprocess_medical_text(text):
    """对非结构化病历文本进行预处理

    Args:
        text (str): 原始非结构化病历文本

    Returns:
        dict: 预处理后的文本，包含原始文本和处理后的文本
    """
    if not text or not isinstance(text, str):
        return {"original": "", "processed": ""}

    # 保存原始文本
    original_text = text

    # 1. 标准化日期格式
    date_pattern = r'(\d{2,4})[年/-](\d{1,2})[月/-](\d{1,2})日?'

    def date_replacer(match):
        year = match.group(1)
        month = match.group(2)
        day = match.group(3)
        # 确保年份是4位数
        if len(year) == 2:
            year = '20' + year
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

    text = re.sub(date_pattern, date_replacer, text)

    # 2. 标准化数值和单位
    # 处理常见的医疗数值格式，如"体重下降6kg"、"血钾6.5mmol/L"
    value_pattern = r'(\d+\.?\d*)\s*(千克|公斤|kg|KG)'
    text = re.sub(value_pattern, lambda m: f"{m.group(1)} kg", text)

    # 3. 分句
    sentences = re.split(r'[。！？；.!?;]', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # 4. 去除无关信息（如过多的空格、特殊字符等）
    processed_sentences = []
    for sentence in sentences:
        # 去除多余空格
        sentence = re.sub(r'\s+', ' ', sentence).strip()
        if sentence:
            processed_sentences.append(sentence)

    processed_text = '。'.join(processed_sentences)

    return {
        "original": original_text,
        "processed": processed_text,
        "sentences": processed_sentences
    }