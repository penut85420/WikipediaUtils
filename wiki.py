import re

x = lambda x: x.group(1)
rm = [
    # ['<page>', '============================================================================'],
    ['&amp;', '&&'], # Replace URL Encode
    ['&lt;', '<'],
    ['&gt;', '>'],
    ['<ref[^<]*<\/ref>', ''], # Remove <ref ...> ... </ref>
    ['<center>', ''],   # Remove <center>
    ['<\/center>', ''], # Remove </center>
    ['<gallery[^<]*<\/gallery>', ''], # Remove <gallery>...</gallery>
    ['<[^>]*>', ''], # Remove HTML Tag
    ['\[https?:[^] ]*]', ''], # Remove Link
    ['\[https?:[^] ]* ([^]]*)]', x], # Replace with Link Title
    ['\[\/\/[^] ]* ([^]]*)]', x],    # Replace [[...|...]]
    ['\{\{lang[^}]*\|([^}]*)}}', x], # Replace with lang
    ["'''\{\{([^}]*)}}'''", x], # Fake Title
    ["'''", ''], # Bold
    ["''", ''],  # Italic
    # ['（[^（]*）', ''], # Remove （...）
    ['-\{[^\}]*zh-hant:([^\}\;]*)[^}]*}-', x], # Left CT Word
    ['-\{[^\}]*zh-tw:([^\}\;]*)[^}]*}-', x],
    ['\{\{ruby-py\|([^\|]*)\|[^}]*}}', x],
    ['-\{([^\}]*)}-', x],
    ['\[\[category:[^\]]*]]', ''], # Remove category tag
    ['\[\[([^\[\]\|]*)\]\]', x],
    ['\[\[[^]:]*\|([^\]\|]*)\]\]', x],
    ['\[\[[a-z]+:[^\[\]]*]]', ''], # Remove file tag
    ['\[\[image:[^]]*]]', ''],     # Remove image tag
    ['\[\[[^]]*\|([^\]\|]*)\]\]', x], # Replace [[...|...]]
    ['\{\{link-[^\|]*\|([^\|]*)\|[^}]*}}', x], # Replace [[link-...|...]]
    ['\{\{[^\{\}]*}}', ''], # Remove {{...}}
    ['\{[^{}]*}', ''], # Remove {...}
    ['&[^; ]*;', ''],  # Remove URL Encode Token, e.g. &quot;
    ['&&', '&amp;'],   # Retain & back to &amp;
    ['^[\*:#;]+ *', ''], # 移除 :#*; 開頭空白
    ['^\|[^\n]*', ''], # 清除 | 開頭的行
    ['\n。', '。\n'], # 修正不合理的句號 (Optimal)
    ['，\n', '，'],   # 修正不合理的逗號 (Optimal)
    ['\n：\n', ''], # 清除 :{...} 殘留的冒號
    ['^ +', ''],    # 清除行頭的空白
    ['\n\n', '\n'], # 清除重複的換行
]

def remove_wikitext(s):
    if not isinstance(s, str):
        return None

    for rr in rm:
        while re.search(rr[0], s, re.M+re.I):
            s = re.sub(rr[0], rr[1], s, flags=re.M+re.I)

    return s.strip()

if __name__ == '__main__':
    s = """[[File:上海市人大頒布的上海市市標.png|thumb|200px|'''[[s:上海市市標製作使用管理暫行規定|上海市市標]]'''：「以市花白玉蘭、沙船和螺旋槳三者組成的三角形圖案。三角圖形似輪船的螺旋槳，象徵著上海是一座不斷前進的城市；圖案中心揚帆出海的沙船，是上海港最古老的船舶，象徵著上海是一個歷史悠久的港口城市；沙船的背景是迎著早春盛開的白玉蘭，展示了城市的勃勃生機。」]]今天天氣真好"""
    print(remove_wikitext(s))

    s = None
    print(remove_wikitext(s))
