#!/usr/bin/env python3
"""
Urdu Alphabet Adventure for Kids
Interactive Urdu alphabet learning platform for children aged 4-7
Learn Urdu letters with fun games, sounds, and activities
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import time

# ===== URDU ALPHABET DATA =====
URDU_ALPHABET_DATA = {
    "letters": [
        {
            "id": 1,
            "letter": "ا",
            "name": "Alif",
            "english": "A",
            "sound": "aa",
            "words": [
                {"word": "آم", "meaning": "Mango", "english": "Aam"},
                {"word": "آنکھ", "meaning": "Eye", "english": "Aankh"},
                {"word": "اسکول", "meaning": "School", "english": "School"}
            ],
            "color": "#FF6B6B"
        },
        {
            "id": 2,
            "letter": "ب",
            "name": "Bay",
            "english": "B",
            "sound": "ba",
            "words": [
                {"word": "بلی", "meaning": "Cat", "english": "Billi"},
                {"word": "بکری", "meaning": "Goat", "english": "Bakri"},
                {"word": "بندر", "meaning": "Monkey", "english": "Bandar"}
            ],
            "color": "#4ECDC4"
        },
        {
            "id": 3,
            "letter": "پ",
            "name": "Pay",
            "english": "P",
            "sound": "pa",
            "words": [
                {"word": "پانی", "meaning": "Water", "english": "Paani"},
                {"word": "پھل", "meaning": "Fruit", "english": "Phal"},
                {"word": "پرندہ", "meaning": "Bird", "english": "Parinda"}
            ],
            "color": "#45B7D1"
        },
        {
            "id": 4,
            "letter": "ت",
            "name": "Tay",
            "english": "T",
            "sound": "ta",
            "words": [
                {"word": "تتلی", "meaning": "Butterfly", "english": "Titli"},
                {"word": "تیرنا", "meaning": "Swimming", "english": "Tairna"},
                {"word": "تارا", "meaning": "Star", "english": "Tara"}
            ],
            "color": "#96CEB4"
        },
        {
            "id": 5,
            "letter": "ٹ",
            "name": "Ttay",
            "english": "Tt",
            "sound": "tta",
            "words": [
                {"word": "ٹماٹر", "meaning": "Tomato", "english": "Tamatar"},
                {"word": "ٹوپی", "meaning": "Hat", "english": "Topi"},
                {"word": "ٹرین", "meaning": "Train", "english": "Train"}
            ],
            "color": "#FFEAA7"
        },
        {
            "id": 6,
            "letter": "ث",
            "name": "Say",
            "english": "S",
            "sound": "sa",
            "words": [
                {"word": "ثعبان", "meaning": "Snake", "english": "Saaban"},
                {"word": "ثواب", "meaning": "Reward", "english": "Sawab"}
            ],
            "color": "#DDA0DD"
        },
        {
            "id": 7,
            "letter": "ج",
            "name": "Jeem",
            "english": "J",
            "sound": "ja",
            "words": [
                {"word": "جہاز", "meaning": "Ship/Plane", "english": "Jahaaz"},
                {"word": "جانور", "meaning": "Animal", "english": "Janwar"},
                {"word": "جوتا", "meaning": "Shoe", "english": "Joota"}
            ],
            "color": "#FFB347"
        },
        {
            "id": 8,
            "letter": "چ",
            "name": "Chay",
            "english": "Ch",
            "sound": "cha",
            "words": [
                {"word": "چاند", "meaning": "Moon", "english": "Chaand"},
                {"word": "چائے", "meaning": "Tea", "english": "Chai"},
                {"word": "چڑیا", "meaning": "Sparrow", "english": "Chiriya"}
            ],
            "color": "#FF69B4"
        },
        {
            "id": 9,
            "letter": "ح",
            "name": "Hay",
            "english": "H",
            "sound": "ha",
            "words": [
                {"word": "حج", "meaning": "Pilgrimage", "english": "Hajj"},
                {"word": "حساب", "meaning": "Math", "english": "Hisaab"}
            ],
            "color": "#87CEEB"
        },
        {
            "id": 10,
            "letter": "خ",
            "name": "Khay",
            "english": "Kh",
            "sound": "kha",
            "words": [
                {"word": "خرگوش", "meaning": "Rabbit", "english": "Khargosh"},
                {"word": "خوشی", "meaning": "Happiness", "english": "Khushi"},
                {"word": "خواب", "meaning": "Dream", "english": "Khwab"}
            ],
            "color": "#98FB98"
        },
        {
            "id": 11,
            "letter": "د",
            "name": "Daal",
            "english": "D",
            "sound": "da",
            "words": [
                {"word": "دودھ", "meaning": "Milk", "english": "Doodh"},
                {"word": "درخت", "meaning": "Tree", "english": "Darakht"},
                {"word": "دل", "meaning": "Heart", "english": "Dil"}
            ],
            "color": "#FF8C94"
        },
        {
            "id": 12,
            "letter": "ڈ",
            "name": "Ddaal",
            "english": "Dd",
            "sound": "dda",
            "words": [
                {"word": "ڈبہ", "meaning": "Box", "english": "Dabba"},
                {"word": "ڈاکٹر", "meaning": "Doctor", "english": "Doctor"}
            ],
            "color": "#A8E6CF"
        },
        {
            "id": 13,
            "letter": "ذ",
            "name": "Zaal",
            "english": "Z",
            "sound": "za",
            "words": [
                {"word": "ذہن", "meaning": "Mind", "english": "Zehan"},
                {"word": "ذخم", "meaning": "Wound", "english": "Zakham"}
            ],
            "color": "#FFD3A5"
        },
        {
            "id": 14,
            "letter": "ر",
            "name": "Ray",
            "english": "R",
            "sound": "ra",
            "words": [
                {"word": "روٹی", "meaning": "Bread", "english": "Roti"},
                {"word": "رنگ", "meaning": "Color", "english": "Rang"},
                {"word": "راجا", "meaning": "King", "english": "Raja"}
            ],
            "color": "#B8A9C9"
        },
        {
            "id": 15,
            "letter": "ڑ",
            "name": "Rray",
            "english": "Rr",
            "sound": "rra",
            "words": [
                {"word": "کڑک", "meaning": "Thunder", "english": "Karak"},
                {"word": "پڑھنا", "meaning": "To Read", "english": "Parhna"}
            ],
            "color": "#C7CEEA"
        },
        {
            "id": 16,
            "letter": "ز",
            "name": "Zay",
            "english": "Z",
            "sound": "za",
            "words": [
                {"word": "زرافہ", "meaning": "Giraffe", "english": "Zarafa"},
                {"word": "زمین", "meaning": "Earth", "english": "Zameen"},
                {"word": "زندگی", "meaning": "Life", "english": "Zindagi"}
            ],
            "color": "#F38BA8"
        },
        {
            "id": 17,
            "letter": "ژ",
            "name": "Zhay",
            "english": "Zh",
            "sound": "zha",
            "words": [
                {"word": "ژالہ", "meaning": "Dew", "english": "Zhala"}
            ],
            "color": "#FAB795"
        },
        {
            "id": 18,
            "letter": "س",
            "name": "Seen",
            "english": "S",
            "sound": "sa",
            "words": [
                {"word": "سورج", "meaning": "Sun", "english": "Suraj"},
                {"word": "سیب", "meaning": "Apple", "english": "Seb"},
                {"word": "سمندر", "meaning": "Ocean", "english": "Samundar"}
            ],
            "color": "#79C99E"
        },
        {
            "id": 19,
            "letter": "ش",
            "name": "Sheen",
            "english": "Sh",
            "sound": "sha",
            "words": [
                {"word": "شیر", "meaning": "Lion", "english": "Sher"},
                {"word": "شہد", "meaning": "Honey", "english": "Shahad"},
                {"word": "شہر", "meaning": "City", "english": "Shehar"}
            ],
            "color": "#A8DADC"
        },
        {
            "id": 20,
            "letter": "ص",
            "name": "Swaad",
            "english": "S",
            "sound": "sa",
            "words": [
                {"word": "صابن", "meaning": "Soap", "english": "Sabun"},
                {"word": "صفر", "meaning": "Zero", "english": "Sifar"}
            ],
            "color": "#F1C0E8"
        },
        {
            "id": 21,
            "letter": "ض",
            "name": "Zwaad",
            "english": "Z",
            "sound": "za",
            "words": [
                {"word": "ضرور", "meaning": "Surely", "english": "Zaroor"}
            ],
            "color": "#CFBAF0"
        },
        {
            "id": 22,
            "letter": "ط",
            "name": "Toay",
            "english": "T",
            "sound": "ta",
            "words": [
                {"word": "طوطا", "meaning": "Parrot", "english": "Tota"},
                {"word": "طالب", "meaning": "Student", "english": "Talib"}
            ],
            "color": "#A3C4F3"
        },
        {
            "id": 23,
            "letter": "ظ",
            "name": "Zoay",
            "english": "Z",
            "sound": "za",
            "words": [
                {"word": "ظہر", "meaning": "Noon", "english": "Zuhar"}
            ],
            "color": "#90DBF4"
        },
        {
            "id": 24,
            "letter": "ع",
            "name": "Ain",
            "english": "A",
            "sound": "aa",
            "words": [
                {"word": "عقل", "meaning": "Wisdom", "english": "Aql"},
                {"word": "عید", "meaning": "Festival", "english": "Eid"}
            ],
            "color": "#8EECF5"
        },
        {
            "id": 25,
            "letter": "غ",
            "name": "Ghain",
            "english": "Gh",
            "sound": "gha",
            "words": [
                {"word": "غذا", "meaning": "Food", "english": "Ghaza"},
                {"word": "غم", "meaning": "Sadness", "english": "Gham"}
            ],
            "color": "#98F5E1"
        },
        {
            "id": 26,
            "letter": "ف",
            "name": "Fay",
            "english": "F",
            "sound": "fa",
            "words": [
                {"word": "فیل", "meaning": "Elephant", "english": "Feel"},
                {"word": "فول", "meaning": "Beans", "english": "Phool"},
                {"word": "فرشتہ", "meaning": "Angel", "english": "Farishta"}
            ],
            "color": "#B9FBC0"
        },
        {
            "id": 27,
            "letter": "ق",
            "name": "Qaaf",
            "english": "Q",
            "sound": "qa",
            "words": [
                {"word": "قلم", "meaning": "Pen", "english": "Qalam"},
                {"word": "قرآن", "meaning": "Quran", "english": "Quran"}
            ],
            "color": "#FDE68A"
        },
        {
            "id": 28,
            "letter": "ک",
            "name": "Kaaf",
            "english": "K",
            "sound": "ka",
            "words": [
                {"word": "کتاب", "meaning": "Book", "english": "Kitab"},
                {"word": "کیلا", "meaning": "Banana", "english": "Kela"},
                {"word": "کبوتر", "meaning": "Pigeon", "english": "Kabootar"}
            ],
            "color": "#FED7AA"
        },
        {
            "id": 29,
            "letter": "گ",
            "name": "Gaaf",
            "english": "G",
            "sound": "ga",
            "words": [
                {"word": "گل", "meaning": "Flower", "english": "Gul"},
                {"word": "گھر", "meaning": "House", "english": "Ghar"},
                {"word": "گائے", "meaning": "Cow", "english": "Gaye"}
            ],
            "color": "#FECACA"
        },
        {
            "id": 30,
            "letter": "ل",
            "name": "Laam",
            "english": "L",
            "sound": "la",
            "words": [
                {"word": "لڑکا", "meaning": "Boy", "english": "Larka"},
                {"word": "لہر", "meaning": "Wave", "english": "Lehar"},
                {"word": "لیموں", "meaning": "Lemon", "english": "Lemon"}
            ],
            "color": "#F3E8FF"
        },
        {
            "id": 31,
            "letter": "م",
            "name": "Meem",
            "english": "M",
            "sound": "ma",
            "words": [
                {"word": "ماں", "meaning": "Mother", "english": "Maa"},
                {"word": "مکھی", "meaning": "Fly", "english": "Makhi"},
                {"word": "مچھلی", "meaning": "Fish", "english": "Machli"}
            ],
            "color": "#E0E7FF"
        },
        {
            "id": 32,
            "letter": "ن",
            "name": "Noon",
            "english": "N",
            "sound": "na",
            "words": [
                {"word": "ناک", "meaning": "Nose", "english": "Naak"},
                {"word": "نیند", "meaning": "Sleep", "english": "Neend"},
                {"word": "نیلا", "meaning": "Blue", "english": "Neela"}
            ],
            "color": "#C7D2FE"
        },
        {
            "id": 33,
            "letter": "ں",
            "name": "Noon Ghunna",
            "english": "N",
            "sound": "n",
            "words": [
                {"word": "پیں", "meaning": "Drink", "english": "Piye"},
                {"word": "میں", "meaning": "I/In", "english": "Main"}
            ],
            "color": "#A5B4FC"
        },
        {
            "id": 34,
            "letter": "و",
            "name": "Waao",
            "english": "W/V/O/U",
            "sound": "wa",
            "words": [
                {"word": "والدین", "meaning": "Parents", "english": "Walidain"},
                {"word": "ولی", "meaning": "Saint", "english": "Wali"},
                {"word": "وقت", "meaning": "Time", "english": "Waqt"}
            ],
            "color": "#8B5CF6"
        },
        {
            "id": 35,
            "letter": "ہ",
            "name": "Hay",
            "english": "H",
            "sound": "ha",
            "words": [
                {"word": "ہاتھ", "meaning": "Hand", "english": "Haath"},
                {"word": "ہنسنا", "meaning": "To Laugh", "english": "Hansna"},
                {"word": "ہوا", "meaning": "Air", "english": "Hawa"}
            ],
            "color": "#A855F7"
        },
        {
            "id": 36,
            "letter": "ھ",
            "name": "Hay Dokhashmay",
            "english": "H",
            "sound": "h",
            "words": [
                {"word": "بھائی", "meaning": "Brother", "english": "Bhai"},
                {"word": "گھوڑا", "meaning": "Horse", "english": "Ghora"}
            ],
            "color": "#9333EA"
        },
        {
            "id": 37,
            "letter": "ء",
            "name": "Hamza",
            "english": "'",
            "sound": "",
            "words": [
                {"word": "آء", "meaning": "Come", "english": "Aa"},
                {"word": "ماء", "meaning": "Water", "english": "Maa"}
            ],
            "color": "#7C3AED"
        },
        {
            "id": 38,
            "letter": "ی",
            "name": "Yay",
            "english": "Y/I/E",
            "sound": "ya",
            "words": [
                {"word": "یہ", "meaning": "This", "english": "Yeh"},
                {"word": "یار", "meaning": "Friend", "english": "Yaar"},
                {"word": "یاد", "meaning": "Memory", "english": "Yaad"}
            ],
            "color": "#6366F1"
        }
    ]
}

# ===== GAMES AND ACTIVITIES =====
GAMES_DATA = {
    "letter_matching": {
        "name": "Letter Matching",
        "description": "Match Urdu letters with their names!",
        "emoji": "🎯"
    },
    "word_building": {
        "name": "Word Building",
        "description": "Build words using Urdu letters!",
        "emoji": "🔤"
    },
    "tracing": {
        "name": "Letter Tracing",
        "description": "Practice writing Urdu letters!",
        "emoji": "✍️"
    },
    "sound_game": {
        "name": "Sound Game",
        "description": "Listen and identify letter sounds!",
        "emoji": "🔊"
    }
}

# ===== PROGRESS TRACKER CLASS =====
class UrduProgressTracker:
    def __init__(self):
        self.user_progress = self._get_default_progress()
        self.badges = self._initialize_badges()
    
    def _get_default_progress(self):
        return {
            "user_name": "",
            "learned_letters": [],
            "completed_games": [],
            "total_stars": 0,
            "current_streak": 0,
            "badges": [],
            "last_active": "",
            "favorite_letters": []
        }
    
    def _initialize_badges(self):
        return {
            "first_letter": {
                "name": "First Letter",
                "description": "Learned your first Urdu letter!",
                "emoji": "🌟",
                "condition": lambda progress: len(progress['learned_letters']) >= 1
            },
            "five_letters": {
                "name": "Letter Explorer",
                "description": "Learned 5 Urdu letters!",
                "emoji": "🎓",
                "condition": lambda progress: len(progress['learned_letters']) >= 5
            },
            "ten_letters": {
                "name": "Alphabet Master",
                "description": "Learned 10 Urdu letters!",
                "emoji": "👑",
                "condition": lambda progress: len(progress['learned_letters']) >= 10
            },
            "game_player": {
                "name": "Game Player",
                "description": "Completed 3 games!",
                "emoji": "🎮",
                "condition": lambda progress: len(progress['completed_games']) >= 3
            },
            "star_collector": {
                "name": "Star Collector",
                "description": "Earned 15 stars!",
                "emoji": "⭐",
                "condition": lambda progress: progress['total_stars'] >= 15
            }
        }
    
    def set_user(self, name):
        self.user_progress['user_name'] = name
        self._update_last_active()
    
    def get_progress(self):
        return self.user_progress.copy()
    
    def learn_letter(self, letter_id):
        if letter_id not in self.user_progress['learned_letters']:
            self.user_progress['learned_letters'].append(letter_id)
            self.user_progress['total_stars'] += 2
            self._update_last_active()
            return True
        return False
    
    def complete_game(self, game_name):
        game_key = f"{game_name}_{datetime.now().strftime('%Y%m%d')}"
        if game_key not in self.user_progress['completed_games']:
            self.user_progress['completed_games'].append(game_key)
            self.user_progress['total_stars'] += 1
            self._update_last_active()
            return True
        return False
    
    def add_favorite_letter(self, letter_id):
        if letter_id not in self.user_progress['favorite_letters']:
            self.user_progress['favorite_letters'].append(letter_id)
    
    def _update_last_active(self):
        self.user_progress['last_active'] = datetime.now().isoformat()
    
    def check_badges(self):
        earned_badge_names = [badge['name'] for badge in self.user_progress['badges']]
        new_badges = []
        
        for badge_id, badge_info in self.badges.items():
            if badge_info['name'] not in earned_badge_names:
                if badge_info['condition'](self.user_progress):
                    new_badge = {
                        'id': badge_id,
                        'name': badge_info['name'],
                        'description': badge_info['description'],
                        'emoji': badge_info['emoji'],
                        'earned_at': datetime.now().strftime("%Y-%m-%d")
                    }
                    self.user_progress['badges'].append(new_badge)
                    new_badges.append(new_badge)
        
        return new_badges

# ===== STREAMLIT APPLICATION =====

# Configure page
st.set_page_config(
    page_title="🌙 Urdu Alphabet Adventure",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'progress_tracker' not in st.session_state:
    st.session_state.progress_tracker = UrduProgressTracker()
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"
if 'current_letter_id' not in st.session_state:
    st.session_state.current_letter_id = 1
if 'game_state' not in st.session_state:
    st.session_state.game_state = {}

# ===== HELPER FUNCTIONS =====

def get_letter_by_id(letter_id):
    """Get letter data by ID"""
    for letter in URDU_ALPHABET_DATA['letters']:
        if letter['id'] == letter_id:
            return letter
    return None

def create_letter_card(letter_data, is_learned=False):
    """Create a beautiful letter card"""
    status_emoji = "✅" if is_learned else "📚"
    
    card_html = f"""
    <div style="
        background: linear-gradient(135deg, {letter_data['color']}20, {letter_data['color']}40);
        border: 3px solid {letter_data['color']};
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        margin: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transform: scale(1);
        transition: transform 0.3s;
    ">
        <div style="font-size: 4em; margin-bottom: 10px;">{letter_data['letter']}</div>
        <div style="font-size: 1.5em; font-weight: bold; margin-bottom: 5px;">{letter_data['name']}</div>
        <div style="font-size: 1.2em; color: #666; margin-bottom: 10px;">"{letter_data['sound']}"</div>
        <div style="font-size: 1.5em;">{status_emoji}</div>
    </div>
    """
    return card_html

def show_home_page():
    """Display the home page"""
    st.title("🌙 اردو حروف تہجی")
    st.title("Urdu Alphabet Adventure")
    st.markdown("### سیکھیں اور مزہ کریں! (Learn and Have Fun!)")
    
    # User name input
    if not st.session_state.user_name:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("#### 👋 آپ کا نام کیا ہے؟ (What's your name?)")
            name = st.text_input("اپنا نام لکھیں (Enter your name):", placeholder="یہاں اپنا نام ٹائپ کریں...")
            if st.button("🌟 شروع کریں! (Start!)", type="primary"):
                if name:
                    st.session_state.user_name = name
                    st.session_state.progress_tracker.set_user(name)
                    st.rerun()
                else:
                    st.error("برائے کرم اپنا نام لکھیں! (Please enter your name!)")
    else:
        # Welcome message
        st.markdown(f"### 🎉 خوش آمدید {st.session_state.user_name}!")
        st.markdown(f"### Welcome back, {st.session_state.user_name}!")
        
        # Progress overview
        progress_data = st.session_state.progress_tracker.get_progress()
        total_letters = len(URDU_ALPHABET_DATA['letters'])
        learned_letters = len(progress_data.get('learned_letters', []))
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📚 حروف سیکھے (Letters Learned)", f"{learned_letters}/{total_letters}")
        with col2:
            st.metric("⭐ ستارے (Stars)", progress_data.get('total_stars', 0))
        with col3:
            st.metric("🏅 بیجز (Badges)", len(progress_data.get('badges', [])))
        with col4:
            completion_rate = (learned_letters / total_letters * 100) if total_letters > 0 else 0
            st.metric("📈 پیش قدمی (Progress)", f"{completion_rate:.0f}%")
        
        # Progress bar
        st.progress(completion_rate / 100)
        
        # Quick navigation
        st.markdown("---")
        st.markdown("### 🎯 آج کیا کرنا چاہتے ہیں؟ (What do you want to do today?)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### 📖 حروف سیکھیں
            #### Learn Letters
            اردو کے حروف سیکھیں!
            """)
            if st.button("حروف دیکھیں 📚 (View Letters)", key="letters_btn", type="primary"):
                st.session_state.current_page = "letters"
                st.rerun()
        
        with col2:
            st.markdown("""
            #### 🎮 کھیل کھیلیں
            #### Play Games
            مزہ کے ساتھ سیکھیں!
            """)
            if st.button("کھیل کھیلیں 🎯 (Play Games)", key="games_btn", type="primary"):
                st.session_state.current_page = "games"
                st.rerun()
        
        with col3:
            st.markdown("""
            #### 🏆 پیش قدمی دیکھیں
            #### View Progress
            اپنی کامیابیاں دیکھیں!
            """)
            if st.button("پیش قدمی 📊 (Progress)", key="progress_btn", type="primary"):
                st.session_state.current_page = "progress"
                st.rerun()

def show_letters_page():
    """Display the letters learning page"""
    st.title("📚 اردو حروف تہجی (Urdu Alphabet)")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🏠 گھر (Home)"):
            st.session_state.current_page = "home"
            st.rerun()
    
    progress_data = st.session_state.progress_tracker.get_progress()
    learned_letters = progress_data.get('learned_letters', [])
    
    # Letter grid
    st.markdown("### حروف کا انتخاب کریں (Choose a letter to learn):")
    
    # Display letters in rows of 5
    letters = URDU_ALPHABET_DATA['letters']
    for i in range(0, len(letters), 5):
        cols = st.columns(5)
        for j, letter in enumerate(letters[i:i+5]):
            if j < len(cols):
                with cols[j]:
                    is_learned = letter['id'] in learned_letters
                    st.markdown(create_letter_card(letter, is_learned), unsafe_allow_html=True)
                    
                    if st.button(f"سیکھیں (Learn)", key=f"learn_{letter['id']}"):
                        st.session_state.current_letter_id = letter['id']
                        st.session_state.current_page = "letter_detail"
                        st.rerun()

def show_letter_detail_page():
    """Show detailed view of a single letter"""
    letter_data = get_letter_by_id(st.session_state.current_letter_id)
    if not letter_data:
        st.error("Letter not found!")
        return
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← واپس (Back)"):
            st.session_state.current_page = "letters"
            st.rerun()
    
    # Letter display
    st.markdown(f"""
    <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, {letter_data['color']}20, {letter_data['color']}40); border-radius: 20px; margin: 20px 0;">
        <div style="font-size: 8em; margin-bottom: 20px;">{letter_data['letter']}</div>
        <div style="font-size: 3em; font-weight: bold; margin-bottom: 10px;">{letter_data['name']}</div>
        <div style="font-size: 2em; color: #666;">Sound: "{letter_data['sound']}"</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Words with this letter
    st.markdown("### اس حرف سے بننے والے الفاظ (Words starting with this letter):")
    
    for word_data in letter_data['words']:
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.markdown(f"""
            <div style="font-size: 2em; text-align: center; padding: 15px; background: #f0f0f0; border-radius: 10px; margin: 5px;">
                {word_data['word']}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="font-size: 1.5em; text-align: center; padding: 15px; margin: 5px;">
                <strong>{word_data['meaning']}</strong><br>
                <em>({word_data['english']})</em>
            </div>
            """)
        
        with col3:
            if st.button("🔊", key=f"sound_{word_data['word']}", help="Play sound (coming soon!)"):
                st.info(f"Sound: {word_data['english']}")
    
    # Mark as learned
    progress_data = st.session_state.progress_tracker.get_progress()
    if st.session_state.current_letter_id not in progress_data.get('learned_letters', []):
        st.markdown("---")
        if st.button("✅ میں نے یہ حرف سیکھ لیا! (I learned this letter!)", type="primary"):
            st.session_state.progress_tracker.learn_letter(st.session_state.current_letter_id)
            st.success("🎉 بہترین! آپ نے ایک نیا حرف سیکھا! (Excellent! You learned a new letter!)")
            st.balloons()
            
            # Check for badges
            badges = st.session_state.progress_tracker.check_badges()
            for badge in badges:
                st.success(f"🏅 نیا بیج ملا: {badge['name']} - {badge['description']}")
            
            time.sleep(2)
            st.rerun()
    else:
        st.success("✅ آپ نے یہ حرف سیکھ لیا ہے! (You have learned this letter!)")
    
    # Add to favorites
    if st.button("❤️ پسندیدہ میں شامل کریں (Add to Favorites)"):
        st.session_state.progress_tracker.add_favorite_letter(st.session_state.current_letter_id)
        st.success("❤️ پسندیدہ میں شامل ہو گیا! (Added to favorites!)")

def show_games_page():
    """Display the games page"""
    st.title("🎮 کھیل اور سرگرمیاں (Games & Activities)")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🏠 گھر (Home)"):
            st.session_state.current_page = "home"
            st.rerun()
    
    st.markdown("### کھیل کا انتخاب کریں (Choose a game):")
    
    # Letter Matching Game
    with st.expander("🎯 حروف ملانا (Letter Matching Game)", expanded=True):
        st.markdown("حروف کو ان کے ناموں سے ملائیں! (Match letters with their names!)")
        
        # Simple matching game
        if 'matching_game' not in st.session_state.game_state:
            # Select 4 random letters for the game
            letters = random.sample(URDU_ALPHABET_DATA['letters'], 4)
            st.session_state.game_state['matching_game'] = {
                'letters': letters,
                'score': 0,
                'attempts': 0
            }
        
        game_data = st.session_state.game_state['matching_game']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### حروف (Letters):")
            selected_letter = st.selectbox(
                "حرف منتخب کریں:",
                options=[letter['letter'] for letter in game_data['letters']],
                key="selected_letter"
            )
        
        with col2:
            st.markdown("#### نام (Names):")
            selected_name = st.selectbox(
                "نام منتخب کریں:",
                options=[letter['name'] for letter in game_data['letters']],
                key="selected_name"
            )
        
        if st.button("جانچیں! (Check!)", type="primary"):
            # Find the correct letter for the selected name
            correct_letter = None
            for letter in game_data['letters']:
                if letter['name'] == selected_name:
                    correct_letter = letter['letter']
                    break
            
            game_data['attempts'] += 1
            
            if selected_letter == correct_letter:
                game_data['score'] += 1
                st.success(f"🎉 صحیح! (Correct!) {selected_letter} = {selected_name}")
                st.balloons()
                
                if game_data['score'] == len(game_data['letters']):
                    st.session_state.progress_tracker.complete_game("letter_matching")
                    st.success("🏆 تمام حروف صحیح! آپ نے کھیل جیت لیا! (All correct! You won the game!)")
            else:
                st.error(f"❌ غلط! دوبارہ کوشش کریں (Wrong! Try again)")
            
            st.info(f"Score: {game_data['score']}/{len(game_data['letters'])}")
        
        if st.button("نیا کھیل (New Game)"):
            del st.session_state.game_state['matching_game']
            st.rerun()
    
    # Word Building Game
    with st.expander("🔤 الفاظ بنانا (Word Building Game)"):
        st.markdown("حروف استعمال کر کے الفاظ بنائیں! (Build words using letters!)")
        
        # Simple word building with common words
        common_words = [
            {"word": "آم", "letters": ["ا", "م"], "meaning": "Mango"},
            {"word": "بلی", "letters": ["ب", "ل", "ی"], "meaning": "Cat"},
            {"word": "چاند", "letters": ["چ", "ا", "ن", "د"], "meaning": "Moon"}
        ]
        
        selected_word = st.selectbox(
            "کون سا لفظ بنانا ہے؟ (Which word to build?):",
            options=[f"{word['word']} ({word['meaning']})" for word in common_words]
        )
        
        # Get the selected word data
        word_index = [f"{word['word']} ({word['meaning']})" for word in common_words].index(selected_word)
        target_word = common_words[word_index]
        
        st.markdown(f"#### یہ لفظ بنائیں: **{target_word['word']}** ({target_word['meaning']})")
        
        # Show required letters in scrambled order
        scrambled_letters = target_word['letters'].copy()
        random.shuffle(scrambled_letters)
        
        st.markdown("#### دستیاب حروف (Available Letters):")
        st.markdown(" | ".join([f"**{letter}**" for letter in scrambled_letters]))
        
        user_word = st.text_input("اپنا لفظ یہاں لکھیں (Write your word here):")
        
        if st.button("جانچیں! (Check Word!)", type="primary"):
            if user_word.strip() == target_word['word']:
                st.success("🎉 بہترین! آپ نے صحیح لفظ بنایا! (Excellent! You built the correct word!)")
                st.balloons()
                st.session_state.progress_tracker.complete_game("word_building")
            else:
                st.error("❌ دوبارہ کوشش کریں (Try again)")
                st.info(f"صحیح لفظ: {target_word['word']}")

def show_progress_page():
    """Display the progress page"""
    st.title("🏆 آپ کی پیش قدمی (Your Progress)")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🏠 گھر (Home)"):
            st.session_state.current_page = "home"
            st.rerun()
    
    progress_data = st.session_state.progress_tracker.get_progress()
    
    if not progress_data.get('user_name'):
        st.warning("آپ نے ابھی سیکھنا شروع نہیں کیا! (You haven't started learning yet!)")
        return
    
    st.markdown(f"### خوش آمدید {progress_data['user_name']}! 👋")
    
    # Statistics
    total_letters = len(URDU_ALPHABET_DATA['letters'])
    learned_letters = len(progress_data.get('learned_letters', []))
    total_stars = progress_data.get('total_stars', 0)
    badges = progress_data.get('badges', [])
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        completion_rate = (learned_letters / total_letters * 100) if total_letters > 0 else 0
        st.metric(
            label="📚 حروف سیکھے (Letters)",
            value=f"{learned_letters}/{total_letters}",
            delta=f"{completion_rate:.1f}%"
        )
    
    with col2:
        st.metric(
            label="⭐ ستارے (Stars)",
            value=total_stars,
            delta="بہترین!"
        )
    
    with col3:
        st.metric(
            label="🏅 بیجز (Badges)",
            value=len(badges),
            delta="مزید جیتیں!"
        )
    
    with col4:
        completed_games = len([g for g in progress_data.get('completed_games', []) if g])
        st.metric(
            label="🎮 کھیل (Games)",
            value=completed_games,
            delta="اور کھیلیں!"
        )
    
    # Progress visualization
    if learned_letters > 0:
        st.markdown("---")
        st.markdown("### 📊 آپ کی پیش قدمی کا چارٹ (Progress Chart)")
        
        # Create a simple progress chart
        letters_data = []
        for letter in URDU_ALPHABET_DATA['letters']:
            letters_data.append({
                'Letter': letter['letter'],
                'Name': letter['name'],
                'Status': 'سیکھا گیا' if letter['id'] in progress_data['learned_letters'] else 'باقی'
            })
        
        df = pd.DataFrame(letters_data)
        
        fig = px.bar(
            df, 
            x='Letter', 
            color='Status',
            title='حروف کی پیش قدمی (Letter Progress)',
            color_discrete_map={'سیکھا گیا': '#4CAF50', 'باقی': '#FFC107'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Badges section
    if badges:
        st.markdown("---")
        st.markdown("### 🏅 آپ کے بیجز (Your Badges)")
        
        badge_cols = st.columns(min(len(badges), 4))
        for i, badge in enumerate(badges):
            with badge_cols[i % 4]:
                st.markdown(f"""
                <div style="text-align: center; padding: 20px; border: 2px solid #FFD700; border-radius: 10px; margin: 10px;">
                    <div style="font-size: 3em;">{badge['emoji']}</div>
                    <div style="font-weight: bold; margin-top: 10px;">{badge['name']}</div>
                    <div style="font-size: 0.9em; color: #666;">{badge['description']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Favorite letters
    favorite_letters = progress_data.get('favorite_letters', [])
    if favorite_letters:
        st.markdown("---")
        st.markdown("### ❤️ پسندیدہ حروف (Favorite Letters)")
        
        fav_cols = st.columns(min(len(favorite_letters), 5))
        for i, letter_id in enumerate(favorite_letters):
            letter_data = get_letter_by_id(letter_id)
            if letter_data:
                with fav_cols[i % 5]:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 15px; background: {letter_data['color']}40; border-radius: 10px; margin: 5px;">
                        <div style="font-size: 2em;">{letter_data['letter']}</div>
                        <div style="font-weight: bold;">{letter_data['name']}</div>
                    </div>
                    """, unsafe_allow_html=True)

# ===== MAIN APPLICATION =====

def main():
    """Main application logic"""
    # Custom CSS for better Urdu text rendering
    st.markdown("""
    <style>
    .urdu-text {
        font-family: 'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', Arial, sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .stSelectbox label {
        font-weight: bold;
    }
    
    .stButton button {
        border-radius: 20px;
        border: 2px solid #4CAF50;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    
    .stButton button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("🌙 رہنمائی (Navigation)")
    
    # Page navigation buttons
    if st.sidebar.button("🏠 گھر (Home)", key="nav_home"):
        st.session_state.current_page = "home"
        st.rerun()
    
    if st.sidebar.button("📚 حروف (Letters)", key="nav_letters"):
        st.session_state.current_page = "letters"
        st.rerun()
    
    if st.sidebar.button("🎮 کھیل (Games)", key="nav_games"):
        st.session_state.current_page = "games"
        st.rerun()
    
    if st.sidebar.button("🏆 پیش قدمی (Progress)", key="nav_progress"):
        st.session_state.current_page = "progress"
        st.rerun()
    
    # Fun facts in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🌟 کیا آپ جانتے ہیں؟")
    st.sidebar.markdown("### Did You Know?")
    
    fun_facts = [
        "اردو میں 38 حروف ہیں! (Urdu has 38 letters!)",
        "اردو دائیں سے بائیں لکھی جاتی ہے! (Urdu is written right to left!)",
        "اردو دنیا کی خوبصورت زبان ہے! (Urdu is the world's beautiful language!)",
        "اردو شاعری بہت مشہور ہے! (Urdu poetry is very famous!)"
    ]
    
    st.sidebar.info(random.choice(fun_facts))
    
    # Display current page
    if st.session_state.current_page == "home":
        show_home_page()
    elif st.session_state.current_page == "letters":
        show_letters_page()
    elif st.session_state.current_page == "letter_detail":
        show_letter_detail_page()
    elif st.session_state.current_page == "games":
        show_games_page()
    elif st.session_state.current_page == "progress":
        show_progress_page()

if __name__ == "__main__":
    main()