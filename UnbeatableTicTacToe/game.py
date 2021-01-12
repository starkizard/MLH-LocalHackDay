import random
import time
def printBoard(board):
    print("\n")
    arr,new=["   "," O "," X "],"_____________"
    for i in range(9):
        if(i%3==0): print("\n",new+"\n|",end="",sep="")
        print(arr[board[i]],end="|")
    print()


def checkGameOver(board):

    rows,cols,diag=[[],[],[]],[[],[],[]],[[],[]]
    for i in range(9):
        r,c,x = i//3,i%3,board[i]
        rows[r].append(x)
        cols[c].append(x)
        if(r ==c): diag[0].append(x)
        if(r+c == 2): diag[1].append(x)

    for ind in range(3):
        if( (0 not in rows[ind]) and len(set(rows[ind]))==1): return rows[ind][0]
        if( (0 not in cols[ind]) and len(set(cols[ind]))==1): return cols[ind][0]
        if( (ind < 2) and (0 not in diag[ind]) and len(set(diag[ind]))==1): return diag[ind][0]

    return 0

def replyMove3(board,n):
    if(n!=3): return
    locations=[]
    for i in range(9):
        if(board[i]==2): locations.append(i)
    
    a,b=locations
    
    if(board[4]==2):
        if(a==4): element=8-b
        else: element=8-a
        if board[element]!=1: return element
        else: return 2
    
    if(board[4]==1):
        if(a==8-b): return 1
        

    # check if same row
    if(a//3 == b//3): 
        r=3 * a//3
        element = list(set([r, r+1, r+2]).difference(set([a,b])))[0]
        if board[element]!=1: return element

    #checl if same column:
    elif(a%3 ==  b%3):
        c=a%3
        element = list(set([c,c+3,c+6]).difference(set([a,b])))[0]
        if board[element]!=1: return element

    for i in [1,3,4,5,7]:
        if(board[i]==0): return i

def replyMove4(board,oppMove,n):
    if(n!=4): return
    if(board[2]==1):
        if(oppMove!=1): return 1  # end
        if(board[8]==2): return 6
        if(board[7]==2): return 4
        return 8
    if(board[6]==1):
        if(oppMove!=3): return 3 #end
        if(board[5]==2): return 4
        return 8
    return 8-oppMove


def replyRest(board):
    rows,cols,diag=[[],[],[]],[[],[],[]],[[],[]]
    for i in range(9):
        r,c,x = i//3,i%3,board[i]
        rows[r].append(x)
        cols[c].append(x)
        if(r ==c): diag[0].append(x)
        if(r+c == 2): diag[1].append(x)

    # WINNING in this move
    #check rows
    for c in range(2):
        for row in range(3):
            if(0 in rows[row] and rows[row].count(c+1)==2): return rows[row].index(0) + 3*row

        #check cols
        for col in range(3):
            if(0 in cols[col] and cols[col].count(c+1)==2): return 3*(cols[col].index(0)) + col

        #check diag1
        if(0 in diag[0] and diag[0].count(c+1)==2): return 3*(diag[0].index(0)) + diag[0].index(0)

        #check diag2
        if(0 in diag[1] and diag[1].count(c+1)==2): return 3*(diag[1].index(0)) + 2 - diag[1].index(0)
    
    for i in range(9):
        if(board[i]==0): return i



def makeMove(board):
    print("\n Enter space separated coordinates (0 based) [ r c ] ")
    
    i,j=map(int,input().split())
    while(not (-1<i<3 and -1<j<3 and board[3*i +j]==0 ) ):
        print("Try again:")
        i,j=map(int,input().split())
    board[3*i + j]=2
    return board,3*i +j


def botMove(board,numberOfHalfMoves,oppMove):
    
    choice = [0, [0,4][oppMove in [0,2,6,8]], [[2,8][oppMove==4] ,6][oppMove in [1,2,5]], replyMove3(board,numberOfHalfMoves), \
        replyMove4(board,oppMove,numberOfHalfMoves)]
    board[ [replyRest(board),choice[numberOfHalfMoves%5]][numberOfHalfMoves<5] ] = 1
    return board
        
    



def start(board,lastStartPlayer):
    
    print(" Welcome to the tic tac toe game you can never beat. I don't know why you're here but congrats.\n")
    print(" Bot is O and the player is X")
    print("Want to start the game Y/n ?")
    c=input()
    score = 0
    while(c.lower()!="n"):
        print("Score: You: 0 , Bot: ",score )
        time.sleep(1)
        board=[0]*9
        if(lastStartPlayer==-1):
            print("Randomly selecting whether player or bot starts...")
            lastStartPlayer=random.randint(0,1)
        else: lastStartPlayer^=1
        print(["You go first","The Bot goes first"][lastStartPlayer])
        numberOfHalfMoves=0
        oppMove=-1
        player=lastStartPlayer
        printBoard(board)
        while(checkGameOver(board)==0 and numberOfHalfMoves<9):
            # moves 
            if(player): board=botMove(board,numberOfHalfMoves,oppMove)
            else: board,oppMove= makeMove(board)
            printBoard(board)
            player^=1 
            numberOfHalfMoves+=1
        
        score+= checkGameOver(board)
        print("Game over , You ",["drew","lost","lmao this condition is impossible"][checkGameOver(board)] , ".... told ya, you can't win. \n")
        print("Want to play again? Y/n")
        c=input()

board=[0, 0, 0, 0, 0, 0, 0, 0, 0]
lastStartPlayer=-1
start(board,lastStartPlayer)
# Demoknight tf2