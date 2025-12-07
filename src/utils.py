import logging
import xmlschema # type: ignore

from config import SCHEMA_FILE

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    filename='students.log',
    filemode='a',
)

logger = logging.getLogger(__name__)


def validate_schema(xml_path: str) -> bool:
    """Validates the generated XML against the XSD schema."""
    try:
        schema = xmlschema.XMLSchema(SCHEMA_FILE)
        schema.validate(xml_path)
        return True
    except Exception as e:
        logger.error(f"Schema Validation Failed for {xml_path}: {e}")
        return False

