from abstract.parser import NewsFilter
from logger import Logger


class LoggingDecorator(NewsFilter):
    """
    Классический Декоратор, оборачивающий другой объект NewsFilter
    и логирующий вызов его метода handle().
    """

    def __init__(self, wrapped: NewsFilter):
        self._wrapped = wrapped
        self._logger = Logger()

    def set_next(self, filter_: NewsFilter):
        self._wrapped.set_next(filter_)
        return self

    def handle(self, headlines: list[str]) -> list[str]:
        self._logger.log(
            f"[LoggingDecorator] Входных заголовков: {len(headlines)}")
        result = self._wrapped.handle(headlines)
        self._logger.log(f"[LoggingDecorator] После фильтра: {len(result)}")
        return result

    def _apply_filter(self, headlines: list[str]) -> list[str]:
        return self._wrapped.handle(headlines)
