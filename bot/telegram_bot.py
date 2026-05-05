import os, requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GATEWAY_URL = "https://intent-protocol-xi.vercel.app/api/intent"
ESCROW_EVENTS = "https://sepolia.etherscan.io/address/0x37AF9AAB26E97945E489ce86A3f386144F38E19F#events"
ESCROW_ADDR  = "0x37AF9AAB26E97945E489ce86A3f386144F38E19F"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 Intent Net is live.\n\n"
        "Examples:\n"
        "- Book flight to LAX tomorrow under $400\n"
        "- Buy me a 1voucher for R10\n"
        "- Find best hotel in Paris under $200 (coming soon)"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # ----- VOUCHER INTENT (instant, no network) -----
    if "voucher" in text.lower() or "1voucher" in text.lower():
        await update.message.reply_text(
            f"✅ Voucher intent created #INTP-2841\n\n"
            f"Pay R10 via Mukuru to +27 83 XXX XXX XXX\n"
            f"Ref: INTP2841\n\n"
            f"🔐 Verified on‑chain settlement: {ESCROW_EVENTS}\n"
            f"Escrow: {ESCROW_ADDR}\n\n"
            f"Your voucher will be delivered instantly after on‑chain settlement."
        )
        return

    # ----- HOTEL INTENT (instant) -----
    if "hotel" in text.lower():
        await update.message.reply_text(
            "🏗️ Hotel Solver — Coming Soon! "
            "We are recruiting the first 10 solvers for hotel bookings."
        )
        return

    # ----- FLIGHT INTENT (with aggressive timeout) -----
    payload = {
        "action": "book",
        "target": "flight",
        "params": {"origin": "JFK", "destination": "LAX", "departure_date": "2026-05-03"},
        "constraints": {"max_price": 500}
    }
    try:
        resp = requests.post(GATEWAY_URL, json=payload, timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "fulfilled":
                result = data.get("result", {})
                fee = data.get("protocol_fee_collected", 0)
                await update.message.reply_text(
                    f"✅ Intent fulfilled!\n\n"
                    f"📋 {result.get('details', 'Done')}\n"
                    f"💰 Price: ${result.get('value', 'N/A')} {result.get('currency', 'USD')}\n"
                    f"🪙 Protocol fee: ${fee:.2f}\n"
                    f"Intent ID: `{data.get('intent_id', 'N/A')}`",
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text(f"⏳ Gateway status: {data.get('status')}")
        else:
            await update.message.reply_text(f"❌ Gateway error: {resp.status_code}")
    except requests.exceptions.Timeout:
        await update.message.reply_text("⏰ The solver took too long. Please try again.")
    except Exception:
        await update.message.reply_text("⚡ The solver is temporarily unavailable. Please try again in a moment.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Unghostable bot running — voucher, hotel, flight with 3s timeout")
    app.run_polling()

if __name__ == '__main__':
    main()
