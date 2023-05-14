from spreadsheetbot.sheets.keyboard import KeyboardAdapterClass

from spreadsheetbot.sheets.i18n import I18n

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

import numpy as np

KeyboardAdapterClass.CALLBACK_SCOUTS_TEMPLATE = 'keyboard_scouts_callback_{squad}'
KeyboardAdapterClass.CALLBACK_SCOUTS_PATTERN  = 'keyboard_scouts_callback_*'
KeyboardAdapterClass.CALLBACK_SCOUTS_PREFIX   = 'keyboard_scouts_callback_'

KeyboardAdapterClass.default_pre_async_init = KeyboardAdapterClass._pre_async_init
async def _pre_async_init(self):
    await self.default_pre_async_init()
    self.SCOUTS_FUNCTION = I18n.scouts
KeyboardAdapterClass._pre_async_init = _pre_async_init

KeyboardAdapterClass.default_process_df_update = KeyboardAdapterClass._process_df_update
async def _process_df_update(self):
    await self.default_process_df_update()
    self.scouts_row = self.as_df.loc[
        self.as_df.function == self.SCOUTS_FUNCTION
    ].iloc[0]
    self.squads = self.scouts_row.squads.split(';')
    self.sqads_keyboard = InlineKeyboardMarkup([
        [ 
            InlineKeyboardButton(squad, callback_data=self.CALLBACK_SCOUTS_TEMPLATE.format(squad=squad))
            for squad in (self.squads[idx:idx+4] if idx+4<len(self.squads) else self.squads[idx:])
        ]
        for idx in range(0,len(self.squads),4)
    ])
KeyboardAdapterClass._process_df_update = _process_df_update