import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

home_dir = os.path.expanduser('~')

carpeta_a_monitorear = os.path.join(home_dir, 'Downloads')

CARPETAS_DESTINO = {
    'videos': os.path.join(carpeta_a_monitorear, 'Videos'),
    'musica': os.path.join(carpeta_a_monitorear, 'Música'),
    'imagenes': os.path.join(carpeta_a_monitorear, 'Imagenes'),
    'documentos': os.path.join(carpeta_a_monitorear, 'Documentos'),
    # Puedes agregar más categorías aquí
}

EXTENSIONES = {
    'videos': ['.mp4', '.mkv', '.avi', '.mov'],
    'musica': ['.mp3', '.wav', '.aac'],
    'imagenes': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'documentos': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
    # Puedes agregar más extensiones aquí
}

EXTENSIONES_IGNORADAS = ['.tmp', '.log', '.part']  

def crear_carpetas_destino():
    for carpeta in CARPETAS_DESTINO.values():
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

class ManejadorArchivos(FileSystemEventHandler):
    def on_created(self, event):
        
        if not event.is_directory:
            
            archivo = event.src_path
            
            _, extension = os.path.splitext(archivo)
            
            self.mover_archivo(archivo, extension.lower())

    def mover_archivo(self, archivo, extension):
        
        if extension in EXTENSIONES_IGNORADAS:
            return

        time.sleep(1)
        for tipo, extensiones in EXTENSIONES.items():
            if extension in extensiones:
                
                destino = CARPETAS_DESTINO.get(tipo)
                if destino:
                    
                    shutil.move(archivo, os.path.join(destino, os.path.basename(archivo)))
                    print(f'Movido: {archivo} -> {destino}')
                break
        else:
            print(f'Extensión desconocida: {archivo}, no se moverá.')

if __name__ == "__main__":
    
    crear_carpetas_destino()

    manejador = ManejadorArchivos()
    observador = Observer()
    observador.schedule(manejador, carpeta_a_monitorear, recursive=False)
    observador.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observador.stop()

    observador.join()
