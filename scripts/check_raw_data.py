import json

with open("data/raw/kpl_raw.json", "r", encoding="utf-8") as f:
    data=json.load(f)

print(f"成功读取{len(data)}条kpl原始数据")

for item in data[:3]:
    print(item["title"],item["type"])