import csv
import xml.etree.ElementTree as ET

# Step 1: Read solutions.csv and transform it into a dictionary
solutions = {}
with open('solutions.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        solutions[row[0]] = row[1:]

#Add the names of the files to validate
alumnes = [
    'yabbou',
    'gcaballe',
    'jcaballe',
    'itomas',
]

for alumne in alumnes:

    # Step 2: Read data.xml and convert it into a dictionary
    tree = ET.parse(alumne+'.xml')
    root = tree.getroot()
    answers = {}
    for field in root.findall('field'):
        key = field.attrib["{http://ns.adobe.com/xfdf-transition/}original"]
        value = field.text.strip()
        answers[key] = value

    # Sort the answers dictionary by keys in numerical order
    answers = dict(sorted(answers.items(), key=lambda x: int(x[0])))

    # Initialize counters
    total = 0
    correct = 0
    incorrect = 0


    # Open the file to write
    with open(alumne+'.txt', 'w') as f:
        # Loop through answers dictionary
        for key, value in answers.items():
            ans = value.translate(str.maketrans('', '', "!¡?¿")).lower().replace('  ',' ').replace('   ',' ')

            # Convert all elements of sols to lowercase
            sols = [s.lower() for s in solutions.get(key, [])]  # Getting the solutions corresponding to the key or an empty list if not found

            
            #print(f'ans: {ans} and sols: {sols}')
            if ans in sols:
                correct += 1
            else:
                incorrect += 1
                f.write(f"Camp {key}:\n{ans}\n{sols[0]}\n")
            
            total += 1

        # Print results
        f.write("\nResults:")
        f.write(f"Total answers:\t{total}")
        f.write(f"Correct answers:\t{correct}")
        f.write(f"Incorrect answers:\t{incorrect}")