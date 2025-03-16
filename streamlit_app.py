import streamlit as st
import json
import random
import os
import base64
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Seitentitel und Konfiguration
st.set_page_config(
    page_title="TFT Analyzer",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
<style>
    .main {
        background-color: #2E3440;
        color: #ECEFF4;
    }
    .stButton>button {
        background-color: #5E81AC;
        color: #ECEFF4;
    }
    .stTextInput>div>div>input {
        background-color: #3B4252;
        color: #ECEFF4;
    }
    .stSelectbox>div>div>select {
        background-color: #3B4252;
        color: #ECEFF4;
    }
    h1, h2, h3 {
        color: #88C0D0;
    }
    .stProgress > div > div > div > div {
        background-color: #5E81AC;
    }
</style>
""", unsafe_allow_html=True)

# Seitentitel
st.title("TFT Analyzer")
st.subheader("KI-gestützte Analyse und Empfehlungen für Teamfight Tactics")

# Sidebar für Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Seite auswählen", ["Dashboard", "Team", "Wirtschaft", "Items", "Positionierung", "Empfehlungen", "Einstellungen"])

# Funktion zum Erstellen eines simulierten Spielzustands
def create_sample_game_state():
    # Definiere mögliche Traits
    traits = [
        'Assassin', 'Blademaster', 'Brawler', 'Elementalist', 'Guardian', 'Knight',
        'Ranger', 'Shapeshifter', 'Sorcerer', 'Demon', 'Dragon', 'Exile', 'Glacial',
        'Imperial', 'Noble', 'Ninja', 'Pirate', 'Phantom', 'Robot', 'Void', 'Wild', 'Yordle'
    ]
    
    # Definiere mögliche Champions mit ihren Traits
    champions = {
        'Ahri': {'cost': 2, 'traits': ['Wild', 'Sorcerer']},
        'Akali': {'cost': 4, 'traits': ['Assassin', 'Ninja']},
        'Anivia': {'cost': 5, 'traits': ['Glacial', 'Elementalist']},
        'Ashe': {'cost': 3, 'traits': ['Glacial', 'Ranger']},
        'Aurelion Sol': {'cost': 4, 'traits': ['Dragon', 'Sorcerer']},
        'Blitzcrank': {'cost': 2, 'traits': ['Robot', 'Brawler']},
        'Brand': {'cost': 4, 'traits': ['Demon', 'Elementalist']},
        'Braum': {'cost': 2, 'traits': ['Glacial', 'Guardian']},
        'Cho\'Gath': {'cost': 4, 'traits': ['Void', 'Brawler']},
        'Darius': {'cost': 1, 'traits': ['Imperial', 'Knight']},
        'Draven': {'cost': 4, 'traits': ['Imperial', 'Blademaster']},
        'Elise': {'cost': 2, 'traits': ['Demon', 'Shapeshifter']},
        'Evelynn': {'cost': 3, 'traits': ['Demon', 'Assassin']},
        'Fiora': {'cost': 1, 'traits': ['Noble', 'Blademaster']},
        'Gangplank': {'cost': 3, 'traits': ['Pirate', 'Blademaster', 'Gunslinger']},
        'Garen': {'cost': 1, 'traits': ['Noble', 'Knight']},
        'Gnar': {'cost': 4, 'traits': ['Wild', 'Yordle', 'Shapeshifter']},
        'Graves': {'cost': 1, 'traits': ['Pirate', 'Gunslinger']},
        'Karthus': {'cost': 5, 'traits': ['Phantom', 'Sorcerer']},
        'Kassadin': {'cost': 1, 'traits': ['Void', 'Sorcerer']},
        'Katarina': {'cost': 3, 'traits': ['Imperial', 'Assassin']},
        'Kayle': {'cost': 5, 'traits': ['Noble', 'Knight']},
        'Kennen': {'cost': 3, 'traits': ['Ninja', 'Yordle', 'Elementalist']},
        'Kindred': {'cost': 4, 'traits': ['Phantom', 'Ranger']},
        'Leona': {'cost': 4, 'traits': ['Noble', 'Guardian']},
        'Lissandra': {'cost': 2, 'traits': ['Glacial', 'Elementalist']},
        'Lucian': {'cost': 2, 'traits': ['Noble', 'Gunslinger']},
        'Lulu': {'cost': 2, 'traits': ['Yordle', 'Sorcerer']},
        'Miss Fortune': {'cost': 5, 'traits': ['Pirate', 'Gunslinger']},
        'Mordekaiser': {'cost': 1, 'traits': ['Phantom', 'Knight']},
        'Morgana': {'cost': 3, 'traits': ['Demon', 'Sorcerer']},
        'Nidalee': {'cost': 1, 'traits': ['Wild', 'Shapeshifter']},
        'Poppy': {'cost': 3, 'traits': ['Yordle', 'Knight']},
        'Pyke': {'cost': 2, 'traits': ['Pirate', 'Assassin']},
        'Rek\'Sai': {'cost': 2, 'traits': ['Void', 'Brawler']},
        'Rengar': {'cost': 3, 'traits': ['Wild', 'Assassin']},
        'Sejuani': {'cost': 4, 'traits': ['Glacial', 'Knight']},
        'Shen': {'cost': 2, 'traits': ['Ninja', 'Blademaster']},
        'Shyvana': {'cost': 3, 'traits': ['Dragon', 'Shapeshifter']},
        'Swain': {'cost': 5, 'traits': ['Imperial', 'Demon', 'Shapeshifter']},
        'Tristana': {'cost': 1, 'traits': ['Yordle', 'Gunslinger']},
        'Varus': {'cost': 2, 'traits': ['Demon', 'Ranger']},
        'Vayne': {'cost': 1, 'traits': ['Noble', 'Ranger']},
        'Veigar': {'cost': 3, 'traits': ['Yordle', 'Sorcerer']},
        'Volibear': {'cost': 3, 'traits': ['Glacial', 'Brawler']},
        'Warwick': {'cost': 1, 'traits': ['Wild', 'Brawler']},
        'Yasuo': {'cost': 5, 'traits': ['Exile', 'Blademaster']},
        'Zed': {'cost': 2, 'traits': ['Ninja', 'Assassin']}
    }
    
    # Definiere mögliche Items
    items = [
        'B.F. Sword', 'Recurve Bow', 'Needlessly Large Rod', 'Tear of the Goddess',
        'Chain Vest', 'Negatron Cloak', 'Giant\'s Belt', 'Spatula', 'Sparring Gloves',
        'Infinity Edge', 'Bloodthirster', 'Last Whisper', 'Rapid Firecannon',
        'Rabadon\'s Deathcap', 'Jeweled Gauntlet', 'Archangel\'s Staff', 'Hextech Gunblade',
        'Warmog\'s Armor', 'Dragon\'s Claw', 'Bramble Vest', 'Gargoyle Stoneplate',
        'Zeke\'s Herald', 'Chalice of Power', 'Redemption', 'Locket of the Iron Solari'
    ]
    
    # Erstelle zufälligen Spielzustand
    game_state = {
        'game_info': {
            'round': f"{random.randint(2, 4)}-{random.randint(1, 7)}",
            'gold': random.randint(10, 50),
            'level': random.randint(4, 8),
            'health': random.randint(30, 100)
        },
        'champions': {
            'board': {},
            'shop': {}
        },
        'items': {
            'bench': random.sample(items, random.randint(2, 5))
        }
    }
    
    # Füge zufällige Champions zum Board hinzu
    board_size = random.randint(5, 9)
    board_champions = random.sample(list(champions.keys()), board_size)
    
    for i, champion_name in enumerate(board_champions):
        # Bestimme Position
        x = i % 7
        y = i // 7
        
        # Bestimme Tier
        tier = 1
        if random.random() < 0.3:
            tier = 2
        if random.random() < 0.1:
            tier = 3
        
        # Bestimme Items
        champion_items = []
        if random.random() < 0.7:  # 70% Chance für Items
            num_items = random.randint(1, min(3, len(items)))
            champion_items = random.sample(items, num_items)
        
        # Füge Champion hinzu
        game_state['champions']['board'][f'champion_{i}'] = {
            'champion_data': {
                'name': champion_name,
                'cost': champions[champion_name]['cost'],
                'traits': champions[champion_name]['traits']
            },
            'tier': tier,
            'position': {'x': x, 'y': y},
            'items': champion_items
        }
    
    # Füge zufällige Champions zum Shop hinzu
    shop_size = 5
    shop_champions = random.sample(list(champions.keys()), shop_size)
    
    for i, champion_name in enumerate(shop_champions):
        # Bestimme Tier
        tier = 1
        if random.random() < 0.1:
            tier = 2
        
        # Füge Champion hinzu
        game_state['champions']['shop'][f'shop_champion_{i}'] = {
            'champion_data': {
                'name': champion_name,
                'cost': champions[champion_name]['cost'],
                'traits': champions[champion_name]['traits']
            },
            'tier': tier
        }
    
    return game_state

# Funktion zur Analyse des Spielzustands
def analyze_game_state(game_state):
    # Simuliere Analyse für das MVP
    
    # Analysiere Teamkomposition
    board_champions = game_state['champions']['board']
    
    # Zähle Traits
    trait_counts = {}
    for champion_key, champion_info in board_champions.items():
        for trait in champion_info['champion_data']['traits']:
            if trait in trait_counts:
                trait_counts[trait] += 1
            else:
                trait_counts[trait] = 1
    
    # Bestimme aktive Traits
    active_traits = {}
    for trait, count in trait_counts.items():
        if count >= 2:
            level = 1
            if count >= 4:
                level = 2
            if count >= 6:
                level = 3
            
            active_traits[trait] = {
                'level': level,
                'count': count,
                'threshold': 2 if level == 1 else (4 if level == 2 else 6)
            }
    
    # Bewerte Teamkomposition
    team_score = min(4, len(active_traits))
    
    # Analysiere Positionierung
    position_score = random.randint(1, 4)
    
    # Analysiere Wirtschaft
    gold = game_state['game_info']['gold']
    level = game_state['game_info']['level']
    
    economy_score = 1
    if gold >= 10:
        economy_score = 2
    if gold >= 30:
        economy_score = 3
    if gold >= 50:
        economy_score = 4
    
    # Analysiere Items
    total_items = 0
    champions_with_items = 0
    
    for champion_key, champion_info in board_champions.items():
        items = champion_info.get('items', [])
        total_items += len(items)
        if len(items) > 0:
            champions_with_items += 1
    
    item_score = 1
    if champions_with_items > 0:
        item_distribution = champions_with_items / len(board_champions)
        if item_distribution >= 0.75:
            item_score = 4
        elif item_distribution >= 0.5:
            item_score = 3
        elif item_distribution >= 0.25:
            item_score = 2
    
    # Berechne Gesamtbewertung
    weights = {
        'team': 0.4,
        'economy': 0.2,
        'items': 0.2,
        'position': 0.2
    }
    
    overall_score = (
        team_score * weights['team'] +
        economy_score * weights['economy'] +
        item_score * weights['items'] +
        position_score * weights['position']
    )
    
    # Erstelle Analyseergebnisse
    analysis_results = {
        'overall_score': overall_score,
        'team_analysis': {
            'score': team_score,
            'trait_details': {
                'active_traits': active_traits
            },
            'strengths': [f"Starke {trait}-Synergie (Stufe {info['level']})" for trait, info in active_traits.items() if info['level'] >= 2],
            'weaknesses': ["Wenig aktive Synergien"] if len(active_traits) < 3 else [],
            'recommendations': ["Füge mehr Champions mit gemeinsamen Traits hinzu"] if len(active_traits) < 3 else ["Verstärke deine stärksten Synergien"]
        },
        'position_analysis': {
            'score': position_score,
            'positioning_details': {
                'description': "Gute Positionierung" if position_score >= 3 else "Verbesserungswürdige Positionierung",
                'distribution_score': position_score,
                'clustering_score': position_score
            },
            'strengths': ["Gute Verteilung der Champions"] if position_score >= 3 else [],
            'weaknesses': ["Suboptimale Positionierung der Champions"] if position_score < 3 else [],
            'recommendations': ["Platziere Tanks in der vorderen Reihe"] if position_score < 3 else ["Achte auf die Positionierung gegen spezifische Gegner"]
        },
        'economy_analysis': {
            'score': economy_score,
            'economy_details': {
                'description': "Exzellente Wirtschaft" if economy_score >= 3 else "Verbesserungswürdige Wirtschaft",
                'gold': gold,
                'level': level,
                'interest': min(5, gold // 10),
                'game_phase': 'mid_game',
                'gold_score': economy_score,
                'level_score': min(4, level // 2)
            },
            'strengths': [f"Guter Gold-Vorrat ({gold} Gold)"] if gold >= 30 else [],
            'weaknesses': ["Zu wenig Gold für optimale Zinsen"] if gold < 30 else [],
            'recommendations': ["Spare auf 50 Gold für maximale Zinsen"] if gold < 50 else ["Halte dein Gold über 50 für maximale Zinsen"]
        },
        'item_analysis': {
            'score': item_score,
            'item_details': {
                'description': "Gute Item-Nutzung" if item_score >= 3 else "Verbesserungswürdige Item-Nutzung",
                'total_items': total_items,
                'champions_with_items': champions_with_items,
                'distribution_score': item_score,
                'quality_score': item_score
            },
            'strengths': ["Gute Verteilung der Items"] if item_score >= 3 else [],
            'weaknesses': ["Ungleichmäßige Verteilung der Items"] if item_score < 3 else [],
            'recommendations': ["Verteile Items gleichmäßiger auf deine Champions"] if item_score < 3 else ["Priorisiere Items für deine Carry-Champions"]
        },
        'strengths': [],
        'weaknesses': [],
        'summary': f"Gesamtbewertung: {'Exzellent' if overall_score >= 3.5 else ('Gut' if overall_score >= 2.5 else ('Mittelmäßig' if overall_score >= 1.5 else 'Verbesserungswürdig'))} ({overall_score:.2f}/4.0)"
    }
    
    # Kombiniere Stärken und Schwächen
    analysis_results['strengths'].extend([f"[Team] {s}" for s in analysis_results['team_analysis']['strengths']])
    analysis_results['strengths'].extend([f"[Wirtschaft] {s}" for s in analysis_results['economy_analysis']['strengths']])
    analysis_results['strengths'].extend([f"[Items] {s}" for s in analysis_results['item_analysis']['strengths']])
    analysis_results['strengths'].extend([f"[Position] {s}" for s in analysis_results['position_analysis']['strengths']])
    
    analysis_results['weaknesses'].extend([f"[Team] {s}" for s in analysis_results['team_analysis']['weaknesses']])
    analysis_results['weaknesses'].extend([f"[Wirtschaft] {s}" for s in analysis_results['economy_analysis']['weaknesses']])
    analysis_results['weaknesses'].extend([f"[Items] {s}" for s in analysis_results['item_analysis']['weaknesses']])
    analysis_results['weaknesses'].extend([f"[Position] {s}" for s in analysis_results['position_analysis']['weaknesses']])
    
    return analysis_results

# Funktion zur Generierung von Empfehlungen
def generate_recommendations(game_state, analysis_results):
    # Extrahiere Empfehlungen aus den Analyseergebnissen
    team_recommendations = analysis_results['team_analysis'].get('recommendations', [])
    position_recommendations = analysis_results['position_analysis'].get('recommendations', [])
    economy_recommendations = analysis_results['economy_analysis'].get('recommendations', [])
    item_recommendations = analysis_results['item_analysis'].get('recommendations', [])
    
    # Priorisiere Empfehlungen
    prioritized_recommendations = []
    
    for rec in team_recommendations:
        prioritized_recommendations.append({
            'type': 'team',
            'priority': 4,
            'text': rec
        })
    
    for rec in economy_recommendations:
        prioritized_recommendations.append({
            'type': 'economy',
            'priority': 3,
            'text': rec
        })
    
    for rec in item_recommendations:
        prioritized_recommendations.append({
            'type': 'items',
            'priority': 2,
            'text': rec
        })
    
    for rec in position_recommendations:
        prioritized_recommendations.append({
            'type': 'position',
            'priority': 1,
            'text': rec
        })
    
    # Sortiere Empfehlungen nach Priorität
    prioritized_recommendations = sorted(prioritized_recommendations, key=lambda x: x['priority'], reverse=True)
    
    # Begrenze die Anzahl der Empfehlungen
    if len(prioritized_recommendations) > 5:
        prioritized_recommendations = prioritized_recommendations[:5]
    
    # Generiere Aktionsempfehlungen
    action_recommendations = [
        "Investiere in Level-Ups, um auf das nächste Level zu kommen",
        "Verbessere deine Teamsynergien basierend auf deinen aktuellen Traits",
        "Optimiere die Positionierung deiner Champions gegen die verbleibenden Gegner"
    ]
    
    # Erstelle Empfehlungsergebnisse
    recommendation_results = {
        'prioritized_recommendations': prioritized_recommendations,
        'action_recommendations': action_recommendations,
        'team_recommendations': team_recommendations,
        'position_recommendations': position_recommendations,
        'economy_recommendations': economy_recommendations,
        'item_recommendations': item_recommendations,
        'summary': "Empfehlungen für dein nächstes Spiel:\n\n" +
                  "Sofortige Aktionen:\n" +
                  "\n".join([f"{i+1}. {rec}" for i, rec in enumerate(action_recommendations)]) +
                  "\n\nAllgemeine Verbesserungen:\n" +
                  "\n".join([f"{i+1}. [{rec['type'].capitalize()}] {rec['text']}" for i, rec in enumerate(prioritized_recommendations)])
    }
    
    return recommendation_results

# Funktion zum Zeichnen des Spielfelds
def draw_board(board_champions):
    # Erstelle ein leeres Spielfeld
    board = [[''] * 7 for _ in range(7)]
    
    # Platziere Champions auf dem Spielfeld
    for champion_key, champion_info in board_champions.items():
        position = champion_info.get('position', {})
        x = min(max(position.get('x', 0), 0), 6)
        y = min(max(position.get('y', 0), 0), 6)
        
        name = champion_info.get('champion_data', {}).get('name', champion_key)
        board[y][x] = name
    
    # Erstelle ein Bild des Spielfelds
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Zeichne Gitter
    for i in range(8):
        ax.axhline(i, color='#3B4252')
        ax.axvline(i, color='#3B4252')
    
    # Zeichne Champions
    for y in range(7):
        for x in range(7):
            if board[y][x]:
                # Zeichne Hintergrund für Champion
                rect = plt.Rectangle((x, y), 1, 1, fill=True, color='#5E81AC', alpha=0.7)
                ax.add_patch(rect)
                
                # Zeichne Champion-Namen
                ax.text(x + 0.5, y + 0.5, board[y][x], ha='center', va='center', color='white', fontsize=8)
    
    # Konfiguriere Achsen
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 7)
    ax.set_xticks(np.arange(0.5, 7.5))
    ax.set_yticks(np.arange(0.5, 7.5))
    ax.set_xticklabels(range(7))
    ax.set_yticklabels(range(7))
    ax.set_title('Spielfeld')
    
    # Invertiere y-Achse, damit 0 oben ist
    ax.invert_yaxis()
    
    # Entferne Rahmen
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Setze Hintergrundfarbe
    ax.set_facecolor('#2E3440')
    fig.patch.set_facecolor('#2E3440')
    
    return fig

# Funktion zum Erstellen eines Balkendiagramms
def create_bar_chart(data, title, x_label, y_label):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Erstelle Balkendiagramm
    bars = ax.bar(data.keys(), data.values(), color='#5E81AC')
    
    # Füge Werte über den Balken hinzu
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1, f'{height:.1f}', ha='center', va='bottom', color='white')
    
    # Konfiguriere Achsen
    ax.set_xlabel(x_label, color='white')
    ax.set_ylabel(y_label, color='white')
    ax.set_title(title, color='white')
    
    # Setze Farben
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    
    # Setze Hintergrundfarbe
    ax.set_facecolor('#2E3440')
    fig.patch.set_facecolor('#2E3440')
    
    return fig

# Funktion zum Erstellen eines Tortendiagramms
def create_pie_chart(data, title):
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Erstelle Tortendiagramm
    wedges, texts, autotexts = ax.pie(
        data.values(),
        labels=data.keys(),
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette('Blues', len(data))
    )
    
    # Setze Farben
    for text in texts:
        text.set_color('white')
    for autotext in autotexts:
        autotext.set_color('white')
    
    # Konfiguriere Diagramm
    ax.set_title(title, color='white')
    
    # Setze Hintergrundfarbe
    ax.set_facecolor('#2E3440')
    fig.patch.set_facecolor('#2E3440')
    
    return fig

# Steuerungselemente
st.sidebar.header("Steuerung")
if st.sidebar.button("Spiel erfassen"):
    st.session_state.game_state = create_sample_game_state()
    st.sidebar.success("Spielzustand erfasst!")

if st.sidebar.button("Analysieren"):
    if 'game_state' in st.session_state:
        st.session_state.analysis_results = analyze_game_state(st.session_state.game_state)
        st.session_state.recommendation_results = generate_recommendations(st.session_state.game_state, st.session_state.analysis_results)
        st.sidebar.success("Analyse abgeschlossen!")
    else:
        st.sidebar.error("Kein Spielzustand verfügbar. Bitte erfassen Sie zuerst ein Spiel.")

# Speichern und Laden
st.sidebar.header("Speichern/Laden")
if st.sidebar.button("Speichern"):
    if 'game_state' in st.session_state and 'analysis_results' in st.session_state:
        data = {
            'game_state': st.session_state.game_state,
            'analysis_results': st.session_state.analysis_results,
            'recommendation_results': st.session_state.recommendation_results
        }
        st.session_state.save_data = json.dumps(data)
        st.sidebar.download_button(
            label="Analyse herunterladen",
            data=st.session_state.save_data,
            file_name="tft_analysis.json",
            mime="application/json"
        )
    else:
        st.sidebar.error("Keine Analyseergebnisse zum Speichern verfügbar.")

uploaded_file = st.sidebar.file_uploader("Analyse laden", type="json")
if uploaded_file is not None:
    try:
        data = json.load(uploaded_file)
        st.session_state.game_state = data['game_state']
        st.session_state.analysis_results = data['analysis_results']
        st.session_state.recommendation_results = data['recommendation_results']
        st.sidebar.success("Analyse erfolgreich geladen!")
    except Exception as e:
        st.sidebar.error(f"Fehler beim Laden der Datei: {str(e)}")

# Dashboard-Seite
if page == "Dashboard":
    st.header("Dashboard")
    
    if 'analysis_results' in st.session_state:
        analysis_results = st.session_state.analysis_results
        
        # Gesamtbewertung
        st.subheader("Gesamtbewertung")
        overall_score = analysis_results['overall_score']
        st.markdown(f"<h1 style='text-align: center; color: #88C0D0;'>{overall_score:.2f}/4.0</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>{analysis_results['summary']}</p>", unsafe_allow_html=True)
        
        # Bereichsbewertungen
        st.subheader("Bereichsbewertungen")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Team", f"{analysis_results['team_analysis']['score']}/4")
            st.progress(analysis_results['team_analysis']['score'] / 4)
            
            st.metric("Wirtschaft", f"{analysis_results['economy_analysis']['score']}/4")
            st.progress(analysis_results['economy_analysis']['score'] / 4)
        
        with col2:
            st.metric("Positionierung", f"{analysis_results['position_analysis']['score']}/4")
            st.progress(analysis_results['position_analysis']['score'] / 4)
            
            st.metric("Items", f"{analysis_results['item_analysis']['score']}/4")
            st.progress(analysis_results['item_analysis']['score'] / 4)
        
        # Stärken und Schwächen
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Stärken")
            for strength in analysis_results['strengths']:
                st.markdown(f"- {strength}")
        
        with col2:
            st.subheader("Schwächen")
            for weakness in analysis_results['weaknesses']:
                st.markdown(f"- {weakness}")
        
        # Visualisierung
        st.subheader("Visualisierung")
        scores = {
            'Team': analysis_results['team_analysis']['score'],
            'Position': analysis_results['position_analysis']['score'],
            'Wirtschaft': analysis_results['economy_analysis']['score'],
            'Items': analysis_results['item_analysis']['score']
        }
        
        fig = create_bar_chart(scores, "Bewertungen nach Bereich", "Bereich", "Bewertung (0-4)")
        st.pyplot(fig)
    else:
        st.info("Keine Analyseergebnisse verfügbar. Bitte erfassen Sie ein Spiel und führen Sie eine Analyse durch.")

# Team-Seite
elif page == "Team":
    st.header("Team-Analyse")
    
    if 'analysis_results' in st.session_state and 'game_state' in st.session_state:
        analysis_results = st.session_state.analysis_results
        game_state = st.session_state.game_state
        
        # Teamkomposition
        st.subheader("Teamkomposition")
        st.metric("Teambewertung", f"{analysis_results['team_analysis']['score']}/4")
        
        # Aktive Traits
        st.subheader("Aktive Traits")
        active_traits = analysis_results['team_analysis']['trait_details']['active_traits']
        
        if active_traits:
            trait_data = {}
            for trait, info in active_traits.items():
                st.markdown(f"**{trait}**: {info['count']}/{info['threshold']} (Stufe {info['level']})")
                trait_data[trait] = info['count']
            
            # Visualisierung der Traits
            fig = create_pie_chart(trait_data, "Trait-Verteilung")
            st.pyplot(fig)
        else:
            st.info("Keine aktiven Traits gefunden.")
        
        # Champions
        st.subheader("Champions")
        board_champions = game_state['champions']['board']
        
        if board_champions:
            champion_data = []
            for champion_key, champion_info in board_champions.items():
                name = champion_info['champion_data']['name']
                tier = champion_info['tier']
                cost = champion_info['champion_data']['cost']
                traits = ", ".join(champion_info['champion_data']['traits'])
                items = ", ".join(champion_info.get('items', []))
                
                champion_data.append({
                    "Name": name,
                    "Tier": f"{tier}★",
                    "Kosten": cost,
                    "Traits": traits,
                    "Items": items
                })
            
            st.table(pd.DataFrame(champion_data))
        else:
            st.info("Keine Champions gefunden.")
        
        # Stärken und Schwächen
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Stärken")
            for strength in analysis_results['team_analysis']['strengths']:
                st.markdown(f"- {strength}")
        
        with col2:
            st.subheader("Schwächen")
            for weakness in analysis_results['team_analysis']['weaknesses']:
                st.markdown(f"- {weakness}")
        
        # Empfehlungen
        st.subheader("Empfehlungen")
        for recommendation in analysis_results['team_analysis']['recommendations']:
            st.markdown(f"- {recommendation}")
    else:
        st.info("Keine Analyseergebnisse verfügbar. Bitte erfassen Sie ein Spiel und führen Sie eine Analyse durch.")

# Wirtschafts-Seite
elif page == "Wirtschaft":
    st.header("Wirtschafts-Analyse")
    
    if 'analysis_results' in st.session_state and 'game_state' in st.session_state:
        analysis_results = st.session_state.analysis_results
        game_state = st.session_state.game_state
        
        # Wirtschaftsübersicht
        st.subheader("Wirtschaftsübersicht")
        st.metric("Wirtschaftsbewertung", f"{analysis_results['economy_analysis']['score']}/4")
        
        # Wirtschaftsmetriken
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Gold", game_state['game_info']['gold'])
        
        with col2:
            st.metric("Level", game_state['game_info']['level'])
        
        with col3:
            st.metric("Zinsen", analysis_results['economy_analysis']['economy_details']['interest'])
        
        with col4:
            st.metric("Spielphase", analysis_results['economy_analysis']['economy_details']['game_phase'].replace('_', ' ').capitalize())
        
        # Wirtschaftsanalyse
        st.subheader("Wirtschaftsanalyse")
        st.markdown(analysis_results['economy_analysis']['economy_details']['description'])
        
        # Visualisierung
        st.subheader("Visualisierung")
        
        # Gold vs. Optimales Gold
        gold_data = {
            'Aktuelles Gold': game_state['game_info']['gold'],
            'Optimales Gold (Zinsen)': 50
        }
        
        fig = create_bar_chart(gold_data, "Gold-Analyse", "Kategorie", "Gold")
        st.pyplot(fig)
        
        # Stärken und Schwächen
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Stärken")
            for strength in analysis_results['economy_analysis']['strengths']:
                st.markdown(f"- {strength}")
        
        with col2:
            st.subheader("Schwächen")
            for weakness in analysis_results['economy_analysis']['weaknesses']:
                st.markdown(f"- {weakness}")
        
        # Empfehlungen
        st.subheader("Empfehlungen")
        for recommendation in analysis_results['economy_analysis']['recommendations']:
            st.markdown(f"- {recommendation}")
    else:
        st.info("Keine Analyseergebnisse verfügbar. Bitte erfassen Sie ein Spiel und führen Sie eine Analyse durch.")

# Items-Seite
elif page == "Items":
    st.header("Item-Analyse")
    
    if 'analysis_results' in st.session_state and 'game_state' in st.session_state:
        analysis_results = st.session_state.analysis_results
        game_state = st.session_state.game_state
        
        # Item-Übersicht
        st.subheader("Item-Übersicht")
        st.metric("Item-Bewertung", f"{analysis_results['item_analysis']['score']}/4")
        
        # Item-Metriken
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Gesamtitems", analysis_results['item_analysis']['item_details']['total_items'])
        
        with col2:
            st.metric("Champions mit Items", analysis_results['item_analysis']['item_details']['champions_with_items'])
        
        with col3:
            st.metric("Verteilung", f"{analysis_results['item_analysis']['item_details']['distribution_score']}/4")
        
        with col4:
            st.metric("Qualität", f"{analysis_results['item_analysis']['item_details']['quality_score']}/4")
        
        # Champion-Items
        st.subheader("Champion-Items")
        board_champions = game_state['champions']['board']
        
        if board_champions:
            champion_items = []
            for champion_key, champion_info in board_champions.items():
                name = champion_info['champion_data']['name']
                items = champion_info.get('items', [])
                
                if items:
                    champion_items.append({
                        "Champion": name,
                        "Items": ", ".join(items)
                    })
                else:
                    champion_items.append({
                        "Champion": name,
                        "Items": "Keine Items"
                    })
            
            st.table(pd.DataFrame(champion_items))
        else:
            st.info("Keine Champions gefunden.")
        
        # Items auf der Bank
        st.subheader("Items auf der Bank")
        bench_items = game_state['items']['bench']
        
        if bench_items:
            st.markdown(", ".join(bench_items))
        else:
            st.info("Keine Items auf der Bank gefunden.")
        
        # Stärken und Schwächen
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Stärken")
            for strength in analysis_results['item_analysis']['strengths']:
                st.markdown(f"- {strength}")
        
        with col2:
            st.subheader("Schwächen")
            for weakness in analysis_results['item_analysis']['weaknesses']:
                st.markdown(f"- {weakness}")
        
        # Empfehlungen
        st.subheader("Empfehlungen")
        for recommendation in analysis_results['item_analysis']['recommendations']:
            st.markdown(f"- {recommendation}")
    else:
        st.info("Keine Analyseergebnisse verfügbar. Bitte erfassen Sie ein Spiel und führen Sie eine Analyse durch.")

# Positionierungs-Seite
elif page == "Positionierung":
    st.header("Positionierungs-Analyse")
    
    if 'analysis_results' in st.session_state and 'game_state' in st.session_state:
        analysis_results = st.session_state.analysis_results
        game_state = st.session_state.game_state
        
        # Positionierungsübersicht
        st.subheader("Positionierungsübersicht")
        st.metric("Positionierungsbewertung", f"{analysis_results['position_analysis']['score']}/4")
        
        # Spielfeld
        st.subheader("Spielfeld")
        board_champions = game_state['champions']['board']
        
        if board_champions:
            fig = draw_board(board_champions)
            st.pyplot(fig)
        else:
            st.info("Keine Champions auf dem Spielfeld gefunden.")
        
        # Positionsanalyse
        st.subheader("Positionsanalyse")
        st.markdown(analysis_results['position_analysis']['positioning_details']['description'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Verteilungs-Score", f"{analysis_results['position_analysis']['positioning_details']['distribution_score']}/4")
        
        with col2:
            st.metric("Clustering-Score", f"{analysis_results['position_analysis']['positioning_details']['clustering_score']}/4")
        
        # Stärken und Schwächen
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Stärken")
            for strength in analysis_results['position_analysis']['strengths']:
                st.markdown(f"- {strength}")
        
        with col2:
            st.subheader("Schwächen")
            for weakness in analysis_results['position_analysis']['weaknesses']:
                st.markdown(f"- {weakness}")
        
        # Empfehlungen
        st.subheader("Empfehlungen")
        for recommendation in analysis_results['position_analysis']['recommendations']:
            st.markdown(f"- {recommendation}")
    else:
        st.info("Keine Analyseergebnisse verfügbar. Bitte erfassen Sie ein Spiel und führen Sie eine Analyse durch.")

# Empfehlungs-Seite
elif page == "Empfehlungen":
    st.header("Empfehlungen")
    
    if 'recommendation_results' in st.session_state:
        recommendation_results = st.session_state.recommendation_results
        
        # Hauptempfehlungen
        st.subheader("Hauptempfehlungen")
        prioritized_recommendations = recommendation_results['prioritized_recommendations']
        
        for i, rec in enumerate(prioritized_recommendations, 1):
            st.markdown(f"{i}. **[{rec['type'].capitalize()}]** {rec['text']}")
        
        # Aktionsempfehlungen
        st.subheader("Aktionsempfehlungen")
        action_recommendations = recommendation_results['action_recommendations']
        
        for i, rec in enumerate(action_recommendations, 1):
            st.markdown(f"{i}. {rec}")
        
        # Champion-Empfehlungen
        st.subheader("Champion-Empfehlungen")
        
        if 'game_state' in st.session_state:
            game_state = st.session_state.game_state
            shop_champions = game_state['champions']['shop']
            
            if shop_champions:
                champion_data = []
                for champion_key, champion_info in shop_champions.items():
                    name = champion_info['champion_data']['name']
                    tier = champion_info['tier']
                    cost = champion_info['champion_data']['cost']
                    traits = ", ".join(champion_info['champion_data']['traits'])
                    
                    champion_data.append({
                        "Name": name,
                        "Tier": f"{tier}★",
                        "Kosten": cost,
                        "Traits": traits,
                        "Empfehlung": "Kaufen" if random.random() > 0.5 else "Ignorieren"
                    })
                
                st.table(pd.DataFrame(champion_data))
            else:
                st.info("Keine Champions im Shop gefunden.")
        else:
            st.info("Kein Spielzustand verfügbar.")
        
        # Bereichsspezifische Empfehlungen
        st.subheader("Bereichsspezifische Empfehlungen")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Team", "Wirtschaft", "Items", "Positionierung"])
        
        with tab1:
            for rec in recommendation_results['team_recommendations']:
                st.markdown(f"- {rec}")
        
        with tab2:
            for rec in recommendation_results['economy_recommendations']:
                st.markdown(f"- {rec}")
        
        with tab3:
            for rec in recommendation_results['item_recommendations']:
                st.markdown(f"- {rec}")
        
        with tab4:
            for rec in recommendation_results['position_recommendations']:
                st.markdown(f"- {rec}")
    else:
        st.info("Keine Empfehlungen verfügbar. Bitte erfassen Sie ein Spiel und führen Sie eine Analyse durch.")

# Einstellungs-Seite
elif page == "Einstellungen":
    st.header("Einstellungen")
    
    # Erfassungseinstellungen
    st.subheader("Erfassungseinstellungen")
    
    capture_interval = st.slider("Erfassungsintervall (Sekunden)", 1, 10, 5)
    st.write(f"Das Spiel wird alle {capture_interval} Sekunden erfasst.")
    
    screen_region = st.radio("Bildschirmbereich", ["Vollbild", "Benutzerdefiniert"])
    
    if screen_region == "Benutzerdefiniert":
        st.info("Diese Funktion ist im MVP noch nicht implementiert.")
    
    # Analyseeinstellungen
    st.subheader("Analyseeinstellungen")
    
    analysis_depth = st.select_slider("Analysetiefe", options=["Einfach", "Standard", "Detailliert"], value="Standard")
    st.write(f"Analysetiefe: {analysis_depth}")
    
    # Benutzeroberflächen-Einstellungen
    st.subheader("Benutzeroberflächen-Einstellungen")
    
    ui_theme = st.radio("Theme", ["Dunkel", "Hell"])
    st.write(f"Theme: {ui_theme}")
    
    # Über
    st.subheader("Über")
    st.markdown("""
    **TFT Analyzer MVP**
    
    Version: 0.1.0
    
    Ein KI-gestütztes Tool zur Analyse von Teamfight Tactics Spielen.
    
    © 2025 TFT Analyzer Team
    """)
    
    # Hilfe
    st.subheader("Hilfe")
    
    with st.expander("Wie verwende ich den TFT Analyzer?"):
        st.markdown("""
        1. Klicken Sie auf "Spiel erfassen", um den Spielzustand zu erfassen
        2. Klicken Sie auf "Analysieren", um den Spielzustand zu analysieren
        3. Sehen Sie sich die Analyseergebnisse und Empfehlungen in den verschiedenen Tabs an
        4. Speichern Sie die Analyse bei Bedarf für spätere Referenz
        """)
    
    with st.expander("Fehlerbehebung"):
        st.markdown("""
        **Problem: Die Anwendung startet nicht**
        
        Lösung:
        - Stellen Sie sicher, dass Python 3.10 oder höher installiert ist
        - Überprüfen Sie, ob alle Abhängigkeiten installiert sind
        - Starten Sie die Anwendung über die Kommandozeile, um Fehlermeldungen zu sehen
        
        **Problem: Die Spielerfassung funktioniert nicht**
        
        Lösung:
        - Stellen Sie sicher, dass TFT im Vollbildmodus läuft
        - Passen Sie den Bildschirmbereich in den Einstellungen an
        - Verwenden Sie für das MVP die simulierte Datenerfassung
        """)
