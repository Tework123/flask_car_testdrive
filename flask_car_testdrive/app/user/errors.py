
class HtmlError(Exception):
    error_place = 'Html error'


class HtmlDbError(HtmlError):
    error_type = "Db error"

