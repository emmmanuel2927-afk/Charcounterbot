"""
🔤 Character Counter Bot - Professional Character Analysis
Detailed letter breakdown, vowel/consonant analysis, and advanced text statistics
"""

import os
import re
import io
import string
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from collections import Counter
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# ==================== CONFIGURATION ====================

# Try multiple possible token variable names
BOT_TOKEN = (
    os.environ.get("TELEGRAM_TOKEN") or
    os.environ.get("TELEGRAM_BOT_TOKEN") or
    os.environ.get("BOT_TOKEN")
)

# If token is not set, try reading from .env file
if not BOT_TOKEN:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        BOT_TOKEN = (
            os.environ.get("TELEGRAM_TOKEN") or
            os.environ.get("TELEGRAM_BOT_TOKEN") or
            os.environ.get("BOT_TOKEN")
        )
    except:
        pass

# If still no token, show error
if not BOT_TOKEN:
    print("=" * 60)
    print("❌ ERROR: No Telegram Bot Token found!")
    print("=" * 60)
    print("Please set one of these environment variables:")
    print("  - TELEGRAM_TOKEN")
    print("  - TELEGRAM_BOT_TOKEN")
    print("  - BOT_TOKEN")
    print("=" * 60)
    raise ValueError("❌ No Telegram Bot Token found in environment variables!")

BOT_NAME = "Character Counter Bot"
BOT_USERNAME = "char_counter_bot"
BOT_VERSION = "1.0.0"

# ==================== CONSTANTS ====================

VOWELS = set('aeiou')
CONSONANTS = set('bcdfghjklmnpqrstvwxyz')
PUNCTUATION = set(string.punctuation)
DIGITS = set(string.digits)

# ==================== USER DATA ====================

user_data: Dict[int, Dict] = {}

def get_user_data(user_id: int) -> Dict:
    if user_id not in user_data:
        user_data[user_id] = {
            "history": [],
            "total_chars": 0,
            "total_analyses": 0,
            "last_text": ""
        }
    return user_data[user_id]

# ==================== KEYBOARDS ====================

def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔤 Analyze Text", callback_data="analyze")],
        [InlineKeyboardButton("📊 Letter Breakdown", callback_data="breakdown")],
        [InlineKeyboardButton("🔢 Character Stats", callback_data="stats")],
        [InlineKeyboardButton("📋 My Stats", callback_data="mystats")],
        [InlineKeyboardButton("❓ Help", callback_data="help")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_analysis_options_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔤 Full Character Analysis", callback_data="full_analysis")],
        [InlineKeyboardButton("📊 Letter Breakdown", callback_data="letter_breakdown")],
        [InlineKeyboardButton("📈 Character Frequency", callback_data="char_frequency")],
        [InlineKeyboardButton("📋 Export Report", callback_data="export_report")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ==================== CHARACTER ANALYSIS FUNCTIONS ====================

def analyze_characters(text: str) -> Dict:
    """
    Comprehensive character analysis
    Returns: Dict with all character statistics
    """
    if not text or not text.strip():
        return {"error": "Empty text"}
    
    # Remove whitespace for character counting
    text_no_spaces = text.replace(" ", "").replace("\n", "").replace("\t", "")
    
    # Basic counts
    total_chars = len(text)
    total_chars_no_spaces = len(text_no_spaces)
    
    # Count letters (alphabetic characters)
    letters = [c for c in text_no_spaces if c.isalpha()]
    total_letters = len(letters)
    
    # Count digits
    digits = [c for c in text_no_spaces if c.isdigit()]
    total_digits = len(digits)
    
    # Count spaces
    total_spaces = text.count(" ")
    
    # Count newlines
    total_newlines = text.count("\n")
    
    # Count punctuation
    punctuation_chars = [c for c in text if c in PUNCTUATION]
    total_punctuation = len(punctuation_chars)
    
    # Vowel count
    vowels = [c for c in text_no_spaces.lower() if c in VOWELS]
    total_vowels = len(vowels)
    
    # Consonant count
    consonants = [c for c in text_no_spaces.lower() if c in CONSONANTS]
    total_consonants = len(consonants)
    
    # Uppercase/Lowercase
    uppercase = [c for c in text_no_spaces if c.isupper()]
    total_uppercase = len(uppercase)
    
    lowercase = [c for c in text_no_spaces if c.islower()]
    total_lowercase = len(lowercase)
    
    # Character frequency
    char_freq = Counter(text_no_spaces.lower())
    top_chars = char_freq.most_common(15)
    
    # Letter frequency (only alphabetic)
    letter_freq = Counter([c.lower() for c in text_no_spaces if c.isalpha()])
    top_letters = letter_freq.most_common(26)
    
    # Special character count
    special_chars = [c for c in text_no_spaces if not c.isalnum() and c not in PUNCTUATION]
    total_special = len(special_chars)
    
    # Average word length
    words = text.split()
    avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
    
    # Longest word
    longest_word = max(words, key=len) if words else ""
    longest_word_length = len(longest_word)
    
    # Shortest word
    shortest_word = min(words, key=len) if words else ""
    shortest_word_length = len(shortest_word)
    
    # Unique characters
    unique_chars = set(text_no_spaces.lower())
    unique_char_count = len(unique_chars)
    
    return {
        "total_chars": total_chars,
        "total_chars_no_spaces": total_chars_no_spaces,
        "total_letters": total_letters,
        "total_digits": total_digits,
        "total_spaces": total_spaces,
        "total_newlines": total_newlines,
        "total_punctuation": total_punctuation,
        "total_vowels": total_vowels,
        "total_consonants": total_consonants,
        "total_uppercase": total_uppercase,
        "total_lowercase": total_lowercase,
        "total_special": total_special,
        "avg_word_length": avg_word_length,
        "longest_word": longest_word,
        "longest_word_length": longest_word_length,
        "shortest_word": shortest_word,
        "shortest_word_length": shortest_word_length,
        "unique_char_count": unique_char_count,
        "top_chars": top_chars,
        "top_letters": top_letters,
        "vowel_consonant_ratio": total_vowels / total_consonants if total_consonants > 0 else 0,
        "letter_percentage": (total_letters / total_chars_no_spaces * 100) if total_chars_no_spaces > 0 else 0,
        "digit_percentage": (total_digits / total_chars_no_spaces * 100) if total_chars_no_spaces > 0 else 0,
        "punctuation_percentage": (total_punctuation / total_chars * 100) if total_chars > 0 else 0,
    }

def format_analysis_result(result: Dict) -> str:
    """Format character analysis result for display"""
    if "error" in result:
        return "❌ " + result["error"]
    
    # Create the text
    text = (
        f"🔤 **Character Analysis Results**\n\n"
        f"📊 **Summary:**\n"
        f"• Total Characters: {result['total_chars']:,}\n"
        f"• Characters (no spaces): {result['total_chars_no_spaces']:,}\n"
        f"• Total Letters: {result['total_letters']:,}\n"
        f"• Total Digits: {result['total_digits']:,}\n"
        f"• Total Spaces: {result['total_spaces']:,}\n"
        f"• Newlines: {result['total_newlines']:,}\n"
        f"• Punctuation: {result['total_punctuation']:,}\n"
        f"• Special Characters: {result['total_special']:,}\n\n"
        
        f"🔤 **Letter Breakdown:**\n"
        f"• Vowels: {result['total_vowels']:,}\n"
        f"• Consonants: {result['total_consonants']:,}\n"
        f"• Vowel/Consonant Ratio: {result['vowel_consonant_ratio']:.2f}\n\n"
        
        f"🔠 **Case Analysis:**\n"
        f"• Uppercase: {result['total_uppercase']:,}\n"
        f"• Lowercase: {result['total_lowercase']:,}\n\n"
        
        f"📏 **Word Analysis:**\n"
        f"• Avg Word Length: {result['avg_word_length']:.2f} chars\n"
        f"• Longest Word: {result['longest_word']} ({result['longest_word_length']} chars)\n"
        f"• Shortest Word: {result['shortest_word']} ({result['shortest_word_length']} chars)\n\n"
        
        f"🔄 **Uniqueness:**\n"
        f"• Unique Characters: {result['unique_char_count']:,}\n\n"
        
        f"📊 **Composition:**\n"
        f"• Letters: {result['letter_percentage']:.1f}%\n"
        f"• Digits: {result['digit_percentage']:.1f}%\n"
        f"• Punctuation: {result['punctuation_percentage']:.1f}%\n"
    )
    
    return text

def create_character_chart(char_freq: List[Tuple[str, int]]) -> bytes:
    """Create a visual character frequency chart"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        width = 600
        height = 50 + len(char_freq) * 28
        img = Image.new('RGB', (width, height), color='#FFFFFF')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        max_count = char_freq[0][1] if char_freq else 1
        
        y = 10
        for char, count in char_freq[:20]:
            # Draw character
            display_char = char if char.isprintable() else '?'
            draw.text((10, y), f"'{display_char}'", fill=(0, 0, 0), font=font)
            
            # Draw bar
            bar_width = int((count / max_count) * 400)
            draw.rectangle([60, y, 60 + bar_width, y + 20], fill=(100, 150, 255))
            
            # Draw count
            draw.text((470, y), str(count), fill=(0, 0, 0), font=font)
            y += 28
        
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes.getvalue()
        
    except Exception as e:
        print(f"Chart error: {e}")
        return None

def create_export_report(text: str, result: Dict) -> bytes:
    """Create a text report for export"""
    # Get top characters
    top_chars = "\n".join([f"{char}: {count}" for char, count in result['top_chars'][:15]])
    top_letters = "\n".join([f"{letter}: {count}" for letter, count in result['top_letters'][:10]])
    
    report = f"""
🔤 CHARACTER COUNTER BOT - ANALYSIS REPORT
═══════════════════════════════════════════
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📝 INPUT TEXT (first 200 chars):
───────────────────────────────────────
{text[:200]}{'...' if len(text) > 200 else ''}

📊 SUMMARY STATISTICS:
───────────────────────────────────────
Total Characters:           {result['total_chars']:,}
Characters (no spaces):     {result['total_chars_no_spaces']:,}
Total Letters:              {result['total_letters']:,}
Total Digits:               {result['total_digits']:,}
Total Spaces:               {result['total_spaces']:,}
Newlines:                   {result['total_newlines']:,}
Punctuation:                {result['total_punctuation']:,}
Special Characters:         {result['total_special']:,}

🔤 LETTER BREAKDOWN:
───────────────────────────────────────
Vowels:                     {result['total_vowels']:,}
Consonants:                 {result['total_consonants']:,}
Vowel/Consonant Ratio:      {result['vowel_consonant_ratio']:.2f}

🔠 CASE ANALYSIS:
───────────────────────────────────────
Uppercase:                  {result['total_uppercase']:,}
Lowercase:                  {result['total_lowercase']:,}

📏 WORD ANALYSIS:
───────────────────────────────────────
Avg Word Length:            {result['avg_word_length']:.2f} chars
Longest Word:               {result['longest_word']} ({result['longest_word_length']} chars)
Shortest Word:              {result['shortest_word']} ({result['shortest_word_length']} chars)

🔄 UNIQUENESS:
───────────────────────────────────────
Unique Characters:          {result['unique_char_count']:,}

📊 COMPOSITION:
───────────────────────────────────────
Letters:                    {result['letter_percentage']:.1f}%
Digits:                     {result['digit_percentage']:.1f}%
Punctuation:                {result['punctuation_percentage']:.1f}%

📈 TOP 15 CHARACTERS:
───────────────────────────────────────
{top_chars}

📊 TOP 10 LETTERS:
───────────────────────────────────────
{top_letters}
"""
    return report.encode('utf-8')

# ==================== COMMAND HANDLERS ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    data = get_user_data(user_id)
    
    welcome = (
        f"🔤 **Welcome to {BOT_NAME}!**\n\n"
        f"👋 Hello @{user.username or user.first_name}!\n\n"
        f"Your professional character analysis assistant.\n\n"
        f"✨ **Features:**\n"
        f"• 🔤 Detailed character counting\n"
        f"• 📊 Letter breakdown (vowels/consonants)\n"
        f"• 🔠 Case analysis\n"
        f"• 📈 Character frequency charts\n"
        f"• 📋 Export reports\n"
        f"• 📊 Usage statistics\n\n"
        f"📊 **Your Stats:**\n"
        f"• Total characters analyzed: {data['total_chars']:,}\n"
        f"• Total analyses: {data['total_analyses']}\n\n"
        f"⬇️ Send me any text or use the buttons below!"
    )
    
    await update.message.reply_text(
        welcome,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        f"📖 **{BOT_NAME} User Guide**\n\n"
        "**🔤 What I Can Analyze:**\n"
        "• Total characters\n"
        "• Letters, digits, spaces\n"
        "• Vowels & Consonants\n"
        "• Uppercase & Lowercase\n"
        "• Punctuation & Special chars\n"
        "• Character frequency\n"
        "• Word length analysis\n\n"
        "**📋 How to Use:**\n"
        "• Send any text message\n"
        "• Click 'Analyze Text' button\n"
        "• Get detailed statistics\n\n"
        "**📌 Commands:**\n"
        "/start - Main menu\n"
        "/help - This help\n"
        "/stats - Your statistics"
    )
    
    await update.message.reply_text(
        help_text,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = get_user_data(user_id)
    
    stats_text = (
        f"📊 **Your Statistics**\n\n"
        f"🔤 Total analyses: {data['total_analyses']}\n"
        f"📝 Total characters analyzed: {data['total_chars']:,}\n\n"
        f"📅 Account active since: {datetime.now().strftime('%Y-%m-%d')}"
    )
    
    await update.message.reply_text(
        stats_text,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

# ==================== CALLBACK HANDLERS ====================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(update.effective_user.id)
    data = get_user_data(user_id)
    
    action = query.data
    
    if action == "analyze":
        await query.edit_message_text(
            "🔤 **Send me any text to analyze!**\n\n"
            "I'll provide:\n"
            "• Character count\n"
            "• Letter breakdown\n"
            "• Vowel/Consonant count\n"
            "• Case analysis\n"
            "• Character frequency\n\n"
            "Just send any text message!",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
        context.user_data["action"] = "analyze_waiting"
        
    elif action == "breakdown":
        await query.edit_message_text(
            "📊 **Letter Breakdown**\n\n"
            "Send me text to analyze letter breakdown!\n\n"
            "I'll show:\n"
            "• Vowels (A, E, I, O, U)\n"
            "• Consonants\n"
            "• Vowel/Consonant ratio\n"
            "• Letter frequency",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
        context.user_data["action"] = "breakdown_waiting"
        
    elif action == "stats":
        await query.edit_message_text(
            "🔢 **Character Statistics**\n\n"
            "Send me text for detailed character stats!\n\n"
            "I'll show:\n"
            "• Character count\n"
            "• Uppercase/Lowercase\n"
            "• Punctuation count\n"
            "• Special characters",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
        context.user_data["action"] = "stats_waiting"
        
    elif action == "mystats":
        stats_text = (
            f"📊 **Your Statistics**\n\n"
            f"🔤 Total analyses: {data['total_analyses']}\n"
            f"📝 Total characters analyzed: {data['total_chars']:,}\n\n"
            f"📅 Account active since: {datetime.now().strftime('%Y-%m-%d')}"
        )
        await query.edit_message_text(
            stats_text,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
        
    elif action == "help":
        await help_command(update, context)
        
    elif action == "back":
        await query.edit_message_text(
            "🏠 **Main Menu**\n\n"
            "What would you like to analyze?",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
        context.user_data["action"] = None
        
    elif action == "full_analysis":
        if "last_text" not in context.user_data:
            await query.edit_message_text(
                "❌ No text to analyze. Send me some text first!",
                parse_mode="Markdown",
                reply_markup=get_main_keyboard()
            )
            return
        
        text = context.user_data["last_text"]
        result = analyze_characters(text)
        
        if result and "error" not in result:
            formatted = format_analysis_result(result)
            await query.message.reply_text(
                formatted,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔤 Full Analysis", callback_data="full_analysis")],
                    [InlineKeyboardButton("📊 Letter Breakdown", callback_data="letter_breakdown")],
                    [InlineKeyboardButton("📈 Character Frequency", callback_data="char_frequency")],
                    [InlineKeyboardButton("📋 Export Report", callback_data="export_report")],
                    [InlineKeyboardButton("🏠 Main Menu", callback_data="back")]
                ])
            )
            
            # Update user stats
            data["total_chars"] += result["total_chars_no_spaces"]
            data["total_analyses"] += 1
            
    elif action == "letter_breakdown":
        if "last_text" not in context.user_data:
            await query.edit_message_text(
                "❌ No text to analyze. Send me some text first!",
                parse_mode="Markdown",
                reply_markup=get_main_keyboard()
            )
            return
        
        text = context.user_data["last_text"]
        result = analyze_characters(text)
        
        if result and "error" not in result:
            # Create letter breakdown
            letters_text = (
                f"📊 **Letter Breakdown**\n\n"
                f"🔤 **Vowels:** {result['total_vowels']:,}\n"
                f"  • A, E, I, O, U (and sometimes Y)\n\n"
                f"🔤 **Consonants:** {result['total_consonants']:,}\n"
                f"  • All other letters\n\n"
                f"📊 **Vowel/Consonant Ratio:** {result['vowel_consonant_ratio']:.2f}\n\n"
                f"📈 **Composition:**\n"
                f"• Vowels: {(result['total_vowels'] / result['total_letters'] * 100):.1f}%\n"
                f"• Consonants: {(result['total_consonants'] / result['total_letters'] * 100):.1f}%\n\n"
                f"📝 **Top Letters:**\n"
            )
            
            for letter, count in result['top_letters'][:10]:
                percentage = (count / result['total_letters'] * 100) if result['total_letters'] > 0 else 0
                letters_text += f"• {letter.upper()}: {count} ({percentage:.1f}%)\n"
            
            await query.message.reply_text(
                letters_text,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔤 Full Analysis", callback_data="full_analysis")],
                    [InlineKeyboardButton("📈 Character Frequency", callback_data="char_frequency")],
                    [InlineKeyboardButton("🏠 Main Menu", callback_data="back")]
                ])
            )
            
    elif action == "char_frequency":
        if "last_text" not in context.user_data:
            await query.edit_message_text(
                "❌ No text to analyze. Send me some text first!",
                parse_mode="Markdown",
                reply_markup=get_main_keyboard()
            )
            return
        
        text = context.user_data["last_text"]
        result = analyze_characters(text)
        
        if result and "error" not in result:
            freq_text = "📈 **Character Frequency**\n\n"
            for char, count in result['top_chars'][:15]:
                percentage = (count / result['total_chars_no_spaces'] * 100) if result['total_chars_no_spaces'] > 0 else 0
                display_char = char if char.isprintable() else '?'
                freq_text += f"• '{display_char}': {count} ({percentage:.1f}%)\n"
            
            # Create chart
            chart_data = create_character_chart(result['top_chars'][:15])
            
            if chart_data:
                await query.message.reply_photo(
                    photo=io.BytesIO(chart_data),
                    caption=freq_text,
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔤 Full Analysis", callback_data="full_analysis")],
                        [InlineKeyboardButton("📊 Letter Breakdown", callback_data="letter_breakdown")],
                        [InlineKeyboardButton("🏠 Main Menu", callback_data="back")]
                    ])
                )
            else:
                await query.message.reply_text(
                    freq_text,
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔤 Full Analysis", callback_data="full_analysis")],
                        [InlineKeyboardButton("🏠 Main Menu", callback_data="back")]
                    ])
                )
            
    elif action == "export_report":
        if "last_text" not in context.user_data:
            await query.edit_message_text(
                "❌ No text to export. Send me some text first!",
                parse_mode="Markdown",
                reply_markup=get_main_keyboard()
            )
            return
        
        text = context.user_data["last_text"]
        result = analyze_characters(text)
        
        if result and "error" not in result:
            report = create_export_report(text, result)
            await query.message.reply_document(
                document=io.BytesIO(report),
                filename=f"character_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                caption="📋 **Character Analysis Report Exported!**\n\nFull report attached.",
                parse_mode="Markdown",
                reply_markup=get_main_keyboard()
            )

# ==================== MESSAGE HANDLERS ====================

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages for analysis"""
    user_id = str(update.effective_user.id)
    data = get_user_data(user_id)
    text = update.message.text.strip()
    
    if not text:
        await update.message.reply_text(
            "❌ Please send some text to analyze!",
            reply_markup=get_main_keyboard()
        )
        return
    
    # Check for commands
    action = context.user_data.get("action", "")
    
    # Analyze the text
    result = analyze_characters(text)
    
    if "error" in result:
        await update.message.reply_text(
            "❌ Could not analyze the text. Please try again.",
            reply_markup=get_main_keyboard()
        )
        return
    
    # Store for later use
    context.user_data["last_text"] = text
    
    # Update user stats
    data["total_chars"] += result["total_chars_no_spaces"]
    data["total_analyses"] += 1
    
    # Format response based on action
    if action == "breakdown_waiting":
        # Letter breakdown
        letters_text = (
            f"📊 **Letter Breakdown**\n\n"
            f"🔤 **Vowels:** {result['total_vowels']:,}\n"
            f"🔤 **Consonants:** {result['total_consonants']:,}\n"
            f"📊 **Vowel/Consonant Ratio:** {result['vowel_consonant_ratio']:.2f}\n\n"
            f"📈 **Composition:**\n"
            f"• Vowels: {(result['total_vowels'] / result['total_letters'] * 100):.1f}%\n"
            f"• Consonants: {(result['total_consonants'] / result['total_letters'] * 100):.1f}%\n\n"
            f"📝 **Top Letters:**\n"
        )
        
        for letter, count in result['top_letters'][:10]:
            percentage = (count / result['total_letters'] * 100) if result['total_letters'] > 0 else 0
            letters_text += f"• {letter.upper()}: {count} ({percentage:.1f}%)\n"
        
        await update.message.reply_text(
            letters_text,
            parse_mode="Markdown",
            reply_markup=get_analysis_options_keyboard()
        )
        context.user_data["action"] = None
        
    elif action == "stats_waiting":
        # Character stats
        stats_text = (
            f"🔢 **Character Statistics**\n\n"
            f"🔤 Total Characters: {result['total_chars']:,}\n"
            f"🔤 Characters (no spaces): {result['total_chars_no_spaces']:,}\n"
            f"🔤 Letters: {result['total_letters']:,}\n"
            f"🔢 Digits: {result['total_digits']:,}\n"
            f"📝 Spaces: {result['total_spaces']:,}\n"
            f"📄 Newlines: {result['total_newlines']:,}\n"
            f"🔣 Punctuation: {result['total_punctuation']:,}\n"
            f"✨ Special Characters: {result['total_special']:,}\n\n"
            f"🔠 **Case Analysis:**\n"
            f"• Uppercase: {result['total_uppercase']:,}\n"
            f"• Lowercase: {result['total_lowercase']:,}\n"
            f"• Uppercase/Lowercase Ratio: {result['total_uppercase'] / result['total_lowercase']:.2f}" if result['total_lowercase'] > 0 else "N/A"
        )
        await update.message.reply_text(
            stats_text,
            parse_mode="Markdown",
            reply_markup=get_analysis_options_keyboard()
        )
        context.user_data["action"] = None
        
    else:
        # Full analysis
        formatted = format_analysis_result(result)
        await update.message.reply_text(
            formatted,
            parse_mode="Markdown",
            reply_markup=get_analysis_options_keyboard()
        )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document files for analysis"""
    try:
        document = update.message.document
        
        # Check if it's a text file
        if not document.mime_type or not document.mime_type.startswith('text/'):
            await update.message.reply_text(
                "❌ Please send a text file (.txt, .docx, etc.)",
                reply_markup=get_main_keyboard()
            )
            return
        
        # Download file
        file = await document.get_file()
        file_content = await file.download_as_bytearray()
        
        try:
            text = file_content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                text = file_content.decode('latin-1')
            except:
                await update.message.reply_text(
                    "❌ Could not read the file. Please send a plain text file.",
                    reply_markup=get_main_keyboard()
                )
                return
        
        if not text.strip():
            await update.message.reply_text(
                "❌ The file is empty.",
                reply_markup=get_main_keyboard()
            )
            return
        
        # Analyze the text
        result = analyze_characters(text)
        
        if "error" in result:
            await update.message.reply_text(
                "❌ Could not analyze the text. Please try again.",
                reply_markup=get_main_keyboard()
            )
            return
        
        # Store for later
        context.user_data["last_text"] = text
        
        # Update stats
        data = get_user_data(str(update.effective_user.id))
        data["total_chars"] += result["total_chars_no_spaces"]
        data["total_analyses"] += 1
        
        formatted = format_analysis_result(result)
        await update.message.reply_text(
            formatted,
            parse_mode="Markdown",
            reply_markup=get_analysis_options_keyboard()
        )
        
    except Exception as e:
        print(f"Document error: {e}")
        await update.message.reply_text(
            "❌ Error processing the file. Please try again.",
            reply_markup=get_main_keyboard()
        )

# ==================== MAIN ====================

async def post_init(application):
    print("=" * 60)
    print(f"🔤 {BOT_NAME} Started Successfully!")
    print(f"🤖 Username: @{BOT_USERNAME}")
    print(f"📦 Version: {BOT_VERSION}")
    print("=" * 60)
    print("✅ Bot is ready to analyze characters!")
    print("=" * 60)

def main():
    print(f"🚀 Starting {BOT_NAME}...")
    print(f"📡 Using token: {BOT_TOKEN[:15]}...{BOT_TOKEN[-5:]}")
    
    application = ApplicationBuilder() \
        .token(BOT_TOKEN) \
        .post_init(post_init) \
        .build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    
    # Callback handler
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    print("✅ Bot is polling for updates...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
