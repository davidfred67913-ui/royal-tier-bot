import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update, context):
    """Send a message with inline keyboard when /start is issued."""
    keyboard = [
        [InlineKeyboardButton("🎮 Play Now", callback_data="play")],
        [InlineKeyboardButton("📞 Support", url="https://www.cazino-big.com/article/faq?agent_id=33")],
        [InlineKeyboardButton("🏆 Today's Offer", callback_data="offer")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Welcome to Royal Tier Rewards Bot! 🎰\n\nChoose an option below:",
        reply_markup=reply_markup
    )

async def button_handler(update, context):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "play":
        await query.edit_message_text(
            text="🎮 Let's play! (Your game link or instructions here)",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")
            ]])
        )
    
    elif query.data == "offer":
        await query.edit_message_text(
            text="🏆 Today's Special Offer!\n\n(Your offer details here)",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")
            ]])
        )
    
    elif query.data == "back_to_menu":
        keyboard = [
            [InlineKeyboardButton("🎮 Play Now", callback_data="play")],
            [InlineKeyboardButton("📞 Support", url="https://www.cazino-big.com/article/faq?agent_id=33")],
            [InlineKeyboardButton("🏆 Today's Offer", callback_data="offer")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text="Welcome to Royal Tier Rewards Bot! 🎰\n\nChoose an option below:",
            reply_markup=reply_markup
        )

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
