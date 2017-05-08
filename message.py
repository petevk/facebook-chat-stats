class Message(object):
  def __init__(self, thread_id, timestamp, author, text):
    self.thread_id = thread_id
    self.timestamp = timestamp
    self.author = author
    self.text = text

  def is_plaintext(self):
    return not self.text.startswith("http")
