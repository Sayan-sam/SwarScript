"""
Taal Definitions Module
Defines Indian Classical Music Taal structures (rhythmic cycles)

A Taal consists of:
- Total Matras (beats)
- Vibhags (sub-divisions)
- Sam position (first/stressed beat)
- Khali positions (empty/unstressed beats)
- Tali positions (clap positions)

This module is designed to be extensible - add new Taals by adding to TAAL_LIBRARY.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Taal:
    """
    Represents a Taal (rhythmic cycle) in Indian Classical Music
    
    Attributes:
        name: Name of the Taal (e.g., "TeenTaal", "Dadra")
        display_name: Human-readable name for UI display
        total_matras: Total number of beats in one cycle (Aavartan)
        vibhag_structure: List of matra counts per vibhag (e.g., [4, 4, 4, 4] for TeenTaal)
        sam_position: Matra number where Sam falls (always 1)
        khali_positions: List of matra numbers where Khali falls
        tali_positions: List of matra numbers where Tali (clap) falls
        bols: Traditional syllables for the Taal (optional)
    """
    name: str
    display_name: str
    total_matras: int
    vibhag_structure: List[int]
    sam_position: int = 1  # Sam is always on beat 1
    khali_positions: List[int] = field(default_factory=list)
    tali_positions: List[int] = field(default_factory=list)
    bols: Optional[List[str]] = None  # Traditional syllables (Dha, Dhin, etc.)
    
    def __post_init__(self):
        """Validate Taal structure after initialization"""
        # Validate that vibhag structure sums to total matras
        if sum(self.vibhag_structure) != self.total_matras:
            raise ValueError(
                f"Vibhag structure {self.vibhag_structure} does not sum to "
                f"total matras {self.total_matras}"
            )
        
        # Validate khali positions are within range
        for pos in self.khali_positions:
            if pos < 1 or pos > self.total_matras:
                raise ValueError(f"Khali position {pos} is out of range (1-{self.total_matras})")
        
        # Validate tali positions are within range
        for pos in self.tali_positions:
            if pos < 1 or pos > self.total_matras:
                raise ValueError(f"Tali position {pos} is out of range (1-{self.total_matras})")
    
    @property
    def num_vibhags(self) -> int:
        """Return the number of vibhags"""
        return len(self.vibhag_structure)
    
    def get_vibhag_for_matra(self, matra: int) -> int:
        """
        Get the vibhag number (1-indexed) for a given matra
        
        Args:
            matra: Matra number (1-indexed)
        
        Returns:
            Vibhag number (1-indexed)
        """
        if matra < 1 or matra > self.total_matras:
            raise ValueError(f"Matra {matra} is out of range (1-{self.total_matras})")
        
        cumulative = 0
        for i, count in enumerate(self.vibhag_structure):
            cumulative += count
            if matra <= cumulative:
                return i + 1
        return len(self.vibhag_structure)
    
    def get_vibhag_start_matras(self) -> List[int]:
        """
        Get the starting matra number for each vibhag
        
        Returns:
            List of matra numbers where each vibhag starts
        """
        starts = [1]
        cumulative = 0
        for count in self.vibhag_structure[:-1]:
            cumulative += count
            starts.append(cumulative + 1)
        return starts
    
    def is_sam(self, matra: int) -> bool:
        """Check if matra is Sam (first beat)"""
        return matra == self.sam_position
    
    def is_khali(self, matra: int) -> bool:
        """Check if matra is Khali (empty beat)"""
        return matra in self.khali_positions
    
    def is_tali(self, matra: int) -> bool:
        """Check if matra is a Tali position"""
        return matra in self.tali_positions
    
    def get_matra_symbol(self, matra: int) -> str:
        """
        Get the symbol to display for a matra position
        
        Returns:
            'X' for Sam, '0' for Khali, vibhag number for Tali, or empty string
        """
        if self.is_sam(matra):
            return 'X'  # Sam is marked with X
        elif self.is_khali(matra):
            return '0'  # Khali is marked with 0
        elif self.is_tali(matra):
            # Return the vibhag number for Tali
            return str(self.get_vibhag_for_matra(matra))
        return ''


# =============================================================================
# TAAL LIBRARY - Add new Taals here
# =============================================================================

TEENTAAL = Taal(
    name="teentaal",
    display_name="TeenTaal (तीनताल)",
    total_matras=16,
    vibhag_structure=[4, 4, 4, 4],
    sam_position=1,
    khali_positions=[9],  # Khali on matra 9 (start of 3rd vibhag)
    tali_positions=[1, 5, 13],  # Tali on 1 (Sam), 5, 13
    bols=["Dha", "Dhin", "Dhin", "Dha",
          "Dha", "Dhin", "Dhin", "Dha",
          "Dha", "Tin", "Tin", "Ta",
          "Ta", "Dhin", "Dhin", "Dha"]
)

DADRA = Taal(
    name="dadra",
    display_name="Dadra (दादरा)",
    total_matras=6,
    vibhag_structure=[3, 3],
    sam_position=1,
    khali_positions=[4],  # Khali on matra 4 (start of 2nd vibhag)
    tali_positions=[1],  # Tali on Sam only
    bols=["Dha", "Dhin", "Na",
          "Dha", "Tin", "Na"]
)

JHAPTAAL = Taal(
    name="jhaptaal",
    display_name="JhapTaal (झपताल)",
    total_matras=10,
    vibhag_structure=[2, 3, 2, 3],
    sam_position=1,
    khali_positions=[6],  # Khali on matra 6 (start of 3rd vibhag)
    tali_positions=[1, 3, 8],  # Tali on 1 (Sam), 3, 8
    bols=["Dhi", "Na",
          "Dhi", "Dhi", "Na",
          "Ti", "Na",
          "Dhi", "Dhi", "Na"]
)

EKTAAL = Taal(
    name="ektaal",
    display_name="EkTaal (एकताल)",
    total_matras=12,
    vibhag_structure=[2, 2, 2, 2, 2, 2],
    sam_position=1,
    khali_positions=[3, 7, 11],  # Multiple Khali positions
    tali_positions=[1, 5, 9],  # Tali positions
    bols=["Dhin", "Dhin",
          "DhaGe", "TiRaKiTa",
          "Tu", "Na",
          "Kat", "Ta",
          "DhaGe", "TiRaKiTa",
          "Dhin", "Na"]
)

RUPAK = Taal(
    name="rupak",
    display_name="Rupak (रूपक)",
    total_matras=7,
    vibhag_structure=[3, 2, 2],
    sam_position=1,
    khali_positions=[1],  # Unique: Sam itself is Khali in Rupak
    tali_positions=[4, 6],  # Tali on 4 and 6
    bols=["Tin", "Tin", "Na",
          "Dhi", "Na",
          "Dhi", "Na"]
)

KEHERWA = Taal(
    name="keherwa",
    display_name="Keherwa (कहरवा)",
    total_matras=8,
    vibhag_structure=[4, 4],
    sam_position=1,
    khali_positions=[5],  # Khali on matra 5
    tali_positions=[1],  # Tali on Sam
    bols=["Dha", "Ge", "Na", "Ti",
          "Na", "Ka", "Dhi", "Na"]
)


# Master dictionary of all available Taals
TAAL_LIBRARY: Dict[str, Taal] = {
    "teentaal": TEENTAAL,
    "dadra": DADRA,
    "jhaptaal": JHAPTAAL,
    "ektaal": EKTAAL,
    "rupak": RUPAK,
    "keherwa": KEHERWA,
}


def get_taal(name: str) -> Optional[Taal]:
    """
    Get a Taal by name
    
    Args:
        name: Taal name (case-insensitive)
    
    Returns:
        Taal object or None if not found
    """
    return TAAL_LIBRARY.get(name.lower())


def get_available_taals() -> List[str]:
    """Get list of available Taal names"""
    return list(TAAL_LIBRARY.keys())


def get_taal_display_names() -> Dict[str, str]:
    """Get dictionary mapping Taal names to display names"""
    return {name: taal.display_name for name, taal in TAAL_LIBRARY.items()}
