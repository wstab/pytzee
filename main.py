import random

TOTAL_DICE = 5
DICE_FACES = 6
SCORE_TYPES = ["1's", "2's", "3's", "4's", "5's", "6's", 'three of a kind', 'four of a kind', 'full house', 'small straight', 'large straight', 'yahtzee', \
'chance']
ACCEPTIONS = ['count 1', 'count 2', 'count 3', 'count 4', 'count 5', 'count 6', 'three of a kind', '3 of a kind', 'four of a kind', '4 of a kind', 'full ho\
use', 'small straight', 'large straight', 'pytzee', 'chance', 'yahtzee', 'skip']


def roll_dice():
    """
    :return: a list containing five integers representing dice rolls between 1 and 6.
    """
    roll_list = []
    for i in range(TOTAL_DICE):
        roll_list.append(random.randint(1, 6))
    return roll_list


def choice_options(roll):
    # returns a list containing the possible ways a user can count the roll excluding "count" and "chance"
    counts = []
    amounts = num_roll(roll)

    if 3 in amounts:
        counts.append('three of a kind')
    if 4 in amounts:
        counts.append('four of a kind')
    if 3 in amounts and 2 in amounts:
        counts.append('full house')
    if 5 in amounts:
        counts.append('yahtzee')

    for i in range(len(amounts)-3):
        if amounts[i] >= 1 and amounts[i+1] >= 1 and amounts[i+2] >= 1 and amounts[i+3] >= 1:
            counts.append('small straight')
    for i in range(len(amounts)-4):
        if amounts[i] >= 1 and amounts[i+1] >= 1 and amounts[i+2] >= 1 and amounts[i+3] >= 1 and amounts[i+4] >= 1:
            counts.append('large straight')

    return counts


def num_roll(roll):
    # returns a list containing the total number of times each dice number was rolled
    amount = [0, 0, 0, 0, 0, 0]
    for x in roll:
        amount[x-1] +=1
    return amount


def score_round(roll, choice, counts):
    # returns the score of the round
    choice_key = score_key(choice)
    if ((choice_key == 'three of a kind' or choice_key == 'four of a kind') and ('three of a kind' in counts or 'four of a kind' in counts)) or choice == '\
chance':
        total = 0
        for x in roll:
            total += x
        return total
    if choice == 'full house' and 'full house' in counts:
        return 25
    if choice == 'small straight' and 'small straight' in counts:
        return 30
    if choice == 'large straight' and 'large straight' in counts:
        return 40
    if choice_key == 'yahtzee' and 'yahtzee' in counts:
        return 50
    if 'count' in choice:
        num = get_count(choice)
        amount = num_roll(roll)
        return amount[num-1]*num


def get_count(choice):
    # returns the number the user wants to count
    words = choice.split()
    num = int(words[1])
    return num


def score_key(choice):
    # returns the user's choice in a way that it can be used as a key in the scorecard dictionary
    if 'count' in choice:
        words = choice.split()
        return words[1] + "'s"
    if 'three of a kind' == choice or '3 of a kind' == choice:
        return 'three of a kind'
    if 'four of a kind' == choice or '4 of a kind' == choice:
        return 'four of a kind'
    if 'pytzee' == choice or 'yahtzee' == choice:
        return 'yahtzee'
    if 'chance' == choice:
        return 'chance'
    return choice


def valid_input(used, counts, roll):
    # returns user input that would not cause the program to crash
    choice = input('How would you like to count this dice roll? ').lower()
    choice_key = score_key(choice)

    # filters out invalid input
    if choice not in ACCEPTIONS:
        print('This is not a valid count')
        choice = valid_input(used, counts, roll)

    # filters out choices that are impossible with the current roll
    elif choice_key not in counts and 'count' not in choice and 'chance' != choice and 'skip' != choice:
        print(f"There is not a {choice_key} in this roll")
        choice = valid_input(used, counts, roll)

    # makers sure the choice hasn't been used already
    elif choice_key in used and choice_key != 'yahtzee':
        print('There was already a score in that slot.')
        choice = valid_input(used, counts, roll)

    # makes sure the number the user wants to count is in the roll
    elif 'count' in choice and get_count(choice) not in roll:
        print(f'There are no {choice_key} in this roll.')
        choice = valid_input(used, counts, roll)

    return choice


def play_game(num_rounds):
    score = 0
    counts_score = 0
    used = []
    scorecard = {"1's": 0, "2's": 0, "3's": 0, "4's": 0, "5's":0, "6's": 0, 'three of a kind': 0, 'four of a kind': 0, 'full house': 0, 'small straight': 0\
, 'large straight': 0, 'yahtzee': 0, 'chance': 0}

    for i in range(num_rounds):
        print(f'***** Beginning Round {str(i+1)} *****')
        print(f'\tYour score is: {str(score)}')
        roll = roll_dice()
        counts = choice_options(roll)
        for x in roll:
            print(f'{str(x)}\t', end='')
        print('')

        choice = valid_input(used, counts, roll)
        choice_key = score_key(choice)

        if choice != 'skip':
            current = score_round(roll, choice, counts)
            # adds another 50 if the user gets multiple yahtzees adding 100 to total
            if choice_key == 'yahtzee' and 'yahtzee' in used:
                current += 50
            score += current
            scorecard[choice_key] += current

            used.append(choice_key)

            if 'count' in choice:
                print(f'Accepted the {get_count(choice)}')
                counts_score += current
            elif 'three of a kind' == choice_key:
                print('Three of a kind!')
            elif 'four of a kind' == choice_key:
                print('Four of a kind!')
            elif 'small straight' == choice or 'large straight' == choice or 'full house' == choice:
                print(f'You have a {choice} and get {str(current)} points.')
            elif 'chance' == choice:
                print(f'Chance, you get {str(current)} points.')
            elif choice_key == 'yahtzee':
                print(f'Yahtzee!!!!')

        # prints scorecard by iterating through dictionary
        print('\n\tScorecard:')
        for i in range(len(SCORE_TYPES)):
            print(f'\t  {SCORE_TYPES[i]}: {scorecard[SCORE_TYPES[i]]}')
        print('\n')

    if counts_score >= 63:
        # adds 35 point bonus
        print("You've also earned a 35 point bonus for having a total score of 63 or greater\n")
        total += 35
    print(f'Your final score was {str(score)}')


if __name__ == '__main__':
    num_rounds = int(input('What is the number of rounds that you want to play? '))
    seed = int(input('Enter the seed or 0 to use a random seed: '))
    if seed:
        random.seed(seed)
    play_game(num_rounds)
