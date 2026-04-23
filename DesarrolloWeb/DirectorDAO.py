"""
DirectorDAO.py
Capa de acceso a datos para la entidad Director.
Patrón: clase concreta con Session inyectada (mismo estilo que VideoDAO.py).
"""

from sqlalchemy.orm import Session
from datetime import date
from models import Director


class DirectorDAO:

    def __init__(self, session: Session):
        self.session = session

    # ── CREATE ────────────────────────────────────────────────────────────────

    def crear(self, nombre: str, apellido: str,
              nacionalidad: str = None, fecha_nac: date = None,
              biografia: str = None) -> Director:
        """
        Crea un nuevo director.
        :param nombre:       Nombre del director.
        :param apellido:     Apellido del director.
        :param nacionalidad: País de origen (opcional).
        :param fecha_nac:    Fecha de nacimiento tipo date (opcional).
        :param biografia:    Texto biográfico (opcional).
        """
        director = Director(
            nombre=nombre,
            apellido=apellido,
            nacionalidad=nacionalidad,
            fecha_nac=fecha_nac,
            biografia=biografia
        )
        self.session.add(director)
        self.session.commit()
        print(f"✅ Director '{nombre} {apellido}' creado exitosamente")
        return director

    # ── READ ──────────────────────────────────────────────────────────────────

    def obtener_todos(self) -> list:
        """Retorna todos los directores registrados."""
        return self.session.query(Director).all()

    def obtener_por_id(self, iddirector: int) -> Director:
        """Busca un director por su ID primario."""
        return self.session.query(Director).filter(
            Director.iddirector == iddirector
        ).first()

    def obtener_por_nombre(self, nombre: str) -> list:
        """Búsqueda parcial por nombre o apellido del director."""
        return self.session.query(Director).filter(
            Director.nombre.ilike(f"%{nombre}%") |
            Director.apellido.ilike(f"%{nombre}%")
        ).all()

    def obtener_por_nacionalidad(self, nacionalidad: str) -> list:
        """Retorna todos los directores de una nacionalidad específica."""
        return self.session.query(Director).filter(
            Director.nacionalidad.ilike(f"%{nacionalidad}%")
        ).all()

    def obtener_videos_por_director(self, iddirector: int) -> list:
        """Retorna todos los videos dirigidos por un director."""
        director = self.obtener_por_id(iddirector)
        if not director:
            raise ValueError(f"No existe director con ID {iddirector}")
        return director.videos

    # ── UPDATE ────────────────────────────────────────────────────────────────

    def actualizar(self, iddirector: int, **kwargs) -> Director:
        """
        Actualiza campos de un director.
        Campos permitidos: nombre, apellido, nacionalidad, fecha_nac, biografia.
        """
        director = self.obtener_por_id(iddirector)
        if not director:
            raise ValueError(f"No existe director con ID {iddirector}")

        campos_permitidos = {'nombre', 'apellido', 'nacionalidad', 'fecha_nac', 'biografia'}

        for campo, valor in kwargs.items():
            if campo not in campos_permitidos:
                raise ValueError(f"Campo no permitido: '{campo}'")
            setattr(director, campo, valor)

        self.session.commit()
        print(f"✅ Director ID {iddirector} actualizado correctamente")
        return director

    # ── DELETE ────────────────────────────────────────────────────────────────

    def eliminar(self, iddirector: int) -> bool:
        """Elimina un director por ID. Retorna True si se eliminó."""
        director = self.obtener_por_id(iddirector)
        if not director:
            return False
        try:
            self.session.delete(director)
            self.session.commit()
            print(f"✅ Director ID {iddirector} eliminado correctamente")
            return True
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error al eliminar director: {str(e)}")

    # ── EXTRA ─────────────────────────────────────────────────────────────────

    def listar_ordenado(self, orden_por: str = 'apellido',
                        ascendente: bool = True) -> list:
        """Retorna directores ordenados por apellido o nombre."""
        campos = {
            'nombre':   Director.nombre,
            'apellido': Director.apellido,
        }
        if orden_por not in campos:
            raise ValueError(f"Campo de orden inválido: '{orden_por}'")

        query = self.session.query(Director)
        campo = campos[orden_por]
        if ascendente:
            return query.order_by(campo).all()
        return query.order_by(campo.desc()).all()