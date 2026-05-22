"""
Hex Viewer - Visualisation hexadecimale interactive
"""

import pandas as pd
from typing import List, Dict, Tuple

def hex_dump(data: bytes, start: int = 0, length: int = 256, width: int = 16) -> pd.DataFrame:
    """Genere un DataFrame pour l'affichage hex dans Streamlit"""
    rows = []
    end = min(start + length, len(data))

    for i in range(start, end, width):
        hex_bytes = []
        ascii_chars = []

        for j in range(width):
            if i + j < end:
                b = data[i + j]
                hex_bytes.append(f"{b:02X}")
                ascii_chars.append(chr(b) if 32 <= b < 127 else "·")
            else:
                hex_bytes.append("  ")
                ascii_chars.append(" ")

        rows.append({
            "offset": f"{i:08X}",
            "hex": " ".join(hex_bytes),
            "ascii": "".join(ascii_chars),
            "type": classify_bytes(data, i, min(width, end - i))
        })

    return pd.DataFrame(rows)

def classify_bytes(data: bytes, offset: int, length: int) -> str:
    """Classifie les bytes (CODE, DATA, ASCII, ZERO, RELOC)"""
    common_opcodes = {
        0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57,
        0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F,
        0x90, 0xC3, 0xCD, 0xE8, 0xE9, 0xEB
    }

    code_count = sum(1 for j in range(length) if offset + j < len(data) and data[offset + j] in common_opcodes)
    ascii_count = sum(1 for j in range(length) if offset + j < len(data) and 32 <= data[offset + j] < 127)
    zero_count = sum(1 for j in range(length) if offset + j < len(data) and data[offset + j] == 0)

    if code_count > length * 0.4:
        return "CODE"
    elif ascii_count > length * 0.6:
        return "ASCII"
    elif zero_count > length * 0.8:
        return "ZERO"
    else:
        return "DATA"

def hex_dump_bytes(data: bytes, start: int = 0, length: int = 256) -> str:
    """Retourne une string formatee pour affichage texte"""
    lines = []
    end = min(start + length, len(data))

    for i in range(start, end, 16):
        hex_part = []
        ascii_part = []

        for j in range(16):
            if i + j < end:
                b = data[i + j]
                hex_part.append(f"{b:02X}")
                ascii_part.append(chr(b) if 32 <= b < 127 else ".")
            else:
                hex_part.append("  ")
                ascii_part.append(" ")

        lines.append(f"{i:08X}  {' '.join(hex_part)}  |{''.join(ascii_part)}|")

    return "\n".join(lines)
