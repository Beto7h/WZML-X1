from pyrogram.filters import command, regex, user
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

from bot import bot, LOGGER
from bot.helper.telegram_helper.message_utils import send_message, edit_message
from bot.helper.telegram_helper.button_maker import ButtonMaker
from bot.helper.ext_utils.bot_utils import new_task

@new_task
async def vt_callback(client, query):
    data = query.data.split()
    user_id = int(data[1])
    action = data[2]
    
    if query.from_user.id != user_id:
        await query.answer("¡No es tu tarea!", show_alert=True)
        return

    if action == "a_conv":
        query.answer()
        buttons = ButtonMaker()
        for fmt in ["mp3", "wav", "aac", "flac"]:
            buttons.ibtn(fmt.upper(), f"vt {user_id} set_audio {fmt}")
        buttons.ibtn("⬅️ Volver", f"vt {user_id} back")
        await edit_message(query.message, "<b>🎵 Selecciona Formato de Audio</b>", buttons.build_menu(2))
    
    elif action == "cancel":
        await query.message.delete()

# Registro del handler de botones
bot.add_handler(CallbackQueryHandler(vt_callback, filters=regex("^vt")))
