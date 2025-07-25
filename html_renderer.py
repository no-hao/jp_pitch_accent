def render_ruby(tokens):
    """
    Render a list of tokens as HTML ruby markup with pitch accent info.
    Each token should be a dict with 'surface', 'reading', and 'pitch' keys.
    Example output: <ruby>食べる<rt>たべる [1]</rt></ruby>
    """
    html = []
    for token in tokens:
        surface = token.get('surface', '')
        reading = token.get('reading', '')
        pitch = token.get('pitch', None)
        if reading and pitch is not None:
            rt = f"{reading} [{pitch}]"
            html.append(f"<ruby>{surface}<rt>{rt}</rt></ruby>")
        else:
            html.append(surface)
    return ''.join(html)
