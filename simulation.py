import xlrd
#test
from openpyxl import load_workbook
from random import randint
from random import seed

class Player:
    def __init__(self, namE, shotTend, twoTend, twoPercX, threePercX, scoreX):
        self.name = namE
        self.shot = shotTend
        self.two = twoTend
        self.twoPerc = twoPercX
        self.threePerc = threePercX
        self.score = scoreX

class Team:
    def __init__(self, A, B, C, rebRate, teamID, offEffX, defEffX):
        self.playerA = A
        self.playerB = B
        self.playerC = C
        self.rebound = rebRate
        self.id = teamID
        self.offEff = offEffX
        self.defEff = defEffX

def getInfo(fileName):
    book = load_workbook(fileName, data_only=True)
    sheet = book["Simulation S3"]

    rows = sheet.rows

    teams = []
    data = []
    players = []
    id = 1
    brk = 1

    for row in rows:
        if brk == 1:
            brk = 2
        else:
            for cell in row:
                data.append(cell.value)
            P = Player((data[0]), (data[1]), (data[4]), (data[7]), (data[10]), 0)
            players.append(P)
            #print(P.name, P.twoPerc, P.threePerc)
            if len(players) == 3:
                TM = Team(players[0], players[1], players[2], (data[13]), id, data[11], data[12])
                teams.append(TM)
                #print(TM.offEff, TM.defEff, TM.offEff + TM.defEff)
                players = []
                id += 1
            data = []

    return teams

def printTeams():
    print("1. Cooper")
    print("2. Montoya")
    print("3. Damski")
    print("4. Zach")
    print("5. Noah")
    print("6. Dylan")
    print("7. Baker")
    print("8. Alec")
    print("9. Cundiff")
    print("10. James")
    print("11. David")
    print("12. Michael")

def typeAndMake(player, A, B):
    type = randint(1,100)
    make = randint(1,100)

    difficulty = -A.offEff + B.defEff #use efficiency ratings here
    make += difficulty

    #print(player.name, int(player.twoPerc*100))

    if type <= player.two*100: #two point attempt
        if make <= int(player.twoPerc*100): #made 2
            return 2
        else:
            return 0
    else: #3 point attempt
        if make <= int(player.threePerc*100):
            return 3
        else:
            return 0

def shotFunction(A, B):
    shot = randint(1,100)
    score = 0
    if shot <= A.playerA.shot*100: #player A shoots
        score = typeAndMake(A.playerA, A, B)
        A.playerA.score += score
    elif shot <= (A.playerA.shot + A.playerB.shot)*100: #player B shoots
        score = typeAndMake(A.playerB, A, B)
        A.playerB.score += score
    else: #playerC shoots
        score = typeAndMake(A.playerC, A, B)
        A.playerC.score += score

    return score

def rebFunction(off,deff):
    offrate = off.rebound
    defrate = int(1.5*deff.rebound)

    reb = randint(1,round(offrate + defrate)) #FIX THIS
    getReb = offrate*100/reb

    if reb <= getReb:
        return 0
    else:
        return 1

def offense(off, deff, ball):
    points = shotFunction(off, deff)
    if points == 0: #miss, rebound
        reb = rebFunction(off, deff)
        if reb == 0: #same possession
            ball = ball
        if reb == 1: #possession change
            if ball == 0:   #xor?
                ball = 1
            elif ball == 1:
                ball = 0
        return points, ball
    else:
        if ball == 0:
            ball = 1
        elif ball == 1:
            ball = 0
        return points, ball


def runGame(A, B, type):
    totalA = 0      #total points across all games
    totalB = 0      #total points across all games
    winsA = 0
    winsB = 0
    scoreA = 0      #single game score
    scoreB = 0      #single game score
    games = 1

    toPlay = 0
    if type == 1:
        toPlay = 50
    elif type == 2:
        toPlay = 1000

    while games <= toPlay:
        ball = 0 #0 for A, 1 for B
        while (bool(scoreA < 50) & bool(scoreB < 50)):
            if ball == 0: #A on offense
                pointsA, ball = offense(A, B, ball)
                scoreA += pointsA
                #print(pointsA, scoreA, ball)
            if ball == 1: #B on offense
                pointsB, ball = offense(B, A, ball)
                scoreB += pointsB

        #print(scoreA, scoreB)
        if scoreA > scoreB:
            winsA += 1
        else:
            winsB += 1

        games += 1
        totalA += scoreA
        totalB += scoreB
        scoreA = 0
        scoreB = 0

    games -= 1
    avgA = totalA/games
    avgB = totalB/games

    if avgA > avgB:
        scale = 50/avgA
        newB = scale*avgB
        spread = 50 - newB
    else:
        scale = 50/avgB
        newA = scale*avgA
        spread = 50 - newA

    if type == 1: #running season
        if avgA > avgB:
            return 1
        else:
            return 0
    elif type == 2: #single game
        print("=====================")
        print("Team "+ A.playerA.name +" average score: ", avgA)
        print("Team "+ A.playerA.name +" total wins: ", winsA)
        print("" + A.playerA.name + " score: ", A.playerA.score / games)
        print("" + A.playerB.name + " score: ", A.playerB.score / games)
        print("" + A.playerC.name + " score: ", A.playerC.score / games)
        print("=====================")
        print("Team "+ B.playerA.name +" average score: ", avgB)
        print("Team "+ B.playerA.name +" total wins: ", winsB)
        print("" + B.playerA.name + " score: ", B.playerA.score / games)
        print("" + B.playerB.name + " score: ", B.playerB.score / games)
        print("" + B.playerC.name + " score: ", B.playerC.score / games)
        print("=====================")
        if avgA > avgB:
            print("Team "+ A.playerA.name +" is the favorite by: ", spread)
            print("Team " + A.playerA.name + " wins at a rate of: ", (winsA*100)/games)
        else:
            print("Team " + B.playerA.name + " is the favorite by: ", spread)
            print("Team " + B.playerA.name + " wins at a rate of: ", (winsB * 100) / games)
        return -1

def runSeason(A, teams, stats):
    wins = 0
    count = 0
    seasons = 1
    while seasons <= 25:
        #print("season:", seasons)
        for t in teams:
            if A.id != t.id:
                wins += runGame(A, t, 1)
                count += 1
        seasons += 1
    seasons -= 1
    avg = wins/seasons
    update = avg*10/11
    print("Team "+A.playerA.name+" is predicted to win "+ str(update) +" games per season")
    if stats == 1:
        print("" + A.playerA.name + " score: ", A.playerA.score / (count*50))
        print("" + A.playerB.name + " score: ", A.playerB.score / (count*50))
        print("" + A.playerC.name + " score: ", A.playerC.score / (count*50))

def allSeason(teams):
    for t in teams:
        print("==========================")
        runSeason(t, teams, 0)

if __name__ == '__main__':
    fileName = 'low rim league.xlsx'

    teams = getInfo(fileName)

    decision = int(input("Press 1 to sim a team's season, press 2 to sim a single game, 3 for entire season: "))
    if decision == 1:
        printTeams()
        teamsel = int(input("Choose team: "))
        team = None
        for t in teams:
            if teamsel == t.id:
                team = t
        runSeason(team, teams, 1)
    elif decision == 2:
        printTeams()
        team1sel = int(input("Choose first team: "))
        team2sel = int(input("Choose second team: "))
        team1 = team2 = None
        for t in teams:
            if team1sel == t.id:
                team1 = t
            if team2sel == t.id:
                team2 = t
        runGame(team1, team2, 2)
    elif decision == 3:
        allSeason(teams)


