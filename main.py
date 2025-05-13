"""
主程序模块，集成所有功能模块，实现从非结构化病历中提取信息、识别缺口并生成指导意见的完整流程
"""

import json
from text_preprocessing import preprocess_medical_text
from entity_recognition import extract_medical_entities
from gap_identification import identify_gaps
from guidance_generation import generate_guidance
from rules import get_rules
from knowledge_base import get_knowledge_base

def process_medical_record(text):
    """处理非结构化病历文本
    
    Args:
        text (str): 非结构化病历文本
        
    Returns:
        dict: 处理结果，包括提取的实体、识别的缺口和指导意见
    """
    # 1. 文本预处理
    preprocessed_text = preprocess_medical_text(text)
    
    # 2. 医疗实体识别
    extracted_entities = extract_medical_entities(preprocessed_text)
    
    # 3. 获取规则库
    rules = get_rules()
    
    # 4. 缺口识别
    gaps = identify_gaps(extracted_entities, rules)
    
    # 5. 获取知识库
    knowledge_base = get_knowledge_base()
    
    # 6. 生成指导意见
    guidance = generate_guidance(gaps, knowledge_base, extracted_entities)
    
    # 7. 整合结果
    result = {
        "preprocessed_text": preprocessed_text,
        "extracted_entities": extracted_entities,
        "gaps": gaps,
        "guidance": guidance
    }
    
    return result

def format_result(result):
    """格式化处理结果为易读的文本
    
    Args:
        result (dict): 处理结果
        
    Returns:
        str: 格式化后的文本
    """
    output = []
    
    # 1. 原始文本
    output.append("=== 原始病历文本 ===")
    output.append(result["preprocessed_text"]["original"])
    output.append("")
    
    # 2. 提取的医疗实体
    output.append("=== 提取的医疗实体 ===")
    
    # 症状
    output.append("症状:")
    if result["extracted_entities"]["symptoms"]:
        for symptom in result["extracted_entities"]["symptoms"]:
            output.append(f"- {symptom}")
    else:
        output.append("- 未提取到症状")
    
    # 体征
    output.append("\n体征:")
    if result["extracted_entities"]["signs"]:
        for sign in result["extracted_entities"]["signs"]:
            output.append(f"- {sign}")
    else:
        output.append("- 未提取到体征")
    
    # 检验值
    output.append("\n检验值:")
    if result["extracted_entities"]["lab_values"]:
        for lab_value in result["extracted_entities"]["lab_values"]:
            output.append(f"- {lab_value}")
    else:
        output.append("- 未提取到检验值")
    
    output.append("")
    
    # 3. 识别的缺口
    output.append("=== 识别的缺口 ===")
    if result["gaps"]:
        for gap in result["gaps"]:
            output.append(f"- {gap}")
    else:
        output.append("- 未识别到缺口")
    
    output.append("")
    
    # 4. 指导意见
    output.append("=== 指导意见 ===")
    if result["guidance"]["suggestions"]:
        for suggestion in result["guidance"]["suggestions"]:
            output.append(f"- {suggestion}")
    else:
        output.append("- 无指导意见")
    
    return "\n".join(output)

def main():
    """主函数"""
    print("=== 非结构化病历分析系统 ===")
    print("请输入病历文本（输入'exit'退出）：")
    
    while True:
        # 获取用户输入
        text = input("> ")
        
        if text.lower() == 'exit':
            print("感谢使用，再见！")
            break
        
        if not text.strip():
            print("请输入有效的病历文本！")
            continue
        
        # 处理病历文本
        try:
            result = process_medical_record(text)
            formatted_result = format_result(result)
            print("\n" + formatted_result)
            
            # 询问是否保存结果
            save = input("\n是否保存结果？(y/n): ")
            if save.lower() == 'y':
                filename = input("请输入文件名（默认为'result.txt'）: ") or "result.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(formatted_result)
                print(f"结果已保存到 {filename}")
        
        except Exception as e:
            print(f"处理过程中出现错误: {str(e)}")
        
        print("\n请输入下一条病历文本（输入'exit'退出）：")

# 示例用法
if __name__ == "__main__":
    main()
