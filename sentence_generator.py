from random import choice

def generateStatus():
    first = ['Hi', 'Hello', 'What\'\'s up', 'Greetings', 'Heya']
    second = ['dear', 'fellow', 'sweet', 'cool']
    third = ['guys', 'friends', 'people']

    return f'{choice(first)} {choice(second)} {choice(third)}'

def generateGameDescription():
    first = ['A lovable', 'A thrilling', 'An outstanding', 'An amazing', 'A glorious']
    second = ['experience', 'game', 'adventure', 'story']
    third = ['for everyone', 'for the children', 'for experienced gamers', 'for adults', 'for families']
    return f'{choice(first)} {choice(second)} {choice(third)}!'

def generateReviewComment():
    first = ['Good', 'Overrated', 'Horrible', 'Amazing', 'Lovely', 'Average', 'Incredible', 'Bad']
    second = ['game', 'experience', 'graphics', 'storyline', 'gameplay', 'voice acting']
    third = ['.', '!']
    return f'{choice(first)} {choice(second)}{choice(third)}'

def generateReviewCommentExtra():
    first = ['somewhat', 'completely', 'wholeheartedly', 'don\'\'t', 'absolutely']
    second = ['agree', 'disagree']
    third = ['.', '!']
    return f'I {choice(first)} {choice(second)}{choice(third)}'