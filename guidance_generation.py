def generate_guidance(gaps, knowledge_base, extracted_entities=None):
    """基于识别的缺口生成指导意见

    Args:
        gaps (list): 识别出的缺口列表
        knowledge_base (dict): 知识库
        extracted_entities (dict, optional): 提取的医疗实体，用于生成更具体的建议

    Returns:
        dict: 指导意见，包括缺口和对应的建议
    """
    if not gaps or not knowledge_base:
        return {"gaps": [], "suggestions": []}

    guidance = []
    gap_guidance = knowledge_base.get("gap_guidance", {})

    for gap in gaps:
        if gap in gap_guidance:
            guidance.append({
                "gap": gap,
                "suggestion": gap_guidance[gap]
            })
        else:
            # 生成通用建议
            guidance.append({
                "gap": gap,
                "suggestion": f"建议补充{gap}相关信息"
            })

    # 如果提供了提取的实体，可以生成更具体的建议
    if extracted_entities:
        symptom_knowledge = knowledge_base.get("symptom_knowledge", {})
        symptoms = extracted_entities.get("symptoms", [])

        # 为特定症状提供额外建议
        for symptom in symptoms:
            for known_symptom, info in symptom_knowledge.items():
                if known_symptom in symptom:
                    guidance.append({
                        "gap": f"症状：{symptom}",
                        "suggestion": f"可能原因：{', '.join(info.get('可能原因', []))}。建议处理：{info.get('建议处理', '')}"
                    })
                    break

    # 整理结果
    result = {
        "gaps": [item["gap"] for item in guidance],
        "suggestions": [item["suggestion"] for item in guidance],
        "detailed_guidance": guidance
    }

    return result