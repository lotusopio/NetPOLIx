"""
models_sic.py
Modelos SQLAlchemy para las entidades:
Calificacion, Genero, Director, Premio, Plataforma
"""

from sqlalchemy import (
    Column, Integer, String, Text, Date,
    ForeignKey, Table, Enum, DateTime, Float
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from sqlalchemy import create_engine
from datetime import datetime
import enum

DATABASE_URL = "mysql+mysqlconnector://root:@localhost:3307/netpolix_sic"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# ─────────────────────────────────────────────
#  ENUMS
# ─────────────────────────────────────────────

class NivelCalificacion(enum.Enum):
    EXCELENTE = "Excelente"
    BUENA     = "Buena"
    REGULAR   = "Regular"
    MALA      = "Mala"


class TipoPremio(enum.Enum):
    OSCAR        = "Oscar"
    GLOBO_DE_ORO = "Globo de Oro"
    BAFTA        = "BAFTA"
    EMMY         = "Emmy"
    OTRO         = "Otro"


# ─────────────────────────────────────────────
#  TABLAS DE ASOCIACIÓN N:M
# ─────────────────────────────────────────────

video_genero = Table(
    'video_genero', Base.metadata,
    Column('idvideo',  Integer, ForeignKey('video.idvideo'),   primary_key=True),
    Column('idgenero', Integer, ForeignKey('genero.idgenero'), primary_key=True),
)

video_plataforma = Table(
    'video_plataforma', Base.metadata,
    Column('idvideo',      Integer, ForeignKey('video.idvideo'),           primary_key=True),
    Column('idplataforma', Integer, ForeignKey('plataforma.idplataforma'), primary_key=True),
)

video_premio = Table(
    'video_premio', Base.metadata,
    Column('idvideo',  Integer, ForeignKey('video.idvideo'),   primary_key=True),
    Column('idpremio', Integer, ForeignKey('premio.idpremio'), primary_key=True),
)

video_director = Table(
    'video_director', Base.metadata,
    Column('idvideo',    Integer, ForeignKey('video.idvideo'),         primary_key=True),
    Column('iddirector', Integer, ForeignKey('director.iddirector'),   primary_key=True),
)


# ─────────────────────────────────────────────
#  MODELOS
# ─────────────────────────────────────────────

class Video(Base):
    __tablename__ = 'video'

    idvideo        = Column(Integer, primary_key=True, autoincrement=True)
    titulo         = Column(String(255), nullable=False)
    anio_produccion = Column(Integer)
    duracion       = Column(Integer)
    descripcion    = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    calificaciones = relationship("Calificacion", back_populates="video", cascade="all, delete-orphan")
    generos        = relationship("Genero",    secondary=video_genero,    back_populates="videos")
    plataformas    = relationship("Plataforma", secondary=video_plataforma, back_populates="videos")
    premios        = relationship("Premio",    secondary=video_premio,    back_populates="videos")
    directores     = relationship("Director",  secondary=video_director,  back_populates="videos")

    def __repr__(self):
        return f"<Video(idvideo={self.idvideo}, titulo='{self.titulo}')>"


class Calificacion(Base):
    __tablename__ = 'calificacion'

    idcalificacion = Column(Integer, primary_key=True, autoincrement=True)
    idvideo        = Column(Integer, ForeignKey('video.idvideo'), nullable=False)
    nivel          = Column(Enum(NivelCalificacion), nullable=False)
    puntaje        = Column(Float)
    comentario     = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    video = relationship("Video", back_populates="calificaciones")

    def __repr__(self):
        return f"<Calificacion(id={self.idcalificacion}, nivel='{self.nivel.value}', idvideo={self.idvideo})>"


class Genero(Base):
    __tablename__ = 'genero'

    idgenero       = Column(Integer, primary_key=True, autoincrement=True)
    nombre         = Column(String(80), unique=True, nullable=False)
    descripcion    = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    videos = relationship("Video", secondary=video_genero, back_populates="generos")

    def __repr__(self):
        return f"<Genero(idgenero={self.idgenero}, nombre='{self.nombre}')>"


class Director(Base):
    __tablename__ = 'director'

    iddirector     = Column(Integer, primary_key=True, autoincrement=True)
    nombre         = Column(String(100), nullable=False)
    apellido       = Column(String(100), nullable=False)
    nacionalidad   = Column(String(60))
    fecha_nac      = Column(Date)
    biografia      = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    videos = relationship("Video", secondary=video_director, back_populates="directores")

    def __repr__(self):
        return f"<Director(iddirector={self.iddirector}, nombre='{self.nombre} {self.apellido}')>"


class Premio(Base):
    __tablename__ = 'premio'

    idpremio       = Column(Integer, primary_key=True, autoincrement=True)
    nombre         = Column(String(150), nullable=False)
    tipo           = Column(Enum(TipoPremio), default=TipoPremio.OTRO)
    categoria      = Column(String(100))
    anio           = Column(Integer)
    descripcion    = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    videos = relationship("Video", secondary=video_premio, back_populates="premios")

    def __repr__(self):
        return f"<Premio(idpremio={self.idpremio}, nombre='{self.nombre}', anio={self.anio})>"


class Plataforma(Base):
    __tablename__ = 'plataforma'

    idplataforma   = Column(Integer, primary_key=True, autoincrement=True)
    nombre         = Column(String(100), unique=True, nullable=False)
    url            = Column(String(255))
    descripcion    = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    videos = relationship("Video", secondary=video_plataforma, back_populates="plataformas")

    def __repr__(self):
        return f"<Plataforma(idplataforma={self.idplataforma}, nombre='{self.nombre}')>"


def init_db():
    """
    Crea todas las tablas en la base de datos si no existen.
    Llama a esta función explícitamente al arrancar la aplicación,
    NO al importar el módulo (evita crash si MySQL está apagado).
    """
    Base.metadata.create_all(engine)
    print("✅ Tablas creadas/verificadas exitosamente")