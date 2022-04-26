from peewee import *
import datetime



# db = SqliteDatabase('database/botdb.db')
# db = PostgresqlDatabase('poisk_muz', user='postgres', host='localhost', password='888888', port='5432')
db = PostgresqlDatabase('downloader_bot', user='postgres', host='localhost', password='888888', port='5432')


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    user_id = BigAutoField()
    first_name = CharField(max_length=100)
    lang = CharField(max_length=20, default='uz')
    data = CharField(default=datetime.datetime.now().strftime("%d/%m/%Y"))
    class Meta:
        db_table = 'users'


class Channels(BaseModel):
    channel_name = CharField(max_length=150)
    channel_id = BigIntegerField(primary_key=True)
    channel_link = CharField(max_length=200)
    class Meta:
        db_table = 'channels'


class Admins(BaseModel):
    admin_id = BigIntegerField(primary_key=True)
    admin_name = CharField(max_length=100)
    class Meta:
        db_table = 'admins'


class Youtube_Videos(BaseModel):
    video_name = CharField(max_length=300)
    video_id = CharField(primary_key=True)

    class Meta:
        db_table = 'youtube_videos'


class VideosQueue(BaseModel):
    user_id = BigAutoField(primary_key=True)
    title = CharField(max_length=500)
    duration = CharField(max_length=50)
    file_path = CharField(max_length=150)
    post_id = IntegerField()
    class Meta:
        db_table = 'videos_queue'






