
import random
firstName = ["Grace", "Maya", "Asher", "Brooklyn", "Joseph", "Sophia", "Emily", "Aubrey", "Addison", "Violet", "Reagan", "Zoe", "Caleb", "Owen", "Camila", "Daniel", "Amelia", "Elijah", "Penelope", "Dylan", "Matthew", "Lincoln", "Layla", "Ariana", "Aria", "Emma", "Molly", "David", "Evelyn", "Savannah", "Ivy", "Aurora", "Catherine", "Maverick", "Liam", "Kennedy", "Victoria", "Everly", "Naomi", "Noah", "Victoria", "Kennedy", "Benjamin", "Mila", "Scarlett", "Samuel", "Ava", "Madelyn", "Nora", "Jacob", "Madison", "Lucy", "Aurora", "Luke", "Julian", "Charlotte", "Isabelle", "Olivia", "Nathan", "Isaac", "Leo", "Elena", "Avery", "Sebastian", "Hannah", "Ellie", "Bella", "Chloe", "Ryan", "Genesis", "Paisley", "Eli", "Xavier", "Harper", "Levi", "Hazel", "Willow", "Genesis", "Wyatt", "Aiden", "Logan", "Isaiah", "Henry", "Alexander", "Caroline", "Isabella", "Gabriel", "Hudson", "Lily", "Stella", "James", "Ethan", "Connor", "Autumn", "Jack", "Mason", "Lucas", "Piper", "Carter", "Hazel"]
lastName = ["Rodriguez", "Turner", "Ruiz", "Allen", "Alvarez", "James", "Long", "Torres", "Rogers", "Harris", "Patel", "Mendoza", "Diaz", "Anderson", "Bailey", "Campbell", "Martinez", "Jenkins", "Carter", "Hall", "Price", "Phillips", "Hill", "Garcia", "Lewis", "Gray", "Ramos", "Ross", "Kelly", "Wilson", "Moore", "Rivera", "Stewart", "Walker", "Evans", "Young", "Collins", "Taylor", "Clark", "Brown", "Cook", "Davis", "Brooks", "Reyes", "Myers", "Scott", "Murphy", "Foster", "Adams", "Williams", "Thomas", "Gutierrez", "Edwards", "Jackson", "Jones", "Ward", "Thompson", "Bennett", "Lee", "Flores", "Baker", "King", "Cox", "Richardson", "Gomez", "White", "Lopez", "Gonzalez", "Miller", "Kim", "Mitchell", "Hernandez", "Robinson", "Wright", "Johnson", "Ortiz", "Green", "Reed", "Parker", "Watson", "Perez", "Howard", "Castillo", "Perry", "Wood", "Roberts", "Peterson", "Sanders", "Morales", "Cooper", "Jimenez", "Chavez", "Nguyen", "Ramirez", "Morgan", "Morris", "Cruz", "Hughes", "Martin", "Nelson"]
cities = ["Seattle","New york","Boston","Los Angles","Toronto","Huston","Austin","dallas","San Fransisco","Quebec","Miami","Tampa","Anchorage","Boise"]
college = ["Washington State Univerity","Univeristy Of Washington","Boise State Univerity","Texas A & M","Miami Dade Univerity","University of California Los Angles"]
major = ["Computer Science","Business","Accounting","Criminal Justice","Mechanical engineering","Electrical Engineering","Civil Engineering","Phyisics","Chemistry","Biology"]
first = 0
last = 0
file = open("Alumni.csv","w")

while(first <100):
    while(last<100):
        file.write(firstName[first]+","+lastName[last]+","+cities[random.randint(0,13)]+","+college[random.randint(0,5)]+","+major[random.randint(0,9)]+","+str(random.randint(1976,2024))+"\n")
        last = last +1
    last = 0
    first = first +1
file.close
