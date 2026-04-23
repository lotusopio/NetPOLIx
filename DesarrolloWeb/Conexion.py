# ============================================================
# Conexion.py
# Interfaz de línea de comandos (CLI) para probar los DAOs
# del sistema SIC-NetPOLIx.
#
# Ejecución:
#   python Conexion.py
# ============================================================

from models_sic import SessionLocal
from dao import GeneroDAO, DirectorDAO, PremioDAO, PlataformaDAO, CalificacionDAO


def menu():
    print("\n==============================")
    print("   SIC-NetPOLIx  CLI")
    print("==============================")
    print("1. Listar géneros")
    print("2. Crear género")
    print("3. Listar directores")
    print("4. Crear director")
    print("5. Listar plataformas")
    print("6. Listar premios")
    print("0. Salir")
    return input("Opción: ").strip()


def main():
    print("🚀 Conectando a la base de datos...")
    session = SessionLocal()

    try:
        while True:
            opcion = menu()

            if opcion == "1":
                dao = GeneroDAO(session)
                generos = dao.obtener_todos()
                if not generos:
                    print("  (sin géneros registrados)")
                for g in generos:
                    print(f"  [{g.idgenero}] {g.nombre} — {g.descripcion or 'sin descripción'}")

            elif opcion == "2":
                nombre = input("Nombre del género: ").strip()
                descripcion = input("Descripción (opcional): ").strip() or None
                dao = GeneroDAO(session)
                try:
                    g = dao.crear(nombre=nombre, descripcion=descripcion)
                    print(f"✅ Género '{g.nombre}' creado con ID {g.idgenero}")
                except ValueError as e:
                    print(f"❌ {e}")

            elif opcion == "3":
                dao = DirectorDAO(session)
                directores = dao.obtener_todos()
                if not directores:
                    print("  (sin directores registrados)")
                for d in directores:
                    print(f"  [{d.iddirector}] {d.nombre} {d.apellido} — {d.nacionalidad or 'N/A'}")

            elif opcion == "4":
                nombre = input("Nombre: ").strip()
                apellido = input("Apellido: ").strip()
                nacionalidad = input("Nacionalidad (opcional): ").strip() or None
                dao = DirectorDAO(session)
                d = dao.crear(nombre=nombre, apellido=apellido, nacionalidad=nacionalidad)
                print(f"✅ Director '{d.nombre} {d.apellido}' creado con ID {d.iddirector}")

            elif opcion == "5":
                dao = PlataformaDAO(session)
                plataformas = dao.obtener_todos()
                if not plataformas:
                    print("  (sin plataformas registradas)")
                for p in plataformas:
                    print(f"  [{p.idplataforma}] {p.nombre} — {p.url or 'sin URL'}")

            elif opcion == "6":
                dao = PremioDAO(session)
                premios = dao.obtener_todos()
                if not premios:
                    print("  (sin premios registrados)")
                for p in premios:
                    print(f"  [{p.idpremio}] {p.nombre} ({p.tipo.value}) — año {p.anio or 'N/A'}")

            elif opcion == "0":
                print("👋 Hasta luego.")
                break

            else:
                print("❌ Opción no válida.")

    except KeyboardInterrupt:
        print("\n⚠️  Interrumpido por el usuario.")
    finally:
        session.close()
        print("🔒 Sesión cerrada.")


if __name__ == "__main__":
    main()