from sentence_generator import *
from name_list import generateNameUsernameAndEmail
from game_list import getGameNameAndPlatform
from insert_statement_formatter import createInsertQuery
from random_date_generator import getRandomDate

from random import choice, randint, shuffle
from itertools import chain
from progressbar import ProgressBar

def generateAccountData(fileName, no_entries = 1500):
    file = open(fileName, 'w')
    accountDict = {}
    print('Generating account data...\n')
    bar = ProgressBar(no_entries)
    bar.start()
    for i in range(no_entries):
        while True:
            name, username, email = generateNameUsernameAndEmail()
            if username in accountDict:
                continue
            accountDict[username] = {'name' : name, 'email' : email}
            accountDict[username]['password'] = ''.join([chr(choice(list(chain(range(ord('0'), ord('9') + 1),
                                                                               range(ord('a'), ord('f') + 1))))) for _ in range(17)])
            accountDict[username]['status'] = None
            if randint(0, 3):
                accountDict[username]['status'] = generateStatus()
            accountDict[username]['registerDate'] = getRandomDate()
            accountDict[username]['critic'] = None
            if not randint(0, 3):
                accountDict[username]['critic'] = choice(['IGN', 'Eurogamer', 'Forbes', 'Level Up', 'Polygon', 'GamesRadar+', 'Guardian'])
            accountDict[username]['picture'] = None
            if randint(0, 3):
                accountDict[username]['picture'] = f'C:\\\\Profile_Pictures\\\\{randint(0, 100000000)}.' + choice(['png', 'jpg', 'heic'])

            file.write(createInsertQuery(
                'Conturi',
                {
                    'USERNAME'          : (username, True),
                    'NUME_COMPLET'      : (accountDict[username]['name'], True),
                    'EMAIL'             : (accountDict[username]['email'], True),
                    'PAROLA'            : (accountDict[username]['password'], True),
                    'DATA_INREGISTRARE' : (accountDict[username]['registerDate'], True),
                    'STATUS'            : (accountDict[username]['status'], True),
                    'NUME_CRITIC'       : (accountDict[username]['critic'], True),
                    'POZA_PROFIL'       : (accountDict[username]['picture'], True)
                }
            ))
            bar.update(i)
            break
    file.close()
    bar.finish()
    return accountDict

def generateGameData(fileName, no_entries = 1000):
    file = open(fileName, 'w')
    gameDict = {}
    print('\nGenerating game data...\n')
    bar = ProgressBar(no_entries)
    bar.start()
    generated = 0
    while no_entries:
        toGenerate = min(no_entries, randint(1, 4))
        gameName, platforms = getGameNameAndPlatform(numberOfPlatforms = toGenerate)
        if gameName in gameDict:
            continue
        no_entries -= toGenerate
        generated += toGenerate
        gameDict[gameName] = {platform : {} for platform in platforms}
        for platform in platforms:
            gameDict[gameName][platform] = {
                'publisher' : choice(['Microsoft', 'Nintendo', 'Bethesda', 'Rockstar', 'Sony', 'Gamefreak', 'Ubisoft', 'EA']),
                'genre' : choice(['RPG', 'Fantasy', 'Sports', 'Shooter', 'Arcade', 'Puzzle', 'Strategy', 'Horror']),
                'launchDate' : None if not randint(0, 10) else getRandomDate(),
                'price' : randint(0, 70) + randint(0, 100) / 100,
                'boxart' : None if not randint(0, 3) else f'C:\\\\Box_arts\\\\{randint(0, 100000000)}.' + choice(['png', 'jpg', 'heic']),
                'description' : None if not randint(0, 3) else generateGameDescription()
            }
            file.write(createInsertQuery(
                'Jocuri',
                {
                    'NUME_JOC'     : (gameName, True),
                    'PLATFORMA'    : (platform, True),
                    'PRODUCATOR'   : (gameDict[gameName][platform]['publisher'], True),
                    'GENRE'        : (gameDict[gameName][platform]['genre'], True),
                    'DATA_LANSARE' : (gameDict[gameName][platform]['launchDate'], True),
                    'PRET'         : (gameDict[gameName][platform]['price'], False),
                    'BOX_ART'      : (gameDict[gameName][platform]['boxart'], True),
                    'DESCRIERE'    : (gameDict[gameName][platform]['description'], True)
                }
            ))
        bar.update(generated)
    file.close()
    bar.finish()
    return gameDict

def generateReviewData(fileName, accDict, gameDict, no_entries = 1800):
    file = open(fileName, 'w')
    reviewDict = {}
    accountUsernames = [user for user in accDict]
    games = [game for game in gameDict]
    print('\nGenerating review data...\n')
    bar = ProgressBar(no_entries)
    bar.start()
    index = 0
    reviewUniqueDict = {}
    while index < no_entries:
        username = choice(accountUsernames)
        game = choice(games)
        platform = choice([platform for platform in gameDict[game]])
        key = str((username, game, platform))
        if key in reviewUniqueDict:
            continue
        reviewUniqueDict[key] = True
        reviewDict[index] = {
            'username' : username,
            'game' : game,
            'platform' : platform,
            'grade' : min(10, randint(0, 10) + randint(0, 9) / 10),
            'date' : getRandomDate(),
            'comment' : generateReviewComment() if randint(0, 3) else None,
            'link' : None if randint(0, 10) else 'https://www.' + choice([
                'IGN', 'Eurogamer', 'Forbes', 'Level Up', 'Polygon', 'GamesRadar+', 'Guardian'
                ]).lower() + '.com/' + str(randint(0, 100000))
        }
        file.write(createInsertQuery(
                'Recenzii',
                {
                    'ID_RECENZIE'  : (index, False),
                    'USERNAME'     : (username, True),
                    'NUME_JOC'     : (game, True),
                    'PLATFORMA'    : (platform, True),
                    'NOTA'         : (reviewDict[index]['grade'], False),
                    'DATA_POSTARE' : (reviewDict[index]['date'], True),
                    'COMENTARIU'   : (reviewDict[index]['comment'], True),
                    'LINK_REVIEW'  : (reviewDict[index]['link'], True)
                }
            ))
        index += 1 
        bar.update(index)
    file.close()
    bar.finish()
    return reviewDict

def generateReviewCommentsData(fileName, accDict, reviewDict, no_entries = 2500):
    file = open(fileName, 'w')
    print('\nGenerating review comments data...\n')
    bar = ProgressBar(no_entries)
    bar.start()
    indexes = list(reviewDict.keys())
    usernames = list(accDict.keys())
    pkDict = {}
    index = 0
    while index < no_entries:
        ind = choice(indexes)
        username = choice(usernames)
        date = getRandomDate()
        key = str((ind, username, date))
        if key in pkDict:
            continue
        pkDict[key] = True
        file.write(createInsertQuery(
                'Comentarii_recenzii',
                {
                    'ID_RECENZIE'  : (ind, False),
                    'USERNAME'     : (username, True),
                    'DATA_POSTARE' : (date, True),
                    'COMENTARIU'   : (generateReviewCommentExtra(), True)
                }
            ))
        index += 1
        bar.update(index)
    file.close()
    bar.finish()

def generateReviewVotesData(fileName, accDict, reviewDict, no_entries = 4000):
    file = open(fileName, 'w')
    print('\nGenerating review votes data...\n')
    bar = ProgressBar(no_entries)
    bar.start()
    indexes = list(reviewDict.keys())
    usernames = list(accDict.keys())
    votes = ['DA', 'NU']
    pkDict = {}
    index = 0
    while index < no_entries:
        ind = choice(indexes)
        username = choice(usernames)
        key = str((ind, username))
        if key in pkDict:
            continue
        pkDict[key] = True
        shuffle(votes)
        file.write(createInsertQuery(
                'Voturi_recenzii',
                {
                    'ID_RECENZIE' : (ind, False),
                    'USERNAME'    : (username, True),
                    'UPVOTE'      : (votes[0], True),
                    'DOWNVOTE'    : (votes[1], True)
                }
            ))
        index += 1
        bar.update(index)
    file.close()
    bar.finish()

def main():
    accDict = generateAccountData('fill_conturi.sql')
    gameDict = generateGameData('fill_jocuri.sql')
    reviewDict = generateReviewData('fill_recenzii.sql', accDict, gameDict)
    generateReviewCommentsData('fill_comentarii.sql', accDict, reviewDict)
    generateReviewVotesData('fill_votes.sql', accDict, reviewDict)

if __name__ == '__main__':
    main()