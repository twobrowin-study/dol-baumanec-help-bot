from spreadsheetbot.sheets.abstract import AbstractSheetAdapter
from spreadsheetbot.sheets.users import UsersAdapterClass

from spreadsheetbot import (
    Switch,
    I18n,
    Settings,
    Keyboard,
    Users
)

from datetime import datetime

from telegram import (
    Update,
    Message,
    ReplyKeyboardRemove
)

from telegram.constants import ParseMode
from telegram.ext import ContextTypes

class IsDataAvaliableClass(AbstractSheetAdapter.AbstractFilter):
    def filter(self, message: Message) -> bool:
        return Switch.data_avaliable

class IsInactiveClass(AbstractSheetAdapter.AbstractFilter):
    def filter(self, message: Message) -> bool:
        df = self.outer_obj.as_df
        return df.loc[
            (self.outer_obj.selector(message.chat_id)) &
            (df.is_active == I18n.yes)
        ].empty

UsersAdapterClass.IsDataAvaliableFilter   = IsDataAvaliableClass(outer_obj=Users)
UsersAdapterClass.IsDataUnavaliableFilter = ~Users.IsDataAvaliableFilter
UsersAdapterClass.IsInactiveFilter        = IsInactiveClass(outer_obj=Users)

UsersAdapterClass.IsActiveFilter                    = Users.IsRegisteredFilter & ~Users.IsInactiveFilter
UsersAdapterClass.DataAvaliableRegistrationFilter   = Users.PrivateChatFilter & Users.IsDataAvaliableFilter   & Users.IsNotRegisteredFilter
UsersAdapterClass.DataUnavaliableRegistrationFilter = Users.PrivateChatFilter & Users.IsDataUnavaliableFilter & Users.IsNotRegisteredFilter
UsersAdapterClass.DataUnavaliableFilter             = Users.PrivateChatFilter & (Users.IsDataUnavaliableFilter | Users.IsInactiveFilter) & Users.IsRegisteredFilter

UsersAdapterClass.DataAvaliableInputFilter = Users.IsDataAvaliableFilter & Users.IsActiveFilter
UsersAdapterClass.KeyboardDataAvaliableKeyInputFilter = Users.DataAvaliableInputFilter & Users.InputInKeyboardKeysClass(outer_obj=Users)

async def start_registration_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_markdown(Settings.start_template, reply_markup=Keyboard.reply_keyboard)
    await self.register_user(update.effective_chat.id, update.effective_chat.username)
UsersAdapterClass.start_registration_handler = start_registration_handler

async def start_registration_on_data_unavalible_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_markdown(Settings.data_unavaliable, reply_markup=ReplyKeyboardRemove())
    await self.register_user(update.effective_chat.id, update.effective_chat.username)
UsersAdapterClass.start_registration_on_data_unavalible_handler = start_registration_on_data_unavalible_handler

async def register_user(self, uid: str|int, username: str) -> None:
    await self._batch_update_or_create_record(uid,
        datetime      = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        username      = username,
        is_bot_banned = I18n.no,
        is_active     = I18n.yes,
    )
UsersAdapterClass.register_user = register_user

async def data_unavalible_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_markdown(Settings.data_unavaliable, reply_markup=ReplyKeyboardRemove())
UsersAdapterClass.data_unavalible_handler = data_unavalible_handler

async def keyboard_key_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard_row = Keyboard.get(update.message.text)
    reply_keyboard = Keyboard.reply_keyboard
    if keyboard_row.function == Keyboard.SCOUTS_FUNCTION:
        reply_keyboard = Keyboard.sqads_keyboard
    await update.message.reply_markdown(keyboard_row.text_markdown, reply_markup=reply_keyboard)
UsersAdapterClass.keyboard_key_handler = keyboard_key_handler

async def squads_callback_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    squad = update.callback_query.data.removeprefix(Keyboard.CALLBACK_SCOUTS_PREFIX)
    text = Keyboard.scouts_row[f"squad_{squad}"]
    await update.callback_query.message.reply_markdown(text, reply_markup=Keyboard.reply_keyboard)
UsersAdapterClass.squads_callback_handler = squads_callback_handler