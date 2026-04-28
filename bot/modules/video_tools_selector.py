from pyrogram.filters import regex
from pyrogram.handlers import CallbackQueryHandler
from bot import bot
from ..helper.telegram_helper.message_utils import edit_message, delete_message
from ..helper.telegram_helper.button_maker import ButtonMaker

async def vt_callback_handler(client, query):
    data = query.data.split()
    user_id = int(data[1])
    action = data[2]

    # Seguridad: Solo el dueño del comando puede usar el menú
    if query.from_user.id != user_id:
        await query.answer("¡Este menú no es para ti!", show_alert=True)
        return

    if action == "a_conv":
        # Menú secundario para elegir formato de audio
        await query.answer()
        buttons = ButtonMaker()
        for fmt in ["mp3", "m4a", "wav", "flac"]:
            buttons.ibtn(fmt.upper(), f"vt {user_id} set_aud {fmt}")
        buttons.ibtn("⬅️ Volver", f"vt {user_id} back")
        await edit_message(query.message, "<b>🎵 Conversor de Audio</b>\nSelecciona el formato de salida:", buttons.build_menu(2))

    elif action == "set_aud":
        # AQUÍ SE RE-LANZA EL PROCESO CON EL NUEVO FLAG
        selected_fmt = data[3]
        await query.answer(f"Configurado a {selected_fmt.upper()}", show_alert=True)
        
        # Obtenemos el mensaje original (el que tenía el link)
        message = query.message.reply_to_message
        
        # Limpiamos el texto para quitar el -vt y poner el -ca (convert audio)
        old_text = message.text
        new_text = old_text.replace("-vt", f"-ca {selected_fmt}")
        message.text = new_text
        
        # Borramos el menú y relanzamos Mirror
        await delete_message(query.message)
        
        # Importación local para evitar errores de importación circular
        from .mirror_leech import Mirror
        await Mirror(client, message, is_leech=True).new_event()

    elif action == "back":
        # Lógica para regresar al menú principal que ya tienes
        await query.answer()
        # Aquí repetirías los botones que ya tienes en tu mirror_leech.py
        # ... (botones de Encode, Convert, etc.)

    elif action == "cancel":
        await query.answer("Operación cancelada")
        await delete_message(query.message)

# Registro del handler para que el bot "escuche" los botones
bot.add_handler(CallbackQueryHandler(vt_callback_handler, filters=regex("^vt")))
