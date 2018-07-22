import logging
import pygogo as gogo
from app.api.exceptions.exceptions import SerializerException
from app.repository.role import RoleRepository
from app.api.serializers.role import RoleSchema


log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
logger = gogo.Gogo(__name__, low_formatter=formatter).logger


class RoleService:
    def __init__(self):
        self.role_repo = RoleRepository()

    def get_all(self, session):
        try:
            roles = self.role_repo.get_all_active(session)
            questions = RoleSchema(many=True).dump(roles)
            return questions
        except SerializerException as err:
            logger.error("Serializer exeption.")
            logger.error(err)
            raise err
        except Exception as err:
            logger.error("Exception.")
            logger.error(err)
            raise err
