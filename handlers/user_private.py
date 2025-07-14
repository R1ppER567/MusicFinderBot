from aiogram import Router, types, filters, F

user_private_router = Router()


@user_private_router.message(filters.CommandStart())
async def command_start_hanlder(msg: types.Message):
    await msg.answer(
        'To find an audio recording, send the name of song of artist'
    )
