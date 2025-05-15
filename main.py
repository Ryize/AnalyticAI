from filters.keyword import KeywordFilter
from filters.length import LengthFilter
from aggregator import NewsAggregator
from ai.chatgpt_requests_adapter import ChatGPTRequestsAdapter
from filters.logger_decorator import LoggingDecorator

if __name__ == "__main__":
    # 1. цепочка фильтров

    # Оборачиваем каждый фильтр декоратором
    keyword_filter = LoggingDecorator(
        KeywordFilter(['доллар', 'cripto', 'bitcoin', 'ethereum']))
    length_filter = LoggingDecorator(LengthFilter(min_length=10))

    keyword_filter.set_next(length_filter)

    # 2. агрегатор собирает и фильтрует
    aggregator = NewsAggregator(
        sources=["rftoday", "blockchair", "tradingview"],
        filters=keyword_filter
    )
    headlines = aggregator.get_news()

    # 3. адаптер анализирует
    adapter = ChatGPTRequestsAdapter()
    analyzed = adapter.analyze(headlines)

    for item in analyzed:
        print(item["headline"])
        print(item["sentiment"], end="\n\n")
