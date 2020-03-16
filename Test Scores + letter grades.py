##Justin Hill

print('This program will request 3 test scores and will output a letter grade')
print()
def get_scores():
    score1 = float(input('Enter score #1: %'))
    while score1 <= 0:
        print('Please enter a positive number.')
        score1 = float(input('Enter score #1: %'))
        
    score2 = float(input('Enter score #2: %'))
    while score2 <= 0:
        print('Please enter a positive number.')
        score2 = float(input('Enter score #2: %'))
            
    score3 = float(input('Enter score #3: %'))
    while score3 <= 0:
        print('Please enter a positive number.')
        score3 = float(input('Enter score #3: %'))
    return score1, score2, score3

def calculate_average(score1, score2, score3):
    average = (score1 + score2 + score3)/3
    return average

def assign_grade(average):
    if average >= 60:
        letter = 'D'
        if average >= 70:
            letter = 'C'
            if average >= 80:
                letter = 'B'
                if average >= 90:
                    letter = 'A'
    else:
        letter = print('Sorry, you did not pass the class.')
        letter = 'F'
    return letter

def show_results(average, letter):
    print('Average Score: %', average)
    print('Letter Grade: ', letter)

def main():
    score1, score2, score3 = get_scores()
    average = calculate_average(score1, score2, score3)
    letter = assign_grade(average)
    show_results(average, letter)

main()
