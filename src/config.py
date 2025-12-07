import os

HOST = "127.0.0.1"  # localhost
PORT = 65432
BUFFER_SIZE = 10
SHARED_DIR = "../buffer"
SCHEMA_FILE = "student.xsd"

if not os.path.exists(SHARED_DIR):
    os.makedirs(SHARED_DIR)

NAMES = [
    "Ncengwa",
    "Thando",
    "Sihlelelwe",
    "Noncedo Masango",
    "Ncobizwe",
    "Silindokuhle",
]

SURNAMES = [
    "Dlamini",
    "Msane",
    "Ngwenya",
    "Masango",
    "Shabangu",
    "Sikhondze",
]

PROGRAMS = [
    "BSc IT",
    "BSc IS",
    "Beng",
    "Master in Data Science",
    "PhD in AI",
]

COURSES = [
    "CSC411",
    "CSC402",
    "CSC301",
    "CSC212",
    "MAT101",
    "STA412",
]
