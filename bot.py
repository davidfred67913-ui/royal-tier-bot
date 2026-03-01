import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURATION ---
TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = "@online_cazino_big"  # Your channel username
CHANNEL_LINK = "https://t.me/online_cazino_big"
WEBSITE_LINK = "https://cazino-big.com?agent_id=33"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def check_membership(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        # Statuses that count as "joined"
        return member.status in ['member', 'administrator', 'creator']
    except Exception:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Step 1: Welcome Screen"""
    keyboard = [
        [InlineKeyboardButton("✅ Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("🔓 I Joined (Unlock)", callback_data="check_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Generic marketing text as requested
    msg = "Welcome 👋 Get access to exclusive drops + winner alerts.\n\nStep 1/2: Join our channel to unlock."
    
    if update.message:
        await update.message.reply_text(msg, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(msg, reply_markup=reply_markup)

async def handle_unlock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    is_joined = await check_membership(user_id, context)

    if is_joined:
        # Step 2: Unlocked Screen
        keyboard = [
            [InlineKeyboardButton("🎰 Play Now", url=WEBSITE_LINK)],
            [InlineKeyboardButton("🎁 Today’s Offer", callback_data="show_offer")],
            [InlineKeyboardButton("💬 Support", url="https://t.me/your_support_handle")] # Update if needed
        ]
        await query.edit_message_text(
            "Unlocked 🎉\n\nStep 2/2: Continue to the site.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        # Failed Check Screen
        keyboard = [
            [InlineKeyboardButton("✅ Join Channel", url=CHANNEL_LINK)],
            [InlineKeyboardButton("🔓 Try Unlock Again", callback_data="check_join")]
        ]
        await query.edit_message_text(
            "Not subscribed yet—join to unlock access.\n\n"
            "• Get Real-time Alerts\n"
            "• Exclusive Member Rewards\n"
            "• 24/7 Priority Access",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def show_offer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton("🎰 Play Now", url=WEBSITE_LINK)]]
    await query.edit_message_text(
        "🎁 SPECIAL OFFER: Your 100% deposit match is waiting! Claim it before it expires.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

if __name__ == '__main__':
    # Build application (Fixed for Python 3.14/PTB 20+)
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_unlock, pattern="check_join"))
    application.add_handler(CallbackQueryHandler(show_offer, pattern="show_offer"))
    
    application.run_polling()
if __name__ == '__main__':
    if not TOKEN:
        print("ERROR: BOT_TOKEN variable is missing in Render Environment!")
    else:
        # Build application
        application = ApplicationBuilder().token(TOKEN).build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(handle_unlock, pattern="check_join"))
        application.add_handler(CallbackQueryHandler(show_offer, pattern="show_offer"))
        
        print("Bot is starting polling...")
        application.run_polling(drop_pending_updates=True)
