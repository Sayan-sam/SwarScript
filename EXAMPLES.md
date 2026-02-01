# Example Outputs

This document shows what the generated notation looks like.

## Basic Notes (No Modifiers)
```
Input:  SA RE GA MA PA DHA NI
Output: SA  RE  GA  MA  PA  DHA  NI
```

## Komal Notes (Underlined)
```
Input:  RE_k GA_k DHA_k NI_k
Output: R̲E̲  G̲A̲  D̲H̲A̲  N̲I̲
```

## Tivra MA (Vertical Bar Above)
```
Input:  MA_t
Output: M̍A
```

## Octave Markers

### Higher Octaves (Dots Above)
```
Input:  SA+1 SA+2 SA+3
Output: SȦ  SȦ̇  SȦ̇̇
```

### Lower Octaves (Dots Below)
```
Input:  SA-1 SA-2 SA-3
Output: SẠ  SẠ̣  SẠ̣̣
```

## Common Ragas and Thaats

### Bilawal Thaat (All Natural Notes)
```
Input:  SA RE GA MA PA DHA NI SA+1
Output: SA  RE  GA  MA  PA  DHA  NI  SȦ
```

### Kafi Thaat (Komal GA and NI)
```
Input:  SA RE GA_k MA PA DHA NI_k SA+1
Output: SA  RE  G̲A̲  MA  PA  DHA  N̲I̲  SȦ
```

### Bhairav Thaat (Komal RE and DHA)
```
Input:  SA RE_k GA MA PA DHA_k NI SA+1
Output: SA  R̲E̲  GA  MA  PA  D̲H̲A̲  NI  SȦ
```

### Yaman Raga Pattern (with Tivra MA)
```
Input:  NI-1 RE GA MA_t DHA NI SA+1
Output: NỊ  RE  GA  M̍A  DHA  NI  SȦ
```

### Bhairavi Raga Pattern (Multiple Komal Notes)
```
Input:  SA RE_k GA_k MA PA DHA_k NI_k SA+1
Output: SA  R̲E̲  G̲A̲  MA  PA  D̲H̲A̲  N̲I̲  SȦ
```

## Complex Combinations

### Komal with Octaves
```
Input:  RE_k+1 GA_k-1 DHA_k+2
Output: R̲Ė̲  G̲A̲̣  D̲H̲Ȧ̲̇
```

### Tivra MA with Octaves
```
Input:  MA_t-1 MA_t MA_t+1
Output: M̍Ạ  M̍A  M̍Ȧ
```

### Octave Demonstration
```
Input:  SA-2 SA-1 SA SA+1 SA+2
Output: SẠ̣  SẠ  SA  SȦ  SȦ̇
```

## Full Scale Examples

### Ascending Scale (Aroha)
```
Input:  SA RE GA MA PA DHA NI SA+1
Output: SA  RE  GA  MA  PA  DHA  NI  SȦ
```

### Descending Scale (Avaroha)
```
Input:  SA+1 NI DHA PA MA GA RE SA
Output: SȦ  NI  DHA  PA  MA  GA  RE  SA
```

### Two Octave Range
```
Input:  SA-1 RE-1 GA-1 MA-1 PA-1 DHA-1 NI-1 SA RE GA MA PA DHA NI SA+1
Output: SẠ  RẠE  GẠA  MẠA  PẠA  DẠHA  NỊ  SA  RE  GA  MA  PA  DHA  NI  SȦ
```

## Visual Notation Symbols Legend

- **No symbol** = Default octave, natural note
- **Underline** (̲) = Komal (flat)
- **Vertical bar above** (̍) = Tivra (sharp)
- **Dot above** (̇) = +1 octave higher
- **Two dots above** (̇̇) = +2 octaves higher
- **Dot below** (̣) = -1 octave lower
- **Two dots below** (̣̣) = -2 octaves lower

## Note on Display

The notation uses Unicode combining characters which should display correctly in:
- Modern web browsers
- Most text editors
- Terminal emulators with good Unicode support
- The Streamlit app interface

Some older systems or fonts may not render the combining characters perfectly aligned.
For best results, use the Streamlit web interface.

## How to Run

```bash
# Install dependencies
pip install streamlit

# Run the application
streamlit run app.py

# Or test the engine directly
python test_notation.py
```

## Copying Notation

The generated notation is plain text and can be:
- Copied from the Streamlit output area
- Pasted into documents, emails, websites
- Used in any Unicode-aware application

The notation preserves its visual formatting when copied because it uses
Unicode combining characters, not special formatting or images.
