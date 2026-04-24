# ============================================================
# app.py
# API REST con Flask — SIC-NetPOLIx
#
# Endpoints disponibles:
#   /calificaciones   CRUD de calificaciones
#   /generos          CRUD de géneros
#   /directores       CRUD de directores
#   /premios          CRUD de premios
#   /plataformas      CRUD de plataformas
#   /health           Health check
#
# Ejecución:
#   python app.py
#   Servidor disponible en http://localhost:5000
# ============================================================
from flask import Flask, request, jsonify
from models_sic import SessionLocal, init_db
from VideoDAO import VideoDAO
from CalificacionDAO import CalificacionDAO
from GeneroDAO import GeneroDAO
from DirectorDAO import DirectorDAO
from PremioDAO import PremioDAO
from PlataformaDAO import PlataformaDAO
app = Flask(__name__)


def get_video_dao():
    session = SessionLocal()
    return VideoDAO(session), session

def get_calificacion_dao():
    session = SessionLocal()
    return CalificacionDAO(session), session

def get_genero_dao():
    session = SessionLocal()
    return GeneroDAO(session), session

def get_director_dao():
    session = SessionLocal()
    return DirectorDAO(session), session

def get_premio_dao():
    session = SessionLocal()
    return PremioDAO(session), session

def get_plataforma_dao():
    session = SessionLocal()
    return PlataformaDAO(session), session

def error_response(mensaje: str, codigo: int = 400):
    return jsonify({"error": mensaje}), codigo

def success_response(datos, codigo: int = 200):
    return jsonify(datos), codigo

# ════════════════════════════════════════════════════════════════
#  VIDEO
# ════════════════════════════════════════════════════════════════

@app.route('/videos', methods=['POST'])
def crear_video():
    try:
        data = request.get_json()
        if 'titulo' not in data:
            return error_response("Campo requerido: titulo", 400)
        dao, session = get_video_dao()
        try:
            v = dao.crear(titulo=data['titulo'],
                          anio_produccion=data.get('anio_produccion'),
                          duracion=data.get('duracion'),
                          descripcion=data.get('descripcion'))
            return success_response({'id': v.idvideo, 'titulo': v.titulo,
                                     'anio_produccion': v.anio_produccion,
                                     'duracion': v.duracion,
                                     'mensaje': 'Video creado exitosamente'}, 201)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al crear video: {str(e)}", 500)

@app.route('/videos', methods=['GET'])
def obtener_videos():
    try:
        dao, session = get_video_dao()
        try:
            registros = dao.obtener_todos()
            datos = [{'id': v.idvideo, 'titulo': v.titulo,
                      'anio_produccion': v.anio_produccion,
                      'duracion': v.duracion} for v in registros]
            return success_response({'total': len(datos), 'videos': datos}, 200)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al obtener videos: {str(e)}", 500)

@app.route('/videos/<int:video_id>', methods=['GET'])
def obtener_video(video_id):
    try:
        dao, session = get_video_dao()
        try:
            v = dao.obtener_por_id(video_id)
            if not v:
                return error_response(f"No existe video con ID {video_id}", 404)
            return success_response({'id': v.idvideo, 'titulo': v.titulo,
                                     'anio_produccion': v.anio_produccion,
                                     'duracion': v.duracion,
                                     'descripcion': v.descripcion}, 200)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al obtener video: {str(e)}", 500)

@app.route('/videos/<int:video_id>', methods=['PUT'])
def actualizar_video(video_id):
    try:
        data = request.get_json()
        dao, session = get_video_dao()
        try:
            v = dao.actualizar(video_id, **data)
            return success_response({'id': v.idvideo, 'titulo': v.titulo,
                                     'mensaje': 'Video actualizado exitosamente'}, 200)
        finally:
            session.close()
    except ValueError as ve:
        return error_response(str(ve), 404 if "No existe" in str(ve) else 400)
    except Exception as e:
        return error_response(f"Error al actualizar video: {str(e)}", 500)

@app.route('/videos/<int:video_id>', methods=['DELETE'])
def eliminar_video(video_id):
    try:
        dao, session = get_video_dao()
        try:
            if dao.eliminar(video_id):
                return success_response({'id': video_id,
                                         'mensaje': 'Video eliminado exitosamente'}, 200)
            return error_response(f"No existe video con ID {video_id}", 404)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al eliminar video: {str(e)}", 500)

# ════════════════════════════════════════════════════════════════
#  CALIFICACION
# ════════════════════════════════════════════════════════════════

@app.route('/calificaciones', methods=['POST'])
def crear_calificacion():
    try:
        data = request.get_json()
        if 'idvideo' not in data or 'nivel' not in data:
            return error_response("Campos requeridos: idvideo, nivel", 400)
        dao, session = get_calificacion_dao()
        try:
            c = dao.crear(idvideo=data['idvideo'], nivel=data['nivel'],
                          puntaje=data.get('puntaje'), comentario=data.get('comentario'))
            return success_response({'id': c.idcalificacion, 'idvideo': c.idvideo,
                                     'nivel': c.nivel.value, 'puntaje': c.puntaje,
                                     'comentario': c.comentario,
                                     'mensaje': 'Calificación creada exitosamente'}, 201)
        finally:
            session.close()
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(f"Error al crear calificación: {str(e)}", 500)

@app.route('/calificaciones', methods=['GET'])
def obtener_calificaciones():
    try:
        dao, session = get_calificacion_dao()
        try:
            registros = dao.obtener_todos()
            datos = [{'id': c.idcalificacion, 'idvideo': c.idvideo,
                      'nivel': c.nivel.value, 'puntaje': c.puntaje,
                      'comentario': c.comentario} for c in registros]
            return success_response({'total': len(datos), 'calificaciones': datos}, 200)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al obtener calificaciones: {str(e)}", 500)

@app.route('/calificaciones/<int:calificacion_id>', methods=['GET'])
def obtener_calificacion(calificacion_id):
    try:
        dao, session = get_calificacion_dao()
        try:
            c = dao.obtener_por_id(calificacion_id)
            if not c:
                return error_response(f"No existe calificación con ID {calificacion_id}", 404)
            return success_response({'id': c.idcalificacion, 'idvideo': c.idvideo,
                                     'nivel': c.nivel.value, 'puntaje': c.puntaje,
                                     'comentario': c.comentario}, 200)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al obtener calificación: {str(e)}", 500)

@app.route('/calificaciones/video/<int:idvideo>', methods=['GET'])
def calificaciones_por_video(idvideo):
    try:
        dao, session = get_calificacion_dao()
        try:
            registros = dao.obtener_por_video(idvideo)
            datos = [{'id': c.idcalificacion, 'nivel': c.nivel.value,
                      'puntaje': c.puntaje, 'comentario': c.comentario} for c in registros]
            return success_response({'total': len(datos), 'calificaciones': datos}, 200)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error: {str(e)}", 500)

@app.route('/calificaciones/<int:calificacion_id>', methods=['PUT'])
def actualizar_calificacion(calificacion_id):
    try:
        data = request.get_json()
        dao, session = get_calificacion_dao()
        try:
            c = dao.actualizar(calificacion_id, **data)
            return success_response({'id': c.idcalificacion, 'nivel': c.nivel.value,
                                     'mensaje': 'Calificación actualizada exitosamente'}, 200)
        finally:
            session.close()
    except ValueError as ve:
        return error_response(str(ve), 404 if "No existe" in str(ve) else 400)
    except Exception as e:
        return error_response(f"Error al actualizar calificación: {str(e)}", 500)

@app.route('/calificaciones/<int:calificacion_id>', methods=['DELETE'])
def eliminar_calificacion(calificacion_id):
    try:
        dao, session = get_calificacion_dao()
        try:
            if dao.eliminar(calificacion_id):
                return success_response({'id': calificacion_id, 'mensaje': 'Calificación eliminada exitosamente'}, 200)
            return error_response(f"No existe calificación con ID {calificacion_id}", 404)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al eliminar calificación: {str(e)}", 500)


# ════════════════════════════════════════════════════════════════
#  GENERO
# ════════════════════════════════════════════════════════════════

@app.route('/generos', methods=['POST'])
def crear_genero():
    try:
        data = request.get_json()
        if 'nombre' not in data:
            return error_response("Campo requerido: nombre", 400)
        dao, session = get_genero_dao()
        try:
            g = dao.crear(nombre=data['nombre'], descripcion=data.get('descripcion'))
            return success_response({'id': g.idgenero, 'nombre': g.nombre,
                                     'descripcion': g.descripcion,
                                     'mensaje': 'Género creado exitosamente'}, 201)
        finally:
            session.close()
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(f"Error al crear género: {str(e)}", 500)

@app.route('/generos', methods=['GET'])
def obtener_generos():
    try:
        dao, session = get_genero_dao()
        try:
            registros = dao.obtener_todos()
            datos = [{'id': g.idgenero, 'nombre': g.nombre, 'descripcion': g.descripcion} for g in registros]
            return success_response({'total': len(datos), 'generos': datos}, 200)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al obtener géneros: {str(e)}", 500)

@app.route('/generos/<int:genero_id>', methods=['GET'])
def obtener_genero(genero_id):
    try:
        dao, session = get_genero_dao()
        try:
            g = dao.obtener_por_id(genero_id)
            if not g:
                return error_response(f"No existe género con ID {genero_id}", 404)
            return success_response({'id': g.idgenero, 'nombre': g.nombre, 'descripcion': g.descripcion}, 200)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al obtener género: {str(e)}", 500)

@app.route('/generos/buscar/<nombre>', methods=['GET'])
def buscar_genero(nombre):
    try:
        dao, session = get_genero_dao()
        try:
            registros = dao.buscar_por_nombre(nombre)
            datos = [{'id': g.idgenero, 'nombre': g.nombre} for g in registros]
            return success_response({'total': len(datos), 'resultados': datos}, 200)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al buscar género: {str(e)}", 500)

@app.route('/generos/<int:genero_id>', methods=['PUT'])
def actualizar_genero(genero_id):
    try:
        data = request.get_json()
        dao, session = get_genero_dao()
        try:
            g = dao.actualizar(genero_id, **data)
            return success_response({'id': g.idgenero, 'nombre': g.nombre,
                                     'mensaje': 'Género actualizado exitosamente'}, 200)
        finally:
            session.close()
    except ValueError as ve:
        return error_response(str(ve), 404 if "No existe" in str(ve) else 400)
    except Exception as e:
        return error_response(f"Error al actualizar género: {str(e)}", 500)

@app.route('/generos/<int:genero_id>', methods=['DELETE'])
def eliminar_genero(genero_id):
    try:
        dao, session = get_genero_dao()
        try:
            if dao.eliminar(genero_id):
                return success_response({'id': genero_id, 'mensaje': 'Género eliminado exitosamente'}, 200)
            return error_response(f"No existe género con ID {genero_id}", 404)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al eliminar género: {str(e)}", 500)


# ════════════════════════════════════════════════════════════════
#  DIRECTOR
# ════════════════════════════════════════════════════════════════

@app.route('/directores', methods=['POST'])
def crear_director():
    try:
        data = request.get_json()
        if 'nombre' not in data or 'apellido' not in data:
            return error_response("Campos requeridos: nombre, apellido", 400)
        dao, session = get_director_dao()
        try:
            d = dao.crear(nombre=data['nombre'], apellido=data['apellido'],
                          nacionalidad=data.get('nacionalidad'),
                          fecha_nac=data.get('fecha_nac'),
                          biografia=data.get('biografia'))
            return success_response({'id': d.iddirector, 'nombre': d.nombre,
                                     'apellido': d.apellido, 'nacionalidad': d.nacionalidad,
                                     'mensaje': 'Director creado exitosamente'}, 201)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al crear director: {str(e)}", 500)

@app.route('/directores', methods=['GET'])
def obtener_directores():
    try:
        dao, session = get_director_dao()
        try:
            registros = dao.obtener_todos()
            datos = [{'id': d.iddirector, 'nombre': d.nombre,
                      'apellido': d.apellido, 'nacionalidad': d.nacionalidad} for d in registros]
            return success_response({'total': len(datos), 'directores': datos}, 200)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al obtener directores: {str(e)}", 500)

@app.route('/directores/<int:director_id>', methods=['GET'])
def obtener_director(director_id):
    try:
        dao, session = get_director_dao()
        try:
            d = dao.obtener_por_id(director_id)
            if not d:
                return error_response(f"No existe director con ID {director_id}", 404)
            return success_response({'id': d.iddirector, 'nombre': d.nombre,
                                     'apellido': d.apellido, 'nacionalidad': d.nacionalidad,
                                     'fecha_nac': str(d.fecha_nac) if d.fecha_nac else None,
                                     'biografia': d.biografia}, 200)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al obtener director: {str(e)}", 500)

@app.route('/directores/buscar/<nombre>', methods=['GET'])
def buscar_director(nombre):
    try:
        dao, session = get_director_dao()
        try:
            registros = dao.buscar_por_nombre(nombre)
            datos = [{'id': d.iddirector, 'nombre': d.nombre, 'apellido': d.apellido} for d in registros]
            return success_response({'total': len(datos), 'resultados': datos}, 200)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al buscar director: {str(e)}", 500)

@app.route('/directores/<int:director_id>', methods=['PUT'])
def actualizar_director(director_id):
    try:
        data = request.get_json()
        dao, session = get_director_dao()
        try:
            d = dao.actualizar(director_id, **data)
            return success_response({'id': d.iddirector, 'nombre': f"{d.nombre} {d.apellido}",
                                     'mensaje': 'Director actualizado exitosamente'}, 200)
        finally:
            session.close()
    except ValueError as ve:
        return error_response(str(ve), 404 if "No existe" in str(ve) else 400)
    except Exception as e:
        return error_response(f"Error al actualizar director: {str(e)}", 500)

@app.route('/directores/<int:director_id>', methods=['DELETE'])
def eliminar_director(director_id):
    try:
        dao, session = get_director_dao()
        try:
            if dao.eliminar(director_id):
                return success_response({'id': director_id, 'mensaje': 'Director eliminado exitosamente'}, 200)
            return error_response(f"No existe director con ID {director_id}", 404)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al eliminar director: {str(e)}", 500)


# ════════════════════════════════════════════════════════════════
#  PREMIO
# ════════════════════════════════════════════════════════════════

@app.route('/premios', methods=['POST'])
def crear_premio():
    try:
        data = request.get_json()
        if 'nombre' not in data:
            return error_response("Campo requerido: nombre", 400)
        dao, session = get_premio_dao()
        try:
            p = dao.crear(nombre=data['nombre'], tipo=data.get('tipo', 'OTRO'),
                          categoria=data.get('categoria'), anio=data.get('anio'),
                          descripcion=data.get('descripcion'))
            return success_response({'id': p.idpremio, 'nombre': p.nombre,
                                     'tipo': p.tipo.value, 'categoria': p.categoria,
                                     'anio': p.anio,
                                     'mensaje': 'Premio creado exitosamente'}, 201)
        finally:
            session.close()
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(f"Error al crear premio: {str(e)}", 500)

@app.route('/premios', methods=['GET'])
def obtener_premios():
    try:
        dao, session = get_premio_dao()
        try:
            registros = dao.obtener_todos()
            datos = [{'id': p.idpremio, 'nombre': p.nombre,
                      'tipo': p.tipo.value, 'categoria': p.categoria,
                      'anio': p.anio} for p in registros]
            return success_response({'total': len(datos), 'premios': datos}, 200)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al obtener premios: {str(e)}", 500)

@app.route('/premios/<int:premio_id>', methods=['GET'])
def obtener_premio(premio_id):
    try:
        dao, session = get_premio_dao()
        try:
            p = dao.obtener_por_id(premio_id)
            if not p:
                return error_response(f"No existe premio con ID {premio_id}", 404)
            return success_response({'id': p.idpremio, 'nombre': p.nombre,
                                     'tipo': p.tipo.value, 'categoria': p.categoria,
                                     'anio': p.anio, 'descripcion': p.descripcion}, 200)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al obtener premio: {str(e)}", 500)

@app.route('/premios/buscar/<nombre>', methods=['GET'])
def buscar_premio(nombre):
    try:
        dao, session = get_premio_dao()
        try:
            registros = dao.buscar_por_nombre(nombre)
            datos = [{'id': p.idpremio, 'nombre': p.nombre, 'tipo': p.tipo.value, 'anio': p.anio} for p in registros]
            return success_response({'total': len(datos), 'resultados': datos}, 200)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al buscar premio: {str(e)}", 500)

@app.route('/premios/<int:premio_id>', methods=['PUT'])
def actualizar_premio(premio_id):
    try:
        data = request.get_json()
        dao, session = get_premio_dao()
        try:
            p = dao.actualizar(premio_id, **data)
            return success_response({'id': p.idpremio, 'nombre': p.nombre,
                                     'mensaje': 'Premio actualizado exitosamente'}, 200)
        finally:
            session.close()
    except ValueError as ve:
        return error_response(str(ve), 404 if "No existe" in str(ve) else 400)
    except Exception as e:
        return error_response(f"Error al actualizar premio: {str(e)}", 500)

@app.route('/premios/<int:premio_id>', methods=['DELETE'])
def eliminar_premio(premio_id):
    try:
        dao, session = get_premio_dao()
        try:
            if dao.eliminar(premio_id):
                return success_response({'id': premio_id, 'mensaje': 'Premio eliminado exitosamente'}, 200)
            return error_response(f"No existe premio con ID {premio_id}", 404)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al eliminar premio: {str(e)}", 500)


# ════════════════════════════════════════════════════════════════
#  PLATAFORMA
# ════════════════════════════════════════════════════════════════

@app.route('/plataformas', methods=['POST'])
def crear_plataforma():
    try:
        data = request.get_json()
        if 'nombre' not in data:
            return error_response("Campo requerido: nombre", 400)
        dao, session = get_plataforma_dao()
        try:
            p = dao.crear(nombre=data['nombre'], url=data.get('url'), descripcion=data.get('descripcion'))
            return success_response({'id': p.idplataforma, 'nombre': p.nombre,
                                     'url': p.url, 'descripcion': p.descripcion,
                                     'mensaje': 'Plataforma creada exitosamente'}, 201)
        finally:
            session.close()
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(f"Error al crear plataforma: {str(e)}", 500)

@app.route('/plataformas', methods=['GET'])
def obtener_plataformas():
    try:
        dao, session = get_plataforma_dao()
        try:
            registros = dao.obtener_todos()
            datos = [{'id': p.idplataforma, 'nombre': p.nombre, 'url': p.url} for p in registros]
            return success_response({'total': len(datos), 'plataformas': datos}, 200)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al obtener plataformas: {str(e)}", 500)

@app.route('/plataformas/<int:plataforma_id>', methods=['GET'])
def obtener_plataforma(plataforma_id):
    try:
        dao, session = get_plataforma_dao()
        try:
            p = dao.obtener_por_id(plataforma_id)
            if not p:
                return error_response(f"No existe plataforma con ID {plataforma_id}", 404)
            return success_response({'id': p.idplataforma, 'nombre': p.nombre,
                                     'url': p.url, 'descripcion': p.descripcion}, 200)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al obtener plataforma: {str(e)}", 500)

@app.route('/plataformas/buscar/<nombre>', methods=['GET'])
def buscar_plataforma(nombre):
    try:
        dao, session = get_plataforma_dao()
        try:
            registros = dao.buscar_por_nombre(nombre)
            datos = [{'id': p.idplataforma, 'nombre': p.nombre, 'url': p.url} for p in registros]
            return success_response({'total': len(datos), 'resultados': datos}, 200)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al buscar plataforma: {str(e)}", 500)

@app.route('/plataformas/<int:plataforma_id>', methods=['PUT'])
def actualizar_plataforma(plataforma_id):
    try:
        data = request.get_json()
        dao, session = get_plataforma_dao()
        try:
            p = dao.actualizar(plataforma_id, **data)
            return success_response({'id': p.idplataforma, 'nombre': p.nombre,
                                     'mensaje': 'Plataforma actualizada exitosamente'}, 200)
        finally:
            session.close()
    except ValueError as ve:
        return error_response(str(ve), 404 if "No existe" in str(ve) else 400)
    except Exception as e:
        return error_response(f"Error al actualizar plataforma: {str(e)}", 500)

@app.route('/plataformas/<int:plataforma_id>', methods=['DELETE'])
def eliminar_plataforma(plataforma_id):
    try:
        dao, session = get_plataforma_dao()
        try:
            if dao.eliminar(plataforma_id):
                return success_response({'id': plataforma_id, 'mensaje': 'Plataforma eliminada exitosamente'}, 200)
            return error_response(f"No existe plataforma con ID {plataforma_id}", 404)
        finally:
            session.close()
    except Exception as e:
        return error_response(f"Error al eliminar plataforma: {str(e)}", 500)


# ── Health check y errores ───────────────────────────────────────────────────

@app.route('/health', methods=['GET'])
def health_check():
    return success_response({'status': 'OK', 'servicio': 'SIC-NetPOLIx API', 'version': '1.0'}, 200)

@app.errorhandler(404)
def not_found(error):
    return error_response("Endpoint no encontrado", 404)

@app.errorhandler(405)
def method_not_allowed(error):
    return error_response("Método HTTP no permitido", 405)

@app.errorhandler(500)
def internal_error(error):
    return error_response("Error interno del servidor", 500)


if __name__ == "__main__":
    print("🚀 Iniciando SIC-NetPOLIx API...")
    print("📍 Servidor disponible en http://localhost:5000")
    print("✅ Health check: http://localhost:5000/health")
    init_db()   # Crea las tablas solo al arrancar el servidor
    app.run(debug=True, port=5000, host='0.0.0.0')