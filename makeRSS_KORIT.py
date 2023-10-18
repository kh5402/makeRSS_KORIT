import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import pytz
import os

def main():
    output_file = "feed_Korit.xml"
    
    # 既存のRSSフィードを読み込む
    existing_links = set()
    if os.path.exists(output_file):
        tree = ET.parse(output_file)
        root = tree.getroot()
        for item in root.findall(".//item/link"):
            existing_links.add(item.text)
    else:
        root = ET.Element("rss", version="2.0")
        channel = ET.SubElement(root, "channel")
        ET.SubElement(channel, "title").text = "KORIT"
        ET.SubElement(channel, "description").text = "韓国のIT&スタートアップ業界専門メディア"
        ET.SubElement(channel, "link").text = "https://www.korit.jp/column"

    for currentPage in range(1, 11):
        url = f"https://www.korit.jp/column?page={currentPage}"
        response = requests.get(url)
        pageContent = response.text
        
        found = False
        for match in pageContent.split('<li class="s-articles__item c-columnList__item">')[1:]:
            found = True
            end_index = match.find('</li>')
            articleContent = match[:end_index]
            
            link = 'https://www.korit.jp' + articleContent.split('<a href="')[1].split('"')[0]
            
            # 既存のリンクならスキップ
            if link in existing_links:
                continue
            
            date = articleContent.split('<time class="c-columnList__date" datetime="')[1].split('"')[0]
            title = articleContent.split('<h2 class="c-columnList__title">')[1].split('</h2>')[0].strip()
            
            dateObj = datetime.fromisoformat(date).astimezone(pytz.timezone('GMT'))
            dateStr = dateObj.strftime('%a, %d %b %Y %H:%M:%S %Z')
            
            channel = root.find("channel")
            item = ET.SubElement(channel, "item")
            ET.SubElement(item, "title").text = title
            ET.SubElement(item, "link").text = link
            ET.SubElement(item, "pubDate").text = dateStr
            
        if not found:
            break
    
    # 整形して保存
    xml_str = ET.tostring(root)
    # 不正なXML文字を取り除く
    xml_str = re.sub(u'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', xml_str.decode()).encode()
    xml_pretty_str = minidom.parseString(xml_str).toprettyxml(indent="  ")
    
    with open(output_file, "w") as f:
        f.write(xml_pretty_str)

if __name__ == "__main__":
    main()
