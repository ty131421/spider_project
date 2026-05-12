import scrapy

class MovieItem(scrapy.Item):
    rank = scrapy.Field()
    title = scrapy.Field()
    title_en = scrapy.Field()
    score = scrapy.Field()
    vote_num = scrapy.Field()
    director = scrapy.Field()
    actors = scrapy.Field()
    intro = scrapy.Field()
    year = scrapy.Field()
    duration = scrapy.Field()
    genre = scrapy.Field()
    imdb = scrapy.Field()
    url = scrapy.Field()
    poster_url = scrapy.Field()

class CommentItem(scrapy.Item):
    movie_id = scrapy.Field()
    user_name = scrapy.Field()
    comment_score = scrapy.Field()
    comment_content = scrapy.Field()
    comment_time = scrapy.Field()