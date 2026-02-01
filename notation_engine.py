"""
Indian Classical Music Notation Engine
Handles note parsing, validation, and symbol generation
"""

from typing import Optional, List, Tuple
from dataclasses import dataclass


# Unicode combining characters for notation
COMBINING_DOT_ABOVE = '\u0307'      # ◌̇
COMBINING_DOT_BELOW = '\u0323'      # ◌̣
COMBINING_UNDERLINE = '\u0332'      # ◌̲
COMBINING_VERTICAL_LINE_ABOVE = '\u030D'  # ◌̍


@dataclass
class Note:
    """
    Represents a single Indian Classical Music note (Swara)
    
    Attributes:
        base: Base note name (SA, RE, GA, MA, PA, DHA, NI)
        komal: Whether the note is komal (flat)
        tivra: Whether the note is tivra (sharp) - only for MA
        octave: Octave offset (-3 to +3, 0 is default)
    """
    base: str
    komal: bool = False
    tivra: bool = False
    octave: int = 0
    
    def __post_init__(self):
        """Validate note after initialization"""
        self.base = self.base.upper()
        errors = self.validate()
        if errors:
            raise ValueError(f"Invalid note: {', '.join(errors)}")
    
    def validate(self) -> List[str]:
        """
        Validate note according to Indian Classical Music rules
        Returns list of error messages (empty if valid)
        """
        errors = []
        
        # Valid base notes
        valid_bases = ['SA', 'RE', 'GA', 'MA', 'PA', 'DHA', 'NI']
        if self.base not in valid_bases:
            errors.append(f"Invalid base note '{self.base}'. Must be one of {valid_bases}")
        
        # Komal rules: only RE, GA, DHA, NI can be komal
        if self.komal and self.base not in ['RE', 'GA', 'DHA', 'NI']:
            errors.append(f"'{self.base}' cannot be komal. Only RE, GA, DHA, NI can be komal")
        
        # Tivra rules: only MA can be tivra
        if self.tivra and self.base != 'MA':
            errors.append(f"'{self.base}' cannot be tivra. Only MA can be tivra")
        
        # MA cannot be both komal and tivra
        if self.komal and self.tivra:
            errors.append("Note cannot be both komal and tivra")
        
        # Octave range validation
        if not -3 <= self.octave <= 3:
            errors.append(f"Octave {self.octave} out of range. Must be between -3 and +3")
        
        return errors
    
    def to_notation(self) -> str:
        """
        Generate the visual notation symbol for this note
        
        Returns:
            String with Unicode combining characters for proper display
        """
        result = self.base
        
        # Step 1: Apply komal (underline beneath all characters)
        if self.komal:
            result = ''.join(char + COMBINING_UNDERLINE for char in result)
        
        # Step 2: Apply tivra (vertical line above) - only for MA
        if self.tivra:
            # Apply to first character only
            result = result[0] + COMBINING_VERTICAL_LINE_ABOVE + result[1:]
        
        # Step 3: Apply octave dots
        if self.octave > 0:
            # Dots above - apply to last character
            dots = COMBINING_DOT_ABOVE * self.octave
            result = result[:-1] + result[-1] + dots
        elif self.octave < 0:
            # Dots below - apply to last character
            dots = COMBINING_DOT_BELOW * abs(self.octave)
            result = result[:-1] + result[-1] + dots
        
        return result


class NotationParser:
    """Parses note sequences and generates notation"""
    
    @staticmethod
    def parse_note_spec(spec: str) -> Tuple[str, bool, bool, int]:
        """
        Parse a note specification string
        
        Format examples:
        - "SA" -> (SA, False, False, 0)
        - "RE_k" -> (RE, True, False, 0)
        - "MA_t" -> (MA, False, True, 0)
        - "PA+1" -> (PA, False, False, 1)
        - "GA_k-1" -> (GA, True, False, -1)
        
        Args:
            spec: Note specification string
        
        Returns:
            Tuple of (base, komal, tivra, octave)
        """
        spec = spec.strip().upper()
        komal = False
        tivra = False
        octave = 0
        
        # Extract komal marker
        if '_K' in spec:
            komal = True
            spec = spec.replace('_K', '')
        
        # Extract tivra marker
        if '_T' in spec:
            tivra = True
            spec = spec.replace('_T', '')
        
        # Extract octave
        if '+' in spec:
            parts = spec.split('+')
            spec = parts[0]
            try:
                octave = int(parts[1])
            except (ValueError, IndexError):
                octave = 1
        elif '-' in spec and spec.count('-') == 1:
            parts = spec.split('-')
            spec = parts[0]
            try:
                octave = -int(parts[1])
            except (ValueError, IndexError):
                octave = -1
        
        return spec, komal, tivra, octave
    
    @staticmethod
    def create_note(base: str, komal: bool = False, tivra: bool = False, octave: int = 0) -> Optional[Note]:
        """
        Create a Note object with validation
        
        Returns:
            Note object or None if invalid
        """
        try:
            return Note(base=base, komal=komal, tivra=tivra, octave=octave)
        except ValueError:
            return None
    
    @staticmethod
    def parse_sequence(sequence: str) -> List[Note]:
        """
        Parse a sequence of notes separated by spaces
        
        Args:
            sequence: String like "SA RE GA MA PA"
        
        Returns:
            List of Note objects
        """
        notes = []
        parts = sequence.strip().split()
        
        for part in parts:
            if not part:
                continue
            
            try:
                base, komal, tivra, octave = NotationParser.parse_note_spec(part)
                note = Note(base=base, komal=komal, tivra=tivra, octave=octave)
                notes.append(note)
            except ValueError as e:
                # Skip invalid notes or handle error
                print(f"Warning: Skipping invalid note '{part}': {e}")
                continue
        
        return notes
    
    @staticmethod
    def generate_notation_sequence(notes: List[Note], separator: str = ' ') -> str:
        """
        Generate notation string for a sequence of notes
        
        Args:
            notes: List of Note objects
            separator: String to place between notes
        
        Returns:
            Formatted notation string
        """
        return separator.join(note.to_notation() for note in notes)


def get_valid_komal_notes() -> List[str]:
    """Return list of notes that can be komal"""
    return ['RE', 'GA', 'DHA', 'NI']


def get_valid_tivra_notes() -> List[str]:
    """Return list of notes that can be tivra"""
    return ['MA']


def can_be_komal(base: str) -> bool:
    """Check if a note can be komal"""
    return base.upper() in get_valid_komal_notes()


def can_be_tivra(base: str) -> bool:
    """Check if a note can be tivra"""
    return base.upper() in get_valid_tivra_notes()
