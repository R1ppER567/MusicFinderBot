from asyncio import to_thread

from aiogram import Router, types, filters, F

from services.audio_finder import search_music
from services.audio_downloader import download_audio
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
    query = message.text.strip()
    tracks = await to_thread(search_music, query)
    
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


@user_router.callback_query(F.data.startswith('download:'))
async def download_handler(callback: types.CallbackQuery):
    video_id = callback.data.split('download:')[1]
    url = f'https://music.youtube.com/watch?v={video_id}'

    await callback.message.answer('Downloading track, please wait...')

    result, error = await to_thread(download_audio, url)

    if error:
        await callback.message.answer(error)
        return None
    
    title = result['title']
    duration = result['duration']
    audio = result['audio']

    await callback.message.answer_audio(
        audio=types.BufferedInputFile(
            file=audio, filename=f'{title}.aac'
        ), 
        title=title, 
        duration=duration
    )


@user_router.callback_query(F.data.in_({"forward", "back"}))
async def pagination_handler(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer('The pagination buttons don\'t work yet')
