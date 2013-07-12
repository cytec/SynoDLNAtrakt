from sqlalchemy import create_engine, MetaData, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


engine = create_engine(
    'postgresql+pg8000://admin:933461@192.168.0.55/mediaserver',
    encoding='utf-8',
    convert_unicode=True,
    echo=False,
    pool_recycle=3600
)

metadata = MetaData()

Base = declarative_base()


# CREATE TABLE video
# (
#   id serial NOT NULL,
#   path text NOT NULL,
#   title text NOT NULL,
#   filesize int8 NOT NULL DEFAULT 0,
#   album text,
#   container_type text NOT NULL,
#   video_codec text,
#   frame_bitrate int4,
#   frame_rate_num int4,
#   frame_rate_den int4,
#   video_bitrate int4,
#   video_profile int4,
#   video_level int4,
#   resolutionX int4,
#   resolutionY int4,
#   audio_codec text,
#   audio_bitrate int4,
#   frequency int4,
#   channel int4,
#   duration int4,
#   date timestamp,
#   mdate timestamp,
#   fs_uuid text,
#   fs_online boolean DEFAULT TRUE,
#   CONSTRAINT video_pkey PRIMARY KEY (id)
# )

class Video(Base):
    __tablename__ = 'video'

    id = Column(Integer, primary_key=True)  # synoindex id
    path = Column(String)                   # path to file
    title = Column(String)                  # title of the video file
    filesize = Column(Integer)              # filesize in byte
    album = Column(String)                  # folder name of file...
    container_type = Column(String)         # avi, mkv, "matroska,webm" etc
    video_codec = Column(String)            # mpeg4, h264 etc
    frame_bitrate = Column(Integer)         # ???
    frame_rate_num = Column(Integer)        # fps (25, 30) etc
    frame_rate_den = Column(Integer)        # ???
    video_bitrate = Column(Integer)         # ???
    video_profile = Column(Integer)         # ???
    video_level = Column(Integer)           # ???
    resolutionx = Column(Integer)           # width
    resolutiony = Column(Integer)           # height
    audio_codec = Column(String)            # ac3, dts, mp3 etc
    audio_bitrate = Column(Integer)         # bitrate of audio stream
    frequency = Column(Integer)             # ???
    channel = Column(Integer)               # audio channels 2, 6 etc
    duration = Column(Integer)              # duration in seconds
    date = Column(Integer)                  # add date timestamp
    mdate = Column(Integer)                 # modifiy date timestamp
    fs_uuid = Column(Integer)               # ???
    fs_online = Column(Integer)             # file is online (True/False)

    def __init__(
            self, path, duration, date, mdate, title, filesize, album, container_type, video_codec, frame_bitrate,
            frame_rate_num, frame_rate_den, video_bitrate, video_profile, video_level, resolutionx, resolutiony,
            audio_codec, audio_bitrate, frequency, channel, fs_uuid, fs_online
    ):
        self.path = path
        self.duration = duration
        self.date = date
        self.mdate = mdate
        self.title = title
        self.filesize = filesize
        self.album = album
        self.container_type = container_type
        self.video_codec = video_codec
        self.frame_bitrate = frame_bitrate
        self.frame_rate_num = frame_rate_num
        self.video_bitrate = video_bitrate
        self.video_profile = video_profile
        self.video_level = video_level
        self.resolutionx = resolutionx
        self.resolutiony = resolutiony
        self.audio_codec = audio_codec
        self.audio_bitrate = audio_bitrate
        self.frequency = frequency
        self.channel = channel
        self.fs_uuid = fs_uuid
        self.fs_online = fs_online

    def __repr__(self):
        return u"<Video(id:{0}, path:{1}, duration:{2}, data:{3}, mdate:{4}, title:{5}, filesize:{6} )>".format(self.id, self.path, self.duration, self.date, self.mdate, self.title, self.filesize)


Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = scoped_session(Session)
