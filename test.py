"""
测试模块，用于测试系统功能
"""

from main import process_medical_record, format_result

# 测试用例
TEST_CASES = [
    {
        "name": "基本测试 - 包含症状和体征",
        "text": "2023年09月28日，患者头晕，体重下降6kg，尿量减少。血压120/80mmHg，脉搏80次/分。"
    },
    {
        "name": "透析记录 - 缺少关键信息",
        "text": "2023年10月15日，患者进行血液透析治疗，使用肝素抗凝，透析过程中出现头晕、恶心症状。"
    },
    {
        "name": "完整透析记录",
        "text": "2023年11月05日，患者进行血液透析治疗，透析器型号FX80，血流量250ml/min，透析液流量500ml/min，使用低分子肝素4000单位抗凝，透析时间4小时，超滤量2.5kg。透析前体重65kg，透析后体重62.5kg，透析前血压150/90mmHg，透析后血压130/80mmHg。内瘘杂音清晰，无并发症。"
    }
]

def run_tests():
    """运行所有测试用例"""
    print("=== 开始测试 ===\n")
    
    for i, test_case in enumerate(TEST_CASES):
        print(f"测试用例 {i+1}: {test_case['name']}")
        print(f"输入文本: {test_case['text']}")
        
        # 处理病历文本
        result = process_medical_record(test_case['text'])
        formatted_result = format_result(result)
        
        print("\n处理结果:")
        print(formatted_result)
        print("\n" + "="*50 + "\n")
    
    print("=== 测试完成 ===")

if __name__ == "__main__":
    run_tests()
