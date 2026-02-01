"""
Export Notation Module
Handles exporting beat notation to various formats (HTML, SVG, Text)

This module generates exportable representations of the notation grid,
suitable for printing, sharing, and archiving.
"""

import base64
from typing import Optional
from dataclasses import dataclass
from beat_grid import BeatGrid


@dataclass
class ExportConfig:
    """Configuration options for export"""
    title: str = "Beat Notation"
    include_taal_name: bool = True
    include_bol_row: bool = False
    include_matra_numbers: bool = True
    font_size: int = 18
    cell_padding: int = 12
    border_color: str = "#333333"
    sam_color: str = "#e74c3c"  # Red for Sam
    khali_color: str = "#3498db"  # Blue for Khali
    header_bg_color: str = "#f8f9fa"
    cell_bg_color: str = "#ffffff"
    vibhag_border_width: int = 3


def generate_svg(grid: BeatGrid, config: Optional[ExportConfig] = None) -> str:
    """
    Generate an SVG representation of the beat grid
    
    Args:
        grid: The BeatGrid to export
        config: Export configuration options
    
    Returns:
        SVG string
    """
    if config is None:
        config = ExportConfig()
    
    taal = grid.taal
    
    # Calculate dimensions
    cell_width = 80
    cell_height = 50
    header_height = 30
    symbol_height = 30
    padding = 20
    title_height = 40 if config.title else 0
    taal_name_height = 30 if config.include_taal_name else 0
    
    total_width = padding * 2 + cell_width * taal.total_matras
    total_height = padding * 2 + title_height + taal_name_height + header_height + symbol_height + cell_height
    
    vibhag_starts = set(taal.get_vibhag_start_matras())
    
    svg_parts = []
    
    # SVG header
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="{total_height}" viewBox="0 0 {total_width} {total_height}">')
    
    # Background
    svg_parts.append(f'<rect width="100%" height="100%" fill="white"/>')
    
    # Title
    current_y = padding
    if config.title:
        svg_parts.append(f'<text x="{total_width/2}" y="{current_y + 25}" text-anchor="middle" font-size="{config.font_size + 6}" font-weight="bold" font-family="Arial, sans-serif">{config.title}</text>')
        current_y += title_height
    
    # Taal name
    if config.include_taal_name:
        svg_parts.append(f'<text x="{total_width/2}" y="{current_y + 20}" text-anchor="middle" font-size="{config.font_size}" fill="#666" font-family="Arial, sans-serif">{taal.display_name} ({taal.total_matras} Matras)</text>')
        current_y += taal_name_height
    
    # Draw grid
    start_x = padding
    
    for i, matra in enumerate(grid.matras):
        x = start_x + i * cell_width
        is_vibhag_start = matra.matra_number in vibhag_starts
        stroke_width = config.vibhag_border_width if is_vibhag_start else 1
        
        # Matra number cell
        svg_parts.append(f'<rect x="{x}" y="{current_y}" width="{cell_width}" height="{header_height}" fill="{config.header_bg_color}" stroke="{config.border_color}" stroke-width="{stroke_width}"/>')
        svg_parts.append(f'<text x="{x + cell_width/2}" y="{current_y + header_height/2 + 5}" text-anchor="middle" font-size="{config.font_size - 4}" fill="#666" font-family="Arial, sans-serif">{matra.matra_number}</text>')
        
        # Symbol cell
        symbol_y = current_y + header_height
        svg_parts.append(f'<rect x="{x}" y="{symbol_y}" width="{cell_width}" height="{symbol_height}" fill="{config.header_bg_color}" stroke="{config.border_color}" stroke-width="{stroke_width}"/>')
        
        symbol_color = config.sam_color if matra.is_sam else (config.khali_color if matra.is_khali else config.border_color)
        symbol_text = matra.symbol if matra.symbol else ''
        svg_parts.append(f'<text x="{x + cell_width/2}" y="{symbol_y + symbol_height/2 + 5}" text-anchor="middle" font-size="{config.font_size}" font-weight="bold" fill="{symbol_color}" font-family="Arial, sans-serif">{symbol_text}</text>')
        
        # Swar cell
        swar_y = symbol_y + symbol_height
        cell_fill = '#ffeaea' if matra.is_sam else ('#eaf4ff' if matra.is_khali else config.cell_bg_color)
        svg_parts.append(f'<rect x="{x}" y="{swar_y}" width="{cell_width}" height="{cell_height}" fill="{cell_fill}" stroke="{config.border_color}" stroke-width="{stroke_width}"/>')
        
        display_text = matra.get_display_text() or ''
        svg_parts.append(f'<text x="{x + cell_width/2}" y="{swar_y + cell_height/2 + 6}" text-anchor="middle" font-size="{config.font_size + 2}" font-family="Arial, sans-serif">{display_text}</text>')
    
    svg_parts.append('</svg>')
    
    return ''.join(svg_parts)


def generate_html_table_multi(grids: list, config: Optional[ExportConfig] = None) -> str:
    """
    Generate an HTML table representation for multiple beat grids (Aavartans)
    
    Args:
        grids: List of BeatGrid objects (one per Aavartan/line)
        config: Export configuration options
    
    Returns:
        HTML string containing the styled tables for all lines
    """
    if config is None:
        config = ExportConfig(font_size=24)  # Larger default font
    
    if not grids:
        return ""
    
    taal = grids[0].taal
    
    # Start building HTML
    html_parts = []
    
    # Add styles with larger fonts
    html_parts.append(f'''
    <style>
        .notation-container {{
            font-family: 'Noto Sans Devanagari', 'Segoe UI', Arial, sans-serif;
            padding: 20px;
            max-width: 100%;
        }}
        .notation-title {{
            font-size: {config.font_size + 8}px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }}
        .taal-name {{
            font-size: {config.font_size + 4}px;
            text-align: center;
            color: #666;
            margin-bottom: 20px;
        }}
        .line-label {{
            font-size: {config.font_size}px;
            font-weight: bold;
            color: #333;
            margin: 15px 0 5px 0;
            padding: 5px;
            background-color: #e8e8e8;
            border-radius: 4px;
        }}
        .notation-table {{
            border-collapse: collapse;
            width: 100%;
            margin: 0 auto 20px auto;
        }}
        .notation-table td, .notation-table th {{
            border: 1px solid {config.border_color};
            padding: {config.cell_padding + 4}px;
            text-align: center;
            font-size: {config.font_size}px;
            min-width: 60px;
        }}
        .vibhag-start {{
            border-left: {config.vibhag_border_width}px solid {config.border_color} !important;
        }}
        .matra-number {{
            background-color: {config.header_bg_color};
            font-size: {config.font_size - 4}px;
            color: #666;
        }}
        .symbol-row {{
            background-color: {config.header_bg_color};
            font-weight: bold;
            font-size: {config.font_size}px;
        }}
        .symbol-sam {{
            color: {config.sam_color};
            font-weight: bold;
        }}
        .symbol-khali {{
            color: {config.khali_color};
            font-weight: bold;
        }}
        .swar-cell {{
            background-color: {config.cell_bg_color};
            font-size: {config.font_size + 4}px;
            min-height: 50px;
            vertical-align: middle;
            font-weight: bold;
        }}
        .swar-sam {{
            background-color: #ffeaea;
        }}
        .swar-khali {{
            background-color: #eaf4ff;
        }}
        .bol-row {{
            font-size: {config.font_size - 2}px;
            color: #888;
            font-style: italic;
        }}
    </style>
    ''')
    
    # Container
    html_parts.append('<div class="notation-container">')
    
    # Title
    if config.title:
        html_parts.append(f'<div class="notation-title">{config.title}</div>')
    
    # Taal name
    if config.include_taal_name:
        html_parts.append(f'<div class="taal-name">{taal.display_name} ({taal.total_matras} Matras) - {len(grids)} Line(s)</div>')
    
    # Get vibhag start positions for border styling
    vibhag_starts = set(taal.get_vibhag_start_matras())
    
    # Generate table for each line
    for line_idx, grid in enumerate(grids):
        line_num = line_idx + 1
        
        # Line label
        html_parts.append(f'<div class="line-label">Line {line_num}</div>')
        
        # Start table
        html_parts.append('<table class="notation-table">')
        
        # Row 1: Matra numbers
        if config.include_matra_numbers:
            html_parts.append('<tr class="matra-number">')
            for matra in grid.matras:
                vibhag_class = 'vibhag-start' if matra.matra_number in vibhag_starts else ''
                html_parts.append(f'<td class="{vibhag_class}">{matra.matra_number}</td>')
            html_parts.append('</tr>')
        
        # Row 2: Symbols (X for Sam, 0 for Khali, numbers for Tali)
        html_parts.append('<tr class="symbol-row">')
        for matra in grid.matras:
            vibhag_class = 'vibhag-start' if matra.matra_number in vibhag_starts else ''
            symbol_class = ''
            if matra.is_sam:
                symbol_class = 'symbol-sam'
            elif matra.is_khali:
                symbol_class = 'symbol-khali'
            
            symbol = matra.symbol if matra.symbol else '&nbsp;'
            html_parts.append(f'<td class="{vibhag_class} {symbol_class}">{symbol}</td>')
        html_parts.append('</tr>')
        
        # Row 3: Swars
        html_parts.append('<tr>')
        for matra in grid.matras:
            vibhag_class = 'vibhag-start' if matra.matra_number in vibhag_starts else ''
            swar_class = 'swar-cell'
            if matra.is_sam:
                swar_class += ' swar-sam'
            elif matra.is_khali:
                swar_class += ' swar-khali'
            
            display_text = matra.get_display_text() or '&nbsp;'
            html_parts.append(f'<td class="{vibhag_class} {swar_class}">{display_text}</td>')
        html_parts.append('</tr>')
        
        # Optional: Bol row
        if config.include_bol_row and taal.bols:
            html_parts.append('<tr class="bol-row">')
            for i, matra in enumerate(grid.matras):
                vibhag_class = 'vibhag-start' if matra.matra_number in vibhag_starts else ''
                bol = taal.bols[i] if i < len(taal.bols) else ''
                html_parts.append(f'<td class="{vibhag_class}">{bol}</td>')
            html_parts.append('</tr>')
        
        html_parts.append('</table>')
    
    html_parts.append('</div>')
    
    return ''.join(html_parts)


def generate_text_notation_multi(grids: list, include_header: bool = True) -> str:
    """
    Generate a plain text representation for multiple beat grids
    
    Args:
        grids: List of BeatGrid objects
        include_header: Whether to include taal info header
    
    Returns:
        Plain text string
    """
    if not grids:
        return ""
    
    taal = grids[0].taal
    lines = []
    
    if include_header:
        lines.append(f"{'=' * 70}")
        lines.append(f"{taal.display_name}")
        lines.append(f"Total Matras: {taal.total_matras} | Vibhags: {taal.num_vibhags} | Lines: {len(grids)}")
        lines.append(f"{'=' * 70}")
        lines.append("")
    
    # Generate text for each line
    for line_idx, grid in enumerate(grids):
        line_num = line_idx + 1
        lines.append(f"--- Line {line_num} ---")
        
        # Build rows for each vibhag
        matra_row = []
        symbol_row = []
        swar_row = []
        
        for vibhag in grid.vibhags:
            vibhag_matras = []
            vibhag_symbols = []
            vibhag_swars = []
            
            for matra in vibhag.matras:
                vibhag_matras.append(f"{matra.matra_number:^8}")
                
                symbol = matra.symbol if matra.symbol else ' '
                vibhag_symbols.append(f"{symbol:^8}")
                
                swar = matra.get_display_text() or '-'
                # Truncate long swars for text display
                if len(swar) > 7:
                    swar = swar[:6] + '…'
                vibhag_swars.append(f"{swar:^8}")
            
            matra_row.append(' '.join(vibhag_matras))
            symbol_row.append(' '.join(vibhag_symbols))
            swar_row.append(' '.join(vibhag_swars))
        
        lines.append("Matra:  " + ' | '.join(matra_row))
        lines.append("Symbol: " + ' | '.join(symbol_row))
        lines.append("Swar:   " + ' | '.join(swar_row))
        lines.append("")
    
    # Legend
    lines.append("-" * 70)
    lines.append("Legend: X = Sam (first beat), 0 = Khali (empty beat)")
    
    return '\n'.join(lines)
