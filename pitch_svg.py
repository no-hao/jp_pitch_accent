import math

def get_pitch_pattern(mora_count: int, drop_pos: int) -> list[str]:
    """
    Generate the correct H/L pattern based on drop position.
    This shows the actual pitch contour - H = high position, L = low position.
    
    drop_pos: The position where pitch drops (0-based)
    - 0: Heiban - starts low, goes high, stays high
    - 1: Atamadaka - starts high, drops, stays low  
    - n: Nakadaka - starts low, rises, drops after n-th mora
    - mora_count: Odaka - starts low, rises, stays high until end
    """
    if mora_count == 0:
        return []
    
    if drop_pos == 0:  # Heiban (平板式)
        if mora_count == 1:
            return ['L']  # Single mora stays low
        return ['L'] + ['H'] * (mora_count - 1)  # Low start, then all high
        
    elif drop_pos == 1:  # Atamadaka (頭高型)
        if mora_count == 1:
            return ['H']
        return ['H'] + ['L'] * (mora_count - 1)  # High start, rest low
        
    elif drop_pos == mora_count:  # Odaka (尾高型)
        if mora_count == 1:
            return ['H']
        return ['L'] + ['H'] * (mora_count - 1)  # Low start, rest high
        
    else:  # Nakadaka (中高型)
        if mora_count <= 1:
            return ['L']
        if mora_count == 2:
            return ['L', 'H']  # Two mora case
        # For longer words, start low, rise to high, stay high until drop position, then drop
        pattern = ['L']  # Start low
        for i in range(1, mora_count):
            if i < drop_pos:
                pattern.append('H')  # Stay high until drop position
            else:
                pattern.append('L')  # Drop after accent mora
        return pattern
        
    return ['L'] * mora_count

def get_accent_position(mora_count: int, drop_pos: int) -> list[bool]:
    """
    Generate accent positions based on drop position.
    Returns a list of booleans where True indicates an accent mora (white dot).
    
    drop_pos: The position where pitch drops (0-based)
    - 0: Heiban (no accent mora)
    - 1: Atamadaka (first mora is accent)
    - n: Nakadaka (n-th mora is accent, where 1 < n < mora_count)
    - mora_count: Odaka (last mora is accent)
    """
    if mora_count == 0:
        return []
    
    # Initialize all positions as False (black dots)
    accent_positions = [False] * mora_count
    
    # Set the accent mora to True (white dot)
    if drop_pos > 0 and drop_pos <= mora_count:
        accent_positions[drop_pos - 1] = True  # Convert to 0-based index
    
    return accent_positions

def generate_pitch_svg(pitch_pattern: list[str], accent_positions: list[bool], text_length: int = None) -> str:
    """
    Generate SVG for a pitch accent pattern.
    pitch_pattern: list of 'H' (high position) or 'L' (low position)
    accent_positions: list of booleans where True = accent mora (white dot), False = normal mora (black dot)
    text_length: length of the text this SVG will annotate (for proportional sizing)
    Returns: SVG string
    """
    if not pitch_pattern or not accent_positions:
        return ""

    # SVG parameters - adjusted for more compact display
    circle_radius = 3
    circle_stroke = 0.75
    
    # Layout parameters
    point_spacing = 15  # Reduced spacing between points
    vertical_gap = 8   # Reduced vertical gap
    margin = 8        # Reduced margin
    
    # Adjust spacing based on text length if provided
    if text_length and text_length > len(pitch_pattern):
        # Scale spacing proportionally to text length
        scale_factor = text_length / len(pitch_pattern)
        point_spacing = int(point_spacing * scale_factor)
    
    # Calculate dimensions
    width = margin * 2 + (len(pitch_pattern) - 1) * point_spacing
    height = margin + vertical_gap + circle_radius * 2
    
    # Y positions for high and low pitch
    high_y = margin
    low_y = high_y + vertical_gap
    
    # Start SVG
    svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
    
    # Calculate points based on pitch pattern (high/low positioning)
    points = []
    for i, pitch in enumerate(pitch_pattern):
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
    
    # Add circles on top of lines - accent morae are white, others are black
    for i, (x, y) in enumerate(points):
        is_accent = accent_positions[i]
        fill_color = "white" if is_accent else "black"
        svg += f'<circle cx="{x}" cy="{y}" r="{circle_radius}" stroke="black" stroke-width="{circle_stroke}" fill="{fill_color}"/>'
    
    svg += '</svg>'
    return svg

def generate_pitch_html(pitch_pattern: list[str], accent_positions: list[bool], text: str = "", label: str = "") -> str:
    """
    Generate HTML with embedded SVG for a pitch accent pattern.
    pitch_pattern: list of 'H' (high), 'L' (low) - for positioning
    accent_positions: list of booleans where True = accent mora (white dot), False = normal mora (black dot)
    text: the text this pattern is annotating (for proportional sizing)
    label: optional label for the pattern
    Returns: HTML string with embedded SVG
    """
    text_length = len(text) if text else None
    svg = generate_pitch_svg(pitch_pattern, accent_positions, text_length)
    html = f'<div class="pitch-accent-container">'
    if text:
        html += f'<div class="word">{text}</div>'
    html += f'<div class="pitch-accent">{svg}</div>'
    if label:
        html += f'<div class="pattern">{label}</div>'
    html += '</div>'
    return html 