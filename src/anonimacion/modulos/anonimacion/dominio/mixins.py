"""Mixins del dominio de Anonimacion de datos médicos

En este archivo usted encontrará Mixins con capacidades 
reusables en el dominio de Anonimacion de datos médicos

"""

from datetime import datetime

class MixinAuditable:
    """ Proporciona atributos de auditoría a las entidades """
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    def actualizar_fecha(self):
        self.fecha_actualizacion = datetime.now()

# Placeholder para futuras implementaciones de mixins
class PlaceholderMixin:
    pass