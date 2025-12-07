import os
import random
import xml.etree.ElementTree as ET
from xml.dom import minidom

from config import COURSES, NAMES, PROGRAMS, SHARED_DIR, SURNAMES
from utils import validate_schema, logger


class ITstudent:
    def __init__(self, name: str, student_id: int, program: str, courses: dict, file_number: int):
        self.name = name
        self.student_id = student_id
        self.program = program
        self.courses = courses
        self.file_number = file_number
        self._filename = f"student{self.file_number}.xml"

    @staticmethod
    def generate_random(file_num: int):
        """Generates random student data."""
        return ITstudent(
            name=f"{random.choice(NAMES)} {random.choice(SURNAMES)}",
            student_id=random.randint(20210000, 20259999),
            program=random.choice(PROGRAMS),
            courses={c: random.randint(40, 95) for c in random.sample(COURSES, 3)},
            file_number=file_num,
        )

    def to_xml(self):
        """Wraps info into XML, saves to buffer dir, and validates schema"""
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
        xml_str = reparsed.toprettyxml(indent="  ")

        full_path = os.path.join(SHARED_DIR, self._filename)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(xml_str)
        
        # Enforce Schema
        if validate_schema(full_path):
            logger.info(f"Producer generated & validated: {self._filename}")
        else:
            logger.error(f"Producer generated INVALID XML: {self._filename}")

    @classmethod
    def from_xml_file(cls, file_identifier):
        """Reads XML, parses it into an object, and deletes the file[cite: 23, 24]."""
        filename = f"student{file_identifier}.xml"
        full_path = os.path.join(SHARED_DIR, filename)

        try:
            # extracting from XML document
            tree = ET.parse(full_path)
            root = tree.getroot()
            name = root.find("Name").text
            s_id = int(root.find("StudentID").text)
            prog = root.find("Programme").text
            courses = {c.get("name"): int(c.text) for c in root.find("Courses")}

            student = cls(name, s_id, prog, courses, file_identifier)
            os.remove(full_path)
            logger.info(f"Consumer processed & deleted: {filename}")
            return student

        except Exception as e:
            logger.error(f"Error parsing {filename}: {e}")
            return None

    def compute_avg(self) -> float:
        return sum(self.courses.values()) / len(self.courses) if self.courses else 0.0
    
    def get_status(self) -> str:
        return 'PASS' if self.compute_avg() >= 50 else 'FAIL'

    def print_report(self) -> None:
        """Calculates average and prints details."""
        avg = self.compute_avg()
        status = self.get_status()
        
        print("\n" + "="*40)
        print(f"STUDENT REPORT: {self.name}")
        print(f"ID: {self.student_id} | Prog: {self.program}")
        print("-" * 40)
        for course, mark in self.courses.items():
            print(f"  - {course}: {mark}")
        print("-" * 40)
        print(f"AVERAGE: {avg:.2f}%")
        print(f"STATUS:  {status}")
        print("="*40 + "\n")