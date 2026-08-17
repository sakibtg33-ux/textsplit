from __future__ import annotations

import logging
import os
import shutil
import tempfile
from pathlib import Path

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# আপনার BotFather token এখানে বসান।
BOT_TOKEN = "8037539784:AAH_A6zognDNzRE66uEnA-raDNmH1Pm55fY"

# আপনার দেওয়া split_d200.py অনুযায়ী প্রতি অংশে ৫০টি line থাকবে।
LINES_PER_PART = 50
MAX_INPUT_SIZE = 20 * 1024 * 1024  # Telegram public Bot API download limit: 20 MB

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def split_txt_file(input_path: Path, output_dir: Path, lines_per_part: int = LINES_PER_PART) -> list[Path]:
    """Split a UTF-8 text file into sequential files, preserving line endings."""
    with input_path.open("r", encoding="utf-8", newline="") as source:
        lines = source.readlines()

    output_dir.mkdir(parents=True, exist_ok=True)
    output_files: list[Path] = []
    for start in range(0, len(lines), lines_per_part):
        part_number = start // lines_per_part + 1
        output_path = output_dir / f"split_{part_number:03d}.txt"
        with output_path.open("w", encoding="utf-8", newline="") as target:
            target.writelines(lines[start : start + lines_per_part])
        output_files.append(output_path)

    # Empty input file হলেও একটি empty output পাঠানো হবে।
    if not output_files:
        output_path = output_dir / "split_001.txt"
        output_path.write_text("", encoding="utf-8")
        output_files.append(output_path)

    return output_files


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(
            "একটি .txt ফাইল পাঠান। আমি প্রতি ৫০টি line করে split করে আলাদা আলাদা file হিসেবে ফেরত পাঠাব।"
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(
            "ব্যবহার:\n১) এই bot-এ একটি UTF-8 .txt file পাঠান।\n"
            "২) bot সেটিকে split_001.txt, split_002.txt ইত্যাদি নামে ফেরত পাঠাবে।\n"
            "প্রতি file-এ ৫০টি line থাকবে।"
        )


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if not message or not message.document:
        return

    document = message.document
    original_name = document.file_name or "uploaded.txt"
    if not original_name.lower().endswith(".txt"):
        await message.reply_text("শুধু .txt ফাইল পাঠান।")
        return

    if document.file_size and document.file_size > MAX_INPUT_SIZE:
        await message.reply_text(
            "এই ফাইলটি ২০ MB-এর বেশি। Telegram-এর public Bot API দিয়ে এত বড় file download করা যায় না।"
        )
        return

    work_dir = Path(tempfile.mkdtemp(prefix="txt_split_"))
    try:
        await message.chat.send_action(ChatAction.TYPING)
        input_path = work_dir / "input.txt"
        telegram_file = await document.get_file()
        await telegram_file.download_to_drive(custom_path=input_path)

        try:
            parts = split_txt_file(input_path, work_dir / "parts")
        except UnicodeDecodeError:
            await message.reply_text("ফাইলটি UTF-8 text file নয়, তাই পড়তে পারিনি।")
            return

        await message.reply_text(f"ফাইলটি {len(parts)}টি অংশে ভাগ করা হয়েছে।")
        for part_path in parts:
            with part_path.open("rb") as part_file:
                await message.reply_document(
                    document=part_file,
                    filename=part_path.name,
                    caption=part_path.name,
                )
    except Exception:
        logger.exception("Failed to process uploaded document")
        await message.reply_text("ফাইলটি process করতে সমস্যা হয়েছে। পরে আবার চেষ্টা করুন।")
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


async def unsupported_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text("একটি .txt file document হিসেবে পাঠান।")


def main() -> None:
    if BOT_TOKEN == "PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE":
        raise RuntimeError("bot.py-তে আপনার BotFather token বসান।")

    application: Application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(~filters.COMMAND, unsupported_message))

    logger.info("TXT split bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
