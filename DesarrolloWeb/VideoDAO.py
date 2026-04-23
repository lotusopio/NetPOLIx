"""
VideoDAO.py
Capa de acceso a datos para la entidad Video.
Patrón: clase concreta con Session inyectada (mismo estilo que el repo).
"""

from sqlalchemy.orm import Session
from models_sic import Video


class VideoDAO:

    def __init__(self, session: Session):
        self.session = session

    # ── CREATE ────────────────────────────────────────────────────────────────

    def crear(self, titulo: str, anio_produccion: int = None,
              duracion: int = None, descripcion: str = None) -> Video:
        """
        Crea un nuevo video.
        :param titulo:          Título del video (requerido).
        :param anio_produccion: Año de producción (opcional).
        :param duracion:        Duración en minutos (opcional).
        :param descripcion:     Descripción del video (opcional).
        """
        v = Video(
            titulo=titulo,
            anio_produccion=anio_produccion,
            duracion=duracion,
            descripcion=descripcion
        )
        self.session.add(v)
        self.session.commit()
        self.session.refresh(v)
        print(f"✅ Video '{titulo}' creado exitosamente con ID {v.idvideo}")
        return v

    def obtener_todos(self) -> list:
        """Retorna todos los videos registrados."""
        return self.session.query(Video).all()

    def obtener_por_id(self, idvideo: int) -> Video:
        """Busca un video por su ID primario."""
        return self.session.query(Video).filter(
            Video.idvideo == idvideo
        ).first()

    def buscar_por_titulo(self, titulo: str) -> list:
        """Búsqueda parcial por título (case-insensitive)."""
        return self.session.query(Video).filter(
            Video.titulo.ilike(f"%{titulo}%")
        ).all()

    def obtener_por_anio(self, anio: int) -> list:
        """Retorna todos los videos de un año específico."""
        return self.session.query(Video).filter(
            Video.anio_produccion == anio
        ).all()

    # ── UPDATE ────────────────────────────────────────────────────────────────

    def actualizar(self, idvideo: int, **kwargs) -> Video:
        """
        Actualiza campos de un video.
        Campos permitidos: titulo, anio_produccion, duracion, descripcion.
        """
        v = self.obtener_por_id(idvideo)
        if not v:
            raise ValueError(f"No existe video con ID {idvideo}")

        campos_permitidos = {'titulo', 'anio_produccion', 'duracion', 'descripcion'}
        for campo, valor in kwargs.items():
            if campo not in campos_permitidos:
                raise ValueError(f"Campo no permitido: '{campo}'")
            setattr(v, campo, valor)

        self.session.commit()
        self.session.refresh(v)
        print(f"✅ Video ID {idvideo} actualizado correctamente")
        return v

    # ── DELETE ────────────────────────────────────────────────────────────────

    def eliminar(self, idvideo: int) -> bool:
        """
        Elimina un video por ID.
        Por CASCADE también elimina sus calificaciones asociadas.
        Retorna True si se eliminó.
        """
        v = self.obtener_por_id(idvideo)
        if not v:
            return False
        try:
            self.session.delete(v)
            self.session.commit()
            print(f"✅ Video ID {idvideo} eliminado correctamente")
            return True
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error al eliminar video: {str(e)}")

    # ── EXTRA ─────────────────────────────────────────────────────────────────

    def listar_ordenado(self, orden_por: str = 'titulo',
                        ascendente: bool = True) -> list:
        """Retorna videos ordenados por título o año."""
        campos = {
            'titulo': Video.titulo,
            'anio':   Video.anio_produccion,
            'duracion': Video.duracion
        }
        if orden_por not in campos:
            raise ValueError(f"Campo de orden inválido: '{orden_por}'")
        query = self.session.query(Video)
        campo = campos[orden_por]
        return query.order_by(campo).all() if ascendente else query.order_by(campo.desc()).all()

    def obtener_estadisticas(self) -> dict:
        """Retorna estadísticas básicas de los videos."""
        total = self.session.query(Video).count()
        return {'total_videos': total}