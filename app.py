"""
Indian Classical Music Notation Generator
Main application entry point - Home Page

This is a multipage Streamlit app with:
- Swar Notation: Generate individual swar symbols with komal, tivra, octaves
- Beat Notation: Create beat-aligned notation using Taal structures
"""

import streamlit as st


# Page configuration
st.set_page_config(
    page_title="Indian Classical Music Notation Generator",
    page_icon="🎵",
    layout="wide"
)


def main():
    """Main application home page"""
    
    st.title("🎵 Indian Classical Music Notation Generator")
    
    st.markdown("""
    Welcome to the Indian Classical Music Notation Generator — a tool for creating 
    correctly formatted visual notation for Hindustani Classical Music.
    
    ---
    
    ## 📌 Features
    
    This application provides two main modes:
    """)
    
    # Feature cards
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 🎵 Swar Notation")
            st.markdown("""
            Generate individual swar (note) symbols with:
            - **7 Base Swaras**: SA, RE, GA, MA, PA, DHA, NI
            - **Komal** (flat): Underline for RE, GA, DHA, NI
            - **Tivra** (sharp): Cap above MA
            - **Octave markers**: Dots above/below for octave shifts
            
            Perfect for quick notation generation and learning.
            """)
            st.page_link("pages/1_🎵_Swar_Notation.py", label="Open Swar Notation →", icon="🎵")
    
    with col2:
        with st.container(border=True):
            st.markdown("### 🥁 Beat Notation")
            st.markdown("""
            Create beat-aligned notation using Taal structures:
            - **Multiple Taals**: TeenTaal, Dadra, JhapTaal, EkTaal, and more
            - **Visual Grid Editor**: Enter swars per matra
            - **Sam & Khali markers**: Proper rhythmic notation
            - **Export**: Download as HTML, SVG, or text
            
            Ideal for compositions and teaching.
            """)
            st.page_link("pages/2_🥁_Beat_Notation.py", label="Open Beat Notation →", icon="🥁")
    
    st.markdown("---")
    
    # Quick reference
    st.markdown("## 📚 Quick Reference")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Swar Input Format")
        st.code("""
SA          → Normal SA
RE_k        → Komal RE (underlined)
MA_t        → Tivra MA (cap above)
PA+1        → PA one octave higher
DHA-1       → DHA one octave lower
GA_k+2      → Komal GA two octaves higher
-           → Continuation/sustain
        """)
    
    with col2:
        st.markdown("### Available Taals")
        st.markdown("""
        | Taal | Matras | Structure |
        |------|--------|-----------|
        | TeenTaal | 16 | 4+4+4+4 |
        | Dadra | 6 | 3+3 |
        | JhapTaal | 10 | 2+3+2+3 |
        | EkTaal | 12 | 2+2+2+2+2+2 |
        | Rupak | 7 | 3+2+2 |
        | Keherwa | 8 | 4+4 |
        """)
    
    st.markdown("---")
    
    # About section
    with st.expander("ℹ️ About This Tool"):
        st.markdown("""
        ### Purpose
        This tool generates **visual text representations** of Indian Classical Music notation.
        It does NOT play audio or analyze music — it purely creates formatted notation symbols
        that can be copied, shared, and printed.
        
        ### Notation Symbols
        - **Komal** (flat): Represented by underline beneath the note
        - **Tivra** (sharp): Represented by a cap (^) above the note (MA only)
        - **Octave up**: Dots above the note (+1, +2, +3)
        - **Octave down**: Dots below the note (-1, -2, -3)
        
        ### Domain Rules
        - SA and PA cannot be komal (they are fixed pitches)
        - Only MA can be tivra
        - MA cannot be komal
        
        ### Technology
        - Built with Python and Streamlit
        - Uses Unicode combining characters for visual formatting
        - No external databases or audio libraries
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
    <p>Built with ❤️ for Indian Classical Music enthusiasts</p>
    <p><small>Use the sidebar to navigate between pages</small></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
