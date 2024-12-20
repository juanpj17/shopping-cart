from ...application.id.id_generator import IdGenerator
import uuid

class UUIDService(IdGenerator):

    def generate_id() -> str:
        return str(uuid.uuid4())