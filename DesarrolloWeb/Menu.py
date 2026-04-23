# -*- coding: utf-8 -*-
"""
Menu.py
Menu interactivo en consola para gestionar las entidades del SIC-NetPOLIx.
Ejecutar: python Menu.py
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from models_sic import SessionLocal
from VideoDAO import VideoDAO
from CalificacionDAO import CalificacionDAO
from GeneroDAO import GeneroDAO
from DirectorDAO import DirectorDAO
from PremioDAO import PremioDAO
from PlataformaDAO import PlataformaDAO

def separador(titulo: str = ""):
    print("\n" + "=" * 50)
    if titulo:
        print(f"  {titulo}")
        print("=" * 50)


def pausar():
    input("\n  Presiona Enter para continuar...")


# ══════════════════════════════════════════════
#  VIDEO
# ══════════════════════════════════════════════

def menu_video(session):
    dao = VideoDAO(session)
    while True:
        separador("VIDEOS")
        print("  1. Listar todos")
        print("  2. Buscar por ID")
        print("  3. Buscar por titulo")
        print("  4. Buscar por anio")
        print("  5. Crear nuevo")
        print("  6. Actualizar")
        print("  7. Eliminar")
        print("  0. Volver al menu principal")
        op = input("\n  Opcion: ").strip()

        if op == "1":
            separador("TODOS LOS VIDEOS")
            registros = dao.obtener_todos()
            if not registros:
                print("  No hay videos registrados.")
            for v in registros:
                print(f"  [{v.idvideo}] {v.titulo} | Anio: {v.anio_produccion or '-'} | Duracion: {v.duracion or '-'} min")

        elif op == "2":
            id_ = int(input("  ID del video: "))
            v = dao.obtener_por_id(id_)
            if v:
                print(f"\n  ID: {v.idvideo} | Titulo: {v.titulo}")
                print(f"  Anio: {v.anio_produccion} | Duracion: {v.duracion} min")
                print(f"  Descripcion: {v.descripcion or '-'}")
            else:
                print("  No encontrado.")

        elif op == "3":
            titulo = input("  Titulo a buscar: ").strip()
            resultados = dao.buscar_por_titulo(titulo)
            if not resultados:
                print("  Sin resultados.")
            for v in resultados:
                print(f"  [{v.idvideo}] {v.titulo} | {v.anio_produccion or '-'}")

        elif op == "4":
            anio = int(input("  Anio: "))
            for v in dao.obtener_por_anio(anio):
                print(f"  [{v.idvideo}] {v.titulo}")

        elif op == "5":
            titulo = input("  Titulo: ").strip()
            anio_s = input("  Anio de produccion (Enter para omitir): ").strip()
            dur_s  = input("  Duracion en minutos (Enter para omitir): ").strip()
            desc   = input("  Descripcion (Enter para omitir): ").strip() or None
            anio   = int(anio_s) if anio_s else None
            dur    = int(dur_s) if dur_s else None
            try:
                v = dao.crear(titulo=titulo, anio_produccion=anio, duracion=dur, descripcion=desc)
                print(f"  Video creado con ID {v.idvideo}")
            except ValueError as e:
                print(f"  Error: {e}")

        elif op == "6":
            id_ = int(input("  ID a actualizar: "))
            datos = {}
            titulo = input("  Nuevo titulo (Enter para omitir): ").strip()
            if titulo:
                datos['titulo'] = titulo
            anio_s = input("  Nuevo anio (Enter para omitir): ").strip()
            if anio_s:
                datos['anio_produccion'] = int(anio_s)
            dur_s = input("  Nueva duracion en min (Enter para omitir): ").strip()
            if dur_s:
                datos['duracion'] = int(dur_s)
            desc = input("  Nueva descripcion (Enter para omitir): ").strip()
            if desc:
                datos['descripcion'] = desc
            try:
                dao.actualizar(id_, **datos)
            except ValueError as e:
                print(f"  Error: {e}")

        elif op == "7":
            id_ = int(input("  ID a eliminar: "))
            confirm = input(f"  Eliminar video {id_} y sus calificaciones? (s/n): ").strip().lower()
            if confirm == 's':
                if not dao.eliminar(id_):
                    print("  No encontrado.")

        elif op == "0":
            break

        else:
            print("  Opcion no valida.")

        pausar()


# ══════════════════════════════════════════════
#  CALIFICACION
# ══════════════════════════════════════════════

def menu_calificacion(session):
    dao = CalificacionDAO(session)
    while True:
        separador("CALIFICACIONES")
        print("  1. Listar todas")
        print("  2. Buscar por ID")
        print("  3. Buscar por video")
        print("  4. Crear nueva")
        print("  5. Actualizar")
        print("  6. Eliminar")
        print("  0. Volver al menu principal")
        op = input("\n  Opcion: ").strip()

        if op == "1":
            separador("TODAS LAS CALIFICACIONES")
            registros = dao.obtener_todos()
            if not registros:
                print("  No hay calificaciones registradas.")
            for r in registros:
                print(f"  [{r.idcalificacion}] Video {r.idvideo} | {r.nivel.value} | Puntaje: {r.puntaje} | {r.comentario or '-'}")

        elif op == "2":
            id_ = int(input("  ID de la calificacion: "))
            r = dao.obtener_por_id(id_)
            if r:
                print(f"\n  ID: {r.idcalificacion} | Video: {r.idvideo} | Nivel: {r.nivel.value}")
                print(f"  Puntaje: {r.puntaje} | Comentario: {r.comentario or '-'}")
            else:
                print("  No encontrada.")

        elif op == "3":
            idvideo = int(input("  ID del video: "))
            registros = dao.obtener_por_video(idvideo)
            if not registros:
                print("  Sin calificaciones para ese video.")
            for r in registros:
                print(f"  [{r.idcalificacion}] {r.nivel.value} | Puntaje: {r.puntaje} | {r.comentario or '-'}")

        elif op == "4":
            idvideo    = int(input("  ID del video: "))
            print("  Niveles: EXCELENTE, BUENA, REGULAR, MALA")
            nivel      = input("  Nivel: ").strip()
            puntaje_s  = input("  Puntaje (1.0-5.0, Enter para omitir): ").strip()
            puntaje    = float(puntaje_s) if puntaje_s else None
            comentario = input("  Comentario (Enter para omitir): ").strip() or None
            try:
                dao.crear(idvideo=idvideo, nivel=nivel, puntaje=puntaje, comentario=comentario)
            except ValueError as e:
                print(f"  Error: {e}")

        elif op == "5":
            id_ = int(input("  ID de la calificacion a actualizar: "))
            datos = {}
            nivel = input("  Nuevo nivel (EXCELENTE/BUENA/REGULAR/MALA, Enter para omitir): ").strip()
            if nivel:
                datos['nivel'] = nivel
            puntaje_s = input("  Nuevo puntaje (Enter para omitir): ").strip()
            if puntaje_s:
                datos['puntaje'] = float(puntaje_s)
            comentario = input("  Nuevo comentario (Enter para omitir): ").strip()
            if comentario:
                datos['comentario'] = comentario
            try:
                dao.actualizar(id_, **datos)
            except ValueError as e:
                print(f"  Error: {e}")

        elif op == "6":
            id_ = int(input("  ID a eliminar: "))
            confirm = input(f"  Eliminar calificacion {id_}? (s/n): ").strip().lower()
            if confirm == 's':
                if not dao.eliminar(id_):
                    print("  No encontrada.")

        elif op == "0":
            break

        else:
            print("  Opcion no valida.")

        pausar()


# ══════════════════════════════════════════════
#  GENERO
# ══════════════════════════════════════════════

def menu_genero(session):
    dao = GeneroDAO(session)
    while True:
        separador("GENEROS")
        print("  1. Listar todos")
        print("  2. Buscar por ID")
        print("  3. Buscar por nombre")
        print("  4. Crear nuevo")
        print("  5. Actualizar")
        print("  6. Eliminar")
        print("  0. Volver al menu principal")
        op = input("\n  Opcion: ").strip()

        if op == "1":
            separador("TODOS LOS GENEROS")
            registros = dao.obtener_todos()
            if not registros:
                print("  No hay generos registrados.")
            for r in registros:
                print(f"  [{r.idgenero}] {r.nombre} | {r.descripcion or '-'}")

        elif op == "2":
            id_ = int(input("  ID del genero: "))
            r = dao.obtener_por_id(id_)
            if r:
                print(f"\n  ID: {r.idgenero} | Nombre: {r.nombre} | Desc: {r.descripcion or '-'}")
            else:
                print("  No encontrado.")

        elif op == "3":
            nombre = input("  Nombre a buscar: ").strip()
            resultados = dao.buscar_por_nombre(nombre)
            if not resultados:
                print("  Sin resultados.")
            for r in resultados:
                print(f"  [{r.idgenero}] {r.nombre}")

        elif op == "4":
            nombre      = input("  Nombre del genero: ").strip()
            descripcion = input("  Descripcion (Enter para omitir): ").strip() or None
            try:
                dao.crear(nombre=nombre, descripcion=descripcion)
            except ValueError as e:
                print(f"  Error: {e}")

        elif op == "5":
            id_ = int(input("  ID a actualizar: "))
            datos = {}
            nombre = input("  Nuevo nombre (Enter para omitir): ").strip()
            if nombre:
                datos['nombre'] = nombre
            descripcion = input("  Nueva descripcion (Enter para omitir): ").strip()
            if descripcion:
                datos['descripcion'] = descripcion
            try:
                dao.actualizar(id_, **datos)
            except ValueError as e:
                print(f"  Error: {e}")

        elif op == "6":
            id_ = int(input("  ID a eliminar: "))
            confirm = input(f"  Eliminar genero {id_}? (s/n): ").strip().lower()
            if confirm == 's':
                if not dao.eliminar(id_):
                    print("  No encontrado.")

        elif op == "0":
            break

        else:
            print("  Opcion no valida.")

        pausar()


# ══════════════════════════════════════════════
#  DIRECTOR
# ══════════════════════════════════════════════

def menu_director(session):
    dao = DirectorDAO(session)
    while True:
        separador("DIRECTORES")
        print("  1. Listar todos")
        print("  2. Buscar por ID")
        print("  3. Buscar por nombre")
        print("  4. Buscar por nacionalidad")
        print("  5. Crear nuevo")
        print("  6. Actualizar")
        print("  7. Eliminar")
        print("  0. Volver al menu principal")
        op = input("\n  Opcion: ").strip()

        if op == "1":
            separador("TODOS LOS DIRECTORES")
            registros = dao.obtener_todos()
            if not registros:
                print("  No hay directores registrados.")
            for r in registros:
                print(f"  [{r.iddirector}] {r.nombre} {r.apellido} | {r.nacionalidad or '-'}")

        elif op == "2":
            id_ = int(input("  ID del director: "))
            r = dao.obtener_por_id(id_)
            if r:
                print(f"\n  ID: {r.iddirector} | {r.nombre} {r.apellido}")
                print(f"  Nacionalidad: {r.nacionalidad or '-'} | Nac: {r.fecha_nac or '-'}")
                print(f"  Biografia: {r.biografia or '-'}")
            else:
                print("  No encontrado.")

        elif op == "3":
            nombre = input("  Nombre/apellido a buscar: ").strip()
            resultados = dao.buscar_por_nombre(nombre)
            if not resultados:
                print("  Sin resultados.")
            for r in resultados:
                print(f"  [{r.iddirector}] {r.nombre} {r.apellido}")

        elif op == "4":
            nac = input("  Nacionalidad: ").strip()
            for r in dao.obtener_por_nacionalidad(nac):
                print(f"  [{r.iddirector}] {r.nombre} {r.apellido} | {r.nacionalidad}")

        elif op == "5":
            nombre   = input("  Nombre: ").strip()
            apellido = input("  Apellido: ").strip()
            nac      = input("  Nacionalidad (Enter para omitir): ").strip() or None
            fn_s     = input("  Fecha nac. YYYY-MM-DD (Enter para omitir): ").strip()
            from datetime import date as _date
            fecha_nac = _date.fromisoformat(fn_s) if fn_s else None
            bio       = input("  Biografia (Enter para omitir): ").strip() or None
            try:
                dao.crear(nombre=nombre, apellido=apellido,
                          nacionalidad=nac, fecha_nac=fecha_nac, biografia=bio)
            except ValueError as e:
                print(f"  Error: {e}")

        elif op == "6":
            id_ = int(input("  ID a actualizar: "))
            datos = {}
            for campo in ['nombre', 'apellido', 'nacionalidad', 'biografia']:
                val = input(f"  Nuevo {campo} (Enter para omitir): ").strip()
                if val:
                    datos[campo] = val
            try:
                dao.actualizar(id_, **datos)
            except ValueError as e:
                print(f"  Error: {e}")

        elif op == "7":
            id_ = int(input("  ID a eliminar: "))
            confirm = input(f"  Eliminar director {id_}? (s/n): ").strip().lower()
            if confirm == 's':
                if not dao.eliminar(id_):
                    print("  No encontrado.")

        elif op == "0":
            break

        else:
            print("  Opcion no valida.")

        pausar()


# ══════════════════════════════════════════════
#  PREMIO
# ══════════════════════════════════════════════

def menu_premio(session):
    dao = PremioDAO(session)
    while True:
        separador("PREMIOS")
        print("  1. Listar todos")
        print("  2. Buscar por ID")
        print("  3. Buscar por nombre")
        print("  4. Filtrar por tipo")
        print("  5. Filtrar por anio")
        print("  6. Crear nuevo")
        print("  7. Actualizar")
        print("  8. Eliminar")
        print("  0. Volver al menu principal")
        op = input("\n  Opcion: ").strip()

        if op == "1":
            separador("TODOS LOS PREMIOS")
            registros = dao.obtener_todos()
            if not registros:
                print("  No hay premios registrados.")
            for r in registros:
                print(f"  [{r.idpremio}] {r.nombre} | {r.tipo.value} | Anio: {r.anio or '-'}")

        elif op == "2":
            id_ = int(input("  ID del premio: "))
            r = dao.obtener_por_id(id_)
            if r:
                print(f"\n  ID: {r.idpremio} | {r.nombre} | {r.tipo.value}")
                print(f"  Categoria: {r.categoria or '-'} | Anio: {r.anio or '-'}")
            else:
                print("  No encontrado.")

        elif op == "3":
            nombre = input("  Nombre a buscar: ").strip()
            for r in dao.buscar_por_nombre(nombre):
                print(f"  [{r.idpremio}] {r.nombre} | {r.tipo.value}")

        elif op == "4":
            print("  Tipos: OSCAR, GLOBO_DE_ORO, BAFTA, EMMY, OTRO")
            tipo = input("  Tipo: ").strip()
            try:
                for r in dao.obtener_por_tipo(tipo):
                    print(f"  [{r.idpremio}] {r.nombre} | {r.anio or '-'}")
            except ValueError as e:
                print(f"  Error: {e}")

        elif op == "5":
            anio = int(input("  Anio: "))
            for r in dao.obtener_por_anio(anio):
                print(f"  [{r.idpremio}] {r.nombre} | {r.tipo.value}")

        elif op == "6":
            nombre    = input("  Nombre del premio: ").strip()
            print("  Tipos: OSCAR, GLOBO_DE_ORO, BAFTA, EMMY, OTRO")
            tipo      = input("  Tipo (Enter = OTRO): ").strip() or "OTRO"
            categoria = input("  Categoria (Enter para omitir): ").strip() or None
            anio_s    = input("  Anio (Enter para omitir): ").strip()
            anio      = int(anio_s) if anio_s else None
            desc      = input("  Descripcion (Enter para omitir): ").strip() or None
            try:
                dao.crear(nombre=nombre, tipo=tipo, categoria=categoria,
                          anio=anio, descripcion=desc)
            except ValueError as e:
                print(f"  Error: {e}")

        elif op == "7":
            id_ = int(input("  ID a actualizar: "))
            datos = {}
            for campo in ['nombre', 'tipo', 'categoria', 'descripcion']:
                val = input(f"  Nuevo {campo} (Enter para omitir): ").strip()
                if val:
                    datos[campo] = val
            anio_s = input("  Nuevo anio (Enter para omitir): ").strip()
            if anio_s:
                datos['anio'] = int(anio_s)
            try:
                dao.actualizar(id_, **datos)
            except ValueError as e:
                print(f"  Error: {e}")

        elif op == "8":
            id_ = int(input("  ID a eliminar: "))
            confirm = input(f"  Eliminar premio {id_}? (s/n): ").strip().lower()
            if confirm == 's':
                if not dao.eliminar(id_):
                    print("  No encontrado.")

        elif op == "0":
            break

        else:
            print("  Opcion no valida.")

        pausar()


# ══════════════════════════════════════════════
#  PLATAFORMA
# ══════════════════════════════════════════════

def menu_plataforma(session):
    dao = PlataformaDAO(session)
    while True:
        separador("PLATAFORMAS")
        print("  1. Listar todas")
        print("  2. Buscar por ID")
        print("  3. Buscar por nombre")
        print("  4. Crear nueva")
        print("  5. Actualizar")
        print("  6. Eliminar")
        print("  0. Volver al menu principal")
        op = input("\n  Opcion: ").strip()

        if op == "1":
            separador("TODAS LAS PLATAFORMAS")
            registros = dao.obtener_todos()
            if not registros:
                print("  No hay plataformas registradas.")
            for r in registros:
                print(f"  [{r.idplataforma}] {r.nombre} | {r.url or '-'}")

        elif op == "2":
            id_ = int(input("  ID de la plataforma: "))
            r = dao.obtener_por_id(id_)
            if r:
                print(f"\n  ID: {r.idplataforma} | {r.nombre}")
                print(f"  URL: {r.url or '-'} | Desc: {r.descripcion or '-'}")
            else:
                print("  No encontrada.")

        elif op == "3":
            nombre = input("  Nombre a buscar: ").strip()
            resultados = dao.buscar_por_nombre(nombre)
            if not resultados:
                print("  Sin resultados.")
            for r in resultados:
                print(f"  [{r.idplataforma}] {r.nombre} | {r.url or '-'}")

        elif op == "4":
            nombre = input("  Nombre: ").strip()
            url    = input("  URL (Enter para omitir): ").strip() or None
            desc   = input("  Descripcion (Enter para omitir): ").strip() or None
            try:
                dao.crear(nombre=nombre, url=url, descripcion=desc)
            except ValueError as e:
                print(f"  Error: {e}")

        elif op == "5":
            id_ = int(input("  ID a actualizar: "))
            datos = {}
            for campo in ['nombre', 'url', 'descripcion']:
                val = input(f"  Nuevo {campo} (Enter para omitir): ").strip()
                if val:
                    datos[campo] = val
            try:
                dao.actualizar(id_, **datos)
            except ValueError as e:
                print(f"  Error: {e}")

        elif op == "6":
            id_ = int(input("  ID a eliminar: "))
            confirm = input(f"  Eliminar plataforma {id_}? (s/n): ").strip().lower()
            if confirm == 's':
                if not dao.eliminar(id_):
                    print("  No encontrada.")

        elif op == "0":
            break

        else:
            print("  Opcion no valida.")

        pausar()


# ══════════════════════════════════════════════
#  MENU PRINCIPAL
# ══════════════════════════════════════════════

def main():
    session = SessionLocal()
    try:
        while True:
            separador("NetPOLIx")
            print("  1. Videos")
            print("  2. Calificaciones")
            print("  3. Generos")
            print("  4. Directores")
            print("  5. Premios")
            print("  6. Plataformas")
            print("  0. Salir")
            separador()
            op = input("  Selecciona una opcion: ").strip()

            if op == "1":
                menu_video(session)
            elif op == "2":
                menu_calificacion(session)
            elif op == "3":
                menu_genero(session)
            elif op == "4":
                menu_director(session)
            elif op == "5":
                menu_premio(session)
            elif op == "6":
                menu_plataforma(session)
            elif op == "0":
                print("\n  Hasta luego!\n")
                break
            else:
                print("  Opcion no valida.")
                pausar()
    finally:
        session.close()


if __name__ == "__main__":
    main()