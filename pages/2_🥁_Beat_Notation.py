"""
Beat Notation Page
Streamlit page for beat-based notation using Taal structures

This page provides a grid-based editor for entering swars aligned to
specific matras within a Taal cycle (Aavartan). Supports multiple Aavartans (lines).
"""

import streamlit as st
import streamlit.components.v1 as components
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from taal_definitions import get_taal, get_available_taals, get_taal_display_names, TAAL_LIBRARY
from beat_grid import BeatGrid, create_beat_grid
from export_notation import (
    generate_html_table_multi, 
    generate_svg, 
    generate_text_notation_multi,
    ExportConfig
)
import base64


# Page configuration
st.set_page_config(
    page_title="Beat Notation - Indian Classical Music",
    page_icon="🥁",
    layout="wide"
)


def initialize_session_state():
    """Initialize session state variables for beat notation"""
    if 'beat_grids' not in st.session_state:
        st.session_state.beat_grids = []  # List of BeatGrid objects (one per Aavartan)
    if 'selected_taal' not in st.session_state:
        st.session_state.selected_taal = None
    if 'matra_inputs' not in st.session_state:
        st.session_state.matra_inputs = {}  # Key: (line_num, matra_num), Value: swar input
    if 'composition_title' not in st.session_state:
        st.session_state.composition_title = "My Composition"
    if 'num_lines' not in st.session_state:
        st.session_state.num_lines = 1


def render_header():
    """Render the page header"""
    st.title("🥁 Beat Notation Editor")
    st.markdown("""
    Create beat-aligned notation using traditional Indian Classical Music Taal structures.
    
    **How to use:**
    1. Select a Taal (rhythmic cycle)
    2. Enter swars in each matra cell
    3. Use `-` for continuation/sustain
    4. Add more lines (Aavartans) as needed
    5. Export your notation when complete
    """)
    st.divider()


def render_taal_selector():
    """Render the Taal selection interface"""
    st.subheader("Step 1: Select Taal")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        taal_names = get_taal_display_names()
        selected_name = st.selectbox(
            "Choose a Taal",
            options=list(taal_names.keys()),
            format_func=lambda x: taal_names[x],
            key='taal_selector'
        )
        
        if st.button("Load Taal", type="primary"):
            st.session_state.selected_taal = selected_name
            # Initialize with one Aavartan (line)
            st.session_state.beat_grids = [create_beat_grid(selected_name)]
            st.session_state.num_lines = 1
            st.session_state.matra_inputs = {}
            st.rerun()
    
    with col2:
        # Show Taal info
        if selected_name:
            taal = get_taal(selected_name)
            if taal:
                st.markdown(f"""
                **{taal.display_name}**
                - Total Matras: **{taal.total_matras}**
                - Vibhags: **{taal.num_vibhags}** ({' + '.join(map(str, taal.vibhag_structure))})
                - Sam: Matra **{taal.sam_position}** (marked with X)
                - Khali: Matra(s) **{', '.join(map(str, taal.khali_positions))}** (marked with 0)
                """)


def render_taal_info_card(taal):
    """Render an info card for the current Taal"""
    with st.expander("ℹ️ Taal Information", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Matras", taal.total_matras)
        with col2:
            st.metric("Vibhags", taal.num_vibhags)
        with col3:
            st.metric("Structure", ' + '.join(map(str, taal.vibhag_structure)))
        
        st.markdown("**Legend:**")
        st.markdown("- **X** = Sam (first beat, emphasized)")
        st.markdown("- **0** = Khali (empty beat)")
        st.markdown("- **2, 3, 4...** = Tali (clap) positions")
        
        if taal.bols:
            st.markdown("**Traditional Bols:**")
            st.code(' '.join(taal.bols))


def render_grid_editor(grids: list):
    """Render the main grid editor interface with multiple Aavartans"""
    st.subheader("Step 2: Enter Swars")
    
    taal = grids[0].taal
    
    # Composition title
    st.session_state.composition_title = st.text_input(
        "Composition Title",
        value=st.session_state.composition_title,
        key='title_input'
    )
    
    st.markdown("---")
    
    # Line management controls
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    
    with col1:
        st.metric("Total Lines (Aavartans)", len(grids))
    
    with col2:
        if st.button("➕ Add Line", type="primary"):
            new_grid = create_beat_grid(st.session_state.selected_taal)
            st.session_state.beat_grids.append(new_grid)
            st.session_state.num_lines = len(st.session_state.beat_grids)
            st.rerun()
    
    with col3:
        if len(grids) > 1:
            if st.button("➖ Remove Last Line", type="secondary"):
                st.session_state.beat_grids.pop()
                st.session_state.num_lines = len(st.session_state.beat_grids)
                # Clean up matra inputs for removed line
                removed_line = len(st.session_state.beat_grids) + 1
                keys_to_remove = [k for k in st.session_state.matra_inputs.keys() if k[0] == removed_line]
                for k in keys_to_remove:
                    del st.session_state.matra_inputs[k]
                st.rerun()
    
    with col4:
        if st.button("🗑️ Clear All", type="secondary"):
            for grid in grids:
                grid.clear_grid()
            st.session_state.matra_inputs = {}
            st.rerun()
    
    st.markdown("---")
    
    # Quick fill option
    with st.expander("⚡ Quick Fill (Enter sequence for current lines)"):
        quick_sequence = st.text_area(
            "Enter space-separated swars",
            placeholder="SA RE GA MA PA DHA NI SA+1 | SA RE GA MA PA DHA NI SA+1",
            help="Enter swars separated by spaces. Use | to separate lines. Use _k for komal, _t for tivra, +/-N for octave. Use - for continuation.",
            key='quick_fill_input'
        )
        
        if st.button("Fill Grids", key='quick_fill_btn'):
            if quick_sequence:
                # Split by | for different lines
                line_sequences = quick_sequence.split('|')
                
                # Add more grids if needed
                while len(st.session_state.beat_grids) < len(line_sequences):
                    new_grid = create_beat_grid(st.session_state.selected_taal)
                    st.session_state.beat_grids.append(new_grid)
                
                # Fill each grid
                for line_idx, seq in enumerate(line_sequences):
                    if line_idx < len(st.session_state.beat_grids):
                        success, message = st.session_state.beat_grids[line_idx].fill_from_sequence(seq.strip())
                        if success:
                            # Update session state inputs
                            for matra in st.session_state.beat_grids[line_idx].matras:
                                key = (line_idx + 1, matra.matra_number)
                                st.session_state.matra_inputs[key] = ' '.join(matra.swars) if matra.swars else ''
                
                st.session_state.num_lines = len(st.session_state.beat_grids)
                st.rerun()
    
    st.markdown("---")
    
    # Render each line (Aavartan)
    for line_idx, grid in enumerate(grids):
        line_num = line_idx + 1
        
        # Line header
        st.markdown(f"### 📝 Line {line_num} (Aavartan {line_num})")
        
        # Render grid by vibhags for this line
        for vibhag in grid.vibhags:
            vibhag_label = f"Vibhag {vibhag.vibhag_number}"
            
            # Check if this vibhag contains Sam or Khali
            contains_sam = any(m.is_sam for m in vibhag.matras)
            contains_khali = any(m.is_khali for m in vibhag.matras)
            
            if contains_sam:
                vibhag_label += " 🔴"
            if contains_khali:
                vibhag_label += " 🔵"
            
            st.markdown(f"**{vibhag_label}**")
            
            # Create columns for matras in this vibhag
            cols = st.columns(len(vibhag.matras))
            
            for i, matra in enumerate(vibhag.matras):
                with cols[i]:
                    # Matra header with symbol
                    symbol_display = matra.symbol if matra.symbol else "·"
                    
                    # Color coding with larger font
                    if matra.is_sam:
                        st.markdown(f"<div style='text-align:center; color:#e74c3c; font-weight:bold; font-size:18px;'>{symbol_display}</div>", unsafe_allow_html=True)
                    elif matra.is_khali:
                        st.markdown(f"<div style='text-align:center; color:#3498db; font-weight:bold; font-size:18px;'>{symbol_display}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='text-align:center; color:#666; font-size:16px;'>{symbol_display}</div>", unsafe_allow_html=True)
                    
                    # Input field for swar - use (line_num, matra_num) as key
                    input_key = (line_num, matra.matra_number)
                    current_value = st.session_state.matra_inputs.get(input_key, '')
                    new_value = st.text_input(
                        f"L{line_num}M{matra.matra_number}",
                        value=current_value,
                        key=f'matra_{line_num}_{matra.matra_number}',
                        label_visibility='collapsed',
                        placeholder=f"{matra.matra_number}"
                    )
                    
                    # Update grid if value changed
                    if new_value != current_value:
                        st.session_state.matra_inputs[input_key] = new_value
                        grid.set_matra_swars(matra.matra_number, new_value)
            
            st.markdown("")  # Spacing between vibhags
        
        # Update all matras from inputs for this line
        for matra_num in range(1, taal.total_matras + 1):
            input_key = (line_num, matra_num)
            if input_key in st.session_state.matra_inputs:
                grid.set_matra_swars(matra_num, st.session_state.matra_inputs[input_key])
        
        # Line status
        filled = grid.get_filled_count()
        total = taal.total_matras
        if grid.is_complete():
            st.success(f"✅ Line {line_num} complete ({filled}/{total} matras)")
        else:
            st.info(f"⏳ Line {line_num}: {filled}/{total} matras filled")
        
        st.markdown("---")


def render_preview(grids: list):
    """Render the notation preview for multiple lines"""
    st.subheader("Step 3: Preview & Export")
    
    # Generate HTML preview
    config = ExportConfig(
        title=st.session_state.composition_title,
        include_taal_name=True,
        include_matra_numbers=True,
        font_size=24  # Increased font size
    )
    
    html_content = generate_html_table_multi(grids, config)
    
    # Display preview
    st.markdown("### Preview")
    # Calculate height based on number of lines
    preview_height = 150 + (len(grids) * 120)
    components.html(html_content, height=preview_height, scrolling=True)
    
    # Text preview
    with st.expander("📝 Text Notation"):
        text_notation = generate_text_notation_multi(grids)
        st.code(text_notation)
    
    # Rendered notation string - large font
    st.markdown("### Rendered Notation")
    
    for line_idx, grid in enumerate(grids):
        rendered = grid.get_rendered_notation()
        st.markdown(f"**Line {line_idx + 1}:**")
        st.markdown(f"<div style='font-size: 28px; font-weight: bold; padding: 10px; background-color: #f0f0f0; border-radius: 5px; margin-bottom: 10px;'>{rendered}</div>", unsafe_allow_html=True)
    
    # Copy-friendly output - all lines combined
    all_rendered = '\n'.join([f"Line {i+1}: {grid.get_rendered_notation()}" for i, grid in enumerate(grids)])
    st.text_area(
        "Copy notation:",
        value=all_rendered,
        height=100 + (len(grids) * 30),
        key='copy_notation'
    )


def render_export_options(grids: list):
    """Render export options for multiple lines"""
    st.markdown("### Export Options")
    
    config = ExportConfig(
        title=st.session_state.composition_title,
        include_taal_name=True,
        include_matra_numbers=True,
        font_size=24  # Increased font size
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # HTML Export
        html_content = generate_html_table_multi(grids, config)
        full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{st.session_state.composition_title}</title>
</head>
<body>
{html_content}
</body>
</html>'''
        
        st.download_button(
            label="📄 Download HTML",
            data=full_html,
            file_name="notation.html",
            mime="text/html"
        )
    
    with col2:
        # SVG Export (first grid only for now)
        svg_content = generate_svg(grids[0], config)
        st.download_button(
            label="🖼️ Download SVG",
            data=svg_content,
            file_name="notation.svg",
            mime="image/svg+xml"
        )
    
    with col3:
        # Text Export
        text_content = generate_text_notation_multi(grids)
        st.download_button(
            label="📝 Download Text",
            data=text_content,
            file_name="notation.txt",
            mime="text/plain"
        )


def render_swar_reference():
    """Render swar input reference guide"""
    with st.expander("📖 Swar Input Reference"):
        st.markdown("""
        ### How to Enter Swars
        
        | Input | Meaning | Example |
        |-------|---------|---------|
        | `SA`, `RE`, etc. | Basic swar | SA |
        | `_k` suffix | Komal (flat) | RE_k, GA_k |
        | `_t` suffix | Tivra (sharp) | MA_t |
        | `+N` suffix | Higher octave | SA+1, PA+2 |
        | `-N` suffix | Lower octave | SA-1, NI-1 |
        | `-` | Continuation | - |
        | Multiple swars | Space-separated | SA RE |
        
        ### Examples
        - `SA` → Normal SA
        - `RE_k` → Komal RE (underlined)
        - `MA_t` → Tivra MA (with cap)
        - `SA+1` → SA one octave higher
        - `GA_k-1` → Komal GA one octave lower
        - `SA RE` → Two swars in one matra
        - `-` → Sustain previous note
        """)


def render_footer():
    """Render page footer"""
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 10px;'>
    <small>Beat Notation Editor | Part of Indian Classical Music Notation Generator</small>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main function for beat notation page"""
    initialize_session_state()
    render_header()
    
    # Sidebar for quick access
    with st.sidebar:
        st.header("🎵 Beat Notation")
        st.markdown("---")
        
        if st.session_state.beat_grids:
            taal = st.session_state.beat_grids[0].taal
            st.markdown(f"**Current Taal:** {taal.display_name}")
            st.markdown(f"**Matras per line:** {taal.total_matras}")
            st.markdown(f"**Total Lines:** {len(st.session_state.beat_grids)}")
            
            if st.button("🔄 Change Taal"):
                st.session_state.beat_grids = []
                st.session_state.selected_taal = None
                st.session_state.matra_inputs = {}
                st.session_state.num_lines = 1
                st.rerun()
        
        st.markdown("---")
        render_swar_reference()
    
    # Main content
    if not st.session_state.beat_grids:
        # Show Taal selector
        render_taal_selector()
        
        # Show available Taals
        st.markdown("---")
        st.markdown("### Available Taals")
        
        cols = st.columns(3)
        for i, (name, taal) in enumerate(TAAL_LIBRARY.items()):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"**{taal.display_name}**")
                    st.markdown(f"Matras: {taal.total_matras}")
                    st.markdown(f"Structure: {' + '.join(map(str, taal.vibhag_structure))}")
    else:
        # Show grid editor with all lines
        grids = st.session_state.beat_grids
        render_taal_info_card(grids[0].taal)
        render_grid_editor(grids)
        
        render_preview(grids)
        render_export_options(grids)
    
    render_footer()


if __name__ == "__main__":
    main()
