"""
PremioDAO.py
Capa de acceso a datos para la entidad Premio.
Patrón: clase concreta con Session inyectada (mismo estilo que VideoDAO.py).
"""

from sqlalchemy.orm import Session
from models import Premio, TipoPremio


class PremioDAO:

    def __init__(self, session: Session):
        self.session = session

    # ── CREATE ────────────────────────────────────────────────────────────────

    def crear(self, nombre: str, tipo: str, categoria: str = None,
              anio: int = None, descripcion: str = None) -> Premio:
        """
        Crea un nuevo premio cinematográfico.
        :param nombre:      Nombre del premio (ej. 'Mejor Película Extranjera').
        :param tipo:        Tipo de ceremonia: OSCAR, GLOBO_DE_ORO, BAFTA, EMMY, OTRO.
        :param categoria:   Categoría interna del premio (opcional).
        :param anio:        Año de entrega (opcional).
        :param descripcion: Descripción adicional (opcional).
        """
        try:
            tipo_enum = TipoPremio[tipo.upper().replace(" ", "_")]
        except KeyError:
            raise ValueError(
                f"Tipo de premio inválido: '{tipo}'. "
                f"Opciones: {[e.name for e in TipoPremio]}"
            )

        premio = Premio(
            nombre=nombre,
            tipo=tipo_enum,
            categoria=categoria,
            anio=anio,
            descripcion=descripcion
        )
        self.session.add(premio)
        self.session.commit()
        print(f"✅ Premio '{nombre}' ({tipo_enum.value}) creado exitosamente")
        return premio

    # ── READ ──────────────────────────────────────────────────────────────────

    def obtener_todos(self) -> list:
        """Retorna todos los premios registrados."""
        return self.session.query(Premio).all()

    def obtener_por_id(self, idpremio: int) -> Premio:
        """Busca un premio por su ID primario."""
        return self.session.query(Premio).filter(
            Premio.idpremio == idpremio
        ).first()

    def obtener_por_nombre(self, nombre: str) -> list:
        """Búsqueda parcial por nombre del premio."""
        return self.session.query(Premio).filter(
            Premio.nombre.ilike(f"%{nombre}%")
        ).all()

    def obtener_por_tipo(self, tipo: str) -> list:
        """Filtra premios por tipo de ceremonia (OSCAR, BAFTA, etc.)."""
        try:
            tipo_enum = TipoPremio[tipo.upper().replace(" ", "_")]
        except KeyError:
            raise ValueError(f"Tipo de premio inválido: '{tipo}'")
        return self.session.query(Premio).filter(
            Premio.tipo == tipo_enum
        ).all()

    def obtener_por_anio(self, anio: int) -> list:
        """Retorna todos los premios entregados en un año específico."""
        return self.session.query(Premio).filter(
            Premio.anio == anio
        ).all()

    def obtener_videos_por_premio(self, idpremio: int) -> list:
        """Retorna todos los videos que han ganado un premio específico."""
        premio = self.obtener_por_id(idpremio)
        if not premio:
            raise ValueError(f"No existe premio con ID {idpremio}")
        return premio.videos

    # ── UPDATE ────────────────────────────────────────────────────────────────

    def actualizar(self, idpremio: int, **kwargs) -> Premio:
        """
        Actualiza campos de un premio.
        Campos permitidos: nombre, tipo, categoria, anio, descripcion.
        """
        premio = self.obtener_por_id(idpremio)
        if not premio:
            raise ValueError(f"No existe premio con ID {idpremio}")

        campos_permitidos = {'nombre', 'tipo', 'categoria', 'anio', 'descripcion'}

        for campo, valor in kwargs.items():
            if campo not in campos_permitidos:
                raise ValueError(f"Campo no permitido: '{campo}'")
            if campo == 'tipo':
                try:
                    valor = TipoPremio[valor.upper().replace(" ", "_")]
                except KeyError:
                    raise ValueError(f"Tipo de premio inválido: '{valor}'")
            setattr(premio, campo, valor)

        self.session.commit()
        print(f"✅ Premio ID {idpremio} actualizado correctamente")
        return premio

    # ── DELETE ────────────────────────────────────────────────────────────────

    def eliminar(self, idpremio: int) -> bool:
        """Elimina un premio por ID. Retorna True si se eliminó."""
        premio = self.obtener_por_id(idpremio)
        if not premio:
            return False
        try:
            self.session.delete(premio)
            self.session.commit()
            print(f"✅ Premio ID {idpremio} eliminado correctamente")
            return True
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error al eliminar premio: {str(e)}")

    # ── EXTRA ─────────────────────────────────────────────────────────────────

    def obtener_estadisticas(self) -> dict:
        """Retorna conteo de premios agrupado por tipo de ceremonia."""
        stats = {}
        for tipo in TipoPremio:
            count = self.session.query(Premio).filter(
                Premio.tipo == tipo
            ).count()
            stats[tipo.value] = count
        stats['total'] = self.session.query(Premio).count()
        return stats