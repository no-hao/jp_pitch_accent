import math

def get_pitch_pattern(mora_count: int, pitch_type: int) -> list[str]:
    """
    Generate the correct H/L pattern based on pitch type and mora count.
    pitch_type: 
        0 = 平板式 (heiban): Starts low, goes high, stays high
        1 = 頭高型 (atamadaka): Starts high, drops, stays low
        2 = 中高型 (nakadaka): Starts low, second mora high, drops, stays low
        3 = 尾高型 (odaka): Starts low, goes high, stays high
    """
    if mora_count == 0:
        return []
        
    if pitch_type == 0:  # 平板式 (heiban)
        if mora_count == 1:
            return ['L']  # Single mora stays low
        return ['L'] + ['H'] * (mora_count - 1)  # Low start, then all high
        
    elif pitch_type == 1:  # 頭高型 (atamadaka)
        if mora_count == 1:
            return ['H']
        return ['H'] + ['L'] * (mora_count - 1)  # High start, rest low
        
    elif pitch_type == 2:  # 中高型 (nakadaka)
        if mora_count <= 1:
            return ['L']
        if mora_count == 2:
            return ['L', 'H']  # Two mora case
        return ['L', 'H'] + ['L'] * (mora_count - 2)  # Low, high, rest low
        
    elif pitch_type == 3:  # 尾高型 (odaka)
        if mora_count == 1:
            return ['H']
        return ['L'] + ['H'] * (mora_count - 1)  # Low start, rest high
        
    return ['L'] * mora_count

def generate_pitch_svg(pattern: list[str], text_length: int = None) -> str:
    """
    Generate SVG for a pitch accent pattern.
    pattern: list of 'H' (high position) or 'L' (low position) - all circles are black
    text_length: length of the text this SVG will annotate (for proportional sizing)
    Returns: SVG string
    """
    if not pattern:
        return ""

    # SVG parameters - adjusted for more compact display
    circle_radius = 3
    circle_stroke = 0.75
    
    # Layout parameters
    point_spacing = 15  # Reduced spacing between points
    vertical_gap = 8   # Reduced vertical gap
    margin = 8        # Reduced margin
    
    # Calculate dimensions
    width = margin * 2 + (len(pattern) - 1) * point_spacing
    height = margin + vertical_gap + circle_radius * 2
    
    # Y positions for high and low pitch
    high_y = margin
    low_y = high_y + vertical_gap
    
    # Start SVG
    svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
    
    # Calculate points
    points = []
    for i, pitch in enumerate(pattern):
        x = margin + (i * point_spacing)
        y = high_y if pitch == 'H' else low_y
        points.append((x, y))

    # Draw connecting lines first
    path = []
    for i in range(len(points)):
        x, y = points[i][0], points[i][1]
        if i == 0:
            path.append(f"M {x},{y}")
        else:
            path.append(f"L {x},{y}")
            
    svg += f'<path d="{" ".join(path)}" stroke="black" fill="none" stroke-width="{circle_stroke}"/>'
    
    # Add circles on top of lines - all black but at different heights
    for x, y in points:
        svg += f'<circle cx="{x}" cy="{y}" r="{circle_radius}" stroke="black" stroke-width="{circle_stroke}" fill="black"/>'
    
    svg += '</svg>'
    return svg

def generate_pitch_html(pattern: list[str], text: str = "", label: str = "") -> str:
    """
    Generate HTML with embedded SVG for a pitch accent pattern.
    pattern: list of 'H' (high), 'L' (low)
    text: the text this pattern is annotating (for proportional sizing)
    label: optional label for the pattern
    Returns: HTML string with embedded SVG
    """
    text_length = len(text) if text else None
    svg = generate_pitch_svg(pattern, text_length)
    html = f'<div class="pitch-accent-container">'
    if text:
        html += f'<div class="word">{text}</div>'
    html += f'<div class="pitch-accent">{svg}</div>'
    if label:
        html += f'<div class="pattern">{label}</div>'
    html += '</div>'
    return html 