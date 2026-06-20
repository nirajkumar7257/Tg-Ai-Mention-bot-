import os
import asyncio
import logging
import random
from telegram import Update, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from google import genai
from telegram.error import RetryAfter, Forbidden

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Environment Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YAHAN_APNA_TELEGRAM_TOKEN_DALEIN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YAHAN_APNA_GEMINI_KEY_DALEIN")
PORT = int(os.getenv("PORT", 8443))
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")

# 👑 OWNER ID SETTING: Apna asli Telegram User ID yahan dalein (bina quotes ke number)
# Example: 123456789 (Aap @MissRose_bot par /id likhkar apni ID jaan sakte hain)
OWNER_ID = int(os.getenv("OWNER_ID", 0)) 

ai_client = genai.Client(api_key=GEMINI_API_KEY)

# Stats aur Broadcast tracking ke liye In-Memory Sets
# Note: Heroku restart hone par ye clear ho jata hai (Production ke liye Database zaroori hai)
served_users = set()
served_chats = set()

running_tags = {}
paused_tags = {}

TAG_STYLES = {
    "hindi": ["Suno dosto!", "Kahan ho sabhi?", "Ek zaroori baat!", "Idhar dekho bhai!"],
    "english": ["Hey everyone!", "Attention please!", "Check this out!", "Wake up guys!"],
    "hinglish": ["Kya chal raha hai?", "Sab log online aao!", "Suno sabke sab!", "Arre idhar toh aao!"],
    "gm": ["Good Morning! ☀️", "Subah ho gayi mamu!", "Have a great day ahead!", "Suprabhat family!"],
    "gn": ["Good Night! 🌙", "Chalo sone jao ab!", "Sweet dreams everyone!", "Shubh ratri dosto!"],
    "joke": ["Ek joke suno aur online aao! 😂", "Haste haste online hazir ho! 💀", "Chalo sab mood fresh karo! ✨"],
    "general": ["Notification Alert! 🔔", "Ping! 😉", "Don't ignore this! 🙌", "Hello hello! 🎉"]
}

# Menu Commands Setup
async def post_init(application: Application) -> None:
    commands = [
        BotCommand("start", "Bot shuru karein"),
        BotCommand("help", "Command list aur styles dekhein"),
        BotCommand("all", "Sabhi members ko tag karein"),
        BotCommand("admin", "Sirf admins ko tag karein"),
        BotCommand("stop", "Tagging loop ko band karein"),
        BotCommand("pause", "Tagging ko thodi der rokein"),
        BotCommand("resume", "Roki hui tagging fir se shuru karein")
    ]
    await application.bot.set_my_commands(commands)

# Tracking Helper: Har chat aur user ki ID yaad rakhna
def track_chat(update: Update):
    if update.effective_chat:
        chat_id = update.effective_chat.id
        if update.effective_chat.type == "private":
            served_users.add(chat_id)
        else:
            served_chats.add(chat_id)

# Admin Verification Helper
async def is_user_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    chat = update.effective_chat
    user_id = update.effective_user.id
    if chat.type == "private":
        return True
    member = await context.bot.get_chat_member(chat.id, user_id)
    return member.status in ["administrator", "creator"]

# 1. /start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_chat(update) # Track chat ID
    chat_type = update.message.chat.type
    bot_username = context.bot.username

    if chat_type == "private":
        keyboard = [
            [InlineKeyboardButton("➕ Add to your group", url=f"https://t.me/{bot_username}?startgroup=true")],
            [
                InlineKeyboardButton("❓ Help", callback_data="help_btn"),
                InlineKeyboardButton("📢 Update Support", url=os.getenv("SUPPORT_LINK", "https://t.me"))
                
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        welcome_text = (
            f"✨ **Welcome {update.effective_user.first_name}!** ✨\n\n"
            "Main ek advanced AI Mention & Mass Tagging Bot hoon.\n"
            "Owner commands enabled hain."
        )
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text("👋 Hello members! Main is group me active hoon. Commands dekhne ke liye `/help` type karein.")

# 👑 OWNER COMMAND 1: /broadcast <msg> — Broadcast to all users & groups
async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Ye command sirf **Bot Owner** use kar sakta hai!")
        return

    if not context.args:
        await update.message.reply_text("❌ Please format use karein: `/broadcast Mera message yahan likhein`")
        return

    broadcast_msg = "📢 **IMPORTANT BROADCAST** 📢\n\n" + " ".join(context.args)
    all_targets = list(served_users) + list(served_chats)
    
    if not all_targets:
        await update.message.reply_text("Broadcast karne ke liye koi bhi user ya group data nahi mila.")
        return

    await update.message.reply_text(f"🚀 Broadcast shuru ho raha hai... Total targets: {len(all_targets)}")
    
    success = 0
    failed = 0

    for chat_id in all_targets:
        try:
            await context.bot.send_message(chat_id=chat_id, text=broadcast_msg, parse_mode="Markdown")
            success += 1
            await asyncio.sleep(1.5)  # ✅ FIXED: Increased from 0.5 to 1.5 seconds for better rate limiting
        except Forbidden:
            failed += 1 # User ne bot block kar diya hai
        except RetryAfter as e:
            await asyncio.sleep(e.retry_after)
            try:
                await context.bot.send_message(chat_id=chat_id, text=broadcast_msg, parse_mode="Markdown")
                success += 1
            except Exception as error:  # ✅ FIXED: Better exception handling
                logging.error(f"Broadcast send failed: {error}")
                failed += 1
        except Exception as error:  # ✅ FIXED: Better exception handling
            logging.error(f"Broadcast error for chat {chat_id}: {error}")
            failed += 1

    await update.message.reply_text(f"✅ **Broadcast Done!**\n\n🟢 Success: {success}\n🔴 Failed/Blocked: {failed}")

# 👑 OWNER COMMAND 2: /stats — View bot usage statistics
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Ye command sirf **Bot Owner** use kar sakta hai!")
        return

    stats_text = (
        "📊 **Bot Current Usage Statistics:**\n\n"
         f"👤 **Total DM Users:** {len(served_users)}\n"
         f"👥 **Total Active Groups:** {len(served_chats)}\n"
         f"📈 **Total Served Chats:** {len(served_users) + len(served_chats)}"
    )
    await update.message.reply_text(stats_text, parse_mode="Markdown")

# Inline Button Click Callback
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "help_btn":
        help_text = "🏷️ **8 Tagging Styles:** `/all hindi`, `/all english`, `/all gm`, `/all gn`, `/all joke` etc."
        await query.message.reply_text(help_text, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_chat(update)
    await update.message.reply_text("💡 Guide dekhne ke liye DM (Private chat) me `/start` karein aur Help button dabayein.")

# ✅ FIXED: Complete Tag Engine with proper all/admin distinction
async def tag_engine(update: Update, context: ContextTypes.DEFAULT_TYPE, target_admins_only=False):
    track_chat(update)
    chat = update.effective_chat
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("❌ Ye command sirf groups me use ho sakta hai!")
        return
    if not await is_user_admin(update, context):
        await update.message.reply_text("❌ Ye command sirf **Admin** use kar sakte hain!")
        return

    chat_id = chat.id
    running_tags[chat_id] = True
    paused_tags[chat_id] = False
    args = context.args
    style = "general"
    custom_msg = ""

    if args:
        if args[0].lower() in TAG_STYLES:
            style = args[0].lower()
            custom_msg = " ".join(args[1:])
        else:
            custom_msg = " ".join(args)

    try:
        users_to_tag = []
        
        # ✅ FIXED: Proper logic for admin_only vs all members
        if target_admins_only:
            # Tag only admins
            targets = await chat.get_administrators()
            users_to_tag = [admin.user for admin in targets if not admin.user.is_bot]
            tag_type = "Admins"
        else:
            # Tag all members - trying multiple methods
            try:
                # Method 1: Try to get all members
                chat_members = await context.bot.get_chat_members(chat.id)
                users_to_tag = [member.user for member in chat_members if not member.user.is_bot]
                tag_type = "All Members"
            except Exception as e:
                logging.warning(f"Could not fetch all members, falling back to admins: {e}")
                # Fallback: Tag admins if we can't get all members
                targets = await chat.get_administrators()
                users_to_tag = [admin.user for admin in targets if not admin.user.is_bot]
                tag_type = "Admins (Fallback)"
        
        if not users_to_tag:
            await update.message.reply_text("❌ Koi users available nahi hain tagging ke liye!")
            running_tags[chat_id] = False
            return

        await update.message.reply_text(f"🚀 {tag_type} ko mention karne ke liye loop shuru ho chuka hai... ({len(users_to_tag)} users)")

        for i in range(0, len(users_to_tag), 5):
            if not running_tags.get(chat_id, False): 
                break
            while paused_tags.get(chat_id, False): 
                await asyncio.sleep(2)

            batch = users_to_tag[i:i+5]
            style_prefix = random.choice(TAG_STYLES[style])
            mention_line = f"✨ {style_prefix}\n✍️ Msg: {custom_msg}\n\n" if custom_msg else f"✨ {style_prefix}\n\n"
            for user in batch: 
                mention_line += f"[{user.first_name}](tg://user?id={user.id}) "

            try:
                await context.bot.send_message(chat_id=chat_id, text=mention_line, parse_mode="Markdown")
                await asyncio.sleep(2)  # ✅ FIXED: Increased from 3 to 2 seconds (better balance)
            except RetryAfter as e:
                logging.warning(f"Rate limited, waiting {e.retry_after} seconds")
                await asyncio.sleep(e.retry_after)
            except Exception as e:
                logging.error(f"Error sending mention batch: {e}")

        running_tags[chat_id] = False
        await update.message.reply_text("✅ Tagging loop complete ho gaya!")
        
    except Exception as e:
        logging.error(f"Tag Engine Error: {e}")
        try:
            await update.message.reply_text(f"❌ Error: {str(e)[:100]}")
        except:
            pass
        running_tags[chat_id] = False

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if await is_user_admin(update, context): 
            running_tags[update.effective_chat.id] = False
            await update.message.reply_text("⏹️ Tagging loop band ho gaya!")
    except Exception as e:
        logging.error(f"Stop command error: {e}")

async def pause_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if await is_user_admin(update, context): 
            paused_tags[update.effective_chat.id] = True
            await update.message.reply_text("⏸️ Tagging pause ho gaya!")
    except Exception as e:
        logging.error(f"Pause command error: {e}")

async def resume_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if await is_user_admin(update, context): 
            paused_tags[update.effective_chat.id] = False
            await update.message.reply_text("▶️ Tagging resume ho gaya!")
    except Exception as e:
        logging.error(f"Resume command error: {e}")

# ✅ FIXED: Better Message Handler with improved error handling
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        track_chat(update)
        user_text = update.message.text
        bot_username = context.bot.username
        is_private = update.message.chat.type == "private"
        is_mentioned = f"@{bot_username}" in user_text

        if is_private or is_mentioned:
            clean_prompt = user_text.replace(f"@{bot_username}", "").strip()
            if not clean_prompt: 
                return
            try:
                response = ai_client.models.generate_content(model="gemini-2.0-flash", contents=clean_prompt)
                ai_reply = response.text
                
                # ✅ FIXED: Better error handling for message reply
                try:
                    await update.message.reply_text(ai_reply, parse_mode="Markdown")
                except Exception as reply_error:
                    # If markdown fails, try without parsing
                    try:
                        await update.message.reply_text(ai_reply)
                    except Exception as fallback_error:
                        logging.error(f"Could not send reply: {fallback_error}")
                        
            except Exception as e:
                logging.error(f"Gemini API Error: {e}")
                try:
                    await update.message.reply_text("❌ AI se error aaya! Kripya baad mein kosis karein.")
                except Exception as error_reply:
                    logging.error(f"Could not send error message: {error_reply}")
    except Exception as e:
        logging.error(f"Message handler error: {e}")

# All Command - Tag all users
async def all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await tag_engine(update, context, target_admins_only=False)

# Admin Command - Tag only admins
async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await tag_engine(update, context, target_admins_only=True)

# Main Application Setup
async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Post Init Setup
    application.post_init = post_init
    
    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("all", all_command))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CommandHandler("stop", stop_command))
    application.add_handler(CommandHandler("pause", pause_command))
    application.add_handler(CommandHandler("resume", resume_command))
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    application.add_handler(CommandHandler("stats", stats_command))
    
    # Callback Query Handler (For inline buttons)
    application.add_handler(CallbackQueryHandler(button_click))
    
    # Message Handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
    
    # Start the bot
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
