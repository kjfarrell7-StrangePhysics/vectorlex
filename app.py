import streamlit as st
import random

st.set_page_config(
    page_title="VectorLex: Riddle Edition",
    page_icon="⚡",
    layout="centered"
)

# Custom Styling
st.markdown("""
<style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stButton button {
        width: 100%;
        background-color: #38bdf8;
        color: #0f172a;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px;
    }
    .stButton button:hover {
        background-color: #0ea5e9;
        color: #ffffff;
    }
    .target-box {
        background-color: #1e293b;
        border: 2px solid #38bdf8;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        font-family: monospace;
        font-size: 1.5rem;
        letter-spacing: 5px;
        color: #38bdf8;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Levels Configuration
LEVELS = [
    {
        "tier": "Tier 1: Newtonian Mechanics",
        "riddle": "What fundamental principle dictates that energy cannot be created or destroyed, only transformed?",
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

# Dictionary
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
    
    # Board Generation
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

# Header
st.title("⚡ VectorLex: Riddle Edition")
col_a, col_b = st.columns(2)
with col_a:
    st.subheader(current_level["tier"])
with col_b:
    st.metric("Guesses Left", st.session_state.words_left)

st.info(f"**Physics Riddle:** {current_level['riddle']}")

# Display Answer Progress
target_word = current_level["target"]
display_answer = " ".join([char if char in st.session_state.revealed_letters else "_" for char in target_word])
st.markdown(f"<div class='target-box'>{display_answer}</div>", unsafe_allow_html=True)

# Word Formation Tracker
selected_word = "".join([st.session_state.grid[i]["letter"] for i in st.session_state.selected_indices])
st.write(f"**Current Word:** `{selected_word}`")

# Render 4x4 Grid
st.write("---")
cols = st.columns(4)
for i in range(16):
    col = cols[i % 4]
    tile = st.session_state.grid[i]
    is_selected = i in st.session_state.selected_indices
    label = f"✅ {tile['letter']} ({tile['vector']})" if is_selected else f"{tile['letter']} ({tile['vector']})"
    if col.button(label, key=f"tile_{i}"):
        if i in st.session_state.selected_indices:
            st.session_state.selected_indices.remove(i)
        else:
            st.session_state.selected_indices.append(i)
        st.rerun()

st.write("---")
btn_col1, btn_col2, btn_col3 = st.columns(3)

# Clear Selection
if btn_col1.button("🧹 Clear"):
    st.session_state.selected_indices = []
    st.rerun()

# Hint Button
if btn_col2.button("💡 Hint"):
    unrevealed = [c for c in target_word if c not in st.session_state.revealed_letters]
    if unrevealed:
        st.session_state.revealed_letters.add(unrevealed[0])
        st.toast(f"Hint: Uncovered '{unrevealed[0]}'")
        st.rerun()

# Submit Word
if btn_col3.button("🚀 Submit Word"):
    if len(selected_word) < 3:
        st.error("Words must be at least 3 letters long!")
    elif selected_word not in VALID_DICTIONARY and selected_word != target_word:
        st.error(f"'{selected_word}' is not in the dictionary.")
    else:
        st.session_state.words_left -= 1
        for char in selected_word:
            if char in target_word:
                st.session_state.revealed_letters.add(char)
        
        # Check Win Condition
        if selected_word == target_word or set(target_word).issubset(st.session_state.revealed_letters):
            st.success(f"🎉 Correct! The answer was {target_word}!")
            if st.session_state.level_index + 1 < len(LEVELS):
                st.session_state.level_index += 1
                init_level(st.session_state.level_index)
                st.rerun()
            else:
                st.balloons()
                st.success("🏆 You conquered all physics tiers!")
        elif st.session_state.words_left <= 0:
            st.error(f"Game Over! The answer was {target_word}.")
        else:
            st.toast(f"Valid word '{selected_word}' submitted!")
            st.session_state.selected_indices = []
            st.rerun()
