from bot.helper.telegram_helper.button_maker import ButtonMaker

async def get_vtool_buttons(user_id):
    buttons = ButtonMaker()
    # Fila 1
    buttons.ibtn("Encode", f"vt {user_id} encode")
    buttons.ibtn("Convert", f"vt {user_id} convert")
    # Fila 2
    buttons.ibtn("Audio Converter 🎵", f"vt {user_id} a_conv")
    buttons.ibtn("Extract", f"vt {user_id} extract")
    # Fila 3
    buttons.ibtn("Watermark", f"vt {user_id} wmark")
    buttons.ibtn("X Cancel", f"vt {user_id} cancel")
    
    return buttons.build_menu(2)
