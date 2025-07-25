from pitch_svg import get_pitch_pattern, generate_pitch_svg

# HTML template parts
HTML_HEAD = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>日本語のアクセントの型</title>
    <style>
        body { 
            font-family: "Hiragino Sans", "Hiragino Kaku Gothic Pro", "Yu Gothic", Meiryo, sans-serif; 
            padding: 20px; 
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            background: #fff;
        }
        h2 {
            font-size: 1.2em;
            margin: 1em 0 0.5em;
            padding: 5px 0;
            border-bottom: 1px solid #ddd;
        }
        .section {
            margin: 20px 0;
            padding: 10px;
            background: #f8f8f8;
            border-radius: 4px;
        }
        .section-title {
            font-size: 1.2em;
            margin: 0 0 10px 0;
            padding: 5px 0;
            border-bottom: 1px solid #ddd;
        }
        .pitch-accent-container { 
            display: flex;
            align-items: center;
            padding: 10px;
            background: white;
            margin: 5px 0;
            gap: 20px;
            border-radius: 2px;
        }
        .word { 
            font-size: 1.2em;
            min-width: 120px;
        }
        .pitch-accent {
            min-width: 150px;
        }
        .pattern { 
            color: #333;
            min-width: 200px;
        }
        .note {
            margin-top: 20px;
            padding: 10px;
            background: #fff;
            border-radius: 4px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
'''

HTML_FOOT = '''
<div class="note">
    <p>平板式 (へいばん)：最初が低く、2拍目から高くなり、そのまま高く続く</p>
    <p>頭高型 (あたまだか)：最初が高く、2拍目から低くなる</p>
    <p>中高型 (なかだか)：最初が低く、2拍目が高く、その後で下がる</p>
    <p>尾高型 (おだか)：最初が低く、2拍目から高くなり、助詞で下がる</p>
</div>
</body>
</html>'''

def generate_section(title, words):
    html = f'''
    <div class="section">
        <div class="section-title">{title}</div>'''
    
    for word, reading, mora_count, mora_text in words:
        pattern = get_pitch_pattern(mora_count, pitch_type_from_title(title))
        
        html += f'''
        <div class="pitch-accent-container">
            <div class="word">{word}</div>
            <div class="pitch-accent">{generate_pitch_svg(pattern)}</div>
            <div class="pattern">{mora_text} ({reading})</div>
        </div>'''
    
    html += '\n    </div>'
    return html

def pitch_type_from_title(title):
    types = {
        "平板式 (へいばん)": 0,
        "頭高型 (あたまだか)": 1,
        "中高型 (なかだか)": 2,
        "尾高型 (おだか)": 3
    }
    return types[title]

# Group words by pattern type
sections = {
    "平板式 (へいばん)": [
        ("名", "な", 1, "一拍語"),
        ("水", "みず", 2, "二拍語"),
        ("会社", "かいしゃ", 3, "三拍語"),
        ("大学", "だいがく", 4, "四拍語"),
        ("中国語", "ちゅうごくご", 5, "五拍語"),
        ("見物人", "けんぶつにん", 6, "六拍語"),
    ],
    "頭高型 (あたまだか)": [
        ("木", "き", 1, "一拍語"),
        ("秋", "あき", 2, "二拍語"),
        ("電気", "でんき", 3, "三拍語"),
        ("文学", "ぶんがく", 4, "四拍語"),
        ("シャーペット", "しゃーぺっと", 5, "五拍語"),
        ("げんもほろろ", "げんもほろろ", 6, "六拍語"),
    ],
    "中高型 (なかだか)": [
        ("花", "はな", 2, "二拍語"),
        ("お菓子", "おかし", 3, "三拍語"),
        ("雪国", "ゆきぐに", 4, "四拍語"),
        ("山登り", "やまのぼり", 5, "五拍語"),
        ("お巡りさん", "おまわりさん", 6, "六拍語"),
    ],
    "尾高型 (おだか)": [
        ("男", "おとこ", 3, "三拍語"),
        ("兄弟", "きょうだい", 4, "四拍語"),
        ("小型車", "こがたしゃ", 5, "五拍語"),
        ("金婚式", "きんこんしき", 6, "六拍語"),
    ],
}

# Generate the complete HTML
html = HTML_HEAD
for title, words in sections.items():
    html += generate_section(title, words)
html += '''
<div class="note">
    <p>平板式 (へいばん)：最初が低く、2拍目から高くなり、そのまま高く続く</p>
    <p>頭高型 (あたまだか)：最初が高く、2拍目から低くなる</p>
    <p>中高型 (なかだか)：最初が低く、2拍目が高く、その後で下がる</p>
    <p>尾高型 (おだか)：最初が低く、2拍目から高くなり、助詞で下がる</p>
</div>
</body>
</html>'''

# Write to file
with open('examples.html', 'w', encoding='utf-8') as f:
    f.write(html) 