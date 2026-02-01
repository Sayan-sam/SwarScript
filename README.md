# Indian Classical Music Notation Generator

A Streamlit web application for generating correctly formatted visual text representations of Indian Classical Music notes (Swaras).

## Features

✅ Generate single notes or sequences of notes  
✅ Supports all 7 base Swaras: SA, RE, GA, MA, PA, DHA, NI  
✅ Komal (flat) notation with underline for RE, GA, DHA, NI  
✅ Tivra (sharp) notation with vertical bar for MA  
✅ Octave markers (-3 to +3) using dots above/below notes  
✅ Input validation following Indian Classical Music rules  
✅ Copy-friendly text output using Unicode combining characters  
✅ Clean, intuitive UI with reference guide and examples  

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

## How to Use

### Single Note Generator
1. Select a base note (SA, RE, GA, MA, PA, DHA, NI)
2. Toggle Komal (flat) if applicable
3. Toggle Tivra (sharp) if applicable (only for MA)
4. Choose octave offset
5. Click "Generate Single Note"

### Sequence Generator
1. Enter notes separated by spaces
2. Use modifiers:
   - `_k` for komal (e.g., `RE_k`)
   - `_t` for tivra (e.g., `MA_t`)
   - `+N` for octave up (e.g., `SA+1`)
   - `-N` for octave down (e.g., `PA-1`)
3. Click "Generate Sequence"

### Example Sequences
```
SA RE GA MA PA DHA NI SA+1          # Basic scale
SA RE GA_k MA PA DHA NI_k SA+1      # Kafi Thaat
SA RE_k GA MA PA DHA_k NI SA+1      # Bhairav Thaat
NI-1 RE GA MA_t DHA NI SA+1         # Yaman pattern
```

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
├── app.py                 # Main Streamlit application
├── notation_engine.py     # Core notation logic and parser
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Technical Details

### Unicode Combining Characters
The notation system uses Unicode combining characters to create visual symbols:
- `\u0332` - Combining underline (for komal)
- `\u030D` - Combining vertical line above (for tivra)
- `\u0307` - Combining dot above (for higher octaves)
- `\u0323` - Combining dot below (for lower octaves)

### Architecture
- **Note class**: Represents a single Swara with validation
- **NotationParser**: Parses note sequences and generates notation strings
- **Streamlit UI**: Interactive web interface with real-time validation

## Future Extensions (Not Implemented)
- Tala/beats notation
- Bar lines and rhythmic grouping
- Export to PDF/text files
- Audio playback (currently out of scope)

## Requirements
- Python 3.7+
- Streamlit 1.28.0+
- No external audio libraries or databases required

## License
This project is for educational and personal use.

## Contributing
Feel free to fork and improve! This is a focused tool for notation generation only.
