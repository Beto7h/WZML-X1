from pyrogram.filters import regex
from pyrogram.handlers import CallbackQueryHandler
from bot import bot, task_dict, task_dict_lock
from ..helper.telegram_helper.message_utils import edit_message, send_message
from ..helper.telegram_helper.button_maker import ButtonMaker

async def video_tool_cb(client, query):
    data = query.data.split()
    user_id = int(data[1])
    action = data[2]
    
    # Solo el dueño de la tarea puede tocar los botones
    if query.from_user.id != user_id:
        return await query.answer("¡Esta no es tu tarea!", show_alert=True)

    if action == "a_conv":
        await query.answer()
        buttons = ButtonMaker()
        # Formatos que soporta tu bot
        for fmt in ["mp3", "wav", "aac", "flac", "m4a"]:
            buttons.ibtn(fmt.upper(), f"vt {user_id} set_aud {fmt}")
        buttons.ibtn("⬅️ Volver", f"vt {user_id} main")
        
        await edit_message(query.message, "<b>🎵 Conversor de Audio</b>\nSelecciona el formato de salida:", buttons.build_menu(3))

    elif action == "set_aud":
        selected_format = data[3]
        # Buscamos la tarea en el diccionario para aplicarle el cambio
        # Nota: En los menús interactivos, usualmente se guarda la config 
        # antes de que la descarga empiece realmente o se aplica al objeto Mirror.
        await query.answer(f"Configurado a {selected_format.upper()}", show_alert=True)
        
        # Aquí es donde le decimos al bot: "Cuando termines, convierte a este formato"
        # Necesitas una forma de pasar 'selected_format' a tu clase Mirror.
        # Una forma común es editar el mensaje original o guardar en un diccionario temporal.
        
    elif action == "cancel":
        await query.answer("Tarea cancelada")
        await query.message.delete()

# Registramos el manejador de los botones que empiezan con "vt"
bot.add_handler(CallbackQueryHandler(video_tool_cb, filters=regex("^vt")))
