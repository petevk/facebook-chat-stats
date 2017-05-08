from collections import defaultdict
import itertools
import sqlite3
from textblob import TextBlob
from message import Message
from sentiment_message import SentimentMessage

def get_all_messages(db_name):
  conn = sqlite3.connect("FacebookChatHistory.db")
  co = conn.cursor()
  res = co.execute("select * from history")
  return (Message(*attrs) for attrs in res)


def fetch_from_generator(gen, n):
  top_n_gen = itertools.islice(gen, n)
  return top_n_gen

def create_sentiment_message(message):
  sentiment = TextBlob(message.text).sentiment.polarity
  return SentimentMessage(sentiment, message)

if __name__ == "__main__":
  messages = get_all_messages("FacebookChatHistory.db")
  sentiments = (create_sentiment_message(message) for message in messages if message.is_plaintext())
  sentiment_sums = defaultdict(int)
  total_messages = defaultdict(int)
  for sm in sentiments:
    total_messages[sm.message.author] += 1
    sentiment_sums[sm.message.author] += sm.sentiment
  average_sentiments = [(author, sentiment_sums[author] / total_messages[author]) for author in total_messages.keys()]
  for author, average_sentiment in sorted(average_sentiments, key=lambda x: x[1]):
    print("{}: {}".format(author, average_sentiment))
  # print(sentiment_sums)
  # sorted_sm = sorted(sentiments, key=lambda sm: -sm.sentiment)
  # for sm in fetch_from_generator(sorted_sm, 50):
  #   print("{}: {}".format(sm.sentiment, sm.message.text))
