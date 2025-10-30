import json
from pathlib import Path
from time import sleep
from deep_translator import GoogleTranslator

# 文件路径
input_path = Path("browser_protocol.json")
output_path = Path("browser_protocol_zh.json")

translator = GoogleTranslator(source="en", target="zh-CN")

def translate_descriptions(obj):
    """递归翻译所有 description 字段"""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "description" and isinstance(v, str):
                try:
                    obj[k] = translator.translate(v)
                    sleep(0.3)  # 防止触发请求限制
                    print(f'翻译完成：{obj[k]}')
                except Exception:
                    obj[k] = v
            else:
                obj[k] = translate_descriptions(v)
    elif isinstance(obj, list):
        obj = [translate_descriptions(i) for i in obj]
    return obj

if __name__ == "__main__":
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data_zh = translate_descriptions(data)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data_zh, f, ensure_ascii=False, indent=2)

    print("✅ 翻译完成，生成文件：", output_path)
