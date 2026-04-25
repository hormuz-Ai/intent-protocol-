import os
import requests
from datetime import date, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GATEWAY_URL = "https://intent-protocol-xi.vercel.app/api/intent"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 Intent Net is live.\n\n"
        "Tell me what you want. Examples:\n"
        "- Book flight to LAX tomorrow under $400\n"
        "- Find best hotel in Paris under $200 (coming soon)\n"
        "- Compare crypto swap rates for ETH to USDC (coming soon)"
    )

def parse_intent(text: str) -> dict:
    """Simple NLP to extract action, target, and params from natural language."""
    text = text.lower()
    
    # Determine action
    if "book" in text:
        action = "book"
    elif "find" in text or "search" in text:
        action = "find"
    elif "compare" in text:
        action = "compare"
    else:
        action = "book"
    
    # Determine target
    if "flight" in text:
        target = "flight"
    elif "hotel" in text:
        target = "hotel"
    elif "swap" in text or "crypto" in text:
        target = "crypto_swap"
    else:
        target = "flight"
    
    # Extract locations
    words = text.split()
    origin = "JFK"
    destination = "LAX"
    
    if "to" in words:
        to_idx = words.index("to")
        if to_idx + 1 < len(words):
            destination = words[to_idx + 1].upper()[:3]
        if to_idx > 0:
            origin = words[to_idx - 1].upper()[:3]
    
    if "from" in words:
        from_idx = words.index("from")
        if from_idx + 1 < len(words):
            origin = words[from_idx + 1].upper()[:3]
    
    # Extract price constraint
    max_price = 500
    if "under" in words:
        under_idx = words.index("under")
        if under_idx + 1 < len(words):
            try:
                max_price = int(words[under_idx + 1].replace("$","").replace(",",""))
            except:
                pass
    
    # Extract date (FIXED: correctly handle relative dates)
    today = date.today()
    if "tomorrow" in text:
        parsed_date = (today + timedelta(days=1)).strftime("%Y-%m-%d")
    elif "today" in text:
        parsed_date = today.strftime("%Y-%m-%d")
    else:
        parsed_date = "2026-04-25"
    
    return {
        "action": action,
        "target": target,
        "params": {
            "origin": origin,
            "destination": destination,
            "departure_date": parsed_date
        },
        "constraints": {"max_price": max_price}
    }

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Parse the intent
    intent = parse_intent(user_text)
    
    # If the intent is NOT a flight, show a "coming soon" message
    if intent["target"] != "flight":
        category = intent["target"].replace("_", " ")
        await update.message.reply_text(
            f"🏗️ {category.title()} Solver — Coming Soon!\n\n"
            f"We're recruiting the first 10 solvers to cover {category} bookings, "
            f"crypto swaps, hotel stays, and more.\n\n"
            f"💰 Early solver developers earn INTP token allocations.\n"
            f"🛠️ Build one yourself: https://github.com/Hormuz-Ai/intent-protocol-\n\n"
            f"Right now, try: 'Book a flight to LAX tomorrow under $400'"
        )
        return
    
    # Send flight intents to gateway
    try:
        response = requests.post(GATEWAY_URL, json=intent, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "fulfilled":
                result = data.get("result", {})
                fee = data.get("protocol_fee_collected", 0)
                await update.message.reply_text(
                    f"✅ Intent fulfilled!\n\n"
                    f"📋 {result.get('details', 'Done')}\n"
                    f"💰 Price: ${result.get('value', 'N/A')} {result.get('currency', 'USD')}\n"
                    f"🔗 Solver: {data.get('solver', 'N/A')}\n"
                    f"🪙 Protocol fee: ${fee:.2f}\n\n"
                    f"Intent ID: `{data.get('intent_id', 'N/A')}`",
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text(
                    f"⏳ Intent received. Status: {data.get('status', 'unknown')}\n"
                    f"Message: {data.get('message', 'Processing...')}"
                )
        else:
            await update.message.reply_text(f"❌ Gateway error: {response.status_code}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
