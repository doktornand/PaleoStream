"""
Report Generator - Generation de rapports de conversion
"""

import json
from typing import Dict, Any, List
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def generate_conversion_report(result: Dict[str, Any]) -> Dict[str, Any]:
    """Genere un rapport complet de conversion"""

    report = {
        "summary": {
            "status": "SUCCESS" if result.get("stats", {}).get("success") else "PARTIAL",
            "duration_ms": result.get("stats", {}).get("duration", 0),
            "phases_completed": len([p for p in result.get("phases", {}).values() if p]),
            "total_phases": 5
        },
        "metrics": {
            "source_lines": result.get("phases", {}).get("emission", {}).get("metadata", {}).get("lines", 0),
            "transformations_applied": result.get("phases", {}).get("transformation", {}).get("metadata", {}).get("rulesApplied", 0),
            "manual_reviews_required": len(result.get("phases", {}).get("transformation", {}).get("manualReview", [])),
            "warnings": len(result.get("warnings", []))
        },
        "phases": {},
        "validation": result.get("phases", {}).get("validation", {}),
        "recommendations": []
    }

    # Details par phase
    for phase_name, phase_data in result.get("phases", {}).items():
        report["phases"][phase_name] = {
            "status": "COMPLETED" if phase_data else "FAILED",
            "details": phase_data
        }

    return report

def create_sankey_diagram(transformations: List[Dict]) -> go.Figure:
    """Cree un diagramme Sankey des transformations"""

    sources = []
    targets = []
    values = []
    labels = []

    categories = list(set(t.get("type", "unknown") for t in transformations))
    labels = categories + ["Win32 API", "MASM Code", "Data Section"]

    label_map = {l: i for i, l in enumerate(labels)}

    for t in transformations:
        cat = t.get("type", "unknown")
        if cat in label_map:
            sources.append(label_map[cat])
            targets.append(label_map.get("Win32 API", len(labels) - 3))
            values.append(1)

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=["#e94560"] * len(categories) + ["#4ecca3", "#4ecca3", "#4ecca3"]
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=["rgba(233, 69, 96, 0.4)"] * len(sources)
        )
    )])

    fig.update_layout(
        title_text="Flux de Transformations",
        font_size=12,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    return fig

def create_complexity_gauge(score: int) -> go.Figure:
    """Cree une jauge de complexite"""

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Complexite", 'font': {'size': 24, 'color': '#eeeeee'}},
        gauge={
            'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': '#eeeeee'},
            'bar': {'color': '#e94560'},
            'bgcolor': '#16213e',
            'borderwidth': 2,
            'bordercolor': '#0f3460',
            'steps': [
                {'range': [0, 3], 'color': '#4ecca330'},
                {'range': [3, 6], 'color': '#f4d03f30'},
                {'range': [6, 10], 'color': '#e9456030'}
            ],
            'threshold': {
                'line': {'color': 'red', 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': '#eeeeee'}
    )

    return fig

def create_register_heatmap(register_usage: Dict[str, int]) -> go.Figure:
    """Cree une heatmap des registres convertis"""

    regs_16 = ['AX', 'BX', 'CX', 'DX', 'SI', 'DI', 'BP', 'SP']
    regs_32 = ['EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP']

    values = [register_usage.get(r, 0) for r in regs_16]

    fig = go.Figure(data=[go.Bar(
        x=regs_16,
        y=values,
        text=regs_32,
        textposition='outside',
        marker_color=['#e94560'] * len(regs_16),
        hovertemplate='%{x} → %{text}<br>Utilisations: %{y}<extra></extra>'
    )])

    fig.update_layout(
        title="Conversion Registres 16→32 bit",
        xaxis_title="Registres 16-bit (DOS)",
        yaxis_title="Nombre d'utilisations",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': '#eeeeee'},
        xaxis={'gridcolor': '#0f3460'},
        yaxis={'gridcolor': '#0f3460'}
    )

    return fig

def export_corpus_data(parsed_data: Dict, transformations: List[Dict]) -> str:
    """Exporte les donnees pour analyse corpus (CodeCartographer)"""

    corpus = {
        "format": parsed_data.get("format", "UNKNOWN"),
        "architecture": {
            "source": "x86_16",
            "target": "x86_32"
        },
        "metrics": {
            "file_size": parsed_data.get("metadata", {}).get("file_size", 0),
            "program_size": parsed_data.get("header", {}).get("calculated_program_size", 0),
            "relocation_count": len(parsed_data.get("relocation_table", [])),
            "segment_count": len(parsed_data.get("segments", [])),
            "zone_count": len(parsed_data.get("zones", []))
        },
        "instruction_distribution": {},
        "api_surface": parsed_data.get("apiSurface", []),
        "transformations": [
            {
                "type": t.get("type"),
                "rule": t.get("rule"),
                "confidence": t.get("confidence", 1.0)
            }
            for t in transformations
        ],
        "complexity": parsed_data.get("complexity", {}),
        "migration_metadata": {
            "auto_convertible": parsed_data.get("conversionDifficulty", {}).get("autoConvertible", False),
            "manual_reviews": len([t for t in transformations if "MANUAL" in str(t)])
        }
    }

    return json.dumps(corpus, indent=2, ensure_ascii=False)
