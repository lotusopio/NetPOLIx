from sqlalchemy.orm import Session
from models_sic import Calificacion, NivelCalificacion
 
 
class CalificacionDAO:
 
    def __init__(self, session: Session):
        self.session = session
 
    # ── CREATE ────────────────────────────────────────────────────────────────
 
    def crear(self, idvideo: int, nivel: str,
              puntaje: float = None, comentario: str = None) -> Calificacion:
        """
        Crea una nueva calificación para un video.
        :param idvideo:    ID del video a calificar.
        :param nivel:      Nivel textual (EXCELENTE, BUENA, REGULAR, MALA).
        :param puntaje:    Puntaje numérico opcional (1.0 – 5.0).
        :param comentario: Texto libre opcional.
        """
        try:
            nivel_enum = NivelCalificacion[nivel.upper()]
        except KeyError:
            raise ValueError(
                f"Nivel de calificación inválido: '{nivel}'. "
                f"Opciones: {[e.name for e in NivelCalificacion]}"
            )
 
        calificacion = Calificacion(
            idvideo=idvideo,
            nivel=nivel_enum,
            puntaje=puntaje,
            comentario=comentario
        )
        self.session.add(calificacion)
        self.session.commit()
        print(f" Calificación '{nivel_enum.value}' creada para video ID {idvideo}")
        return calificacion
 
    # ── READ ──────────────────────────────────────────────────────────────────
 
    def obtener_todos(self) -> list:
        """Retorna todas las calificaciones registradas."""
        return self.session.query(Calificacion).all()
 
    def obtener_por_id(self, idcalificacion: int) -> Calificacion:
        """Busca una calificación por su ID primario."""
        return self.session.query(Calificacion).filter(
            Calificacion.idcalificacion == idcalificacion
        ).first()
 
    def obtener_por_video(self, idvideo: int) -> list:
        """Retorna todas las calificaciones de un video específico."""
        return self.session.query(Calificacion).filter(
            Calificacion.idvideo == idvideo
        ).all()
 
    def obtener_por_nivel(self, nivel: str) -> list:
        """Filtra calificaciones por nivel (EXCELENTE, BUENA, REGULAR, MALA)."""
        try:
            nivel_enum = NivelCalificacion[nivel.upper()]
        except KeyError:
            raise ValueError(f"Nivel inválido: '{nivel}'")
        return self.session.query(Calificacion).filter(
            Calificacion.nivel == nivel_enum
        ).all()
 
    def promedio_puntaje_video(self, idvideo: int) -> float:
        """Calcula el promedio de puntaje numérico para un video."""
        calificaciones = self.obtener_por_video(idvideo)
        puntajes = [c.puntaje for c in calificaciones if c.puntaje is not None]
        if not puntajes:
            return 0.0
        return round(sum(puntajes) / len(puntajes), 2)
 
    # ── UPDATE ────────────────────────────────────────────────────────────────
 
    def actualizar(self, idcalificacion: int, **kwargs) -> Calificacion:
        """
        Actualiza campos de una calificación.
        Campos permitidos: nivel, puntaje, comentario.
        """
        calificacion = self.obtener_por_id(idcalificacion)
        if not calificacion:
            raise ValueError(f"No existe calificación con ID {idcalificacion}")
 
        campos_permitidos = {'nivel', 'puntaje', 'comentario'}
 
        for campo, valor in kwargs.items():
            if campo not in campos_permitidos:
                raise ValueError(f"Campo no permitido: '{campo}'")
            if campo == 'nivel':
                try:
                    valor = NivelCalificacion[valor.upper()]
                except KeyError:
                    raise ValueError(f"Nivel inválido: '{valor}'")
            setattr(calificacion, campo, valor)
 
        self.session.commit()
        print(f" Calificación ID {idcalificacion} actualizada correctamente")
        return calificacion
 
    # ── DELETE ────────────────────────────────────────────────────────────────
 
    def eliminar(self, idcalificacion: int) -> bool:
        """Elimina una calificación por ID. Retorna True si se eliminó."""
        calificacion = self.obtener_por_id(idcalificacion)
        if not calificacion:
            return False
        try:
            self.session.delete(calificacion)
            self.session.commit()
            print(f" Calificación ID {idcalificacion} eliminada correctamente")
            return True
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error al eliminar calificación: {str(e)}")
 
    def eliminar_por_video(self, idvideo: int) -> int:
        """Elimina todas las calificaciones de un video. Retorna cantidad eliminada."""
        calificaciones = self.obtener_por_video(idvideo)
        count = len(calificaciones)
        for c in calificaciones:
            self.session.delete(c)
        self.session.commit()
        print(f" {count} calificación(es) eliminadas para video ID {idvideo}")
        return count