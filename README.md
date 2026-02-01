# Indian Classical Music Notation Generator

A Streamlit web application for generating correctly formatted visual text representations of Indian Classical Music notes (Swaras) and beat-aligned compositions.

## Features

### 🎵 Swar Notation
✅ Generate single notes or sequences of notes  
✅ Supports all 7 base Swaras: SA, RE, GA, MA, PA, DHA, NI  
✅ Komal (flat) notation with underline for RE, GA, DHA, NI  
✅ Tivra (sharp) notation with cap for MA  
✅ Octave markers (-3 to +3) using dots above/below notes  
✅ Input validation following Indian Classical Music rules  
✅ Copy-friendly text output using Unicode combining characters  

### 🥁 Beat Notation (NEW!)
✅ Beat-aligned notation using Taal structures  
✅ Multiple Taals: TeenTaal (16), Dadra (6), JhapTaal (10), EkTaal (12), Rupak (7), Keherwa (8)  
✅ Visual grid editor with Sam and Khali markers  
✅ Export to HTML, SVG, and text formats  
✅ Extensible Taal configuration  

## Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## Pages

The app has multiple pages accessible from the sidebar:

1. **Home** - Overview and quick reference
2. **🎵 Swar Notation** - Generate individual swar symbols
3. **🥁 Beat Notation** - Create beat-aligned compositions with Taal structures

## How to Use

### Swar Notation Page

#### Single Note Generator
1. Select a base note (SA, RE, GA, MA, PA, DHA, NI)
2. Toggle Komal (flat) if applicable
3. Toggle Tivra (sharp) if applicable (only for MA)
4. Choose octave offset
5. Click "Generate Single Note"

#### Sequence Generator
1. Enter notes separated by spaces
2. Use modifiers:
   - `_k` for komal (e.g., `RE_k`)
   - `_t` for tivra (e.g., `MA_t`)
   - `+N` for octave up (e.g., `SA+1`)
   - `-N` for octave down (e.g., `PA-1`)
3. Click "Generate Sequence"

### Beat Notation Page

1. **Select a Taal** - Choose from TeenTaal, Dadra, JhapTaal, etc.
2. **Click "Load Taal"** - This creates a grid with the correct number of matras
3. **Enter Swars** - Fill in each matra cell with swars
   - Use `-` for continuation/sustain
   - Use space-separated swars for multiple notes in one matra
4. **Preview** - See the rendered notation
5. **Export** - Download as HTML, SVG, or text

### Example Sequences
```
SA RE GA MA PA DHA NI SA+1          # Basic scale
SA RE GA_k MA PA DHA NI_k SA+1      # Kafi Thaat
SA RE_k GA MA PA DHA_k NI SA+1      # Bhairav Thaat
NI-1 RE GA MA_t DHA NI SA+1         # Yaman pattern
```

## Available Taals

| Taal | Matras | Vibhag Structure | Sam | Khali |
|------|--------|------------------|-----|-------|
| TeenTaal | 16 | 4+4+4+4 | 1 | 9 |
| Dadra | 6 | 3+3 | 1 | 4 |
| JhapTaal | 10 | 2+3+2+3 | 1 | 6 |
| EkTaal | 12 | 2+2+2+2+2+2 | 1 | 3,7,11 |
| Rupak | 7 | 3+2+2 | 1 | 1 |
| Keherwa | 8 | 4+4 | 1 | 5 |

## Domain Rules

### Base Notes (Swaras)
- **SA** (Shadaj) - Cannot be modified
- **RE** (Rishabh) - Can be komal
- **GA** (Gandhar) - Can be komal
- **MA** (Madhyam) - Can be tivra (only note that can be sharp)
- **PA** (Pancham) - Cannot be modified
- **DHA** (Dhaivat) - Can be komal
- **NI** (Nishad) - Can be komal

### Visual Notation
- **Underline beneath note**: Komal (flat) - half semitone lower
- **Vertical bar above note**: Tivra (sharp) - half semitone higher (MA only)
- **Dot above note**: +1 octave (multiple dots for +2, +3)
- **Dot below note**: -1 octave (multiple dots for -2, -3)

### Validation Rules
❌ SA and PA cannot be komal  
❌ Only MA can be tivra  
❌ MA cannot be komal  
❌ Notes cannot be both komal and tivra  
✅ Octave range: -3 to +3  

## Project Structure

```
notation/
├── app.py                 # Main Streamlit application (Home page)
├── pages/
│   ├── 1_🎵_Swar_Notation.py   # Swar notation page
│   └── 2_🥁_Beat_Notation.py   # Beat notation page
├── notation_engine.py     # Core notation logic and parser
├── taal_definitions.py    # Taal configurations (TeenTaal, Dadra, etc.)
├── beat_grid.py           # Grid generation and swar-to-matra mapping
├── export_notation.py     # Export functionality (HTML, SVG, text)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Technical Details

### Unicode Combining Characters
The notation system uses Unicode combining characters to create visual symbols:
- `\u0332` - Combining underline (for komal)
- `\u0302` - Combining circumflex/cap (for tivra)
- `\u0307` - Combining dot above (for higher octaves)
- `\u0323` - Combining dot below (for lower octaves)

### Architecture
- **Note class**: Represents a single Swara with validation
- **NotationParser**: Parses note sequences and generates notation strings
- **Taal class**: Defines rhythmic structures (matras, vibhags, sam, khali)
- **BeatGrid class**: Manages grid-based notation for Taal cycles
- **Export module**: Generates HTML, SVG, and text outputs
- **Streamlit UI**: Interactive multipage web interface

## Adding New Taals

To add a new Taal, edit `taal_definitions.py`:

```python
NEW_TAAL = Taal(
    name="newtaal",
    display_name="New Taal (नया ताल)",
    total_matras=12,
    vibhag_structure=[3, 3, 3, 3],  # Must sum to total_matras
    sam_position=1,
    khali_positions=[7],  # Matra numbers
    tali_positions=[1, 4, 10],  # Matra numbers
)

# Add to TAAL_LIBRARY
TAAL_LIBRARY["newtaal"] = NEW_TAAL
```

## Future Extensions
- ~~Tala/beats notation~~ ✅ Implemented!
- ~~Bar lines and rhythmic grouping~~ ✅ Implemented!
- ~~Export to HTML/SVG/text~~ ✅ Implemented!
- PDF export with custom fonts
- Layakari (Dugun, Tigun, Chaugun)
- Tihai notation
- Audio playback (out of scope for this tool)

## Requirements
- Python 3.7+
- Streamlit 1.28.0+
- No external audio libraries or databases required

## License
This project is for educational and personal use.

## Contributing
Feel free to fork and improve! This is a focused tool for notation generation only.
