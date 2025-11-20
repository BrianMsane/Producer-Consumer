import os
import random
import xml.etree.ElementTree as ET
from xml.dom import minidom

from config import COURSES
from config import NAMES
from config import PROGRAMS
from config import SHARED_DIR
from config import SURNAMES
from utils import logger


class ITstudent:
    def __init__(
        self, name: str, student_id: int, program: str, courses: dict, file_number: int
    ):
        assert file_number >= 1 and file_number <= 10, (
            "File number should be between 1 and 10"
        )

        self.name = name
        self.student_id = student_id
        self.program = program
        self.courses = courses
        self.file_number = file_number
        self._filename = f"student{self.file_number}.xml"

    @staticmethod
    def generate_random(file_num):
        """Generates a student using a random generating algorithm."""
        return ITstudent(
            name=f"{random.choice(NAMES)} {random.choice(SURNAMES)}",
            student_id=random.randint(20210000, 20259999),
            program=random.choice(PROGRAMS),
            courses={c: random.randint(40, 95) for c in random.sample(COURSES, 3)},
            file_number=file_num,
        )

    def compute_average(self) -> float:
        if not self.courses:
            logger.debug("No courses found for student %s", self.name)
            return 0.0
        return sum(self.courses.values()) / len(self.courses)

    def get_pass_status(self) -> str:
        return "Pass" if self.compute_average() >= 50 else "Fail"

    def to_xml(self):
        """Wraps student info into XML format and saves to shared directory."""

        xml_string = self.get_xml_string()

        full_path = os.path.join(SHARED_DIR, self._filename)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(xml_string)

        logger.info("Producer Created %s", str(self._filename))

    @classmethod
    def process_xml_file(cls, file_identifier):
        """Parses an XML file, returns a student object."""

        is_server_mode = isinstance(file_identifier, str)

        if is_server_mode:
            filename = file_identifier
            full_path = filename
            file_num = 1
        else:
            filename = f"student{file_identifier}.xml"
            full_path = os.path.join(SHARED_DIR, filename)
            file_num = file_identifier

        try:
            tree = ET.parse(full_path)
            root = tree.getroot()
            name = root.find("Name").text
            s_id = int(root.find("StudentID").text)
            prog = root.find("Programme").text

            courses = {}
            for c in root.find("Courses"):
                courses[c.get("name")] = int(c.text)

            if not is_server_mode:
                os.remove(full_path)
                logger.info("Consumer Deleted %s", str(filename))

            return cls(name, s_id, prog, courses, file_number=file_num)

        except FileNotFoundError:
            logger.error("File %s not found.", full_path)
            raise
        except Exception as e:
            logger.error("Error parsing XML: %s", str(e))
            return None

    def get_xml_string(self) -> str:
        """Returns the XML string representation of the object."""
        root = ET.Element("ITstudent")
        ET.SubElement(root, "Name").text = self.name
        ET.SubElement(root, "StudentID").text = str(self.student_id)
        ET.SubElement(root, "Programme").text = self.program

        courses_elem = ET.SubElement(root, "Courses")
        for course, mark in self.courses.items():
            c_elem = ET.SubElement(courses_elem, "Course")
            c_elem.set("name", course)
            c_elem.text = str(mark)

        rough_string = ET.tostring(root, encoding="utf-8")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
