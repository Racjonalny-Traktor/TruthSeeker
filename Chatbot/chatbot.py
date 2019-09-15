from fbchat import Client
from fbchat.models import *
from getpass import getpass

email = input()
password = getpass()

class CustomClient(Client):
    def onMessage(self, mid, author_id, message_object, thread_id, thread_type, ts, metadata, msg, **kwargs):
        if author_id != self.uid:
            if message_object.text.lower().startswith('http'):
                domain = 'wyborcza.pl'
                client.send(Message(text=f'''This article seems to be a bit old!\nSome keywords may signalize this article being manipulative!\nYou may want check out what the opposite political option thinks: example.pl/test/test'''), thread_id=thread_id,
                            thread_type=ThreadType.USER)
                # Only a mock but it is easily pluggable to REST used by chrome extension, unfortunatelly I have no time for this
            else:
                client.send(Message(text='Hey, if you want send me link to an article to check!'), thread_id=thread_id, thread_type=ThreadType.USER)

client = CustomClient(email, password)
client.listen()















