"""
Claire's Wordle Bot - Vercel Webhook Handler
Serverless function for Telegram webhook updates
"""

import os
import json
import random
import hashlib
import requests
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler

# ============ CONFIG ============
BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# For serverless, we use in-memory (resets between invocations)
# In production, use KV store like Upstash Redis
USER_DATA = {}

# ============ WORD LISTS ============
DAILY_WORDS = [
    "crane", "slate", "trace", "crate", "stare", "share", "spare", "scare",
    "flame", "blame", "claim", "drain", "train", "grain", "brain", "plain",
    "shine", "spine", "swine", "twine", "whine", "stone", "phone", "clone",
    "grace", "space", "place", "brace", "pride", "bride", "glide",
    "globe", "probe", "grove", "stove", "drove", "prove", "above", "shove",
    "bread", "dread", "tread", "steam", "dream", "cream", "gleam",
    "pearl", "swear", "spear", "clear", "smear", "heart", "start", "chart",
    "plant", "grant", "slant", "chant", "giant", "paint", "faint", "saint",
    "house", "mouse", "cloud", "proud", "crowd",
    "beach", "peach", "reach", "teach", "bench", "wrench",
    "light", "night", "might", "right", "sight", "tight", "fight",
    "sleep", "sweep", "steep", "creep", "sheep", "speed", "bleed", "greed",
    "smile", "while", "style", "taste", "waste", "haste",
    "peace", "lease", "cease", "tease", "dance", "lance", "chance",
    "world", "sword", "hoard", "board", "chord", "storm", "sworn", "scorn",
    "music", "magic", "logic", "topic", "comic", "sonic", "tonic", "panic",
    "happy", "peppy", "jumpy", "bumpy", "lumpy", "crisp", "grasp", "clasp",
    "fresh", "flesh", "crash", "trash", "brash", "flash", "clash", "slash",
    "think", "drink", "brink", "stink", "blink", "clink", "slink",
    "angel", "anger", "eager", "legal", "regal", "metal", "pedal", "medal",
    "river", "liver", "giver", "diver",
    "power", "tower", "lower", "mower", "shower", "flower", "cower",
    "lemon", "melon", "felon", "talon", "salon", "baron", "wagon",
    "tiger", "rider", "cider", "wider",
    "queen", "green", "sheen", "scene",
    "jolly", "folly", "holly", "molly", "dolly",
    "zebra", "extra", "ultra",
    "piano",
    "yacht", "catch", "match", "patch", "batch", "latch", "hatch", "watch",
    "prize", "seize", "froze", "blaze", "craze", "glaze", "graze", "amaze"
]

VALID_WORDS = set(DAILY_WORDS + [
    "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult",
    "after", "again", "agent", "agree", "ahead", "alarm", "album", "alert",
    "alien", "align", "alike", "alive", "allow", "alone", "along", "alter",
    "among", "angel", "anger", "angle", "angry", "apart", "apple", "apply",
    "arena", "argue", "arise", "array", "arrow", "asset", "avoid", "award",
    "aware", "awful", "bacon", "badge", "badly", "basic", "basin", "basis",
    "beach", "beard", "beast", "began", "begin", "begun", "being", "belly",
    "below", "bench", "berry", "birth", "black", "blade", "blame", "blank",
    "blast", "blaze", "bleed", "blend", "bless", "blind", "block", "blood",
    "blown", "blues", "blunt", "board", "boast", "bonus", "boost", "booth",
    "bound", "brain", "brake", "brand", "brass", "brave", "bread", "break",
    "breed", "brick", "bride", "brief", "bring", "broad", "broke", "brook",
    "brown", "brush", "build", "built", "bunch", "burst", "buyer", "cabin",
    "cable", "camel", "candy", "carry", "catch", "cause", "cease", "chain",
    "chair", "chalk", "champ", "chaos", "charm", "chart", "chase", "cheap",
    "check", "cheek", "cheer", "chess", "chest", "chief", "child", "china",
    "chose", "chunk", "civic", "civil", "claim", "clash", "class", "clean",
    "clear", "clerk", "click", "cliff", "climb", "cling", "clock", "close",
    "cloth", "cloud", "coach", "coast", "colon", "color", "couch", "cough",
    "could", "count", "court", "cover", "crack", "craft", "crane", "crash",
    "crawl", "crazy", "cream", "creek", "crime", "crisp", "cross", "crowd",
    "crown", "crude", "cruel", "crush", "curve", "cycle", "daily", "dairy",
    "dance", "dealt", "death", "debut", "delay", "dense", "depth", "devil",
    "diary", "dirty", "disco", "doubt", "dough", "dozen", "draft", "drain",
    "drama", "drank", "drawn", "dread", "dream", "dress", "dried", "drift",
    "drill", "drink", "drive", "drown", "drunk", "dying", "eager",
    "early", "earth", "eight", "elder", "elect", "elite", "email", "empty",
    "enemy", "enjoy", "enter", "entry", "equal", "equip", "error", "essay",
    "event", "every", "exact", "excel", "exist", "extra", "faint", "fairy",
    "faith", "false", "fancy", "fatal", "fault", "favor", "feast", "fence",
    "ferry", "fever", "fiber", "field", "fiery", "fifth", "fifty", "fight",
    "final", "fired", "first", "fixed", "flame", "flash", "flask", "flesh",
    "float", "flock", "flood", "floor", "flour", "fluid", "flung", "flush",
    "flyer", "focal", "focus", "force", "forge", "forth", "forty", "forum",
    "found", "frame", "frank", "fraud", "fresh", "fried", "front", "frost",
    "fruit", "fully", "funny", "ghost", "giant", "given", "glass", "globe",
    "glory", "glove", "going", "grace", "grade", "grain", "grand", "grant",
    "grape", "graph", "grasp", "grass", "grave", "great", "green", "greet",
    "grief", "grill", "grind", "groan", "gross", "group", "grove", "grown",
    "guard", "guess", "guest", "guide", "guild", "guilt", "habit", "happy",
    "harsh", "haste", "hasty", "hatch", "haven", "heard", "heart", "heavy",
    "hedge", "hello", "hence", "hinge", "hobby", "honor", "horse", "hotel",
    "house", "human", "humid", "humor", "hurry", "ideal", "image", "imply",
    "index", "inner", "input", "issue", "ivory",
    "jelly", "jewel", "joint", "joker", "jolly", "judge", "juice", "juicy",
    "jumbo", "jumpy", "known", "label", "labor", "lance", "large", "laser",
    "later", "laugh", "layer", "learn", "lease", "least", "leave", "legal",
    "lemon", "level", "lever", "light", "limit", "linen", "liver", "lobby",
    "local", "lodge", "logic", "loose", "lorry", "loser", "lotus",
    "lover", "lower", "loyal", "lucky", "lunch", "lying", "lyric", "magic",
    "major", "maker", "manor", "maple", "march", "marry",
    "marsh", "mason", "match", "maybe", "mayor", "meant", "media", "melon",
    "mercy", "merge", "merit", "merry", "metal", "meter", "midst", "might",
    "minor", "minus", "mirth", "mixed", "model", "modem", "money", "month",
    "moral", "motor", "mount", "mouse", "mouth", "moved", "mover", "movie",
    "music", "naive", "named", "nasty", "naval", "needs", "nerve", "never",
    "newer", "newly", "night", "ninth", "noble", "noise", "noisy", "north",
    "notch", "noted", "novel", "nurse", "nylon", "occur", "ocean", "offer",
    "often", "olive", "onion", "opera", "orbit", "order", "organ", "other",
    "ought", "outer", "owned", "owner", "oxide", "ozone", "paint",
    "panel", "panic", "paper", "party", "pasta", "paste", "patch", "pause",
    "peace", "peach", "pearl", "penny", "perch", "peril", "petal", "petty",
    "phase", "phone", "photo", "piano", "piece", "pilot", "pinch", "pitch",
    "pizza", "place", "plain", "plane", "plant", "plate", "plaza", "plead",
    "point", "polar", "porch", "posed", "poser", "pound", "power", "press",
    "price", "pride", "prime", "print", "prior", "prize", "probe", "prone",
    "proof", "proud", "prove", "proxy", "pulse", "punch", "pupil", "purse",
    "queen", "query", "quest", "queue", "quick", "quiet", "quilt", "quite",
    "quota", "quote", "radar", "radio", "raise", "rally", "ranch", "range",
    "rapid", "ratio", "reach", "react", "ready", "realm", "rebel", "refer",
    "relax", "relay", "relic", "reply", "reset", "resin", "rider", "ridge",
    "rifle", "right", "rigid", "rigor", "rinse", "ripen", "risen", "risky",
    "rival", "river", "robot", "rocky", "roman", "roofs", "roots",
    "rough", "round", "route", "rover", "royal", "rugby", "ruler",
    "rural", "rusty", "sadly", "saint", "salad", "sales", "salon", "sandy",
    "sauce", "saved", "scale", "scare", "scene", "scent", "scope", "score",
    "scout", "scrap", "screw", "seize", "sense", "serum", "serve", "setup",
    "seven", "shade", "shaft", "shake", "shall", "shame", "shape", "share",
    "shark", "sharp", "sheep", "sheer", "sheet", "shelf", "shell", "shift",
    "shine", "shirt", "shock", "shoot", "shore", "short", "shout", "shown",
    "shrug", "sight", "silly", "since", "sixth", "sixty", "sized",
    "skill", "skirt", "skull", "slate", "slave", "sleep", "slice", "slide",
    "slope", "small", "smart", "smell", "smile", "smoke", "snake", "snare",
    "sneak", "solar", "solid", "solve", "sonic", "sorry", "sound", "south",
    "space", "spare", "spark", "spawn", "speak", "speed", "spell", "spend",
    "spent", "spice", "spicy", "spine", "split", "spoke", "spoon", "sport",
    "spray", "spree", "squad", "stack", "staff", "stage", "stain", "stake",
    "stale", "stamp", "stand", "stare", "stark", "start", "state", "stays",
    "steak", "steal", "steam", "steel", "steep", "steer", "stern", "stick",
    "stiff", "still", "sting", "stock", "stomp", "stone", "stood", "stool",
    "store", "storm", "story", "stout", "stove", "strap", "straw", "stray",
    "strip", "stuck", "study", "stuff", "stump", "style", "sugar", "suite",
    "sunny", "super", "surge", "sweet", "swift", "swing", "swiss", "sword",
    "swore", "sworn", "table", "tacit", "taken", "tasty", "teach", "teeth",
    "tempt", "tenor", "tense", "tenth", "terms", "thank", "theft", "their",
    "theme", "there", "these", "thick", "thief", "thing", "think", "third",
    "thorn", "those", "three", "threw", "throw", "thumb", "tiger", "tight",
    "timer", "tired", "title", "today", "token", "tonne", "tooth", "topic",
    "torch", "total", "touch", "tough", "tower", "toxic", "trace", "track",
    "trade", "trail", "train", "trait", "trash", "treat", "trend", "trial",
    "tribe", "trick", "tried", "troop", "truck", "truly", "trump", "trunk",
    "trust", "truth", "twice", "twins", "twist", "tying", "ultra", "uncle",
    "under", "unify", "union", "unite", "unity", "until", "upper", "upset",
    "urban", "urged", "usage", "usual", "utter", "vague", "valid", "value",
    "valve", "vault", "venue", "verse", "video", "views", "villa", "viral",
    "virus", "visit", "vital", "vivid", "vocal", "vodka", "voice", "voter",
    "wagon", "waist", "waste", "watch", "water", "waved", "waves", "weary",
    "weave", "wedge", "weigh", "weird", "whale", "wheat", "wheel", "where",
    "which", "while", "white", "whole", "whose", "widen", "wider", "widow",
    "width", "wired", "witch", "woman", "women", "woods", "world", "worry",
    "worse", "worst", "worth", "would", "wound", "woven", "wrath", "wreck",
    "wrist", "write", "wrong", "wrote", "xenon", "yacht", "yearn", "years",
    "yeast", "yield", "young", "yours", "youth", "zebra", "zones"
])

# ============ TELEGRAM HELPERS ============
def send_message(chat_id, text, parse_mode="Markdown", reply_markup=None):
    """Send a message via Telegram API"""
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    
    requests.post(f"{TELEGRAM_API}/sendMessage", json=payload)

def answer_callback(callback_id, text=None):
    """Answer a callback query"""
    payload = {"callback_query_id": callback_id}
    if text:
        payload["text"] = text
    requests.post(f"{TELEGRAM_API}/answerCallbackQuery", json=payload)

def edit_message(chat_id, message_id, text, parse_mode="Markdown"):
    """Edit a message"""
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": parse_mode
    }
    requests.post(f"{TELEGRAM_API}/editMessageText", json=payload)

# ============ DATA PERSISTENCE (Vercel KV in production) ============
# For now using Upstash Redis via REST API
UPSTASH_URL = os.environ.get("UPSTASH_REST_URL")
UPSTASH_TOKEN = os.environ.get("UPSTASH_REST_TOKEN")

def redis_get(key):
    """Get data from Upstash Redis"""
    if not UPSTASH_URL or not UPSTASH_TOKEN:
        return USER_DATA.get(key)
    try:
        resp = requests.get(
            f"{UPSTASH_URL}/get/{key}",
            headers={"Authorization": f"Bearer {UPSTASH_TOKEN}"}
        )
        data = resp.json()
        if data.get("result"):
            return json.loads(data["result"])
    except:
        pass
    return None

def redis_set(key, value):
    """Set data in Upstash Redis"""
    if not UPSTASH_URL or not UPSTASH_TOKEN:
        USER_DATA[key] = value
        return
    try:
        requests.post(
            f"{UPSTASH_URL}/set/{key}",
            headers={"Authorization": f"Bearer {UPSTASH_TOKEN}"},
            data=json.dumps(value)
        )
    except:
        pass

def load_user_data(user_id):
    """Load user data from storage"""
    data = redis_get(f"user:{user_id}")
    if data:
        return data
    return {
        "user_id": user_id,
        "games_played": 0,
        "games_won": 0,
        "current_streak": 0,
        "max_streak": 0,
        "last_daily_date": None,
        "last_daily_won": False,
        "daily_guesses": [],
        "practice_guesses": [],
        "practice_word": None,
        "hint_cost_paid": False,
        "distribution": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0}
    }

def save_user_data(user_id, data):
    """Save user data to storage"""
    redis_set(f"user:{user_id}", data)

# ============ GAME LOGIC ============
def get_daily_word():
    """Get today's word - same for everyone, changes daily"""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    hash_val = int(hashlib.md5(today.encode()).hexdigest(), 16)
    return DAILY_WORDS[hash_val % len(DAILY_WORDS)]

def get_daily_number():
    """Get the puzzle number (days since start)"""
    start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    return (now - start).days

def check_guess(guess, target):
    """Return emoji feedback for a guess"""
    guess = guess.lower()
    target = target.lower()
    result = ["⬛"] * 5
    target_chars = list(target)
    
    # First pass: exact matches (green)
    for i in range(5):
        if guess[i] == target[i]:
            result[i] = "🟩"
            target_chars[i] = None
    
    # Second pass: wrong position (yellow)
    for i in range(5):
        if result[i] == "⬛" and guess[i] in target_chars:
            result[i] = "🟨"
            target_chars[target_chars.index(guess[i])] = None
    
    return "".join(result)

def is_valid_word(word):
    return len(word) == 5 and word.lower() in VALID_WORDS

def get_keyboard_status(guesses, target):
    """Show keyboard with letter status"""
    status = {}
    for guess in guesses:
        guess = guess.lower()
        for i, letter in enumerate(guess):
            if letter == target[i]:
                status[letter] = "🟩"
            elif letter in target and status.get(letter) != "🟩":
                status[letter] = "🟨"
            elif letter not in status:
                status[letter] = "⬛"
    
    rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    result = []
    for row in rows:
        line = ""
        for letter in row:
            if letter in status:
                line += f"{status[letter]}{letter.upper()} "
            else:
                line += f"⬜{letter.upper()} "
        result.append(line)
    return "\n".join(result)

# ============ HANDLERS ============
def handle_start(chat_id, user):
    first_name = user.get("first_name", "friend")
    data = load_user_data(user["id"])
    save_user_data(user["id"], data)
    
    send_message(chat_id,
        f"🎮 *Welcome to Claire's Wordle!*\n\n"
        f"Hey {first_name}! Ready to become addicted?\n\n"
        f"*How to play:*\n"
        f"• Guess the 5-letter word in 6 tries\n"
        f"• 🟩 = Right letter, right spot\n"
        f"• 🟨 = Right letter, wrong spot\n"
        f"• ⬛ = Letter not in word\n\n"
        f"*Commands:*\n"
        f"/play - Start today's daily puzzle\n"
        f"/practice - Unlimited practice games\n"
        f"/stats - Your statistics\n"
        f"/hint - Get a hint (costs 1 streak point!)\n\n"
        f"🔥 Don't break your streak!"
    )

def handle_play(chat_id, user):
    data = load_user_data(user["id"])
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    if data["last_daily_date"] == today:
        word = get_daily_word()
        if data["last_daily_won"]:
            send_message(chat_id,
                f"✅ You already solved today's puzzle!\n\n"
                f"The word was: *{word.upper()}*\n"
                f"🔥 Current streak: *{data['current_streak']}*\n\n"
                f"Come back tomorrow for a new puzzle!\n"
                f"Or try /practice for unlimited games."
            )
        else:
            guesses_display = "\n".join([f"{check_guess(g, word)} {g.upper()}" for g in data["daily_guesses"]])
            send_message(chat_id,
                f"😢 You already played today and didn't get it.\n\n"
                f"Your guesses:\n{guesses_display}\n\n"
                f"The word was: *{word.upper()}*\n"
                f"💔 Streak broken - back to 0\n\n"
                f"Come back tomorrow!\n"
                f"Or try /practice to redeem yourself."
            )
        return
    
    data["last_daily_date"] = today
    data["daily_guesses"] = []
    data["hint_cost_paid"] = False
    data["last_daily_won"] = False
    save_user_data(user["id"], data)
    
    puzzle_num = get_daily_number()
    send_message(chat_id,
        f"📅 *Daily Puzzle #{puzzle_num}*\n\n"
        f"🔥 Current streak: *{data['current_streak']}*\n"
        f"🏆 Best streak: *{data['max_streak']}*\n\n"
        f"Send your first guess (5 letters)!\n"
        f"You have 6 attempts."
    )

def handle_practice(chat_id, user):
    data = load_user_data(user["id"])
    
    data["practice_word"] = random.choice(DAILY_WORDS)
    data["practice_guesses"] = []
    save_user_data(user["id"], data)
    
    send_message(chat_id,
        f"🎯 *Practice Mode*\n\n"
        f"A random word has been chosen!\n"
        f"Send your guesses (5 letters).\n\n"
        f"Practice doesn't affect your streak.\n"
        f"Type /quit to give up."
    )

def handle_quit(chat_id, user):
    data = load_user_data(user["id"])
    
    if data.get("practice_word"):
        word = data["practice_word"]
        data["practice_word"] = None
        data["practice_guesses"] = []
        save_user_data(user["id"], data)
        send_message(chat_id,
            f"👋 Gave up!\n\nThe word was: *{word.upper()}*\n\n"
            f"Type /practice to try another!"
        )
    else:
        send_message(chat_id, "You're not in a practice game!")

def handle_stats(chat_id, user):
    data = load_user_data(user["id"])
    first_name = user.get("first_name", "Player")
    
    total = data["games_played"]
    wins = data["games_won"]
    win_pct = (wins / total * 100) if total > 0 else 0
    
    dist = data.get("distribution", {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0})
    max_dist = max(int(v) for v in dist.values()) if dist.values() else 1
    dist_display = ""
    for i in range(1, 7):
        count = int(dist.get(str(i), 0))
        bar_len = int((count / max_dist) * 10) if max_dist > 0 else 0
        bar = "🟩" * bar_len + "⬜" * (10 - bar_len)
        dist_display += f"{i}: {bar} {count}\n"
    
    streak_fire = "🔥" * min(data["current_streak"], 10) if data["current_streak"] > 0 else "💔"
    
    send_message(chat_id,
        f"📊 *{first_name}'s Stats*\n\n"
        f"*Streak*\n"
        f"{streak_fire}\n"
        f"Current: *{data['current_streak']}* | Best: *{data['max_streak']}*\n\n"
        f"*Performance*\n"
        f"Played: {total} | Won: {wins} ({win_pct:.0f}%)\n\n"
        f"*Guess Distribution*\n"
        f"{dist_display}"
    )

def handle_hint(chat_id, user):
    data = load_user_data(user["id"])
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    in_daily = data["last_daily_date"] == today and not data.get("last_daily_won", True)
    in_practice = data.get("practice_word") is not None
    
    if not in_daily and not in_practice:
        send_message(chat_id, "Start a game first with /play or /practice!")
        return
    
    word = get_daily_word() if in_daily else data["practice_word"]
    guesses = data["daily_guesses"] if in_daily else data["practice_guesses"]
    
    revealed = set()
    for guess in guesses:
        for i, letter in enumerate(guess.lower()):
            if letter == word[i]:
                revealed.add(i)
    
    unrevealed = [i for i in range(5) if i not in revealed]
    if not unrevealed:
        send_message(chat_id, "You've already revealed all letters!")
        return
    
    if in_daily and data["current_streak"] > 0 and not data.get("hint_cost_paid", False):
        reply_markup = {
            "inline_keyboard": [[
                {"text": "🔓 Yes, reveal a letter", "callback_data": "hint_confirm"},
                {"text": "❌ Keep my streak", "callback_data": "hint_cancel"}
            ]]
        }
        send_message(chat_id,
            f"⚠️ *Hint costs 1 streak point!*\n\n"
            f"Your current streak: *{data['current_streak']}*\n"
            f"After hint: *{data['current_streak'] - 1}*\n\n"
            f"Are you sure?",
            reply_markup=reply_markup
        )
    else:
        pos = random.choice(unrevealed)
        letter = word[pos]
        send_message(chat_id, f"💡 *Hint:* Position {pos + 1} is *{letter.upper()}*")

def handle_hint_callback(chat_id, message_id, callback_id, user, action):
    answer_callback(callback_id)
    data = load_user_data(user["id"])
    
    if action == "hint_cancel":
        edit_message(chat_id, message_id, "💪 Smart choice! Keep that streak alive!")
        return
    
    data["current_streak"] = max(0, data["current_streak"] - 1)
    data["hint_cost_paid"] = True
    save_user_data(user["id"], data)
    
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    in_daily = data["last_daily_date"] == today
    word = get_daily_word() if in_daily else data.get("practice_word", "")
    guesses = data["daily_guesses"] if in_daily else data.get("practice_guesses", [])
    
    revealed = set()
    for guess in guesses:
        for i, letter in enumerate(guess.lower()):
            if letter == word[i]:
                revealed.add(i)
    
    unrevealed = [i for i in range(5) if i not in revealed]
    if unrevealed:
        pos = random.choice(unrevealed)
        letter = word[pos]
        edit_message(chat_id, message_id,
            f"💡 *Hint purchased!* (-1 streak)\n\n"
            f"Position {pos + 1} is *{letter.upper()}*\n\n"
            f"🔥 Streak now: *{data['current_streak']}*"
        )
    else:
        edit_message(chat_id, message_id, "All letters already revealed!")

def handle_guess(chat_id, user, text):
    text = text.strip().lower()
    
    if len(text) != 5 or not text.isalpha():
        return
    
    data = load_user_data(user["id"])
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    in_daily = (data["last_daily_date"] == today and 
                len(data["daily_guesses"]) < 6 and 
                not data.get("last_daily_won", True))
    in_practice = (data.get("practice_word") is not None and 
                   len(data.get("practice_guesses", [])) < 6)
    
    if not in_daily and not in_practice:
        return
    
    if not is_valid_word(text):
        send_message(chat_id, f"❌ *{text.upper()}* is not in my word list!\nTry another word.")
        return
    
    if in_daily:
        word = get_daily_word()
        data["daily_guesses"].append(text)
        guesses = data["daily_guesses"]
        mode = "daily"
    else:
        word = data["practice_word"]
        data["practice_guesses"].append(text)
        guesses = data["practice_guesses"]
        mode = "practice"
    
    feedback = check_guess(text, word)
    display = "\n".join([f"{check_guess(g, word)} {g.upper()}" for g in guesses])
    remaining = 6 - len(guesses)
    
    won = text == word
    lost = len(guesses) >= 6 and not won
    
    if won:
        if mode == "daily":
            data["games_played"] += 1
            data["games_won"] += 1
            data["current_streak"] += 1
            data["max_streak"] = max(data["max_streak"], data["current_streak"])
            data["last_daily_won"] = True
            num_guesses = str(len(guesses))
            data["distribution"][num_guesses] = data["distribution"].get(num_guesses, 0) + 1
            
            puzzle_num = get_daily_number()
            share_grid = "\n".join([check_guess(g, word) for g in guesses])
            share_text = f"Claire's Wordle #{puzzle_num} {len(guesses)}/6\n\n{share_grid}"
            
            streak_fire = "🔥" * min(data["current_streak"], 10)
            
            save_user_data(user["id"], data)
            
            send_message(chat_id,
                f"🎉 *BRILLIANT!*\n\n"
                f"{display}\n\n"
                f"You got it in *{len(guesses)}* guess{'es' if len(guesses) > 1 else ''}!\n\n"
                f"*{streak_fire}*\n"
                f"🔥 Streak: *{data['current_streak']}* days!\n"
                f"🏆 Best: *{data['max_streak']}*\n\n"
                f"📋 *Share your result:*\n```\n{share_text}\n```\n\n"
                f"Want more? Try /practice!"
            )
        else:
            data["practice_word"] = None
            data["practice_guesses"] = []
            save_user_data(user["id"], data)
            
            send_message(chat_id,
                f"🎉 *Nice one!*\n\n"
                f"{display}\n\n"
                f"Got it in *{len(guesses)}*!\n\n"
                f"Play again? /practice"
            )
    elif lost:
        if mode == "daily":
            data["games_played"] += 1
            data["current_streak"] = 0
            data["last_daily_won"] = False
            save_user_data(user["id"], data)
            
            send_message(chat_id,
                f"😢 *So close!*\n\n"
                f"{display}\n\n"
                f"The word was: *{word.upper()}*\n\n"
                f"💔 Streak broken!\n"
                f"Come back tomorrow to start a new streak!\n\n"
                f"Practice? /practice"
            )
        else:
            data["practice_word"] = None
            data["practice_guesses"] = []
            save_user_data(user["id"], data)
            
            send_message(chat_id,
                f"😅 *Better luck next time!*\n\n"
                f"{display}\n\n"
                f"The word was: *{word.upper()}*\n\n"
                f"Try again? /practice"
            )
    else:
        keyboard = get_keyboard_status(guesses, word)
        save_user_data(user["id"], data)
        
        send_message(chat_id,
            f"{display}\n\n"
            f"*{remaining}* guess{'es' if remaining > 1 else ''} left\n\n"
            f"```\n{keyboard}\n```"
        )

# ============ MAIN HANDLER ============
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            update = json.loads(body)
            process_update(update)
        except Exception as e:
            print(f"Error processing update: {e}")
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"ok": true}')
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status": "Claire\'s Wordle Bot is running!"}')

def process_update(update):
    """Process a Telegram update"""
    
    # Handle callback queries (button presses)
    if "callback_query" in update:
        callback = update["callback_query"]
        user = callback["from"]
        chat_id = callback["message"]["chat"]["id"]
        message_id = callback["message"]["message_id"]
        callback_id = callback["id"]
        data = callback.get("data", "")
        
        if data.startswith("hint_"):
            handle_hint_callback(chat_id, message_id, callback_id, user, data)
        return
    
    # Handle messages
    if "message" not in update:
        return
    
    message = update["message"]
    chat_id = message["chat"]["id"]
    user = message.get("from", {})
    text = message.get("text", "")
    
    if not text:
        return
    
    # Command handling
    if text.startswith("/start"):
        handle_start(chat_id, user)
    elif text.startswith("/play"):
        handle_play(chat_id, user)
    elif text.startswith("/practice"):
        handle_practice(chat_id, user)
    elif text.startswith("/quit"):
        handle_quit(chat_id, user)
    elif text.startswith("/stats"):
        handle_stats(chat_id, user)
    elif text.startswith("/hint"):
        handle_hint(chat_id, user)
    elif not text.startswith("/"):
        handle_guess(chat_id, user, text)
