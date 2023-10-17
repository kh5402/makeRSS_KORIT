import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import pytz

def main():
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    
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
            date = articleContent.split('<time class="c-columnList__date" datetime="')[1].split('"')[0]
            title = articleContent.split('<h2 class="c-columnList__title">')[1].split('</h2>')[0].strip()
            
            dateObj = datetime.fromisoformat(date).astimezone(pytz.timezone('GMT'))
            dateStr = dateObj.strftime('%a, %d %b %Y %H:%M:%S %Z')
            
            item = ET.SubElement(channel, "item")
            ET.SubElement(item, "title").text = title
            ET.SubElement(item, "link").text = link
            ET.SubElement(item, "pubDate").text = dateStr
            
        if not found:
            break
            
    tree = ET.ElementTree(rss)
    tree.write("feed_Korit.xml")

if __name__ == "__main__":
    main()
