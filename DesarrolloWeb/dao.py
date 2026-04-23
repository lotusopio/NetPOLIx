"""
dao.py
DAOs para: Calificacion, Genero, Director, Premio, Plataforma
Patrón: clase concreta con Session inyectada.
"""

from sqlalchemy.orm import Session
from models_sic import (
    Calificacion, NivelCalificacion,
    Genero, Director, Premio, TipoPremio, Plataforma, Video
)
from datetime import date


# ══════════════════════════════════════════════
#  CALIFICACION DAO
# ══════════════════════════════════════════════

class CalificacionDAO:

    def __init__(self, session: Session):
        self.session = session

    def crear(self, idvideo: int, nivel: str,
              puntaje: float = None, comentario: str = None) -> Calificacion:
        try:
            nivel_enum = NivelCalificacion[nivel.upper()]
        except KeyError:
            raise ValueError(f"Nivel inválido: '{nivel}'. Opciones: {[e.name for e in NivelCalificacion]}")
        c = Calificacion(idvideo=idvideo, nivel=nivel_enum, puntaje=puntaje, comentario=comentario)
        self.session.add(c)
        self.session.commit()
        self.session.refresh(c)
        print(f"✅ Calificación '{nivel_enum.value}' creada para video ID {idvideo}")
        return c

    def obtener_todos(self) -> list:
        return self.session.query(Calificacion).all()

    def obtener_por_id(self, idcalificacion: int) -> Calificacion:
        return self.session.query(Calificacion).filter(
            Calificacion.idcalificacion == idcalificacion
        ).first()

    def obtener_por_video(self, idvideo: int) -> list:
        return self.session.query(Calificacion).filter(
            Calificacion.idvideo == idvideo
        ).all()

    def obtener_por_nivel(self, nivel: str) -> list:
        try:
            nivel_enum = NivelCalificacion[nivel.upper()]
        except KeyError:
            raise ValueError(f"Nivel inválido: '{nivel}'")
        return self.session.query(Calificacion).filter(
            Calificacion.nivel == nivel_enum
        ).all()

    def actualizar(self, idcalificacion: int, **kwargs) -> Calificacion:
        c = self.obtener_por_id(idcalificacion)
        if not c:
            raise ValueError(f"No existe calificación con ID {idcalificacion}")
        campos = {'nivel', 'puntaje', 'comentario'}
        for campo, valor in kwargs.items():
            if campo not in campos:
                raise ValueError(f"Campo no permitido: '{campo}'")
            if campo == 'nivel':
                valor = NivelCalificacion[valor.upper()]
            setattr(c, campo, valor)
        self.session.commit()
        self.session.refresh(c)
        print(f"✅ Calificación ID {idcalificacion} actualizada")
        return c

    def eliminar(self, idcalificacion: int) -> bool:
        c = self.obtener_por_id(idcalificacion)
        if not c:
            return False
        self.session.delete(c)
        self.session.commit()
        print(f"✅ Calificación ID {idcalificacion} eliminada")
        return True


# ══════════════════════════════════════════════
#  GENERO DAO
# ══════════════════════════════════════════════

class GeneroDAO:

    def __init__(self, session: Session):
        self.session = session

    def crear(self, nombre: str, descripcion: str = None) -> Genero:
        if self.session.query(Genero).filter(Genero.nombre.ilike(nombre)).first():
            raise ValueError(f"El género '{nombre}' ya existe")
        g = Genero(nombre=nombre, descripcion=descripcion)
        self.session.add(g)
        self.session.commit()
        self.session.refresh(g)
        print(f"✅ Género '{nombre}' creado exitosamente")
        return g

    def obtener_todos(self) -> list:
        return self.session.query(Genero).all()

    def obtener_por_id(self, idgenero: int) -> Genero:
        return self.session.query(Genero).filter(
            Genero.idgenero == idgenero
        ).first()

    def buscar_por_nombre(self, nombre: str) -> list:
        return self.session.query(Genero).filter(
            Genero.nombre.ilike(f"%{nombre}%")
        ).all()

    def actualizar(self, idgenero: int, **kwargs) -> Genero:
        g = self.obtener_por_id(idgenero)
        if not g:
            raise ValueError(f"No existe género con ID {idgenero}")
        campos = {'nombre', 'descripcion'}
        for campo, valor in kwargs.items():
            if campo not in campos:
                raise ValueError(f"Campo no permitido: '{campo}'")
            setattr(g, campo, valor)
        self.session.commit()
        self.session.refresh(g)
        print(f"✅ Género ID {idgenero} actualizado")
        return g

    def eliminar(self, idgenero: int) -> bool:
        g = self.obtener_por_id(idgenero)
        if not g:
            return False
        self.session.delete(g)
        self.session.commit()
        print(f"✅ Género ID {idgenero} eliminado")
        return True


# ══════════════════════════════════════════════
#  DIRECTOR DAO
# ══════════════════════════════════════════════

class DirectorDAO:

    def __init__(self, session: Session):
        self.session = session

    def crear(self, nombre: str, apellido: str,
              nacionalidad: str = None, fecha_nac: date = None,
              biografia: str = None) -> Director:
        d = Director(nombre=nombre, apellido=apellido,
                     nacionalidad=nacionalidad, fecha_nac=fecha_nac,
                     biografia=biografia)
        self.session.add(d)
        self.session.commit()
        self.session.refresh(d)
        print(f"✅ Director '{nombre} {apellido}' creado exitosamente")
        return d

    def obtener_todos(self) -> list:
        return self.session.query(Director).all()

    def obtener_por_id(self, iddirector: int) -> Director:
        return self.session.query(Director).filter(
            Director.iddirector == iddirector
        ).first()

    def buscar_por_nombre(self, nombre: str) -> list:
        return self.session.query(Director).filter(
            Director.nombre.ilike(f"%{nombre}%") |
            Director.apellido.ilike(f"%{nombre}%")
        ).all()

    def obtener_por_nacionalidad(self, nacionalidad: str) -> list:
        return self.session.query(Director).filter(
            Director.nacionalidad.ilike(f"%{nacionalidad}%")
        ).all()

    def actualizar(self, iddirector: int, **kwargs) -> Director:
        d = self.obtener_por_id(iddirector)
        if not d:
            raise ValueError(f"No existe director con ID {iddirector}")
        campos = {'nombre', 'apellido', 'nacionalidad', 'fecha_nac', 'biografia'}
        for campo, valor in kwargs.items():
            if campo not in campos:
                raise ValueError(f"Campo no permitido: '{campo}'")
            setattr(d, campo, valor)
        self.session.commit()
        self.session.refresh(d)
        print(f"✅ Director ID {iddirector} actualizado")
        return d

    def eliminar(self, iddirector: int) -> bool:
        d = self.obtener_por_id(iddirector)
        if not d:
            return False
        self.session.delete(d)
        self.session.commit()
        print(f"✅ Director ID {iddirector} eliminado")
        return True


# ══════════════════════════════════════════════
#  PREMIO DAO
# ══════════════════════════════════════════════

class PremioDAO:

    def __init__(self, session: Session):
        self.session = session

    def crear(self, nombre: str, tipo: str = "OTRO",
              categoria: str = None, anio: int = None,
              descripcion: str = None) -> Premio:
        try:
            tipo_enum = TipoPremio[tipo.upper().replace(" ", "_")]
        except KeyError:
            raise ValueError(f"Tipo inválido: '{tipo}'. Opciones: {[e.name for e in TipoPremio]}")
        p = Premio(nombre=nombre, tipo=tipo_enum, categoria=categoria,
                   anio=anio, descripcion=descripcion)
        self.session.add(p)
        self.session.commit()
        self.session.refresh(p)
        print(f"✅ Premio '{nombre}' ({tipo_enum.value}) creado exitosamente")
        return p

    def obtener_todos(self) -> list:
        return self.session.query(Premio).all()

    def obtener_por_id(self, idpremio: int) -> Premio:
        return self.session.query(Premio).filter(
            Premio.idpremio == idpremio
        ).first()

    def buscar_por_nombre(self, nombre: str) -> list:
        return self.session.query(Premio).filter(
            Premio.nombre.ilike(f"%{nombre}%")
        ).all()

    def obtener_por_tipo(self, tipo: str) -> list:
        try:
            tipo_enum = TipoPremio[tipo.upper().replace(" ", "_")]
        except KeyError:
            raise ValueError(f"Tipo inválido: '{tipo}'")
        return self.session.query(Premio).filter(Premio.tipo == tipo_enum).all()

    def obtener_por_anio(self, anio: int) -> list:
        return self.session.query(Premio).filter(Premio.anio == anio).all()

    def actualizar(self, idpremio: int, **kwargs) -> Premio:
        p = self.obtener_por_id(idpremio)
        if not p:
            raise ValueError(f"No existe premio con ID {idpremio}")
        campos = {'nombre', 'tipo', 'categoria', 'anio', 'descripcion'}
        for campo, valor in kwargs.items():
            if campo not in campos:
                raise ValueError(f"Campo no permitido: '{campo}'")
            if campo == 'tipo':
                valor = TipoPremio[valor.upper().replace(" ", "_")]
            setattr(p, campo, valor)
        self.session.commit()
        self.session.refresh(p)
        print(f"✅ Premio ID {idpremio} actualizado")
        return p

    def eliminar(self, idpremio: int) -> bool:
        p = self.obtener_por_id(idpremio)
        if not p:
            return False
        self.session.delete(p)
        self.session.commit()
        print(f"✅ Premio ID {idpremio} eliminado")
        return True


# ══════════════════════════════════════════════
#  PLATAFORMA DAO
# ══════════════════════════════════════════════

class PlataformaDAO:

    def __init__(self, session: Session):
        self.session = session

    def crear(self, nombre: str, url: str = None,
              descripcion: str = None) -> Plataforma:
        if self.session.query(Plataforma).filter(Plataforma.nombre.ilike(nombre)).first():
            raise ValueError(f"La plataforma '{nombre}' ya existe")
        p = Plataforma(nombre=nombre, url=url, descripcion=descripcion)
        self.session.add(p)
        self.session.commit()
        self.session.refresh(p)
        print(f"✅ Plataforma '{nombre}' creada exitosamente")
        return p

    def obtener_todos(self) -> list:
        return self.session.query(Plataforma).all()

    def obtener_por_id(self, idplataforma: int) -> Plataforma:
        return self.session.query(Plataforma).filter(
            Plataforma.idplataforma == idplataforma
        ).first()

    def buscar_por_nombre(self, nombre: str) -> list:
        return self.session.query(Plataforma).filter(
            Plataforma.nombre.ilike(f"%{nombre}%")
        ).all()

    def actualizar(self, idplataforma: int, **kwargs) -> Plataforma:
        p = self.obtener_por_id(idplataforma)
        if not p:
            raise ValueError(f"No existe plataforma con ID {idplataforma}")
        campos = {'nombre', 'url', 'descripcion'}
        for campo, valor in kwargs.items():
            if campo not in campos:
                raise ValueError(f"Campo no permitido: '{campo}'")
            setattr(p, campo, valor)
        self.session.commit()
        self.session.refresh(p)
        print(f"✅ Plataforma ID {idplataforma} actualizada")
        return p

    def eliminar(self, idplataforma: int) -> bool:
        p = self.obtener_por_id(idplataforma)
        if not p:
            return False
        self.session.delete(p)
        self.session.commit()
        print(f"✅ Plataforma ID {idplataforma} eliminada")
        return True