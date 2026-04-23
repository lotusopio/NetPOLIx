"""
models.py
=========
Re-exporta todos los modelos y enums desde models_sic.py.

Este archivo existe para compatibilidad con los DAOs individuales
(CalificacionDAO.py, DirectorDAO.py, etc.) que importan desde aquí.
NO redefine nada — todo viene de models_sic.py para evitar el error:

    InvalidRequestError: Table 'xxx' is already defined for this MetaData instance
"""

from models_sic import (
    # Motor y sesión
    Base,
    engine,
    SessionLocal,

    # Enums
    NivelCalificacion,
    TipoPremio,

    # Tablas de asociación N:M
    video_genero,
    video_plataforma,
    video_premio,
    video_director,

    # Modelos ORM
    Video,
    Calificacion,
    Genero,
    Director,
    Premio,
    Plataforma,
)

__all__ = [
    "Base", "engine", "SessionLocal",
    "NivelCalificacion", "TipoPremio",
    "video_genero", "video_plataforma", "video_premio", "video_director",
    "Video", "Calificacion", "Genero", "Director", "Premio", "Plataforma",
]