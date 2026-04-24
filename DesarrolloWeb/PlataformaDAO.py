"""
PlataformaDAO.py
Capa de acceso a datos para la entidad Plataforma.
Patrón: clase concreta con Session inyectada (mismo estilo que VideoDAO.py).
"""

from sqlalchemy.orm import Session
from models_sic import Plataforma


class PlataformaDAO:

    def __init__(self, session: Session):
        self.session = session

    # ── CREATE ────────────────────────────────────────────────────────────────

    def crear(self, nombre: str, url: str = None,
              descripcion: str = None) -> Plataforma:
        """
        Registra una nueva plataforma de distribución.
        :param nombre:      Nombre único de la plataforma (ej. 'NetPOLIx Streaming').
        :param url:         URL principal de la plataforma (opcional).
        :param descripcion: Descripción del servicio (opcional).
        """
        if self.obtener_por_nombre(nombre):
            raise ValueError(f"La plataforma '{nombre}' ya existe en la base de datos")

        plataforma = Plataforma(nombre=nombre, url=url, descripcion=descripcion)
        self.session.add(plataforma)
        self.session.commit()
        print(f"✅ Plataforma '{nombre}' creada exitosamente")
        return plataforma

    # ── READ ──────────────────────────────────────────────────────────────────

    def obtener_todos(self) -> list:
        """Retorna todas las plataformas registradas."""
        return self.session.query(Plataforma).all()

    def obtener_por_id(self, idplataforma: int) -> Plataforma:
        """Busca una plataforma por su ID primario."""
        return self.session.query(Plataforma).filter(
            Plataforma.idplataforma == idplataforma
        ).first()

    def obtener_por_nombre(self, nombre: str) -> Plataforma:
        """Busca una plataforma por nombre exacto (case-insensitive)."""
        return self.session.query(Plataforma).filter(
            Plataforma.nombre.ilike(nombre)
        ).first()

    def buscar_por_nombre(self, nombre: str) -> list:
        """Búsqueda parcial por nombre de plataforma."""
        return self.session.query(Plataforma).filter(
            Plataforma.nombre.ilike(f"%{nombre}%")
        ).all()

    def obtener_videos_por_plataforma(self, idplataforma: int) -> list:
        """Retorna todos los videos disponibles en una plataforma."""
        plataforma = self.obtener_por_id(idplataforma)
        if not plataforma:
            raise ValueError(f"No existe plataforma con ID {idplataforma}")
        return plataforma.videos

    # ── UPDATE ────────────────────────────────────────────────────────────────

    def actualizar(self, idplataforma: int, **kwargs) -> Plataforma:
        """
        Actualiza campos de una plataforma.
        Campos permitidos: nombre, url, descripcion.
        """
        plataforma = self.obtener_por_id(idplataforma)
        if not plataforma:
            raise ValueError(f"No existe plataforma con ID {idplataforma}")

        campos_permitidos = {'nombre', 'url', 'descripcion'}

        for campo, valor in kwargs.items():
            if campo not in campos_permitidos:
                raise ValueError(f"Campo no permitido: '{campo}'")
            if campo == 'nombre' and self.obtener_por_nombre(valor):
                raise ValueError(f"Ya existe una plataforma con el nombre '{valor}'")
            setattr(plataforma, campo, valor)

        self.session.commit()
        print(f"✅ Plataforma ID {idplataforma} actualizada correctamente")
        return plataforma

    # ── DELETE ────────────────────────────────────────────────────────────────

    def eliminar(self, idplataforma: int) -> bool:
        """Elimina una plataforma por ID. Retorna True si se eliminó."""
        plataforma = self.obtener_por_id(idplataforma)
        if not plataforma:
            return False
        try:
            self.session.delete(plataforma)
            self.session.commit()
            print(f"✅ Plataforma ID {idplataforma} eliminada correctamente")
            return True
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error al eliminar plataforma: {str(e)}")

    # ── EXTRA ─────────────────────────────────────────────────────────────────

    def listar_ordenado(self, ascendente: bool = True) -> list:
        """Retorna las plataformas ordenadas alfabéticamente por nombre."""
        query = self.session.query(Plataforma)
        if ascendente:
            return query.order_by(Plataforma.nombre).all()
        return query.order_by(Plataforma.nombre.desc()).all()

    def obtener_estadisticas(self) -> dict:
        """Retorna estadísticas básicas: total plataformas y videos por plataforma."""
        plataformas = self.obtener_todos()
        stats = {
            'total_plataformas': len(plataformas),
            'detalle': [
                {
                    'nombre': p.nombre,
                    'total_videos': len(p.videos)
                }
                for p in plataformas
            ]
        }
        return stats