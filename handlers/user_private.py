from asyncio import to_thread

from aiogram import Router, types, filters, F

from services.audio_finder import search_music
from services.audio_downloader import download_audio
from keyboards.tracks_keyboard import get_tracks_keyboard
from db.redis_client import RedisClient
from db import session_storage 
from common import consts

user_router = Router()


@user_router.message(filters.CommandStart())
async def command_start_hanlder(msg: types.Message):
    await msg.answer(
        'To find an audio recording, send the name of song of artist'
    )


@user_router.message(F.text)
async def query_handler(message: types.Message, redis: RedisClient):
    query = message.text.strip()
    tracks = await to_thread(search_music, query)
    
    if not tracks:
        await message.answer('Nothing found')
        return None
    
    keyboard = await message.answer(
        'Select track:',
        reply_markup=get_tracks_keyboard(
            tracks=tracks,
            page=consts.FIRST_PAGE
        )
    )

    await session_storage.save_tracks(redis, 
        user_id=message.from_user.id,
        message_id=keyboard.message_id,
        tracks=tracks,
        page= consts.FIRST_PAGE
    )


@user_router.callback_query(F.data.startswith('download:'))
async def download_handler(callback: types.CallbackQuery):
    video_id = callback.data.split('download:')[1]
    url = f'https://music.youtube.com/watch?v={video_id}'

    downloading_msg = await callback.message.answer(
        'Downloading track, please wait...'
    )

    result, error = await to_thread(download_audio, url)

    if error:
        await callback.message.answer(error)
        return None
    
    title = result['title']
    duration = result['duration']
    audio = result['audio']

    await callback.message.answer_audio(
        audio=types.BufferedInputFile(
            file=audio, filename=title + consts.AUDIO_FORMAT
        ), 
        title=title, 
        duration=duration
    )
    await downloading_msg.delete()
    

@user_router.callback_query(F.data.in_({"forward", "back"}))
async def pagination_handler(callback: types.CallbackQuery, redis: RedisClient):
    user_id = callback.from_user.id
    message_id = callback.message.message_id
    result = await session_storage.get_tracks(redis, user_id, message_id)
    
    if result is None:
        await callback.answer(
            'The data out of range! Make new request',
            show_alert=True
        )
        return None
    tracks, page = result

    if callback.data == 'forward':
        current_page = min(page + 1, consts.LAST_PAGE)
    else:
        current_page = max(page - 1, consts.FIRST_PAGE)

    if current_page == page:
        await callback.answer()
        return None

    await session_storage.update_page(redis, user_id, message_id, page=current_page)
    keyboard = get_tracks_keyboard(tracks, current_page)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


@user_router.callback_query(F.data == 'no_data')
async def info_button_handler(callback: types.CallbackQuery):
    await callback.answer()
