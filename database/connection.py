from peewee import *



# db = SqliteDatabase('database/botdb.db')
db = PostgresqlDatabase('poisk_muz', user='postgres', host='localhost', password='888888', port='5432')
# db = PostgresqlDatabase('poisk_muz', user='mirabbos', host='localhost', password='888888', port='5432')


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    user_id = BigAutoField()
    first_name = CharField(max_length=100)
    lang = CharField(max_length=20, default='uz')
    class Meta:
        db_table = 'users'


class Songs_Db(BaseModel):
    song_id = CharField(unique=True, primary_key=True)
    song_token = CharField(max_length=300)
    song_title = CharField()
    song_subtitle = CharField(default='@poiskmuzikabot')
    song_size = CharField(max_length=100)
    song_duration = CharField(max_length=100)

    class Meta:
        db_table = 'songs_db'



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



