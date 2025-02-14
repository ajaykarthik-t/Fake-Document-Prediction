import json
import random

# Load existing database
file_path = "users_db.json"

try:
    with open(file_path, "r") as file:
        db = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    db = {}

# Tamil first and last names
first_names = [
    "Arun", "Balaji", "Chandru", "Dinesh", "Elango", "Gokul", "Hari", "Ilayaraja", "Jayakumar", "Karthik",
    "Lakshmanan", "Manikandan", "Naveen", "Omprakash", "Prabhu", "Quadir", "Ramesh", "Senthil", "Thirumal", "Vignesh",
    "Venkatesh", "Yogesh", "Bharath", "Rajkumar", "Saravanan", "Muthu", "Vetrivel", "Ravi", "Mohan", "Ganesh",
    "Sivakumar", "Vijay", "Guhan", "Aravind", "Sathish", "Kannan", "Raghu", "Udhay", "Suresh", "Deepak",
    "Sundar", "Kumaran", "Thiruvengadam", "Jagan", "Sakthivel", "Jeeva", "Arul", "Vimal", "Ramkumar", "Vasanth"
]


last_names = [
    "Subramanian", "Krishnan", "Murugan", "Panneerselvam", "Rajendran", "Sundar", "Velu", "Sekar", "Aravindhan", "Ganapathy",
    "Chidambaram", "Eswaran", "Gopal", "Iyer", "Jeyaraj", "Kumaran", "Loganathan", "Mahadevan", "Narayanan", "Palaniappan",
    "Periyasamy", "Thangaraj", "Veerappan", "Sivaprakash", "Ramalingam", "Manoharan", "Natarajan", "Kaliappan", "Thirunavukarasu", "Balasubramaniam",
    "Padmanabhan", "Devaraj", "Somasundaram", "Soundararajan", "Muthusamy", "Shanmugam", "Alagappan", "Valluvan", "Perumal", "Marimuthu",
    "Karthikeyan", "Arumugam", "Velmurugan", "Ravichandran", "Rangarajan", "Chockalingam", "Jayachandran", "Selvakumar", "Ramanujam", "Madhavan"
]


# Generate 5000 users
for i in range(len(db) + 1, len(db) + 5001):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    username = f"user{i}"
    full_name = f"{first_name} {last_name}"
    db[username] = full_name

# Save updated database
with open(file_path, "w") as file:
    json.dump(db, file, indent=4, ensure_ascii=False)

print("✅ 5000 Tamil users added successfully!")
