from configs.app_config import BOT_TOKEN
from services.sender_receiver_service import button, schedule_jobs, start, load_users_from_file
from telegram.ext import Application, CallbackQueryHandler, CommandHandler

def main():
    schedule_jobs()
    load_users_from_file()
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == "__main__":
    # asyncio.run(send_price_update())
    main()
