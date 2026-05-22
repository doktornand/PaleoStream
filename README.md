# Scadassembler v2.0 - Application Streamlit

Application web interactive pour la conversion de code assembleur x86 16-bit (MS-DOS) vers x86 32-bit (Win32), avec support SCADA/IoT.

## 🚀 Deploiement

### Streamlit Cloud (Recommande)

1. Forkez ce repository sur GitHub
2. Connectez-vous sur [share.streamlit.io](https://share.streamlit.io)
3. Deployez depuis votre repository
4. L'application sera accessible a `https://votre-app.streamlit.app`

### Local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Structure

```
scadassembler-streamlit/
├── app.py                          # Point d'entree
├── pages/
│   ├── 1_🔍_Analyseur_Binaire.py  # Upload + analyse hex
│   ├── 2_⚙️_Conversion.py         # Pipeline conversion
│   ├── 3_📊_Rapport_et_Métriques.py  # Visualisations
│   └── 4_📚_Documentation.py      # Docs integrees
├── core/
│   ├── mz_parser.py               # Parser MZ complet
│   ├── com_parser.py              # Parser COM
│   └── rule_engine.py             # Moteur regles
├── utils/
│   ├── hex_viewer.py              # Visualisation hex
│   ├── styling.py                 # CSS custom
│   └── report_generator.py        # Rapports
└── config/
    └── hierarchical_rules.json    # Regles de conversion
```

## 🎨 Features UI

- **Theme cyberpunk/SCADA** : Couleurs sombres, accents neon (#e94560)
- **Hex dump interactif** : Classification automatique CODE/DATA/ASCII
- **Visualisations Plotly** : Sankey, heatmap, jauge de complexite
- **Pipeline anime** : Progression des 5 phases en temps reel
- **Export CodeCartographer** : JSON structure pour analyse corpus

## 🔧 Fonctionnalites

| Fonction | Description |
|----------|-------------|
| Parser MZ | Header DOS, relocation table, segments, zones code/data |
| Parser COM | Format plat 64K, detection interruptions |
| Regles hierarchiques | 11 categories, resolution conflits par priorite |
| Conversion ASM | 16→32 bit, interruptions DOS→Win32 |
| Mode SCADA | Bridge ports serie, timers, protocoles IoT |

## 📄 Licence

MIT
