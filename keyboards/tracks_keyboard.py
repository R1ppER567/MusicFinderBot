from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from common import consts


def get_tracks_keyboard(
        tracks: list[dict],
        page: int
    ) -> types.InlineKeyboardMarkup:
    start = page * consts.TRACKS_PER_PAGE - consts.TRACKS_PER_PAGE
    end = start + consts.TRACKS_PER_PAGE
    current_tracks = tracks[start:end]

    keyboard = InlineKeyboardBuilder()
    for index, track in enumerate(current_tracks):
        title = f'{track['duration']} | {track['title']} - {track['artists'][0]['name']}'
        keyboard.row(types.InlineKeyboardButton(
            text=title,
            callback_data=f'track_{index}'
        ))

    nav_buttons = (
        types.InlineKeyboardButton(text="⬅️", callback_data="back"),
        types.InlineKeyboardButton(text=f"{page}/{consts.LAST_PAGE}", callback_data="no_data"),  # this is an information button, it is not processed
        types.InlineKeyboardButton(text="➡️", callback_data="forward")
    )
    keyboard.row(*nav_buttons)

    return keyboard.as_markup()
