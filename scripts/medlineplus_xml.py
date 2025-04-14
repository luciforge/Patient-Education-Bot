import xml.etree.ElementTree as ET
import json
from pathlib import Path

xml_path = Path("data/medlineplus/mplus_topics_2025-04-04.xml")
tree = ET.parse(xml_path)
root = tree.getroot()

topics = []
for topic in root.findall("health-topic"):
    title = topic.attrib.get("title")
    summary = topic.findtext("full-summary")
    url = topic.attrib.get("url")
    aliases = [ac.text for ac in topic.findall("also-called")]
    source = "MedlinePlus"

    if summary:
        summary = summary.replace("&lt;", "<").replace("&gt;", ">")

    topics.append({
        "term": title,
        "definition": summary,
        "aliases": aliases,
        "source": source,
        "source_url": url
    })

#Output path
out_path = Path("data/medlineplus/medical_kb.json")
out_path.write_text(json.dumps(topics, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Extracted {len(topics)} health topics to: {out_path.resolve()}")
