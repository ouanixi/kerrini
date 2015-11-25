import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.usertype import UserType
from cassandra.cqlengine.models import Model
import bcrypt
from json import JSONEncoder
from uuid import UUID

JSONEncoder_olddefault = JSONEncoder.default

def JSONEncoder_newdefault(self, o):
    if isinstance(o, UUID): return str(o)
    return JSONEncoder_olddefault(self, o)
JSONEncoder.default = JSONEncoder_newdefault

class User(Model):
    user_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    reputation = columns.Integer(primary_key=True, default=0)
    first_name = columns.Text(required=True, max_length=50)
    last_name = columns.Text(required=True, max_length=50)
    bio = columns.Text(max_length=500)

class UserLogin(Model):
    username = columns.Text(required=True, max_length=50, primary_key=True)
    email = columns.Text(required=True, max_length=100, index=True)
    password = columns.Text(required=True, min_length=6, max_length=200)
    user_id = columns.UUID()

    def encrypt(self):
        return bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())

    def save(self, *args, **kwargs):
        #self.password = self.encrypt().decode('utf-8')
        self.email = self.email.lower()
        super(UserLogin, self).save(*args, **kwargs)

class Picture(Model):
    pic_uuid = columns.UUID(primary_key=True, default=uuid.uuid4)
    data = columns.Blob()
    user_id = columns.UUID()


# This is a user defined type
class Link(UserType):
    link_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    url = columns.Text()
    comment = columns.Text(max_length=200)
    time_tag = columns.Text(min_length=2, max_length=10)


class Video(Model):
    video_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    language = columns.Text(min_length=1, max_length=100, default='English', partition_key=True)
    correctness = columns.Decimal(default=0.0, primary_key=True)
    video_codec = columns.Text()
    user_id = columns.UUID()
    date_created = columns.DateTime(index=True)
    title = columns.Text(required=True, max_length=500)
    description = columns.Text(min_length=1, max_length=1000)
    data = columns.Text(required=True)
    links = columns.List(value_type=columns.UserDefinedType(Link))


class Vote(Model):
    vote = columns.Set(value_type=columns.Integer)
    video_id = columns.UUID(primary_key=True)


class Playlist(Model):
    playlist_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    playlist_name = columns.Text(min_length=1, max_length=200)
    vid_order = columns.Integer(required=True, primary_key=True)
    video_id = columns.UUID()
    user_id = columns.UUID(primary_key=True)


class Viewing(Model):
    video_id = columns.UUID(primary_key=True)
    user_id = columns.UUID(primary_key=True)
    stopped_at = columns.Text(min_length=2, max_length=10)
