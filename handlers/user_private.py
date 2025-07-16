from aiogram import Router, types, filters, F

from services.audio_finder import seatch_music
from keyboards.tracks_keyboard import get_tracks_keyboard
from common import consts

user_router = Router()


@user_router.message(filters.CommandStart())
async def command_start_hanlder(msg: types.Message):
    await msg.answer(
        'To find an audio recording, send the name of song of artist'
    )


@user_router.message(F.text)
async def query_handler(message: types.Message):
    tracks = seatch_music(query=message.text)
    
    if not tracks:
        await message.answer('Nothing found')
        return None
    
    await message.answer(
        'Select track:',
        reply_markup=get_tracks_keyboard(
            tracks=tracks,
            page=consts.FIRST_PAGE
        )
    )
