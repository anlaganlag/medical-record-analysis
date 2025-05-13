import re

def extract_medical_entities(text_data):
    """提取医疗实体（症状、体征、检验值等）

    Args:
        text_data (dict): 预处理后的文本数据，包含原始文本和处理后的文本

    Returns:
        dict: 提取的医疗实体，包括症状、体征和检验值
    """
    if not text_data or not isinstance(text_data, dict):
        return {"symptoms": [], "signs": [], "lab_values": []}

    processed_text = text_data.get("processed", "")
    sentences = text_data.get("sentences", [])

    if not processed_text or not sentences:
        return {"symptoms": [], "signs": [], "lab_values": []}

    # 在实际项目中，这里应该使用预训练的医疗NER模型（如BioBERT）
    # 但在MVP中，我们使用基于规则的方法进行简单识别

    # 常见症状词典
    symptom_keywords = [
        "头晕", "头痛", "恶心", "呕吐", "乏力", "疲劳", "胸闷", "胸痛", "腹痛",
        "腹胀", "咳嗽", "咳痰", "发热", "发烧", "畏寒", "寒战", "多汗", "盗汗",
        "食欲不振", "失眠", "心悸", "气短", "呼吸困难", "水肿", "浮肿"
    ]

    # 常见体征词典
    sign_keywords = [
        "体重", "体温", "血压", "脉搏", "呼吸", "心率", "意识", "瞳孔",
        "皮肤", "黄疸", "水肿", "肺部", "心脏", "腹部", "肝脏", "脾脏",
        "透析器", "血流量", "透析液流量", "抗凝剂", "肝素", "透析时间", "超滤量", "内瘘",
        "透析前体重", "透析后体重", "透析前血压", "透析后血压", "并发症"
    ]

    # 常见检验值词典
    lab_value_keywords = [
        "血红蛋白", "白细胞", "血小板", "肌酐", "尿素氮", "血糖", "血钾",
        "血钠", "血氯", "血钙", "血磷", "血白蛋白", "总蛋白", "谷丙转氨酶",
        "谷草转氨酶", "总胆红素", "直接胆红素", "C反应蛋白", "降钙素原"
    ]

    # 提取症状
    symptoms = []
    for symptom in symptom_keywords:
        if symptom in processed_text:
            # 提取症状及其描述
            pattern = f"([^，。,;；]*{symptom}[^，。,;；]*)"
            matches = re.findall(pattern, processed_text)
            symptoms.extend(matches)

    # 提取体征
    signs = []
    for sign in sign_keywords:
        if sign in processed_text:
            # 提取体征及其数值
            pattern = f"([^，。,;；]*{sign}[^，。,;；]*(?:[0-9]+\\.?[0-9]*\\s*(?:kg|℃|mmHg|次/分|bpm|ml/min|小时|单位))?)"
            matches = re.findall(pattern, processed_text)
            signs.extend(matches)

    # 提取检验值
    lab_values = []
    for lab in lab_value_keywords:
        if lab in processed_text:
            # 提取检验项目及其结果
            pattern = f"([^，。,;；]*{lab}[^，。,;；]*[0-9]+\\.?[0-9]*\\s*(?:g/L|mmol/L|U/L|mg/dL|mg/L)?)"
            matches = re.findall(pattern, processed_text)
            lab_values.extend(matches)

    # 去重
    symptoms = list(set(symptoms))
    signs = list(set(signs))
    lab_values = list(set(lab_values))

    return {
        "symptoms": symptoms,
        "signs": signs,
        "lab_values": lab_values
    }