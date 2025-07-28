#!/usr/bin/env python3
"""
Comprehensive visual demonstration of Japanese pitch accent patterns from the chart.
Generates an HTML file showing the actual SVG output for all examples in the chart.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pitch_svg import get_pitch_pattern, get_accent_position, generate_pitch_svg, generate_pitch_html
from pitch_db import katakana_to_hiragana

def create_chart_visual_demo():
    """Create a visual demonstration of all pitch accent patterns from the chart"""
    
    print("📊 Generating Chart-Based Pitch Accent Demonstration...")
    print("=" * 60)
    print("This will generate an HTML file with all examples from the provided chart.")
    print("You can compare the generated SVGs directly with the chart.\n")
    
    # All examples from the Japanese pitch accent chart
    # Format: (word, reading, mora_count, drop_pos, pitch_type_description)
    chart_examples = [
        # 一拍語 (1 mora)
        ("名", "な", 1, 0, "Heiban (平板式)"),
        ("木", "き", 1, 1, "Atamadaka (頭高型)"),

        # 二拍語 (2 morae)
        ("水", "みず", 2, 0, "Heiban (平板式)"),
        ("秋", "あき", 2, 1, "Atamadaka (頭高型)"),
        ("花", "はな", 2, 2, "Odaka (尾高型)"),

        # 三拍語 (3 morae)
        ("会社", "かいしゃ", 3, 0, "Heiban (平板式)"),
        ("電気", "でんき", 3, 1, "Atamadaka (頭高型)"),
        ("お菓子", "おかし", 3, 2, "Nakadaka (中高型)"),
        ("男", "おとこ", 3, 3, "Odaka (尾高型)"),

        # 四拍語 (4 morae)
        ("大学", "だいがく", 4, 0, "Heiban (平板式)"),
        ("文学", "ぶんがく", 4, 1, "Atamadaka (頭高型)"),
        ("雪国", "ゆきぐに", 4, 2, "Nakadaka (中高型)"),
        ("祭日", "さいじき", 4, 3, "Nakadaka (中高型)"),
        ("弟", "おとうと", 4, 4, "Odaka (尾高型)"),

        # 五拍語 (5 morae)
        ("中国語", "ちゅうごくご", 5, 0, "Heiban (平板式)"),
        ("シャーペン", "しゃあぺん", 5, 1, "Atamadaka (頭高型)"),
        ("普及率", "ふきゅうりつ", 5, 2, "Nakadaka (中高型)"),
        ("山登り", "やまのぼり", 5, 3, "Nakadaka (中高型)"),
        ("小型バス", "こがたばす", 5, 4, "Nakadaka (中高型)"),
        ("桃の花", "もものはな", 5, 5, "Odaka (尾高型)"),

        # 六拍語 (6 morae)
        ("見物人", "けんぶつにん", 6, 0, "Heiban (平板式)"),
        ("けんもほろろ", "けんもほろろ", 6, 1, "Atamadaka (頭高型)"),
        ("お巡りさん", "おまわりさん", 6, 2, "Nakadaka (中高型)"),
        ("金婚式", "きんこんしき", 6, 3, "Nakadaka (中高型)"),
        ("国語辞典", "こくごじてん", 6, 4, "Nakadaka (中高型)"),
        ("炭酸ガス", "たんさんがす", 6, 5, "Nakadaka (中高型)"),
        ("十一月", "じゅういちがつ", 6, 6, "Odaka (尾高型)"),
    ]

    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Japanese Pitch Accent Chart - Complete Visual Guide</title>
    <style>
        body {
            font-family: 'Hiragino Kaku Gothic Pro', 'Yu Gothic', 'Segoe UI', sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
            color: #333;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        .header p {
            margin: 10px 0 0 0;
            font-size: 1.2em;
            opacity: 0.9;
        }
        .legend {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 20px 0;
            text-align: center;
        }
        .legend h3 {
            margin-top: 0;
            color: #2c5aa0;
            font-size: 1.3em;
        }
        .legend-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 8px;
            font-size: 14px;
        }
        .legend-dot {
            display: inline-block;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            margin-right: 12px;
            border: 2px solid #333;
        }
        .legend-dot.black {
            background-color: black;
        }
        .legend-dot.white {
            background-color: white;
        }
        .info {
            background-color: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .info h3 {
            margin-top: 0;
            color: #1976d2;
        }
        .info ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        .info li {
            margin: 8px 0;
            line-height: 1.5;
        }
        .mora-section {
            margin: 40px 0;
        }
        .mora-section h2 {
            color: #2c5aa0;
            border-bottom: 3px solid #2c5aa0;
            padding-bottom: 10px;
            margin-bottom: 25px;
            font-size: 1.8em;
        }
        .examples-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .example-card {
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            padding: 20px;
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .example-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        .word {
            font-size: 1.8em;
            font-weight: bold;
            margin-bottom: 8px;
            color: #2c3e50;
        }
        .reading {
            font-size: 1.2em;
            color: #7f8c8d;
            margin-bottom: 12px;
        }
        .pitch-type {
            font-size: 1em;
            color: #e74c3c;
            font-weight: bold;
            margin-bottom: 15px;
            padding: 5px 12px;
            background-color: #fdf2f2;
            border-radius: 20px;
            display: inline-block;
        }
        .pattern-info {
            background-color: #f8f9fa;
            padding: 12px;
            border-radius: 8px;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            text-align: left;
        }
        .svg-container {
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 15px;
            background-color: #fafafa;
            margin: 15px 0;
            display: inline-block;
        }
        .visual-summary {
            font-family: monospace;
            font-size: 16px;
            margin-top: 10px;
            padding: 8px;
            background-color: #f1f3f4;
            border-radius: 5px;
        }
        .stats {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 20px 0;
            text-align: center;
        }
        .stats h3 {
            color: #2c5aa0;
            margin-top: 0;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .stat-item {
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 8px;
        }
        .stat-number {
            font-size: 1.5em;
            font-weight: bold;
            color: #2c5aa0;
        }
        .stat-label {
            font-size: 0.9em;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🇯🇵 Japanese Pitch Accent Chart</h1>
        <p>Complete Visual Guide - All Examples from the Official Chart</p>
    </div>
    
    <div class="legend">
        <h3>📖 How to Read This Guide</h3>
        <div class="legend-grid">
            <div class="legend-item">
                <span class="legend-dot black"></span>
                <strong>Black dot:</strong> Normal mora (no accent)
            </div>
            <div class="legend-item">
                <span class="legend-dot white"></span>
                <strong>White dot:</strong> Accent mora (where pitch drops)
            </div>
            <div class="legend-item">
                <strong>Position:</strong> Dots show actual pitch contour (high/low)
            </div>
            <div class="legend-item">
                <strong>Pattern:</strong> Follows official Japanese pitch accent rules
            </div>
        </div>
    </div>
    
    <div class="info">
        <h3>🎵 Understanding Japanese Pitch Accent Patterns</h3>
        <ul>
            <li><strong>Heiban (平板式):</strong> Starts low, goes high, stays high (no accent mora)</li>
            <li><strong>Atamadaka (頭高型):</strong> Starts high, drops after first mora (first mora is accent)</li>
            <li><strong>Nakadaka (中高型):</strong> Starts low, rises, drops after accent mora (middle mora is accent)</li>
            <li><strong>Odaka (尾高型):</strong> Starts low, rises, stays high until end (last mora is accent)</li>
        </ul>
    </div>
"""
    
    # Group examples by mora count
    mora_groups = {}
    for example in chart_examples:
        word, reading, mora_count, drop_pos, pitch_type = example
        if mora_count not in mora_groups:
            mora_groups[mora_count] = []
        mora_groups[mora_count].append(example)
    
    # Add each mora group
    for mora_count in sorted(mora_groups.keys()):
        examples = mora_groups[mora_count]
        html_content += f"""
    <div class="mora-section">
        <h2>{mora_count} Mora Words ({len(examples)} examples)</h2>
        <div class="examples-grid">
"""
        
        for word, reading, mora_count, drop_pos, pitch_type in examples:
            pitch_pattern = get_pitch_pattern(mora_count, drop_pos)
            accent_positions = get_accent_position(mora_count, drop_pos)
            svg_html = generate_pitch_html(pitch_pattern, accent_positions, reading, pitch_type)
            
            # Create visual representation
            visual = ""
            height_visual = ""
            for pitch, is_accent in zip(pitch_pattern, accent_positions):
                if is_accent:
                    visual += "○"  # White accent dot
                else:
                    visual += "●"  # Black normal dot
                height_visual += "↑" if pitch == 'H' else "↓"
            
            html_content += f"""
            <div class="example-card">
                <div class="word">{word}</div>
                <div class="reading">({reading})</div>
                <div class="pitch-type">{pitch_type}</div>
                <div class="pattern-info">
                    <strong>Pattern:</strong> {pitch_pattern}<br>
                    <strong>Accent:</strong> {accent_positions}<br>
                    <strong>Height:</strong> {height_visual}
                </div>
                <div class="svg-container">
                    {svg_html}
                </div>
                <div class="visual-summary">
                    {visual} | {height_visual}
                </div>
            </div>
"""
        
        html_content += """
        </div>
    </div>
"""
    
    # Add statistics
    total_examples = len(chart_examples)
    heiban_count = sum(1 for _, _, _, drop_pos, _ in chart_examples if drop_pos == 0)
    atamadaka_count = sum(1 for _, _, _, drop_pos, _ in chart_examples if drop_pos == 1)
    nakadaka_count = sum(1 for _, _, _, drop_pos, _ in chart_examples if 1 < drop_pos < max(e[2] for e in chart_examples))
    odaka_count = sum(1 for _, _, mora_count, drop_pos, _ in chart_examples if drop_pos == mora_count)
    
    html_content += f"""
    <div class="stats">
        <h3>📊 Chart Statistics</h3>
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-number">{total_examples}</div>
                <div class="stat-label">Total Examples</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{heiban_count}</div>
                <div class="stat-label">Heiban (平板式)</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{atamadaka_count}</div>
                <div class="stat-label">Atamadaka (頭高型)</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{nakadaka_count}</div>
                <div class="stat-label">Nakadaka (中高型)</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{odaka_count}</div>
                <div class="stat-label">Odaka (尾高型)</div>
            </div>
        </div>
    </div>
"""
    
    html_content += """
</body>
</html>
"""
    
    # Write to file
    output_filename = "pitch_accent_chart_guide.html"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ Generated '{output_filename}' successfully!")
    print(f"📊 Total examples: {len(chart_examples)}")
    print(f"🎯 All examples from the official chart included")
    print(f"🌐 Open the HTML file in your web browser to see the complete visual guide!")

if __name__ == '__main__':
    create_chart_visual_demo() 