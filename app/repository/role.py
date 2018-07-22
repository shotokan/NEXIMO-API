import sqlalchemy
import logging
import pygogo as gogo


from app.model.role import RoleModel

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
logger = gogo.Gogo(__name__, low_formatter=formatter).logger


class RoleRepository:

    def get_all_active(self, session=None):
        logger.info("Get UserRepository")
        role = session.query(RoleModel).filter(RoleModel.active)
        return role
