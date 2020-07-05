def add_attrs(html, url, state={}):
    attrs = f' data-cable-url={url}'
    for key, value in state.items():
        if callable(value):
            continue
        attrs += f' data-cable-{key}="{value}"'
    pos = html.index('>')
    return html[:pos] + attrs + html[pos:]
