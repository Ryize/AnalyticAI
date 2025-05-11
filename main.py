from filters.keyword import KeywordFilter
from filters.length import LengthFilter
from aggregator import NewsAggregator

if __name__ == "__main__":
    keywords = ["crypto", "биткоин", "market", "доллар", "stocks", "рубли"]
    keyword_filter = KeywordFilter(keywords)
    length_filter = LengthFilter(min_length=20)
    keyword_filter.set_next(length_filter)

    aggregator = NewsAggregator(
        sources=["rftoday", "blockchair", "tradingview"],
        filters=keyword_filter,
    )

    for headline in aggregator.get_news():
        print(f"- {headline}")
