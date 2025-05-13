"""
规则库模块，定义了病历规范检查的规则
"""

# 透析病历必填字段规则
REQUIRED_FIELDS = {
    "basic": [
        "患者姓名",
        "患者ID",
        "日期",
        "透析方式"
    ],
    "dialysis_parameters": [
        "透析器型号",
        "血流量",
        "透析液流量",
        "抗凝剂",
        "抗凝剂剂量",
        "透析时间",
        "超滤量"
    ],
    "vital_signs": [
        "透析前体重",
        "透析后体重",
        "透析前血压",
        "透析后血压"
    ],
    "assessment": [
        "内瘘评估",
        "并发症记录"
    ]
}

# 透析相关症状关键词
DIALYSIS_SYMPTOMS = [
    "头晕", "头痛", "恶心", "呕吐", "乏力", "肌肉痉挛", "低血压", "高血压",
    "胸闷", "胸痛", "心悸", "气短", "呼吸困难", "水肿", "瘙痒", "失眠"
]

# 透析相关体征关键词
DIALYSIS_SIGNS = [
    "体重", "血压", "脉搏", "体温", "呼吸", "水肿", "内瘘杂音", "内瘘震颤"
]

# 透析相关检验值关键词
DIALYSIS_LAB_VALUES = [
    "血红蛋白", "白细胞", "血小板", "肌酐", "尿素氮", "血钾", "血钠", "血钙", "血磷",
    "甲状旁腺素", "白蛋白", "Kt/V", "URR"
]

# 逻辑规则检查
LOGIC_RULES = [
    {
        "name": "体重与超滤量一致性",
        "description": "透析前后体重差应与超滤量基本一致",
        "check": lambda entities: check_weight_ultrafiltration_consistency(entities)
    },
    {
        "name": "抗凝剂与剂量匹配",
        "description": "抗凝剂应有对应的剂量记录",
        "check": lambda entities: check_anticoagulant_dose_match(entities)
    },
    {
        "name": "透析时间合理性",
        "description": "透析时间通常应在3-5小时范围内",
        "check": lambda entities: check_dialysis_time_reasonable(entities)
    }
]

# 逻辑规则检查函数
def check_weight_ultrafiltration_consistency(entities):
    """检查体重变化与超滤量是否一致"""
    # 在实际项目中，这里应该有更复杂的逻辑
    # 简化版本仅检查是否同时存在体重变化和超滤量记录
    signs = entities.get("signs", [])
    
    has_weight = any("体重" in sign for sign in signs)
    has_ultrafiltration = any("超滤" in sign for sign in signs)
    
    if has_weight and not has_ultrafiltration:
        return False, "记录了体重变化但缺少超滤量记录"
    
    return True, ""

def check_anticoagulant_dose_match(entities):
    """检查抗凝剂与剂量是否匹配"""
    # 简化版本
    signs = entities.get("signs", [])
    
    has_anticoagulant = any("抗凝" in sign for sign in signs)
    has_dose = any("剂量" in sign or "单位" in sign for sign in signs)
    
    if has_anticoagulant and not has_dose:
        return False, "记录了抗凝剂但缺少剂量记录"
    
    return True, ""

def check_dialysis_time_reasonable(entities):
    """检查透析时间是否合理"""
    # 简化版本
    signs = entities.get("signs", [])
    
    for sign in signs:
        if "透析时间" in sign:
            # 尝试提取时间数值
            import re
            time_match = re.search(r'(\d+\.?\d*)\s*小时', sign)
            if time_match:
                time_value = float(time_match.group(1))
                if time_value < 2 or time_value > 6:
                    return False, f"透析时间 {time_value} 小时不在合理范围内(2-6小时)"
    
    return True, ""

# 获取规则库
def get_rules():
    """获取完整的规则库"""
    return {
        "required_fields": REQUIRED_FIELDS,
        "dialysis_symptoms": DIALYSIS_SYMPTOMS,
        "dialysis_signs": DIALYSIS_SIGNS,
        "dialysis_lab_values": DIALYSIS_LAB_VALUES,
        "logic_rules": LOGIC_RULES
    }
