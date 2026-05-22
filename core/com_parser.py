"""
COM Parser - Analyseur de fichiers .COM MS-DOS
"""

from typing import Dict, List, Any

class COMParser:
    def __init__(self):
        self.PSP_SIZE = 0x100
        self.MAX_SIZE = 0xFF00

    def parse(self, data: bytes) -> Dict[str, Any]:
        if len(data) > self.MAX_SIZE:
            raise ValueError(f"Fichier COM trop grand: {len(data)} bytes (max: {self.MAX_SIZE})")

        memory = bytearray(0x10000)
        memory[self.PSP_SIZE:self.PSP_SIZE + len(data)] = data

        return {
            "format": "COM",
            "file_size": len(data),
            "loaded_size": len(data) + self.PSP_SIZE,
            "entry_point": {
                "segment": 0,
                "offset": self.PSP_SIZE,
                "physical": self.PSP_SIZE,
                "description": "CS:IP = S0:0100h (standard COM)"
            },
            "memory_layout": {
                "psp": {"start": 0x0000, "end": 0x00FF, "size": 0x100},
                "code": {"start": 0x0100, "end": 0x0100 + len(data) - 1, "size": len(data)},
                "free": {"start": 0x0100 + len(data), "end": 0xFFFF}
            },
            "program_image": data,
            "zones": self._detect_zones(data),
            "interrupts": self._detect_interrupts(data),
            "patterns": self._detect_patterns(data)
        }

    def _detect_zones(self, data: bytes) -> List[Dict]:
        zones = []
        current_zone = None

        common_opcodes = {
            0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57,
            0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F,
            0xB8, 0xB9, 0xBA, 0xBB, 0xBC, 0xBD, 0xBE, 0xBF,
            0xCD, 0xE8, 0xE9, 0xEB, 0xC3, 0x90
        }

        for i, byte in enumerate(data):
            is_code = byte in common_opcodes

            if current_zone is None or current_zone["type"] != ("code" if is_code else "data"):
                if current_zone:
                    zones.append(current_zone)
                current_zone = {"type": "code" if is_code else "data", "offset": i, "size": 1}
            else:
                current_zone["size"] += 1

        if current_zone:
            zones.append(current_zone)

        return zones

    def _detect_interrupts(self, data: bytes) -> List[Dict]:
        ints = []
        for i in range(len(data) - 1):
            if data[i] == 0xCD:
                ints.append({
                    "offset": i,
                    "number": data[i + 1],
                    "hex": f"{data[i + 1]:02X}"
                })
        return ints

    def _detect_patterns(self, data: bytes) -> Dict[str, bool]:
        return {
            "has_self_modifying_code": self._check_self_modifying(data),
            "has_stack_manipulation": self._check_stack_ops(data),
            "has_direct_video": self._check_video_access(data)
        }

    def _check_self_modifying(self, data: bytes) -> bool:
        for i in range(len(data) - 2):
            if data[i] in (0xA2, 0xA3):
                addr = struct.unpack('<H', data[i+1:i+3])[0] if i+2 < len(data) else 0
                if 0x100 <= addr < 0x100 + len(data):
                    return True
        return False

    def _check_stack_ops(self, data: bytes) -> bool:
        for i in range(len(data) - 1):
            if data[i:i+2] == bytes([0x8B, 0xEC]):
                return True
        return False

    def _check_video_access(self, data: bytes) -> bool:
        for i in range(len(data) - 1):
            if data[i] == 0xCD and data[i+1] == 0x10:
                return True
            if i+2 < len(data) and data[i:i+3] == bytes([0xB8, 0x00, 0xB8]):
                return True
        return False

import struct
