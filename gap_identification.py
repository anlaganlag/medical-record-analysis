def identify_gaps(extracted_entities, rules):
    """基于规则识别病历中的缺口

    Args:
        extracted_entities (dict): 从病历中提取的医疗实体
        rules (dict): 规则库

    Returns:
        list: 识别出的缺口列表
    """
    if not extracted_entities or not rules:
        return []

    gaps = []

    # 1. 检查必填字段是否缺失
    required_fields = rules.get("required_fields", {})

    # 检查透析参数必填字段
    for field_category, fields in required_fields.items():
        for field in fields:
            # 检查字段是否在提取的实体中
            field_found = False

            # 创建相关字段的映射
            field_mapping = {
                "抗凝剂": ["抗凝剂", "肝素"],
                "抗凝剂剂量": ["单位抗凝", "剂量"],
                "内瘘评估": ["内瘘杂音", "内瘘震颤"],
                "并发症记录": ["并发症", "无并发症"],
                "透析器型号": ["透析器型号"],
                "血流量": ["血流量"],
                "透析液流量": ["透析液流量"],
                "透析时间": ["透析时间"],
                "超滤量": ["超滤量"],
                "透析前体重": ["透析前体重"],
                "透析后体重": ["透析后体重"],
                "透析前血压": ["透析前血压"],
                "透析后血压": ["透析后血压"]
            }

            # 获取当前字段的相关关键词
            related_keywords = field_mapping.get(field, [field])

            # 检查症状中是否包含相关关键词
            for symptom in extracted_entities.get("symptoms", []):
                for keyword in related_keywords:
                    if keyword in symptom:
                        field_found = True
                        break
                if field_found:
                    break

            # 检查体征中是否包含相关关键词
            if not field_found:
                for sign in extracted_entities.get("signs", []):
                    for keyword in related_keywords:
                        if keyword in sign:
                            field_found = True
                            break
                    if field_found:
                        break

            # 检查检验值中是否包含相关关键词
            if not field_found:
                for lab_value in extracted_entities.get("lab_values", []):
                    for keyword in related_keywords:
                        if keyword in lab_value:
                            field_found = True
                            break
                    if field_found:
                        break

            # 如果未找到该字段，添加到缺口列表
            if not field_found:
                gaps.append(f"缺少{field}记录")

    # 2. 检查逻辑一致性
    logic_rules = rules.get("logic_rules", [])
    for rule in logic_rules:
        check_func = rule.get("check")
        if check_func:
            is_valid, message = check_func(extracted_entities)
            if not is_valid and message:
                gaps.append(message)

    return gaps