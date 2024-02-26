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
    'abbou',
    'castellvi',
    'corral',
    'pardo',
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
                total += 1
            else:
                try:
                    f.write(f"\nCamp {key}:\nAnswer submitted:\t{ans}\nCorrect answer:\t\t{sols[0]}\n")
                    incorrect += 1
                    total += 1
                except IndexError:
                    a = 1
                    #f.write(f"\nCamp {key}:\n{ans}\nSENSE SOLUCIÓ \n")

        # Calculate percentage of correct answers
        percentage_correct = (correct / total) * 100 if total != 0 else 0
        percentage_incorrect = (incorrect / total) * 100 if total != 0 else 0
        points_per_question = (100 / total) if total != 0 else 0

        # Print results
        f.write("\nResults:\n")
        f.write(f"Total answers:\t\t{total} ({points_per_question:.2f} points per question)\n")
        f.write(f"Correct answers:\t{correct} ({percentage_correct:.2f}%)\n")
        f.write(f"Incorrect answers:\t{incorrect} ({percentage_incorrect:.2f}%)\n")