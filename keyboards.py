from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def kb_set_language():
    keyboard = [[InlineKeyboardButton('Русский', callback_data='Ru')],
                [InlineKeyboardButton('English', callback_data='En')]]
    return InlineKeyboardMarkup(keyboard)


def kb_cryptocurrency():
    keyboard = [[InlineKeyboardButton('Bitcoin', callback_data='BTC')],
                [InlineKeyboardButton('Ethereun', callback_data='ETH')],
                [InlineKeyboardButton('Ripple', callback_data='XRP')]]
    return InlineKeyboardMarkup(keyboard)