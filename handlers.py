import logging
import os
from io import BytesIO
from aiogram import Router
from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    FSInputFile,
    ReplyKeyboardMarkup,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from config import ADMIN_IDS # Your database operations

router = Router()
logger = logging.getLogger(__name__)

def is_admin(user_id: int):
    return user_id in ADMIN_IDS
    #return user_id == 5597902483

# ADMIN keyboard
def get_admin_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Testlar")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

# USER keyboard
def get_user_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="📝 Test ishlash")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

@router.message(Command("start"))
async def start_command(message: types.Message):
    try:
        # user_id = message.from_user.id
        # channel_username = '@matematikadanonlinetestlar'  # masalan: '@mychannel'
        #
        # try:
        #     member = await message.bot.get_chat_member(channel_username, user_id)
        #     if member.status not in ("member", "administrator", "creator"):
        #         invite_link = f"https://t.me/{channel_username.lstrip('@')}"
        #         await message.answer(
        #             f"Botdan foydalanishdan oldin quyidagi kanalga a'zo bo'lishingiz kerak:\n\n👉 {invite_link}\n\nA'zo bo‘lgach, /start buyrug'ini qayta yuboring."
        #         )
        #         return
        # except Exception as e:
        #     await message.answer(f"A'zolikni tekshirib bo‘lmadi. Iltimos, keyinroq urinib ko‘ring.")
        #     return

        photo_path = "images/welcome.png"
        if not os.path.exists(photo_path):
            raise FileNotFoundError(f"Rasm topilmadi: {photo_path}")

        photo = FSInputFile(photo_path)
        if is_admin(message.from_user.id):
            caption = "Assalomu alaykum, Admin!\n\nQuyidagi tugmadan foydalaning:"
            reply_markup = get_admin_keyboard()
        else:
            caption = "Assalomu alaykum!\n\nTest javoblarini yuborish uchun quyidagi '📝 Test ishlash' tugmasini bosing:\n\n❗️❗️❗️ Eslatib o'tamiz bot hozir test rejimida ishlayapti. Xato va kamchiliklar uchun oldindan uzr so'raymiz.❗️❗️❗"
            reply_markup = get_user_keyboard()

        await message.answer_photo(photo=photo, caption=caption, reply_markup=reply_markup)

    except FileNotFoundError as e:
        logger.warning(str(e))
        await message.answer(
            "Xush kelibsiz!\n\nQuyidagi tugmadan foydalaning:",
            reply_markup=get_admin_keyboard() if is_admin(message.from_user.id) else get_user_keyboard()
        )
    except Exception as e:
        logger.error(f"Start commandda xato: {e}", exc_info=True)
        await message.answer(
            "Xush kelibsiz! Botda xatolik yuz berdi.",
            reply_markup=get_admin_keyboard() if is_admin(message.from_user.id) else get_user_keyboard()
        )
#start handler
@router.message(F.text == "Testlar")
async def admin_test(message: Message, state: FSMContext):
    # user_id = message.from_user.id
    # channel_username = '@matematikadanonlinetestlar'  # masalan: '@mychannel'
    #
    # try:
    #     member = await message.bot.get_chat_member(channel_username, user_id)
    #     if member.status not in ("member", "administrator", "creator"):
    #         invite_link = f"https://t.me/{channel_username.lstrip('@')}"
    #         await message.answer(
    #             f"Botdan foydalanishdan oldin quyidagi kanalga a'zo bo'lishingiz kerak:\n\n👉 {invite_link}\n\nA'zo bo‘lgach, /start buyrug'ini qayta yuboring."
    #         )
    #         return
    # except Exception as e:
    #     await message.answer(f"A'zolikni tekshirib bo‘lmadi. Iltimos, keyinroq urinib ko‘ring.")
    #     return

    telegram_id = message.from_user.id + 4321
    url = f"https://exam-elf.web.app?telegram_id={telegram_id}"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Testlar", url=url)]
        ]
    )

    await message.answer("Shu yerga kiring:", reply_markup=keyboard)


#####---------------------------USER--------------------------------------------
#start handler
@router.message(F.text == "📝 Test ishlash")
async def start_test(message: Message, state: FSMContext):
    # user_id = message.from_user.id
    # channel_username = '@matematikadanonlinetestlar'  # masalan: '@mychannel'
    #
    # try:
    #     member = await message.bot.get_chat_member(channel_username, user_id)
    #     if member.status not in ("member", "administrator", "creator"):
    #         invite_link = f"https://t.me/{channel_username.lstrip('@')}"
    #         await message.answer(
    #             f"Botdan foydalanishdan oldin quyidagi kanalga a'zo bo'lishingiz kerak:\n\n👉 {invite_link}\n\nA'zo bo‘lgach, /start buyrug'ini qayta yuboring."
    #         )
    #         return
    # except Exception as e:
    #     await message.answer(f"A'zolikni tekshirib bo‘lmadi. Iltimos, keyinroq urinib ko‘ring.")
    #     return

    telegram_id = message.from_user.id + 4321
    url = f"https://exam-elf.web.app?telegram_id={telegram_id}"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Testni boshlash", url=url)]
        ]
    )

    await message.answer("Testni shu yerda boshlang:", reply_markup=keyboard)



@router.message()
async def handle_unknown_messages(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    channel_username = '@matematikadanonlinetestlar'  # masalan: '@mychannel'

    try:
        member = await message.bot.get_chat_member(channel_username, user_id)
        if member.status not in ("member", "administrator", "creator"):
            invite_link = f"https://t.me/{channel_username.lstrip('@')}"
            await message.answer(
                f"Botdan foydalanishdan oldin quyidagi kanalga a'zo bo'lishingiz kerak:\n\n👉 {invite_link}\n\nA'zo bo‘lgach, /start buyrug'ini qayta yuboring."
            )
            return
    except Exception as e:
        await message.answer(f"A'zolikni tekshirib bo‘lmadi. Iltimos, keyinroq urinib ko‘ring.")
        return

    # Default message for all other cases

    if is_admin(message.from_user.id):
        await message.answer(
            "❌ Noto'g'ri buyruq!\n\n"
            "Iltimos, quyidagilardan birini tanlang:",
            reply_markup=get_admin_keyboard()
        )
    else:
        await message.answer(
            "❌ Noto'g'ri buyruq!\n\n"
            "Test ishlash uchun quyidagi tugmani bosing:",
            reply_markup=get_user_keyboard()
        )