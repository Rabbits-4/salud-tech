"""Reglas de negocio del dominio de procesamiento de datos médicos

En este archivo usted encontrará reglas de negocio del dominio de procesamiento de datos médicos

"""

from salud_tech.seedwork.dominio.reglas import ReglaNegocio

class ImagenConUrlValida(ReglaNegocio):    
    url: str

    def __init__(self, url, mensaje='La URL de la imagen no es válida'):
        super().__init__(mensaje)
        self.url = url

    def es_valido(self) -> bool:
        return self.url.startswith('http')

class DiagnosticoDebeTenerPatologia(ReglaNegocio):
    patologia: str

    def __init__(self, patologia, mensaje='El diagnóstico debe contener una patología válida'):
        super().__init__(mensaje)
        self.patologia = patologia

    def es_valido(self) -> bool:
        return bool(self.patologia)

class MetadataDebeSerCompleta(ReglaNegocio):
    metadata: dict

    def __init__(self, metadata, mensaje='Los metadatos deben estar completos'):
        super().__init__(mensaje)
        self.metadata = metadata

    def es_valido(self) -> bool:
        return all(self.metadata.values()) if self.metadata else False

class PacienteDebeTenerHistorial(ReglaNegocio):
    historial: str

    def __init__(self, historial, mensaje='El paciente debe contar con un historial clínico registrado'):
        super().__init__(mensaje)
        self.historial = historial

    def es_valido(self) -> bool:
        return bool(self.historial)

class FechaDiagnosticoDebeSerValida(ReglaNegocio):
    fecha: str

    def __init__(self, fecha, mensaje='La fecha del diagnóstico debe ser válida y no futura'):
        super().__init__(mensaje)
        self.fecha = fecha

    def es_valido(self) -> bool:
        from datetime import datetime
        try:
            fecha_diagnostico = datetime.strptime(self.fecha, "%Y-%m-%d")
            return fecha_diagnostico <= datetime.now()
        except ValueError:
            return False
