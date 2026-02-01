"""
Swar Notation Page (Original App)
Streamlit page for generating individual swar notation symbols
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from notation_engine import (
    Note, NotationParser, 
    can_be_komal, can_be_tivra,
    get_valid_komal_notes, get_valid_tivra_notes
)


# Page configuration
st.set_page_config(
    page_title="Swar Notation - Indian Classical Music",
    page_icon="🎵",
    layout="wide"
)


def initialize_session_state():
    """Initialize session state variables"""
    if 'generated_notation' not in st.session_state:
        st.session_state.generated_notation = ""
    if 'last_sequence' not in st.session_state:
        st.session_state.last_sequence = ""


def render_header():
    """Render the application header"""
    st.title("🎵 Swar Notation Generator")
    st.markdown("""
    Generate correctly formatted visual notation for Indian Classical Music notes (Swaras).
    
    **Notation Rules:**
    - **Komal** (flat): Underline beneath note — applicable to RE, GA, DHA, NI
    - **Tivra** (sharp): Cap above note — applicable only to MA
    - **Octave**: Dots above (+1, +2) or below (-1, -2) the note
    """)
    st.divider()


def render_single_note_generator():
    """Render the single note generator section"""
    st.header("Single Note Generator")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        base_note = st.selectbox(
            "Base Note",
            options=['SA', 'RE', 'GA', 'MA', 'PA', 'DHA', 'NI'],
            key='single_base'
        )
    
    with col2:
        # Enable komal only for valid notes
        komal_enabled = can_be_komal(base_note)
        komal = st.checkbox(
            "Komal (Flat)",
            disabled=not komal_enabled,
            key='single_komal',
            help="Only RE, GA, DHA, NI can be komal" if not komal_enabled else "Add underline beneath note"
        )
    
    with col3:
        # Enable tivra only for MA
        tivra_enabled = can_be_tivra(base_note)
        tivra = st.checkbox(
            "Tivra (Sharp)",
            disabled=not tivra_enabled,
            key='single_tivra',
            help="Only MA can be tivra" if not tivra_enabled else "Add cap above note"
        )
    
    with col4:
        octave = st.selectbox(
            "Octave",
            options=list(range(-3, 4)),
            index=3,  # Default to 0
            key='single_octave',
            help="0 = default, positive = dots above, negative = dots below"
        )
    
    if st.button("Generate Single Note", type="primary", key='gen_single'):
        try:
            note = Note(base=base_note, komal=komal, tivra=tivra, octave=octave)
            notation = note.to_notation()
            st.session_state.generated_notation = notation
            
            # Display with large font
            st.success("Generated Notation:")
            st.markdown(f"### {notation}")
            
            # Provide copyable text
            st.code(notation, language=None)
            
        except ValueError as e:
            st.error(f"❌ Invalid note configuration: {e}")


def render_sequence_generator():
    """Render the sequence generator section"""
    st.header("Note Sequence Generator")
    
    st.markdown("""
    Enter a sequence of notes separated by spaces. Use modifiers:
    - `_k` for komal (e.g., `RE_k`)
    - `_t` for tivra (e.g., `MA_t`)
    - `+N` for octave up (e.g., `SA+1`)
    - `-N` for octave down (e.g., `PA-1`)
    
    **Example:** `SA RE_k GA MA_t PA+1 DHA NI SA+1`
    """)
    
    # Text input for sequence
    sequence_input = st.text_area(
        "Note Sequence",
        value="SA RE GA MA PA DHA NI SA+1",
        height=100,
        key='sequence_input',
        help="Enter notes separated by spaces"
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        generate_btn = st.button("Generate Sequence", type="primary", key='gen_sequence')
    
    with col2:
        separator = st.text_input(
            "Separator between notes",
            value="  ",
            key='separator',
            help="Characters to place between notes (default: double space)"
        )
    
    if generate_btn:
        if not sequence_input.strip():
            st.warning("⚠️ Please enter a note sequence")
        else:
            try:
                # Parse the sequence
                notes = NotationParser.parse_sequence(sequence_input)
                
                if not notes:
                    st.error("❌ No valid notes found in sequence")
                else:
                    # Generate notation
                    notation = NotationParser.generate_notation_sequence(notes, separator=separator)
                    st.session_state.generated_notation = notation
                    st.session_state.last_sequence = sequence_input
                    
                    # Display results
                    st.success(f"✅ Generated {len(notes)} notes:")
                    
                    # Large display
                    st.markdown(f"### {notation}")
                    
                    # Copyable output
                    st.text_area(
                        "Copy notation from here:",
                        value=notation,
                        height=100,
                        key='output_area'
                    )
                    
                    # Show parsed notes for reference
                    with st.expander("View parsed notes details"):
                        for i, note in enumerate(notes, 1):
                            details = f"{i}. **{note.base}**"
                            if note.komal:
                                details += " (Komal)"
                            if note.tivra:
                                details += " (Tivra)"
                            if note.octave != 0:
                                details += f" [Octave: {note.octave:+d}]"
                            details += f" → {note.to_notation()}"
                            st.markdown(details)
            
            except Exception as e:
                st.error(f"❌ Error generating notation: {e}")


def render_reference_guide():
    """Render the reference guide section"""
    with st.expander("📚 Notation Reference Guide"):
        st.markdown("""
        ### Base Notes (Swaras)
        | Note | Name | Can be Komal? | Can be Tivra? |
        |------|------|---------------|---------------|
        | SA   | Shadaj | ❌ | ❌ |
        | RE   | Rishabh | ✅ | ❌ |
        | GA   | Gandhar | ✅ | ❌ |
        | MA   | Madhyam | ❌ | ✅ |
        | PA   | Pancham | ❌ | ❌ |
        | DHA  | Dhaivat | ✅ | ❌ |
        | NI   | Nishad | ✅ | ❌ |
        
        ### Visual Symbols
        - **Underline** (beneath text): Komal (flat) — half semitone lower
        - **Cap** (above text): Tivra (sharp) — half semitone higher
        - **Dot above** (top-right): Octave up
        - **Dot below** (bottom-right): Octave down
        - **Multiple dots**: Multiple octaves
        
        ### Sequence Input Format
        ```
        SA          → Normal SA
        RE_k        → Komal RE (underlined)
        MA_t        → Tivra MA (cap above)
        PA+1        → PA one octave higher (dot above)
        DHA-1       → DHA one octave lower (dot below)
        GA_k+2      → Komal GA two octaves higher
        ```
        """)


def render_examples():
    """Render example sequences"""
    with st.expander("🎼 Example Sequences"):
        examples = {
            "Basic Scale (Aroha)": "SA RE GA MA PA DHA NI SA+1",
            "Bilawal Thaat": "SA RE GA MA PA DHA NI SA+1",
            "Kafi Thaat": "SA RE GA_k MA PA DHA NI_k SA+1",
            "Bhairav Thaat": "SA RE_k GA MA PA DHA_k NI SA+1",
            "Yaman Raga Pattern": "NI-1 RE GA MA_t DHA NI SA+1",
            "Octave Demonstration": "SA-1 SA SA+1 SA+2"
        }
        
        for name, sequence in examples.items():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f"**{name}**")
            with col2:
                if st.button(f"Load", key=f"load_{name}"):
                    st.session_state.sequence_input = sequence
                    st.rerun()


def render_footer():
    """Render the application footer"""
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
    <p>Built with ❤️ for Indian Classical Music enthusiasts</p>
    <p><small>This tool generates visual notation only. No audio playback or analysis features.</small></p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application entry point"""
    initialize_session_state()
    render_header()
    
    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["📝 Sequence Generator", "🎯 Single Note"])
    
    with tab1:
        render_sequence_generator()
        render_examples()
    
    with tab2:
        render_single_note_generator()
    
    # Reference guide available on all tabs
    render_reference_guide()
    render_footer()


if __name__ == "__main__":
    main()
