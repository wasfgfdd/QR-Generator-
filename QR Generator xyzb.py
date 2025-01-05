from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import qrcode
from qrcode.image.styledpil import StyledPilImage
from PIL import Image
import io

# Command to start the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Hi! I can generate QR codes for you. \n"
        "Send any text to create a standard QR code, or send /custom to create a custom QR code with a photo.\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/custom - Create a QR code with a photo\n"
        "/design - Generate a styled QR code\n"
    )

# Generate a basic QR code
def generate_qr(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code as a BytesIO object
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)

    update.message.reply_photo(photo=InputFile(bio, filename="qr.png"))

# Generate a QR code with an embedded photo
def custom_qr(update: Update, context: CallbackContext) -> None:
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        file = context.bot.get_file(file_id)
        file.download("photo.jpg")

        # Open the downloaded photo
        photo = Image.open("photo.jpg").resize((200, 200))

        # Generate QR code
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        qr.add_data("Your custom message here!")
        qr.make(fit=True)

        qr_img = qr.make_image(image_factory=StyledPilImage, embeded_image_path="photo.jpg")

        # Save the styled QR code
        bio = io.BytesIO()
        qr_img.save(bio, format="PNG")
        bio.seek(0)

        update.message.reply_photo(photo=InputFile(bio, filename="custom_qr.png"))
    else:
        update.message.reply_text("Please send a photo to embed in the QR code!")

# Generate a styled QR code
def styled_qr(update: Update, context: CallbackContext) -> None:
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    qr.add_data("Styled QR Code Message")
    qr.make(fit=True)

    qr_img = qr.make_image(image_factory=StyledPilImage, module_drawer="rounded")
    bio = io.BytesIO()
    qr_img.save(bio, format="PNG")
    bio.seek(0)

    update.message.reply_photo(photo=InputFile(bio, filename="styled_qr.png"))

# Main function to run the bot
def main():
    updater = Updater("7796122716:AAHbSt4ZcjVNUwWWtbqRaPN362gJh8fu9xE)  # Replace YOUR_BOT_TOKEN with your actual Telegram bot token

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("custom", custom_qr))
    dispatcher.add_handler(CommandHandler("design", styled_qr))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, generate_qr))
    dispatcher.add_handler(MessageHandler(Filters.photo, custom_qr))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()