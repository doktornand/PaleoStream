"""
MZ Parser - Analyseur de fichiers executables MS-DOS (.EXE)
Portage Python du module Node.js original
"""

import struct
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass

@dataclass
class MZHeader:
    magic: str
    last_page_bytes: int
    pages_in_file: int
    relocation_count: int
    header_paragraphs: int
    min_alloc: int
    max_alloc: int
    initial_ss: int
    initial_sp: int
    checksum: int
    initial_ip: int
    initial_cs: int
    relocation_offset: int
    overlay_number: int

    @property
    def header_size(self) -> int:
        return self.header_paragraphs * 16

    @property
    def program_size(self) -> int:
        size = self.pages_in_file * 512
        if self.last_page_bytes:
            size -= (512 - self.last_page_bytes)
        return max(0, size - self.header_size)

@dataclass
class RelocationEntry:
    offset: int
    segment: int
    file_address: int
    index: int

class MZParser:
    def __init__(self):
        self.header: Optional[MZHeader] = None
        self.relocation_table: List[RelocationEntry] = []
        self.program_image: Optional[bytes] = None
        self.is_extended: bool = False
        self.extended_header: Optional[Dict] = None

    def parse(self, data: bytes) -> Dict[str, Any]:
        if len(data) < 28:
            raise ValueError(f"Fichier trop petit: {len(data)} bytes (minimum 28)")

        # Phase 1: Parse header
        self.header = self._parse_header(data)

        # Phase 2: Detection format etendu
        self.is_extended = self._detect_extended_format(data)

        # Phase 3: Parse relocation table
        self.relocation_table = self._parse_relocation_table(data)

        # Phase 4: Extract program image
        self.program_image = self._extract_program_image(data)

        # Phase 5: Analyze segments
        segments = self._analyze_segments()

        # Phase 6: Detect code/data zones
        zones = self._detect_zones()

        return {
            "header": {
                "magic": self.header.magic,
                "last_page_bytes": self.header.last_page_bytes,
                "pages_in_file": self.header.pages_in_file,
                "relocation_count": self.header.relocation_count,
                "header_paragraphs": self.header.header_paragraphs,
                "min_alloc": self.header.min_alloc,
                "max_alloc": self.header.max_alloc,
                "initial_ss": self.header.initial_ss,
                "initial_sp": self.header.initial_sp,
                "checksum": self.header.checksum,
                "initial_ip": self.header.initial_ip,
                "initial_cs": self.header.initial_cs,
                "relocation_offset": self.header.relocation_offset,
                "overlay_number": self.header.overlay_number,
                "calculated_program_size": self.header.program_size,
                "header_size": self.header.header_size
            },
            "is_extended": self.is_extended,
            "extended_header": self.extended_header,
            "relocation_table": [
                {
                    "index": r.index,
                    "offset": r.offset,
                    "segment": r.segment,
                    "file_address": r.file_address
                }
                for r in self.relocation_table
            ],
            "program_image": {
                "offset": self.header.header_size,
                "size": len(self.program_image) if self.program_image else 0,
                "checksum": self._calculate_checksum()
            },
            "entry_point": {
                "ip": self.header.initial_ip,
                "cs": self.header.initial_cs,
                "description": f"CS:IP = {self.header.initial_cs:04X}:{self.header.initial_ip:04X}",
                "file_offset": self.header.initial_cs * 16 + self.header.initial_ip
            },
            "stack": {
                "sp": self.header.initial_sp,
                "ss": self.header.initial_ss,
                "description": f"SS:SP = {self.header.initial_ss:04X}:{self.header.initial_sp:04X}"
            },
            "segments": segments,
            "zones": zones,
            "metadata": {
                "file_size": len(data),
                "has_relocations": len(self.relocation_table) > 0,
                "is_overlay": self.header.overlay_number != 0,
                "min_memory": self.header.min_alloc * 16,
                "max_memory": self.header.max_alloc * 16
            }
        }

    def _parse_header(self, data: bytes) -> MZHeader:
        magic = data[0:2].decode('ascii', errors='replace')
        if magic not in ('MZ', 'ZM'):
            raise ValueError(f"Signature MZ invalide: '{magic}'")

        return MZHeader(
            magic=magic,
            last_page_bytes=struct.unpack('<H', data[2:4])[0],
            pages_in_file=struct.unpack('<H', data[4:6])[0],
            relocation_count=struct.unpack('<H', data[6:8])[0],
            header_paragraphs=struct.unpack('<H', data[8:10])[0],
            min_alloc=struct.unpack('<H', data[10:12])[0],
            max_alloc=struct.unpack('<H', data[12:14])[0],
            initial_ss=struct.unpack('<h', data[14:16])[0],
            initial_sp=struct.unpack('<H', data[16:18])[0],
            checksum=struct.unpack('<H', data[18:20])[0],
            initial_ip=struct.unpack('<H', data[20:22])[0],
            initial_cs=struct.unpack('<h', data[22:24])[0],
            relocation_offset=struct.unpack('<H', data[24:26])[0],
            overlay_number=struct.unpack('<H', data[26:28])[0]
        )

    def _detect_extended_format(self, data: bytes) -> bool:
        if len(data) < 64:
            return False

        pe_offset = struct.unpack('<I', data[60:64])[0]
        if pe_offset >= len(data) - 2:
            return False

        ext_magic = data[pe_offset:pe_offset+2].decode('ascii', errors='replace')
        self.extended_header = {
            "pe_offset": pe_offset,
            "type": ext_magic,
            "is_valid": ext_magic in ('PE', 'NE', 'LE', 'LX')
        }

        return self.extended_header["is_valid"]

    def _parse_relocation_table(self, data: bytes) -> List[RelocationEntry]:
        entries = []
        count = self.header.relocation_count
        offset = self.header.relocation_offset

        if count == 0 or offset == 0:
            return entries

        table_end = offset + count * 4
        if table_end > len(data):
            return entries

        for i in range(count):
            entry_offset = offset + i * 4
            reloc_offset = struct.unpack('<H', data[entry_offset:entry_offset+2])[0]
            reloc_segment = struct.unpack('<H', data[entry_offset+2:entry_offset+4])[0]
            file_addr = reloc_segment * 16 + reloc_offset

            entries.append(RelocationEntry(
                offset=reloc_offset,
                segment=reloc_segment,
                file_address=file_addr,
                index=i
            ))

        return entries

    def _extract_program_image(self, data: bytes) -> bytes:
        header_size = self.header.header_size
        image_size = self.header.program_size
        actual_size = min(image_size, len(data) - header_size)
        return data[header_size:header_size + actual_size]

    def _analyze_segments(self) -> List[Dict]:
        segments = []

        if self.header.initial_cs != 0 or self.header.initial_ip != 0:
            segments.append({
                "name": "CS",
                "type": "code",
                "relative_base": self.header.initial_cs,
                "entry_point": self.header.initial_ip,
                "purpose": "Segment de code (point d'entree)"
            })

        if self.header.initial_ss != 0 or self.header.initial_sp != 0:
            segments.append({
                "name": "SS",
                "type": "stack",
                "relative_base": self.header.initial_ss,
                "stack_top": self.header.initial_sp,
                "purpose": "Segment de pile"
            })

        reloc_segments = set(r.segment for r in self.relocation_table)
        for seg in reloc_segments:
            if not any(s["relative_base"] == seg for s in segments):
                count = sum(1 for r in self.relocation_table if r.segment == seg)
                segments.append({
                    "name": f"SEG_{seg:04X}",
                    "type": "data",
                    "relative_base": seg,
                    "relocation_count": count,
                    "purpose": "Segment de donnees (identifie par relocations)"
                })

        return segments

    def _detect_zones(self) -> List[Dict]:
        zones = []
        if not self.program_image:
            return zones

        image = self.program_image
        min_zone_size = 16
        current_zone = None

        common_opcodes = {
            0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57,
            0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F,
            0xB0, 0xB1, 0xB2, 0xB3, 0xB4, 0xB5, 0xB6, 0xB7,
            0xB8, 0xB9, 0xBA, 0xBB, 0xBC, 0xBD, 0xBE, 0xBF,
            0x90, 0xC3, 0xCD, 0xE8, 0xE9, 0xEB
        }

        for i in range(len(image)):
            byte = image[i]
            is_code = byte in common_opcodes

            if current_zone is None or current_zone["type"] != ("code" if is_code else "data"):
                if current_zone and current_zone["size"] >= min_zone_size:
                    zones.append(current_zone)
                current_zone = {
                    "type": "code" if is_code else "data",
                    "offset": i,
                    "size": 1,
                    "confidence": 0.6 if is_code else 0.4
                }
            else:
                current_zone["size"] += 1

        if current_zone and current_zone["size"] >= min_zone_size:
            zones.append(current_zone)

        # Refine with relocations
        for reloc in self.relocation_table:
            for zone in zones:
                if reloc.file_address >= zone["offset"] and reloc.file_address < zone["offset"] + zone["size"]:
                    zone["has_relocations"] = True
                    zone["relocation_count"] = zone.get("relocation_count", 0) + 1
                    if zone["type"] == "code" and zone.get("relocation_count", 0) > 2:
                        zone["type"] = "data"
                        zone["confidence"] = 0.7

        return zones

    def _calculate_checksum(self) -> int:
        if not self.program_image:
            return 0

        total = 0
        for i in range(0, len(self.program_image), 2):
            if i + 1 < len(self.program_image):
                total += struct.unpack('<H', self.program_image[i:i+2])[0]
            else:
                total += self.program_image[i]
            total &= 0xFFFF

        return (~total) & 0xFFFF

    def generate_migration_report(self) -> Dict:
        complexity = self._assess_complexity()

        return {
            "file_type": "MS-DOS MZ Executable",
            "complexity": complexity,
            "recommendations": self._generate_recommendations(),
            "conversion_difficulty": self._calculate_difficulty(complexity),
            "estimated_manual_work": self._estimate_manual_work(complexity)
        }

    def _assess_complexity(self) -> Dict:
        score = 0

        if self.header.calculated_program_size < 1024:
            score += 1
        elif self.header.calculated_program_size < 32768:
            score += 2
        else:
            score += 3

        if len(self.relocation_table) > 100:
            score += 2
        elif len(self.relocation_table) > 10:
            score += 1

        if self.header.overlay_number != 0:
            score += 2

        if self.is_extended:
            score += 1

        return {
            "score": score,
            "level": "LOW" if score <= 2 else "MEDIUM" if score <= 5 else "HIGH",
            "factors": {
                "program_size": self.header.calculated_program_size,
                "relocation_count": len(self.relocation_table),
                "has_overlays": self.header.overlay_number != 0,
                "is_extended": self.is_extended
            }
        }

    def _generate_recommendations(self) -> List[Dict]:
        recs = []

        if len(self.relocation_table) > 50:
            recs.append({
                "priority": "HIGH",
                "category": "MEMORY_MODEL",
                "message": "Nombreuses relocations: considerer un modele FLAT avec fixups",
                "action": "Utiliser .MODEL FLAT avec table de relocation PE"
            })

        if self.header.overlay_number != 0:
            recs.append({
                "priority": "CRITICAL",
                "category": "OVERLAY",
                "message": "Overlays detectes: necessite refactoring manuel",
                "action": "Extraire les overlays en DLLs separees"
            })

        return recs

    def _calculate_difficulty(self, complexity: Dict) -> Dict:
        return {
            "score": complexity["score"],
            "level": complexity["level"],
            "auto_convertible": complexity["score"] <= 3,
            "requires_review": 3 < complexity["score"] <= 6,
            "requires_rewrite": complexity["score"] > 6
        }

    def _estimate_manual_work(self, complexity: Dict) -> Dict:
        hours = complexity["score"] * 2 + len(self.relocation_table) // 20
        return {
            "estimated_hours": hours,
            "confidence": "HIGH" if complexity["level"] == "LOW" else "MEDIUM"
        }
