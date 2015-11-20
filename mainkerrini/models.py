import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.usertype import UserType
from cassandra.cqlengine.models import Model


class User(Model):
    user_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    reputation = columns.Integer(primary_key=True, default=0)
    username = columns.Text(required=True, max_length=50)
    password = columns.Text(required=True, min_length=6, max_length=50)
    first_name = columns.Text(required=True, max_length=50)
    last_name = columns.Text(required=True, max_length=50)


class Picture(Model):
    pic_uuid = columns.UUID(primary_key=True, default=uuid.uuid4)
    data = columns.Blob()
    user_id = columns.UUID()


# This is a user defined type
class Link(UserType):
    link_id = columns.UUID(primary_key=True)
    url = columns.Text()
    comment = columns.Text(max_length=200)


class Video(Model):
    video_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    correctness = columns.Decimal(default=0.0, primary_key=True)
    user_id = columns.UUID()
    date_created = columns.DateTime(index=True)
    title = columns.Text(required=True, max_length=500)
    description = columns.Text(min_length=1, max_length=1000)
    data = columns.Blob(required=True)
    links = columns.List(value_type=columns.UserDefinedType(Link))


class Vote(Model):
    vote = columns.Set(value_type=columns.Integer)
    video_id = columns.UUID(primary_key=True)


class Playlist(Model):
    playlist_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    playlist_name = columns.Text(min_length=1, max_length=200)
    vid_order = columns.Integer(required=True, primary_key=True)
    video_id = columns.UUID()
    user_id = columns.UUID()
