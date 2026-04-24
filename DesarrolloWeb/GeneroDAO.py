"""
GeneroDAO.py
Capa de acceso a datos para la entidad Genero.
Patrón: clase concreta con Session inyectada (mismo estilo que VideoDAO.py).
"""

from sqlalchemy.orm import Session
from models_sic import Genero


class GeneroDAO:

    def __init__(self, session: Session):
        self.session = session

    # ── CREATE ────────────────────────────────────────────────────────────────

    def crear(self, nombre: str, descripcion: str = None) -> Genero:
        """
        Crea un nuevo género cinematográfico.
        :param nombre:      Nombre único del género (ej. 'Acción', 'Drama').
        :param descripcion: Descripción opcional.
        """
        if self.obtener_por_nombre(nombre):
            raise ValueError(f"El género '{nombre}' ya existe en la base de datos")

        genero = Genero(nombre=nombre, descripcion=descripcion)
        self.session.add(genero)
        self.session.commit()
        print(f"✅ Género '{nombre}' creado exitosamente")
        return genero

    # ── READ ──────────────────────────────────────────────────────────────────

    def obtener_todos(self) -> list:
        """Retorna todos los géneros registrados."""
        return self.session.query(Genero).all()

    def obtener_por_id(self, idgenero: int) -> Genero:
        """Busca un género por su ID primario."""
        return self.session.query(Genero).filter(
            Genero.idgenero == idgenero
        ).first()

    def obtener_por_nombre(self, nombre: str) -> Genero:
        """Busca un género por nombre exacto (case-insensitive)."""
        return self.session.query(Genero).filter(
            Genero.nombre.ilike(nombre)
        ).first()

    def buscar_por_nombre(self, nombre: str) -> list:
        """Búsqueda parcial por nombre de género."""
        return self.session.query(Genero).filter(
            Genero.nombre.ilike(f"%{nombre}%")
        ).all()

    def obtener_videos_por_genero(self, idgenero: int) -> list:
        """Retorna todos los videos asociados a un género."""
        genero = self.obtener_por_id(idgenero)
        if not genero:
            raise ValueError(f"No existe género con ID {idgenero}")
        return genero.videos

    # ── UPDATE ────────────────────────────────────────────────────────────────

    def actualizar(self, idgenero: int, **kwargs) -> Genero:
        """
        Actualiza campos de un género.
        Campos permitidos: nombre, descripcion.
        """
        genero = self.obtener_por_id(idgenero)
        if not genero:
            raise ValueError(f"No existe género con ID {idgenero}")

        campos_permitidos = {'nombre', 'descripcion'}

        for campo, valor in kwargs.items():
            if campo not in campos_permitidos:
                raise ValueError(f"Campo no permitido: '{campo}'")
            if campo == 'nombre' and self.obtener_por_nombre(valor):
                raise ValueError(f"Ya existe un género con el nombre '{valor}'")
            setattr(genero, campo, valor)

        self.session.commit()
        print(f" Género ID {idgenero} actualizado correctamente")
        return genero

    # ── DELETE ────────────────────────────────────────────────────────────────

    def eliminar(self, idgenero: int) -> bool:
        """Elimina un género por ID. Retorna True si se eliminó."""
        genero = self.obtener_por_id(idgenero)
        if not genero:
            return False
        try:
            self.session.delete(genero)
            self.session.commit()
            print(f" Género ID {idgenero} eliminado correctamente")
            return True
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error al eliminar género: {str(e)}")

    # ── EXTRA ─────────────────────────────────────────────────────────────────

    def listar_ordenado(self, ascendente: bool = True) -> list:
        """Retorna los géneros ordenados alfabéticamente."""
        query = self.session.query(Genero)
        if ascendente:
            return query.order_by(Genero.nombre).all()
        return query.order_by(Genero.nombre.desc()).all()