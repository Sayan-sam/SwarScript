"""
Beat Grid Module
Handles grid generation, swar-to-matra mapping, and beat notation rendering

This module creates and manages the visual grid structure for Taal-based notation,
mapping swars to specific matras and rendering the notation with proper formatting.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict, Any, Union
from taal_definitions import Taal, get_taal
from notation_engine import Note, NotationParser


@dataclass
class MatraCell:
    """
    Represents a single Matra (beat) cell in the notation grid
    
    Attributes:
        matra_number: The matra position (1-indexed)
        vibhag_number: Which vibhag this matra belongs to (1-indexed)
        is_sam: Whether this is the Sam (first beat)
        is_khali: Whether this is a Khali position
        is_tali: Whether this is a Tali position
        symbol: The symbol to display (X, 0, or vibhag number)
        swars: List of swar strings for this matra
        rendered_notation: The rendered notation string with Unicode
    """
    matra_number: int
    vibhag_number: int
    is_sam: bool = False
    is_khali: bool = False
    is_tali: bool = False
    symbol: str = ''
    swars: List[str] = field(default_factory=list)
    rendered_notation: str = ''
    
    def set_swars(self, swar_input: str):
        """
        Set swars for this matra from a space-separated string
        
        Args:
            swar_input: Space-separated swar string (e.g., "SA RE" or "-")
        """
        if swar_input.strip() == '-':
            self.swars = ['-']
        elif swar_input.strip():
            self.swars = swar_input.strip().split()
        else:
            self.swars = []
        
        # Render the notation
        self._render_notation()
    
    def _render_notation(self):
        """Render the swars to notation with Unicode combining characters"""
        if not self.swars:
            self.rendered_notation = ''
            return
        
        rendered_parts = []
        for swar in self.swars:
            if swar == '-':
                # Continuation marker - render as is
                rendered_parts.append('-')
            else:
                # Use the NotationParser to render the swar
                try:
                    notes = NotationParser.parse_sequence(swar)
                    if notes:
                        rendered = NotationParser.generate_notation_sequence(notes, separator=' ')
                        rendered_parts.append(rendered)
                    else:
                        rendered_parts.append(swar)  # Keep original if parsing fails
                except Exception:
                    rendered_parts.append(swar)  # Keep original on error
        
        self.rendered_notation = ' '.join(rendered_parts)
    
    def is_empty(self) -> bool:
        """Check if the matra cell has no swars"""
        return len(self.swars) == 0
    
    def get_display_text(self) -> str:
        """Get the text to display in the cell"""
        return self.rendered_notation if self.rendered_notation else ''


@dataclass
class VibhagGroup:
    """
    Represents a Vibhag (sub-division) containing multiple matras
    
    Attributes:
        vibhag_number: The vibhag position (1-indexed)
        matras: List of MatraCell objects in this vibhag
        start_matra: First matra number in this vibhag
        end_matra: Last matra number in this vibhag
    """
    vibhag_number: int
    matras: List[MatraCell] = field(default_factory=list)
    start_matra: int = 0
    end_matra: int = 0


class BeatGrid:
    """
    Manages the complete beat grid for a Taal cycle (Aavartan)
    
    This class creates and manages the visual grid structure,
    handles swar input and rendering, and provides methods for
    accessing and modifying the grid.
    """
    
    def __init__(self, taal: Taal):
        """
        Initialize a beat grid for a given Taal
        
        Args:
            taal: The Taal object defining the rhythmic structure
        """
        self.taal = taal
        self.matras: List[MatraCell] = []
        self.vibhags: List[VibhagGroup] = []
        self._initialize_grid()
    
    def _initialize_grid(self):
        """Create the initial empty grid structure based on the Taal"""
        self.matras = []
        self.vibhags = []
        
        matra_num = 1
        for vibhag_idx, matra_count in enumerate(self.taal.vibhag_structure):
            vibhag = VibhagGroup(
                vibhag_number=vibhag_idx + 1,
                start_matra=matra_num,
                end_matra=matra_num + matra_count - 1
            )
            
            for _ in range(matra_count):
                cell = MatraCell(
                    matra_number=matra_num,
                    vibhag_number=vibhag_idx + 1,
                    is_sam=self.taal.is_sam(matra_num),
                    is_khali=self.taal.is_khali(matra_num),
                    is_tali=self.taal.is_tali(matra_num),
                    symbol=self.taal.get_matra_symbol(matra_num)
                )
                self.matras.append(cell)
                vibhag.matras.append(cell)
                matra_num += 1
            
            self.vibhags.append(vibhag)
    
    def set_matra_swars(self, matra_number: int, swar_input: str) -> bool:
        """
        Set swars for a specific matra
        
        Args:
            matra_number: The matra position (1-indexed)
            swar_input: Space-separated swar string
        
        Returns:
            True if successful, False if matra number is invalid
        """
        if matra_number < 1 or matra_number > self.taal.total_matras:
            return False
        
        self.matras[matra_number - 1].set_swars(swar_input)
        return True
    
    def get_matra(self, matra_number: int) -> Optional[MatraCell]:
        """Get a specific matra cell"""
        if matra_number < 1 or matra_number > self.taal.total_matras:
            return None
        return self.matras[matra_number - 1]
    
    def clear_grid(self):
        """Clear all swars from the grid"""
        for matra in self.matras:
            matra.swars = []
            matra.rendered_notation = ''
    
    def fill_from_sequence(self, sequence: str) -> Tuple[bool, str]:
        """
        Fill the grid from a sequence of swars
        
        Distributes swars evenly across matras. Each space-separated element
        goes to one matra. Use | (pipe) to explicitly separate vibhags.
        
        Args:
            sequence: Space-separated swar sequence
        
        Returns:
            Tuple of (success, message)
        """
        # Clear existing
        self.clear_grid()
        
        # Parse the sequence
        parts = sequence.strip().split()
        
        if not parts:
            return True, "Grid cleared"
        
        if len(parts) > self.taal.total_matras:
            return False, f"Too many swars ({len(parts)}) for {self.taal.display_name} ({self.taal.total_matras} matras)"
        
        # Fill matras one by one
        for i, swar in enumerate(parts):
            if i < self.taal.total_matras:
                self.matras[i].set_swars(swar)
        
        return True, f"Filled {len(parts)} matras"
    
    def get_all_swars_as_sequence(self) -> str:
        """Get all swars as a space-separated sequence"""
        parts = []
        for matra in self.matras:
            if matra.swars:
                parts.append(' '.join(matra.swars))
            else:
                parts.append('')
        return ' | '.join(
            ' '.join(parts[v.start_matra-1:v.end_matra])
            for v in self.vibhags
        )
    
    def get_rendered_notation(self) -> str:
        """Get the complete rendered notation"""
        parts = []
        for matra in self.matras:
            parts.append(matra.get_display_text() or '-')
        return ' '.join(parts)
    
    def is_complete(self) -> bool:
        """Check if all matras have swars"""
        return all(not matra.is_empty() for matra in self.matras)
    
    def get_filled_count(self) -> int:
        """Get the number of filled matras"""
        return sum(1 for matra in self.matras if not matra.is_empty())
    
    def to_display_data(self) -> Dict[str, Any]:
        """
        Convert grid to a dictionary suitable for display/export
        
        Returns:
            Dictionary with taal info and grid data
        """
        return {
            'taal_name': self.taal.name,
            'taal_display_name': self.taal.display_name,
            'total_matras': self.taal.total_matras,
            'vibhag_structure': self.taal.vibhag_structure,
            'vibhags': [
                {
                    'vibhag_number': v.vibhag_number,
                    'start_matra': v.start_matra,
                    'end_matra': v.end_matra,
                    'matras': [
                        {
                            'matra_number': m.matra_number,
                            'symbol': m.symbol,
                            'is_sam': m.is_sam,
                            'is_khali': m.is_khali,
                            'swars': m.swars,
                            'rendered': m.rendered_notation
                        }
                        for m in v.matras
                    ]
                }
                for v in self.vibhags
            ]
        }


def create_beat_grid(taal_or_name: Union[str, Taal]) -> Optional[BeatGrid]:
    """
    Create a BeatGrid for a given Taal name or Taal object
    
    Args:
        taal_or_name: Name of the Taal (case-insensitive) or Taal object
    
    Returns:
        BeatGrid object or None if Taal not found
    """
    if isinstance(taal_or_name, Taal):
        return BeatGrid(taal_or_name)
    
    taal = get_taal(taal_or_name)
    if taal is None:
        return None
    return BeatGrid(taal)


def distribute_swars_to_matras(swars: List[str], total_matras: int) -> List[List[str]]:
    """
    Distribute a list of swars evenly across matras
    
    This is a utility function for distributing swars when the count
    doesn't match the matra count exactly.
    
    Args:
        swars: List of swar strings
        total_matras: Number of matras to distribute across
    
    Returns:
        List of lists, where each inner list contains swars for one matra
    """
    if not swars:
        return [[] for _ in range(total_matras)]
    
    result = [[] for _ in range(total_matras)]
    
    if len(swars) <= total_matras:
        # Fewer swars than matras - one swar per matra
        for i, swar in enumerate(swars):
            result[i] = [swar]
    else:
        # More swars than matras - distribute evenly
        swars_per_matra = len(swars) / total_matras
        for i in range(total_matras):
            start_idx = int(i * swars_per_matra)
            end_idx = int((i + 1) * swars_per_matra)
            result[i] = swars[start_idx:end_idx]
    
    return result
