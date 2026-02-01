"""
Quick Start Guide for Indian Classical Music Notation Generator
"""

# INSTALLATION & RUNNING
# ======================
# 
# 1. Install Streamlit:
#    pip install streamlit
# 
# 2. Run the app:
#    streamlit run app.py
# 
# 3. Open browser at: http://localhost:8501


# HOW UNICODE COMBINING CHARACTERS WORK
# ======================================
#
# The notation system uses Unicode combining characters that modify
# the previous character. These are rendered by combining multiple
# Unicode code points:
#
# Base character + Combining character = Displayed result
# 
# Examples:
# - 'R' + '\u0332' (combining underline) = R̲
# - 'M' + '\u030D' (combining vertical line above) = M̍
# - 'A' + '\u0307' (combining dot above) = Ȧ
# - 'A' + '\u0323' (combining dot below) = Ạ
#
# For multi-character notes like "SA", each character gets the underline:
# - 'S' + '\u0332' + 'A' + '\u0332' = S̲A̲


# NOTATION CONSTRUCTION LOGIC
# ============================
#
# Step 1: Start with base note (e.g., "RE")
# Step 2: If komal, add underline to each character → R̲E̲
# Step 3: If tivra, add vertical bar above first character → M̍A
# Step 4: Add octave dots to last character:
#         - Positive octave: dots above → SȦ (+1), SȦ̇ (+2)
#         - Negative octave: dots below → SẠ (-1), SẠ̣ (-2)
#
# Example: RE komal with +1 octave
# - Start: "RE"
# - Add komal: "R̲E̲" (each char gets underline)
# - Add octave: "R̲Ė̲" (last char gets dot above)


# DOMAIN RULES VALIDATION
# ========================
#
# The Note class enforces these rules in __post_init__:
# 
# 1. Base note must be in: SA, RE, GA, MA, PA, DHA, NI
# 2. Komal only for: RE, GA, DHA, NI
# 3. Tivra only for: MA
# 4. Cannot be both komal and tivra
# 5. Octave range: -3 to +3
#
# Invalid combinations raise ValueError with descriptive message


# SEQUENCE PARSING FORMAT
# ========================
#
# Input format: Space-separated notes with modifiers
# 
# Modifiers:
# - _k  = komal
# - _t  = tivra
# - +N  = N octaves up
# - -N  = N octaves down
#
# Examples:
# "SA"      → SA (normal)
# "RE_k"    → R̲E̲ (komal RE)
# "MA_t"    → M̍A (tivra MA)
# "PA+1"    → PȦ (PA one octave up)
# "DHA-2"   → DẠ̣HA (DHA two octaves down)
# "GA_k+1"  → G̲Ȧ̲ (komal GA one octave up)
#
# Full sequence:
# "SA RE_k GA MA_t PA DHA NI SA+1"
# 
# Parser splits by spaces, extracts modifiers, creates Note objects,
# then generates notation for each and joins with separator


# FILE STRUCTURE
# ==============
#
# notation_engine.py
# ├── Note class
# │   ├── Dataclass with base, komal, tivra, octave
# │   ├── validate() - checks all domain rules
# │   └── to_notation() - generates Unicode string
# │
# ├── NotationParser class
# │   ├── parse_note_spec() - extracts modifiers from string
# │   ├── parse_sequence() - splits and parses multiple notes
# │   └── generate_notation_sequence() - creates output string
# │
# └── Helper functions
#     ├── can_be_komal() - check if note allows komal
#     └── can_be_tivra() - check if note allows tivra
#
# app.py
# ├── Page configuration
# ├── Session state management
# ├── Single note generator UI
# ├── Sequence generator UI
# ├── Reference guide
# ├── Example sequences
# └── Error handling with user-friendly messages


# TESTING
# =======
#
# Run test_notation.py to verify:
# - Basic note generation
# - Komal notes (underlined)
# - Tivra MA (vertical bar)
# - Octave markers (dots)
# - Combinations of modifiers
# - Sequence parsing
# - Validation rules
#
# Command: python test_notation.py


# EXTENDING THE APPLICATION
# ==========================
#
# Future enhancements could include:
#
# 1. Rhythm/Tala notation
#    - Add beat markers
#    - Bar lines
#    - Matra/Sam indicators
#
# 2. Duration markers
#    - Underscores for extended notes
#    - Dashes for connecting notes
#
# 3. Export functionality
#    - Save to text file
#    - Generate PDF with proper fonts
#    - Copy as HTML with CSS
#
# 4. Raga templates
#    - Pre-defined aroha/avaroha for common ragas
#    - Pakad phrases
#
# 5. Visual improvements
#    - Custom fonts optimized for notation
#    - Color coding for different note types
#    - Adjustable font sizes
#
# All extensions should maintain the core principle:
# Pure visual notation without audio functionality
