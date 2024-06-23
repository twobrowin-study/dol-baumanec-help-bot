from spreadsheetbot.sheets.abstract import AbstractSheetAdapter

async def _next_available_row(self: AbstractSheetAdapter) -> int:
    str_list = list(filter(None, await self.wks.col_values(1)))
    return len(str_list)+1
AbstractSheetAdapter._next_available_row = _next_available_row