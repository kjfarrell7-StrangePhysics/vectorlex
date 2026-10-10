import streamlit as st
import random

st.set_page_config(
    page_title="VectorLex: Riddle Edition",
    page_icon="⚡",
    layout="centered"
)

# Professional Dark Theme UI Styling
st.markdown("""
<style>
    :root {
        --bg-color: #0f172a;
        --panel-color: #1e293b;
        --accent-color: #38bdf8;
        --accent-hover: #0ea5e9;
        --hint-color: #f59e0b;
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
        --tile-bg: #334155;
        --tile-hover: #475569;
        --tile-selected: #0284c7;
        --border-color: #475569;
    }

    .stApp {
        background-color: var(--bg-color);
        color: var(--text-main);
    }

    .container-card {
        background: var(--panel-color);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        margin-bottom: 20px;
        border: 1px solid var(--border-color);
    }

    .riddle-box {
        background: rgba(56, 189, 248, 0.1);
        border-left: 4px solid var(--accent-color);
        padding: 12px 14px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 15px;
    }

    .riddle-box h3 {
        margin: 0 0 4px 0;
        font-size: 0.8rem;
        color: var(--accent-color);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .riddle-box p {
        margin: 0;
        font-size: 0.95rem;
        font-style: italic;
        line-height: 1.3;
        color: var(--text-main);
    }

    .target-display {
        text-align: center;
        font-size: 1.3rem;
        letter-spacing: 4px;
        font-weight: bold;
        background: #0f172a;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid var(--border-color);
        color: var(--accent-color);
        font-family: monospace;
        margin-bottom: 15px;
    }

    .status-bar {
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        color: var(--text-muted);
        font-weight: 600;
        margin-bottom: 10px;
    }

    .stButton button {
        width: 100%;
        background-color: var(--accent-color);
        color: #0f172a;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px;
        transition: background 0.2s;
    }

    .stButton button:hover {
        background-color: var(--accent-hover);
        color: #0f172a;
    }
</style>
""", unsafe_allow_html=True)

# Levels Configuration
LEVELS = [
    {
        "tier": "Tier 1: Newtonian Mechanics",
        "riddle": "What fundamental principle states that total energy remains constant over time in an isolated system?",
        "target": "CONSERVATION",
        "words_allowed": 6,
        "vectors": ["N1", "S1", "E1", "W1"]
    },
    {
        "tier": "Tier 2: Thermodynamics",
        "riddle": "What universal metric measures the degree of disorder or randomness in a closed system?",
        "target": "ENTROPY",
        "words_allowed": 6,
        "vectors": ["N1", "S1", "E1", "W1", "NE1"]
    },
    {
        "tier": "Tier 3: Relativistic Physics",
        "riddle": "What four-dimensional continuum bends under the mass-energy weight of massive celestial bodies?",
        "target": "SPACETIME",
        "words_allowed": 5,
        "vectors": ["N1", "S1", "E1", "W1", "NE1", "SW1"]
    },
    {
        "tier": "Tier 4: Quantum Mechanics",
        "riddle": "What fundamental limit bounds our simultaneous precision when measuring position and momentum?",
        "target": "UNCERTAINTY",
        "words_allowed": 5,
        "vectors": ["N1", "S1", "E1", "W1", "NE1", "NW1", "SE1", "SW1"]
    }
]

# Expanded Physics & General Dictionary
VALID_DICTIONARY = set([
    "CONSERVATION", "ENTROPY", "SPACETIME", "UNCERTAINTY",
    "AXION", "BOSON", "PHOTON", "FERMION", "HADRON", "LEPTON", "GLUON", "GRAVITON",
    "NEUTRINO", "MUON", "PION", "TENSOR", "VECTOR", "SCALAR", "MATRIX", "SPIN",
    "FLUX", "FIELD", "WAVE", "NODE", "LATTICE", "ORBIT", "PLASMA", "KINETIC",
    "ISOTOPE", "MASS", "FORCE", "MOTION", "LIGHT", "TIME", "SPACE", "GRAVITY",
    "CHARGE", "CURRENT", "POWER", "HEAT", "WORK", "GAS", "ATOM", "CORE", "STATE",
    "SPEED", "QUANTA", "QUANTUM", "RAY", "COIN", "STARS", "ACTION", "RATES", "TRAIN",
    "COVER", "NATION", "DARK", "STAR", "THERMO", "FLUID", "PARTICLE", "QUARK",
    "SON", "SUN", "VAN", "VIN", "VIA", "SINK", "SCAN", "AXIS", "KIN", "OAT", "NOT",
    "NET", "TON", "TIN", "PIN", "PEN", "CAN", "CAT", "RAT", "RUN", "RAN", "SET",
    "SIT", "SAT", "FIT", "FAR", "FAN", "MAN", "MAP", "TAP", "TOP", "POT", "DOT",
    "ONE", "TWO", "SIX", "TEN", "ION", "ARC", "BAR", "CAR", "OAR", "ROW", "SEA"
])

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def init_level(level_idx):
    level = LEVELS[level_idx]
    st.session_state.words_left = level["words_allowed"]
    st.session_state.revealed_letters = set()
    st.session_state.selected_indices = []
    
    # Board Generation with Target Prioritization
    target_chars = list(level["target"])
    filler = ["A","E","I","O","U","N","R","S","T","L","C","V","X","K","P"]
    grid = []
    for i in range(16):
        char = target_chars[i] if i < len(target_chars) else random.choice(filler)
        grid.append({"letter": char, "vector": random.choice(level["vectors"])})
    random.shuffle(grid)
    st.session_state.grid = grid

# Session Initialization
if "level_index" not in st.session_state:
    st.session_state.level_index = 0
    init_level(0)

current_level = LEVELS[st.session_state.level_index]

# Main App Container
st.markdown("<h1 style='text-align: center; color: #38bdf8; margin-bottom: 0;'>VectorLex</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2px;'>Riddle Edition</p>", unsafe_allow_html=True)

# Status Bar
col_status1, col_status2 = st.columns(2)
with col_status1:
    st.markdown(f"**{current_level['tier']}**")
with col_status2:
    st.markdown(f"<div style='text-align: right;'><b>Guesses Left:</b> <span style='color: #38bdf8;'>{st.session_state.words_left}</span></div>", unsafe_allow_html=True)

# Riddle Box
st.markdown(f"""
<div class="riddle-box">
    <h3>Physics Riddle</h3>
    <p>{current_level['riddle']}</p>
</div>
""", unsafe_allow_html=True)

# Target Display
target_word = current_level["target"]
display_answer = " ".join([char if char in st.session_state.revealed_letters else "_" for char in target_word])
st.markdown(f"<div class='target-display'>{display_answer}</div>", unsafe_allow_html=True)

# Current Selected Word Tracker
selected_word = "".join([st.session_state.grid[i]["letter"] for i in st.session_state.selected_indices])
st.markdown(f"<div style='text-align: center; margin-bottom: 12px; font-family: monospace; font-size: 1.1rem;'>Selected: <span style='color: #38bdf8;'>{selected_word if selected_word else '...'}</span></div>", unsafe_allow_html=True)

# 4x4 Grid Rendering
cols = st.columns(4)
for i in range(16):
    col = cols[i % 4]
    tile = st.session_state.grid[i]
    is_selected = i in st.session_state.selected_indices
    
    # Style active selection visually inside button label
    label = f"✦ {tile['letter']} \n [{tile['vector']}]" if is_selected else f"{tile['letter']} \n [{tile['vector']}]"
    
    if col.button(label, key=f"tile_{i}"):
        if i in st.session_state.selected_indices:
            st.session_state.selected_indices.remove(i)
        else:
            st.session_state.selected_indices.append(i)
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Control Buttons
btn_col1, btn_col2, btn_col3 = st.columns(3)

with btn_col1:
    if st.button("Clear"):
        st.session_state.selected_indices = []
        st.rerun()

with btn_col2:
    if st.button("💡 Hint"):
        unrevealed = [c for c in target_word if c not in st.session_state.revealed_letters]
        if unrevealed:
            st.session_state.revealed_letters.add(unrevealed[0])
            st.toast(f"💡 Hint: Revealed letter '{unrevealed[0]}'!")
            st.rerun()
        else:
            st.toast("All letters already revealed! Spell the target word to clear.")

with btn_col3:
    if st.button("Submit Word"):
        if len(selected_word) < 3:
            st.error("Words must be at least 3 letters long.")
        elif selected_word not in VALID_DICTIONARY and selected_word != target_word:
            st.error(f"'{selected_word}' is not in the dictionary.")
        else:
            st.session_state.words_left -= 1
            for char in selected_word:
                if char in target_word:
                    st.session_state.revealed_letters.add(char)
            
            # Check Win Condition
            all_solved = all(c in st.session_state.revealed_letters for c in target_word)
            if selected_word == target_word or all_solved:
                st.success(f"🎉 Correct! The answer was {target_word}!")
                if st.session_state.level_index + 1 < len(LEVELS):
                    st.session_state.level_index += 1
                    init_level(st.session_state.level_index)
                    st.rerun()
                else:
                    st.balloons()
                    st.success("🏆 Amazing! You conquered all physics riddle tiers!")
            elif st.session_state.words_left <= 0:
                st.error(f"Game Over! Out of word guesses. The answer was {target_word}.")
            else:
                st.toast(f"Valid word '{selected_word}'! Clues uncovered.")
                st.session_state.selected_indices = []
                st.rerun()
