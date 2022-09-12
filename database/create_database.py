from peewee import SqliteDatabase, Model, CharField, IntegerField, ForeignKeyField, DateField


db = SqliteDatabase("request_history.db")


class User(Model):
    name = CharField()
    age = IntegerField()
    country = CharField()
    city = CharField()
    phone_number = IntegerField(unique=True)

    class Meta:
        database = db


class Request(Model):
    user_id = ForeignKeyField(User, backref='request')
    name = CharField()
    lang = CharField(5)
    curr = CharField(3)
    location = CharField()
    rooms_amount = IntegerField()
    people_count = IntegerField()
    check_in = DateField(formats=['%Y-%m-%d'])
    check_out = DateField(formats=['%Y-%m-%d'])
    hotels_count = IntegerField()
    price_range = CharField(null=True)
    distance_range = CharField(null=True)

    class Meta:
        database = db


class Hotel(Model):
    request_id = ForeignKeyField(Request, backref='hotel')
    hotel_id = IntegerField()
    name = CharField()
    star_rating = IntegerField()
    address = CharField()
    price = CharField()

    class Meta:
        database = db


class Landmark(Model):
    hotel_id = ForeignKeyField(Hotel, backref='landmark')
    name = CharField()
    distance = CharField()

    class Meta:
        database = db


class Photo(Model):
    hotel_id = ForeignKeyField(Hotel, backref='photo')
    photo_url = CharField()

    class Meta:
        database = db


db.create_tables([User, Request, Hotel, Landmark, Photo])