"""Script que iniciliza la bd con sus tablas y los roles necesarios"""

import pygogo as gogo
import logging
from app.model import db_init, Session
from app.model.role import RoleModel


log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
logger = gogo.Gogo('BD-SCRIPT', low_formatter=formatter).logger

session = Session()
logger.info("Creando BD y tablas...")
try:
    db_init()
except Exception as err:
    logger.error("No se ha podido crear la bd")
    logger.error(err)
    raise err

logger.info("Creando roles de Estudiante y Profesor")
exist = session.query(RoleModel).filter(RoleModel.name == "Estudiante").first()
if exist is None:
    estudiante = RoleModel()
    estudiante.name = 'Estudiante'
    estudiante.active = True
    session.add(estudiante)
exist = session.query(RoleModel).filter(RoleModel.name == "Profesor").first()
if exist is None:
    profesor = RoleModel()
    profesor.name = 'Profesor'
    profesor.active = True
    session.add(profesor)
session.commit()
