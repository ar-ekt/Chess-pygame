def r_counter(board,x1,y1,x2,y2):
    rook_counter=0
    if x1==x2:
        for rook_y in range(min(y1,y2)+1,max(y1,y2)):
            if board[rook_y][x2]!="  ":
                rook_counter+=1
                break
    elif y1==y2:
        for rook_x in range(min(x1,x2)+1,max(x1,x2)):
            if board[y2][rook_x]!="  ":
                rook_counter+=1
                break
    return rook_counter
#---------------------------------------------------------------------------------------------------------------------------------------------
def b_counter(board,x1,y1,x2,y2):
    bishop_counter=0
    if y2>y1: signy=1
    if y1>y2: signy=-1
    if x2>x1: signx=1
    if x1>x2: signx=-1
    for bishop_i in range(1,abs(y2-y1)):
        if board[y1+(signy*bishop_i)][x1+(signx*bishop_i)]!="  ":
            bishop_counter+=1
            break
    return bishop_counter
#---------------------------------------------------------------------------------------------------------------------------------------------
def check(board,chessmans,color):
    for iline in range(8):
        if (color+"k") in board[iline]:
            y=iline
            break
    x=board[y].index(color+"k")
    for idanger in chessmans:
        if chessmans[idanger][0]==color:
            continue
        yd,xd=idanger[0],idanger[1]
        if chessmans[idanger][1]=="p" and color=="W" and yd-y==1 and abs(x-xd)==1:
            return 0
        elif chessmans[idanger][1]=="p" and color=="B" and y-yd==1 and abs(x-xd)==1:
            return 0
        elif chessmans[idanger][1]=="n" and ((abs(yd-y)==2 and abs(xd-x)==1) or (abs(yd-y)==1 and abs(xd-x)==2)):
            return 0
        elif chessmans[idanger][1]=="b" and abs(yd-y)==abs(xd-x) and b_counter(board,x,y,xd,yd)==0:
            return 0
        elif chessmans[idanger][1]=="r" and (x==xd or y==yd) and r_counter(board,x,y,xd,yd)==0:
            return 0
        elif chessmans[idanger][1]=="q" and abs(yd-y)==abs(xd-x) and b_counter(board,x,y,xd,yd)==0:
            return 0
        elif chessmans[idanger][1]=="q" and (x==xd or y==yd) and r_counter(board,x,y,xd,yd)==0:
            return 0
        elif chessmans[idanger][1]=="k" and (abs(yd-y)==1 or yd-y==0) and (abs(xd-x)==1 or xd-x==0) and not xd-x==yd-y==0:
            return 0
    return 1
#---------------------------------------------------------------------------------------------------------------------------------------------
def check_y_n(board,chessmans,x1,y1,x2,y2,chessman_sign,color):
    boo=[l.copy() for l in board]
    chessoo=chessmans.copy()
    boo[y2][x2]=boo[y1][x1]
    boo[y1][x1]="  "
    chessoo[(y2,x2)]=color+chessman_sign
    del chessoo[(y1,x1)]
    num_check=check(boo,chessoo,color)
    return num_check
#---------------------------------------------------------------------------------------------------------------------------------------------
def checkmate(board,chessmans,color,oppo_color):
    if check(board,chessmans,color)==1:
        return 1
    for iman in chessmans:
        if chessmans[iman][0]==oppo_color:
            continue
        y,x=iman[0],iman[1]
        if chessmans[iman][1]=="p":
            fake=[]
            if color=="W" and y+1<=7 and board[y+1][x]=="  ":
                fake.append((y+1,x))
            if color=="W" and y==1 and board[y+1][x]=="  " and board[y+2][x]=="  ":
                fake.append((y+2,x))
            if color=="W" and y+1<=7 and x+1<=7 and board[y+1][x+1][0]==oppo_color:
                fake.append((y+1,x+1))
            if color=="W" and y+1<=7 and x-1>=0 and board[y+1][x-1][0]==oppo_color:
                fake.append((y+1,x-1))
            if color=="B" and y-1<=7 and board[y-1][x]=="  ":
                fake.append((y-1,x))
            if color=="B" and y==6 and board[y-1][x]=="  " and board[y-2][x]=="  ":
                fake.append((y-2,x))
            if color=="B" and y-1<=7 and x+1<=7 and board[y-1][x+1][0]==oppo_color:
                fake.append((y-1,x+1))
            if color=="B" and y-1<=7 and x-1>=0 and board[y-1][x-1][0]==oppo_color:
                fake.append((y-1,x-1))
            for coor in fake:
                if check_y_n(board,chessmans,x,y,coor[1],coor[0],"p",color)==1:
                    return 1
        if chessmans[iman][1]=="n":
            fake=[(y+2,x+1),(y+1,x+2),(y-2,x-1),(y-1,x-2),(y-2,x+1),(y-1,x+2),(y+2,x-1),(y+1,x-2)]
            for coor in fake:
                yy,xx=coor[0],coor[1]
                if not (0<=yy<=7 and 0<=xx<=7 and board[yy][xx][0]!=color):
                    continue
                if check_y_n(board,chessmans,x,y,coor[1],coor[0],"n",color)==1:
                    return 1
        if chessmans[iman][1]=="r":
            fake=[]
            for iz in range(-7,8):
                if iz==0:
                    continue
                if 0<=y+iz<=7 and r_counter(board,x,y,x,y+iz)==0 and board[y+iz][x][0]!=color:
                    fake.append((y+iz,x))
                if 0<=x+iz<=7 and r_counter(board,x,y,x+iz,y)==0 and board[y][x+iz][0]!=color:
                    fake.append((y,x+iz))
            for coor in fake:
                if check_y_n(board,chessmans,x,y,coor[1],coor[0],"r",color)==1:
                    return 1
        if chessmans[iman][1]=="b":
            fake=[]
            for iz in range(-7,8):
                if iz==0:
                    continue
                if 0<=y+iz<=7 and 0<=x+iz<=7 and b_counter(board,x,y,x+iz,y+iz)==0 and board[y+iz][x+iz][0]!=color:
                    fake.append((y+iz,x+iz))
                if 0<=y+iz<=7 and 0<=x-iz<=7 and b_counter(board,x,y,x-iz,y+iz)==0 and board[y+iz][x-iz][0]!=color:
                    fake.append((y+iz,x-iz))
            for coor in fake:
                if check_y_n(board,chessmans,x,y,coor[1],coor[0],"b",color)==1:
                    return 1
        if chessmans[iman][1]=="q":
            fake=[]
            for iz in range(-7,8):
                if iz==0:
                    continue
                if 0<=y+iz<=7 and r_counter(board,x,y,x,y+iz)==0 and board[y+iz][x][0]!=color:
                    fake.append((y+iz,x))
                if 0<=x+iz<=7 and r_counter(board,x,y,x+iz,y)==0 and board[y][x+iz][0]!=color:
                    fake.append((y,x+iz))
                if 0<=y+iz<=7 and 0<=x+iz<=7 and b_counter(board,x,y,x+iz,y+iz)==0 and board[y+iz][x+iz][0]!=color:
                    fake.append((y+iz,x+iz))
                if 0<=y+iz<=7 and 0<=x-iz<=7 and b_counter(board,x,y,x-iz,y+iz)==0 and board[y+iz][x-iz][0]!=color:
                    fake.append((y+iz,x-iz))
            for coor in fake:
                if check_y_n(board,chessmans,x,y,coor[1],coor[0],"q",color)==1:
                    return 1
        if chessmans[iman][1]=="k":
            fake=[]
            for iy in range(-1,2):
                for ix in range(-1,2):
                    if ix==0 and iy==0:
                        continue
                    if 0<=y+iy<=7 and 0<=x+ix<=7 and board[y+iy][x+ix][0]!=color:
                        fake.append((y+iy,x+ix))
            for coor in fake:
                if check_y_n(board,chessmans,x,y,coor[1],coor[0],"k",color)==1:
                    return 1
    return 0
#---------------------------------------------------------------------------------------------------------------------------------------------
def stalemate(board,chessmans,color,oppo_color):
    if check(board,chessmans,color)==0:
        return 1
    for iman in chessmans:
        if chessmans[iman][0]==oppo_color:
            continue
        y,x=iman[0],iman[1]
        if chessmans[iman][1]=="p":
            fake=[]
            if color=="W" and y+1<=7 and board[y+1][x]=="  ":
                fake.append((y+1,x))
            if color=="W" and y+1<=7 and x+1<=7 and board[y+1][x+1][0]==oppo_color:
                fake.append((y+1,x+1))
            if color=="W" and y+1<=7 and x-1>=0 and board[y+1][x-1][0]==oppo_color:
                fake.append((y+1,x-1))
            if color=="B" and y-1>=0 and board[y-1][x]=="  ":
                fake.append((y-1,x))
            if color=="B" and y-1>=0 and x+1<=7 and board[y-1][x+1][0]==oppo_color:
                fake.append((y-1,x+1))
            if color=="B" and y-1>=0 and x-1>=0 and board[y-1][x-1][0]==oppo_color:
                fake.append((y-1,x-1))
            for coor in fake:
                if check_y_n(board,chessmans,x,y,coor[1],coor[0],"p",color)==1:
                    return 1
        if chessmans[iman][1]=="n":
            fake=[(y+2,x+1),(y+1,x+2),(y-2,x-1),(y-1,x-2),(y-2,x+1),(y-1,x+2),(y+2,x-1),(y+1,x-2)]
            for coor in fake:
                yy,xx=coor[0],coor[1]
                if 0<=yy<=7 and 0<=xx<=7 and board[yy][xx][0]!=color and check_y_n(board,chessmans,x,y,coor[1],coor[0],"n",color)==1:
                    return 1
        if chessmans[iman][1]=="r":
            fake=[(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
            for coor in fake:
                yy,xx=coor[0],coor[1]
                if 0<=yy<=7 and 0<=xx<=7 and board[yy][xx][0]!=color and check_y_n(board,chessmans,x,y,coor[1],coor[0],"r",color)==1:
                    return 1
        if chessmans[iman][1]=="b":
            fake=[(y+1,x+1),(y+1,x-1),(y-1,x+1),(y-1,x-1)]
            for coor in fake:
                yy,xx=coor[0],coor[1]
                if 0<=yy<=7 and 0<=xx<=7 and board[yy][xx][0]!=color and check_y_n(board,chessmans,x,y,coor[1],coor[0],"b",color)==1:
                    return 1
        if chessmans[iman][1]=="q":
            fake=[(y+1,x),(y-1,x),(y,x+1),(y,x-1),(y+1,x+1),(y+1,x-1),(y-1,x+1),(y-1,x-1)]
            for coor in fake:
                yy,xx=coor[0],coor[1]
                if 0<=yy<=7 and 0<=xx<=7 and board[yy][xx][0]!=color and check_y_n(board,chessmans,x,y,coor[1],coor[0],"q",color)==1:
                    return 1
        if chessmans[iman][1]=="k":
            fake=[]
            for iy in range(-1,2):
                for ix in range(-1,2):
                    if ix==0 and iy==0:
                        continue
                    if 0<=y+iy<=7 and 0<=x+ix<=7 and board[y+iy][x+ix][0]!=color:
                        fake.append((y+iy,x+ix))
            for coor in fake:
                if check_y_n(board,chessmans,x,y,coor[1],coor[0],"k",color)==1:
                    return 1
    return 0
#---------------------------------------------------------------------------------------------------------------------------------------------
def choose_replace_of_pawn(color,x):
    img = pygame.image.load('Chess/which'+color+'.png')
    img = pygame.transform.scale(img, (156, 156))
    screen.blit(img,(80+(119*(x+1)),80+(119)))
    pygame.display.flip();
    choose = None
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if 80+(119*(x+1)) <= pygame.mouse.get_pos()[0] <= 80+(119*(x+1))+78 and 80+(119) <= pygame.mouse.get_pos()[1] <= 80+(119)+78:
                    choose = "q"
                elif 80+(119*(x+1))+78 <= pygame.mouse.get_pos()[0] <= 80+(119*(x+1))+156 and 80+(119) <= pygame.mouse.get_pos()[1] <= 80+(119)+78:
                    choose = "r"
                elif 80+(119*(x+1)) <= pygame.mouse.get_pos()[0] <= 80+(119*(x+1))+78 and 80+(119)+78 <= pygame.mouse.get_pos()[1] <= 80+(119)+156:
                    choose = "n"
                elif 80+(119*(x+1))+78 <= pygame.mouse.get_pos()[0] <= 80+(119*(x+1))+156 and 80+(119)+78 <= pygame.mouse.get_pos()[1] <= 80+(119)+156:
                    choose = "b"
        if choose != None:
            return choose
#---------------------------------------------------------------------------------------------------------------------------------------------
def change_board_chessmans(board,chessmans,chessman_sign,color,x1,y1,x2,y2):
    chessmans[(y2,x2)]=color+chessman_sign
    board[y2][x2]=color+chessman_sign
    del chessmans[(y1,x1)]
    board[y1][x1]="  "
#---------------------------------------------------------------------------------------------------------------------------------------------
def pawn_black(board,chessmans,chessman_sign_dict,wb_dict,hits,color,oppo_color,x1,y1,x2,y2,x_saved,y_saved):
    if check_y_n(board,chessmans,x1,y1,x2,y2,"p",color)==0:
        return 0
    if x1==x2 and y1-y2==1 and board[y2][x2]=="  " and y2==0:
        choose=choose_replace_of_pawn(color,x1)
        change_board_chessmans(board,chessmans,choose,color,x1,y1,x2,y2)
        return 1
    elif x1==x2 and y1-y2==1 and board[y2][x2]=="  " and y2!=0:
        change_board_chessmans(board,chessmans,"p",color,x1,y1,x2,y2)
        return 1
    elif x1==x2 and y1-y2==2 and board[y2][x2]=="  " and board[y2+1][x2]=="  " and y1==6:
        change_board_chessmans(board,chessmans,"p",color,x1,y1,x2,y2)
        return 1
    elif y1-y2==1 and abs(x2-x1)==1 and board[y2][x2][0]==oppo_color and y2==0:
        hits[oppo_color] += board[y2][x2][1]
        choose=choose_replace_of_pawn(color,x1)
        change_board_chessmans(board,chessmans,choose,color,x1,y1,x2,y2)
        return 1
    elif y1-y2==1 and abs(x2-x1)==1 and board[y2][x2][0]==oppo_color and y2!=0:
        hits[oppo_color] += board[y2][x2][1]
        change_board_chessmans(board,chessmans,"p",color,x1,y1,x2,y2)
        return 1
    elif y1-y2==1 and abs(x2-x1)==1 and board[y2][x2]=="  " and board[y2+1][x2]==oppo_color+"p" and y2+1==y_saved and x2==x_saved:
        hits[oppo_color] += board[y2+1][x2][1]
        del chessmans[(y2+1,x2)]
        board[y2+1][x2]="  "
        change_board_chessmans(board,chessmans,"p",color,x1,y1,x2,y2)
        return 1
    else:
        return 0
#---------------------------------------------------------------------------------------------------------------------------------------------
def pawn_white(board,chessmans,chessman_sign_dict,wb_dict,hits,color,oppo_color,x1,y1,x2,y2,x_saved,y_saved):
    if check_y_n(board,chessmans,x1,y1,x2,y2,"p",color)==0:
        return 0
    if x1==x2 and y2-y1==1 and board[y2][x2]=="  " and y2==7:
        choose=choose_replace_of_pawn(color,x1)
        change_board_chessmans(board,chessmans,choose,color,x1,y1,x2,y2)
        return 1
    elif x1==x2 and y2-y1==1 and board[y2][x2]=="  " and y2!=7:
        change_board_chessmans(board,chessmans,"p",color,x1,y1,x2,y2)
        return 1
    elif x1==x2 and y2-y1==2 and board[y2][x2]=="  " and board[y2-1][x2]=="  " and y1==1:
        change_board_chessmans(board,chessmans,"p",color,x1,y1,x2,y2)
        return 1
    elif y2-y1==1 and abs(x2-x1)==1 and board[y2][x2][0]==oppo_color and y2==7:
        hits[oppo_color] += board[y2][x2][1]
        choose=choose_replace_of_pawn(color,x1)
        change_board_chessmans(board,chessmans,choose,color,x1,y1,x2,y2)
        return 1
    elif y2-y1==1 and abs(x2-x1)==1 and board[y2][x2][0]==oppo_color and y2!=7:
        hits[oppo_color] += board[y2][x2][1]
        change_board_chessmans(board,chessmans,"p",color,x1,y1,x2,y2)
        return 1
    elif y2-y1==1 and abs(x2-x1)==1 and board[y2][x2]=="  " and board[y2-1][x2]==oppo_color+"p" and y2-1==y_saved and x2==x_saved:
        hits[oppo_color] += board[y2-1][x2][1]
        del chessmans[(y2-1,x2)]
        board[y2-1][x2]="  "
        change_board_chessmans(board,chessmans,"p",color,x1,y1,x2,y2)
        return 1
    else:
        return 0
#---------------------------------------------------------------------------------------------------------------------------------------------
def nerve(board,chessmans,chessman_sign_dict,wb_dict,hits,color,oppo_color,x1,y1,x2,y2):
    if check_y_n(board,chessmans,x1,y1,x2,y2,"n",color)==0:
        return 0
    if ((abs(y2-y1)==2 and abs(x2-x1)==1) or (abs(y2-y1)==1 and abs(x2-x1)==2)) and board[y2][x2]=="  ":
        change_board_chessmans(board,chessmans,"n",color,x1,y1,x2,y2)
        return 1
    elif ((abs(y2-y1)==2 and abs(x2-x1)==1) or (abs(y2-y1)==1 and abs(x2-x1)==2)) and board[y2][x2][0]==oppo_color:
        hits[oppo_color] += board[y2][x2][1]
        change_board_chessmans(board,chessmans,"n",color,x1,y1,x2,y2)
        return 1
    else:
        return 0
#---------------------------------------------------------------------------------------------------------------------------------------------
def rook(board,chessmans,chessman_sign_dict,wb_dict,hits,color,oppo_color,x1,y1,x2,y2):
    if check_y_n(board,chessmans,x1,y1,x2,y2,"r",color)==0:
        return 0
    if r_counter(board,x1,y1,x2,y2)==0 and (x1==x2 or y1==y2) and board[y2][x2]=="  ":
        change_board_chessmans(board,chessmans,"r",color,x1,y1,x2,y2)
        return 1
    elif r_counter(board,x1,y1,x2,y2)==0 and (x1==x2 or y1==y2) and board[y2][x2][0]==oppo_color:
        hits[oppo_color] += board[y2][x2][1]
        change_board_chessmans(board,chessmans,"r",color,x1,y1,x2,y2)
        return 1
    else:
        return 0
#---------------------------------------------------------------------------------------------------------------------------------------------
def bishop(board,chessmans,chessman_sign_dict,wb_dict,hits,color,oppo_color,x1,y1,x2,y2):
    if check_y_n(board,chessmans,x1,y1,x2,y2,"b",color)==0:
        return 0
    if abs(y2-y1)==abs(x2-x1) and b_counter(board,x1,y1,x2,y2)==0 and board[y2][x2]=="  ":
        change_board_chessmans(board,chessmans,"b",color,x1,y1,x2,y2)
        return 1
    elif abs(y2-y1)==abs(x2-x1) and b_counter(board,x1,y1,x2,y2)==0 and board[y2][x2][0]==oppo_color:
        hits[oppo_color] += board[y2][x2][1]
        change_board_chessmans(board,chessmans,"b",color,x1,y1,x2,y2)
        return 1
    else:
        return 0
#---------------------------------------------------------------------------------------------------------------------------------------------
def queen(board,chessmans,chessman_sign_dict,wb_dict,hits,color,oppo_color,x1,y1,x2,y2):
    if check_y_n(board,chessmans,x1,y1,x2,y2,"q",color)==0:
        return 0
    if r_counter(board,x1,y1,x2,y2)==0 and (x1==x2 or y1==y2) and board[y2][x2]=="  ":
        change_board_chessmans(board,chessmans,"q",color,x1,y1,x2,y2)
        return 1
    elif r_counter(board,x1,y1,x2,y2)==0 and (x1==x2 or y1==y2) and board[y2][x2][0]==oppo_color:
        hits[oppo_color] += board[y2][x2][1]
        change_board_chessmans(board,chessmans,"q",color,x1,y1,x2,y2)
        return 1
    elif abs(y2-y1)==abs(x2-x1) and b_counter(board,x1,y1,x2,y2)==0 and board[y2][x2]=="  ":
        change_board_chessmans(board,chessmans,"q",color,x1,y1,x2,y2)
        return 1
    elif abs(y2-y1)==abs(x2-x1) and b_counter(board,x1,y1,x2,y2)==0 and board[y2][x2][0]==oppo_color:
        hits[oppo_color] += board[y2][x2][1]
        change_board_chessmans(board,chessmans,"q",color,x1,y1,x2,y2)
        return 1
    else:
        return 0
#---------------------------------------------------------------------------------------------------------------------------------------------
def king(board,chessmans,chessman_sign_dict,wb_dict,hits,king_rook,color,oppo_color,x1,y1,x2,y2):
    if check_y_n(board,chessmans,x1,y1,x2,y2,"k",color)==0:
        return 0
    if y2==y1 and x2-x1==2 and (color+"k") not in king_rook and (color+"r"+str(y1)+str(x1+3)) not in king_rook and board[y1][x1+1]=="  " and board[y1][x1+2]=="  ":
        if check(board,chessmans,color)==0:
            return 0
        for idi in [(y1,x1+1),(y1,x1+2)]:
            if check_y_n(board,chessmans,x1,y1,idi[1],idi[0],"k",color)==0:
                return 0
        change_board_chessmans(board,chessmans,"k",color,x1,y1,x2,y2)
        change_board_chessmans(board,chessmans,"r",color,x1+3,y1,x1+1,y1)
        return 1
    elif y2==y1 and x1-x2==2 and (color+"k") not in king_rook and (color+"r"+str(y1)+str(x1-4)) not in king_rook and board[y1][x1-1]=="  " and board[y1][x1-2]=="  " and board[y1][x1-3]=="  ":
        if check(board,chessmans,color)==0:
            return 0
        for idi in [(y1,x1-1),(y1,x1-2)]:
            if check_y_n(board,chessmans,x1,y1,idi[1],idi[0],"k",color)==0:
                return 0
        change_board_chessmans(board,chessmans,"k",color,x1,y1,x2,y2)
        change_board_chessmans(board,chessmans,"r",color,x1-4,y1,x1-1,y1)
        return 1
    elif (abs(y2-y1)==1 or y2-y1==0) and (abs(x2-x1)==1 or x2-x1==0) and not x2-x1==y2-y1==0 and (board[y2][x2]=="  " or board[y2][x2][0]==oppo_color):
        if board[y2][x2][0]==oppo_color:
            hits[oppo_color] += board[y2][x2][1]
        change_board_chessmans(board,chessmans,"k",color,x1,y1,x2,y2)
        return 1
    else:
        return 0
#---------------------------------------------------------------------------------------------------------------------------------------------
def possible(board,chessmans,x,y,chessman_sign,color,oppo_color,king_rook,x_saved,y_saved):
    poss = []
    fake = []
    if chessman_sign=="p":
        if color=="W" and y+1<=7 and board[y+1][x]=="  ":
            fake.append((y+1,x))
        if color=="W" and y==1 and board[y+1][x]=="  " and board[y+2][x]=="  ":
            fake.append((y+2,x))
        if color=="W" and y+1<=7 and x+1<=7 and board[y+1][x+1][0]==oppo_color:
            fake.append((y+1,x+1))
        if color=="W" and y+1<=7 and x-1>=0 and board[y+1][x-1][0]==oppo_color:
            fake.append((y+1,x-1))
        if color=="W" and y_saved==y and x_saved-x==1 and board[y+1][x+1]=="  " and board[y][x+1]==oppo_color+"p":
            fake.append((y+1,x+1))
        if color=="W" and y_saved==y and x-x_saved==1 and board[y+1][x-1]=="  " and board[y][x-1]==oppo_color+"p":
            fake.append((y+1,x-1))
        if color=="B" and y-1<=7 and board[y-1][x]=="  ":
            fake.append((y-1,x))
        if color=="B" and y==6 and board[y-1][x]=="  " and board[y-2][x]=="  ":
            fake.append((y-2,x))
        if color=="B" and y-1<=7 and x+1<=7 and board[y-1][x+1][0]==oppo_color:
            fake.append((y-1,x+1))
        if color=="B" and y-1<=7 and x-1>=0 and board[y-1][x-1][0]==oppo_color:
            fake.append((y-1,x-1))
        if color=="B" and y_saved==y and x_saved-x==1 and board[y-1][x+1]=="  " and board[y][x+1]==oppo_color+"p":
            fake.append((y-1,x+1))
        if color=="B" and y_saved==y and x-x_saved==1 and board[y-1][x-1]=="  " and board[y][x-1]==oppo_color+"p":
            fake.append((y-1,x-1))
        for coor in fake:
            if check_y_n(board,chessmans,x,y,coor[1],coor[0],"p",color)==1:
                poss.append((coor[1],coor[0]))
    if chessman_sign=="n":
        fake=[(y+2,x+1),(y+1,x+2),(y-2,x-1),(y-1,x-2),(y-2,x+1),(y-1,x+2),(y+2,x-1),(y+1,x-2)]
        for coor in fake:
            if not (0<=coor[0]<=7 and 0<=coor[1]<=7 and board[coor[0]][coor[1]][0]!=color):
                continue
            if check_y_n(board,chessmans,x,y,coor[1],coor[0],"n",color)==1:
                poss.append((coor[1],coor[0]))
    if chessman_sign=="r":
        for iz in range(-7,8):
            if iz==0:
                continue
            if 0<=y+iz<=7 and r_counter(board,x,y,x,y+iz)==0 and board[y+iz][x][0]!=color:
                fake.append((y+iz,x))
            if 0<=x+iz<=7 and r_counter(board,x,y,x+iz,y)==0 and board[y][x+iz][0]!=color:
                fake.append((y,x+iz))
        for coor in fake:
            if check_y_n(board,chessmans,x,y,coor[1],coor[0],"r",color)==1:
                poss.append((coor[1],coor[0]))
    if chessman_sign=="b":
        for iz in range(-7,8):
            if iz==0:
                continue
            if 0<=y+iz<=7 and 0<=x+iz<=7 and b_counter(board,x,y,x+iz,y+iz)==0 and board[y+iz][x+iz][0]!=color:
                fake.append((y+iz,x+iz))
            if 0<=y+iz<=7 and 0<=x-iz<=7 and b_counter(board,x,y,x-iz,y+iz)==0 and board[y+iz][x-iz][0]!=color:
                fake.append((y+iz,x-iz))
        for coor in fake:
            if check_y_n(board,chessmans,x,y,coor[1],coor[0],"b",color)==1:
                poss.append((coor[1],coor[0]))
    if chessman_sign=="q":
        for iz in range(-7,8):
            if iz==0:
                continue
            if 0<=y+iz<=7 and r_counter(board,x,y,x,y+iz)==0 and board[y+iz][x][0]!=color:
                fake.append((y+iz,x))
            if 0<=x+iz<=7 and r_counter(board,x,y,x+iz,y)==0 and board[y][x+iz][0]!=color:
                fake.append((y,x+iz))
            if 0<=y+iz<=7 and 0<=x+iz<=7 and b_counter(board,x,y,x+iz,y+iz)==0 and board[y+iz][x+iz][0]!=color:
                fake.append((y+iz,x+iz))
            if 0<=y+iz<=7 and 0<=x-iz<=7 and b_counter(board,x,y,x-iz,y+iz)==0 and board[y+iz][x-iz][0]!=color:
                fake.append((y+iz,x-iz))
        for coor in fake:
            if check_y_n(board,chessmans,x,y,coor[1],coor[0],"q",color)==1:
                poss.append((coor[1],coor[0]))
    if chessman_sign=="k":
        for iy in range(-1,2):
            for ix in range(-1,2):
                if ix==0 and iy==0:
                    continue
                if 0<=y+iy<=7 and 0<=x+ix<=7 and board[y+iy][x+ix][0]!=color:
                    fake.append((y+iy,x+ix))
        if (color+"k") not in king_rook and (color+"r"+str(y)+str(x+3)) not in king_rook and board[y][x+1]=="  " and board[y][x+2]=="  " and check(board,chessmans,color) == 1:
            for idi in [(y,x+1),(y,x+2)]:
                if check_y_n(board,chessmans,x,y,idi[1],idi[0],"k",color) == 0:
                    continue
            else:
                fake.append((y,x+2))
        elif (color+"k") not in king_rook and (color+"r"+str(y)+str(x-4)) not in king_rook and board[y][x-1]=="  " and board[y][x-2]=="  " and board[y][x-3]=="  " and check(board,chessmans,color) == 1:
            for idi in [(y,x-1),(y,x-2)]:
                if check_y_n(board,chessmans,x,y,idi[1],idi[0],"k",color) == 0:
                    continue
            else:
                fake.append((y,x-2))
        for coor in fake:
            if check_y_n(board,chessmans,x,y,coor[1],coor[0],"k",color) == 1:
                poss.append((coor[1],coor[0]))
    return poss
#---------------------------------------------------------------------------------------------------------------------------------------------
board=[["  "]*8 for i in range(8)]
board[7][0],board[7][1],board[7][2],board[7][3],board[7][4],board[7][5],board[7][6],board[7][7]="Br","Bn","Bb","Bq","Bk","Bb","Bn","Br"
board[6][0],board[6][1],board[6][2],board[6][3],board[6][4],board[6][5],board[6][6],board[6][7]="Bp","Bp","Bp","Bp","Bp","Bp","Bp","Bp"
board[1][0],board[1][1],board[1][2],board[1][3],board[1][4],board[1][5],board[1][6],board[1][7]="Wp","Wp","Wp","Wp","Wp","Wp","Wp","Wp"
board[0][0],board[0][1],board[0][2],board[0][3],board[0][4],board[0][5],board[0][6],board[0][7]="Wr","Wn","Wb","Wq","Wk","Wb","Wn","Wr"
#---------------------------------------------------------------------------------------------------------------------------------------------
# W E L C O M E
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
from pygame.locals import*
import time
import pyautogui
sc = list(pyautogui.size())
#---------------------------------------------------------------------------------------------------------------------------------------------
chessman_sign_dict={"k":"king","q":"queen","r":"rook","b":"bishop","n":"nerve","p":"pawn"}
alphabet={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
alphabet_res={0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h"}
chessmans={(0,0):"Wr",(0,1):"Wn",(0,2):"Wb",(0,3):"Wq",(0,4):"Wk",(0,5):"Wb",(0,6):"Wn",(0,7):"Wr",(1,0):"Wp",(1,1):"Wp",(1,2):"Wp",(1,3):"Wp",(1,4):"Wp",(1,5):"Wp",(1,6):"Wp",(1,7):"Wp",(7,0):"Br",(7,1):"Bn",(7,2):"Bb",(7,3):"Bq",(7,4):"Bk",(7,5):"Bb",(7,6):"Bn",(7,7):"Br",(6,0):"Bp",(6,1):"Bp",(6,2):"Bp",(6,3):"Bp",(6,4):"Bp",(6,5):"Bp",(6,6):"Bp",(6,7):"Bp"}
hits = {"W":[],"B":[]}
wb_dict={"W":"White","B":"Black"}
king_rook=[]
counter=x_saved=y_saved=0
color,oppo_color="W","B"
cbor = 0
modebor = 0
motion = []
xx = (1111, 1174, 1256, 1320)
s_b = s_w = 0
m_b = m_w = 10
#---------------------------------------------------------------------------------------------------------------------------------------------
pygame.init();
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("Chess");

for ime in range(1,3):
    me = pygame.image.load('Chess/chess'+str(ime)+'.jpg')
    me = pygame.transform.scale(me, (sc[0],sc[1]))
    screen.blit(me,(0,0))
    pygame.display.flip();
    time.sleep(1.5)
br = True
while br:
    for evento in pygame.event.get():
        if evento.type == pygame.MOUSEBUTTONDOWN:
            br = False
img = pygame.image.load('Chess/board.png')
screen.blit(img,(0,0))
for j in range(8):
    for i in range(8):
        man = board[j][i]
        if man != "  ":
            img = pygame.image.load('Chess/320/'+wb_dict[man[0]]+chessman_sign_dict[man[1]]+'.png')
            img = pygame.transform.scale(img, (100, 100))
            screen.blit(img,(80+(119*i),80+(119*(7-j))))
#---------------------------------------------------------------------------------------------------------------------------------------------
time1 = time.localtime()[5]
c_check = 0
while True:
    num_check = check(board,chessmans,color)
    if num_check == 0 and c_check == 0:
        for iline in range(8):
            if (color+"k") in board[iline]:
                y_king = iline
                break
        x_king = board[y_king].index(color+"k")
        one = pygame.image.load('Chess/one3.png')
        one = pygame.transform.scale(one, (119, 119))
        my_king = pygame.image.load('Chess/320/'+wb_dict[color]+'king.png')
        my_king = pygame.transform.scale(my_king, (100, 100))
        if counter % 2 == 0:
            screen.blit(one,(70+(119*x_king),70+(119*(7-y_king))))
            screen.blit(my_king,(80+(119*x_king),80+(119*(7-y_king))))
        elif counter % 2 == 1:
            screen.blit(one,(70+(119*x_king),70+(119*y_king)))
            screen.blit(my_king,(80+(119*x_king),80+(119*y_king)))
        c_check = 1
    num_checkmate=checkmate(board,chessmans,color,oppo_color)
    if num_checkmate==0:
        img = pygame.image.load('Chess/checkmate'+oppo_color+'.png')
        img = pygame.transform.scale(img, (624, 312))
        screen.blit(img,((sc[0]-624)//2,(sc[1]-312)//2))
        pygame.display.flip();
        break
    num_stalemate=stalemate(board,chessmans,color,oppo_color)
    if num_stalemate==0:
        img = pygame.image.load('Chess/stalemate.png')
        img = pygame.transform.scale(img, (624, 312))
        screen.blit(img,((sc[0]-624)//2,(sc[1]-312)//2))
        pygame.display.flip();
        break
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT or ( evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE ):
            pygame.quit()
            sys.exit(0)
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if 70 <= pygame.mouse.get_pos()[0] <= 1022 and 70 <= pygame.mouse.get_pos()[1] <= 1022:
                man1 = (pygame.mouse.get_pos()[0]-70)//119
                man2 = (pygame.mouse.get_pos()[1]-70) // 119
                if counter % 2 == 0:
                    man2 = 7 - man2
                if board[man2][man1][0] == color:
                    if cbor == 1:
                        if yman == man2 and xman == man1 and modebor == 1:
                            modebor = 2
                        if xman % 2 == yman % 2:
                            img = pygame.image.load('Chess/Border2.png')
                        elif xman % 2 != yman % 2:
                            img = pygame.image.load('Chess/Border1.png')
                        img = pygame.transform.scale(img, (119, 119))
                        if counter % 2 == 1:
                            screen.blit(img,(70+(119*xman),70+(119*yman)))
                        elif counter % 2 == 0:
                            screen.blit(img,(70+(119*xman),70+(119*(7-yman))))
                        for possi in poss:
                            if possi[0] % 2 == possi[1] % 2:
                                img = pygame.image.load('Chess/one2.png')
                            else:
                                img = pygame.image.load('Chess/one1.png')
                            img = pygame.transform.scale(img, (119, 119))
                            if counter % 2 == 1:
                                screen.blit(img,(70+(119*possi[0]),70+(119*possi[1])))
                            elif counter % 2 == 0:
                                screen.blit(img,(70+(119*possi[0]),70+(119*(7-possi[1]))))
                            if counter % 2 == 0 :
                                man = board[possi[1]][possi[0]]
                                if man != "  ":
                                    img = pygame.image.load('Chess/320/'+wb_dict[man[0]]+chessman_sign_dict[man[1]]+'.png')
                                    img = pygame.transform.scale(img, (100, 100))
                                    screen.blit(img,(80+(119*possi[0]),80+(119*(7-possi[1]))))
                            elif counter % 2 == 1 :
                                man = board[possi[1]][possi[0]]
                                if man != "  ":
                                    img = pygame.image.load('Chess/320/'+wb_dict[man[0]]+chessman_sign_dict[man[1]]+'.png')
                                    img = pygame.transform.scale(img, (100, 100))
                                    screen.blit(img,(80+(119*possi[0]),80+(119*possi[1])))
                        if num_check == 0 and xman == x_king and yman == y_king:
                            if x_king % 2 == y_king % 2:
                                img = pygame.image.load('Chess/one2.png')
                            else:
                                img = pygame.image.load('Chess/one1.png')
                            img = pygame.transform.scale(img, (119, 119))
                            if counter % 2 == 1:
                                screen.blit(img,(70+(119*x_king),70+(119*y_king)))
                            elif counter % 2 == 0:
                                screen.blit(img,(70+(119*x_king),70+(119*(7-y_king))))
                            one = pygame.image.load('Chess/one3.png')
                            one = pygame.transform.scale(one, (119, 119))
                            my_king = pygame.image.load('Chess/320/'+wb_dict[color]+'king.png')
                            my_king = pygame.transform.scale(my_king, (100, 100))
                            if counter % 2 == 0:
                                screen.blit(one,(70+(119*x_king),70+(119*(7-y_king))))
                                screen.blit(my_king,(80+(119*x_king),80+(119*(7-y_king))))
                            elif counter % 2 == 1:
                                screen.blit(one,(70+(119*x_king),70+(119*y_king)))
                                screen.blit(my_king,(80+(119*x_king),80+(119*y_king)))
                    if modebor != 2:
                        xman = man1
                        yman = man2
                        img = pygame.image.load('Chess/Border.png')
                        if counter % 2 == 1:
                            screen.blit(img,(70+(119*xman),70+(119*yman)))
                        elif counter % 2 == 0:
                            screen.blit(img,(70+(119*xman),70+(119*(7-yman))))
                        motion = [board[yman][xman][1], alphabet_res[xman] + str(yman)]
                        poss = possible(board,chessmans,xman,yman,motion[0],color,oppo_color,king_rook,x_saved,y_saved)
                        for possi in poss:
                            img = pygame.image.load('Chess/point.png')
                            img = pygame.transform.scale(img, (34, 34))
                            if counter % 2 == 1:
                                screen.blit(img,(112+(119*possi[0]),112+(119*possi[1])))
                            elif counter % 2 == 0:
                                screen.blit(img,(112+(119*possi[0]),112+(119*(7-possi[1]))))
                        modebor = 1
                    else:
                        for possi in poss:
                            if possi[0] % 2 == possi[1] % 2:
                                img = pygame.image.load('Chess/one2.png')
                            else:
                                img = pygame.image.load('Chess/one1.png')
                            img = pygame.transform.scale(img, (119, 119))
                            if counter % 2 == 1:
                                screen.blit(img,(70+(119*possi[0]),70+(119*possi[1])))
                            elif counter % 2 == 0:
                                screen.blit(img,(70+(119*possi[0]),70+(119*(7-possi[1]))))
                            if counter % 2 == 0 :
                                man = board[possi[1]][possi[0]]
                                if man != "  ":
                                    img = pygame.image.load('Chess/320/'+wb_dict[man[0]]+chessman_sign_dict[man[1]]+'.png')
                                    img = pygame.transform.scale(img, (100, 100))
                                    screen.blit(img,(80+(119*possi[0]),80+(119*(7-possi[1]))))
                            elif counter % 2 == 1 :
                                man = board[possi[1]][possi[0]]
                                if man != "  ":
                                    img = pygame.image.load('Chess/320/'+wb_dict[man[0]]+chessman_sign_dict[man[1]]+'.png')
                                    img = pygame.transform.scale(img, (100, 100))
                                    screen.blit(img,(80+(119*possi[0]),80+(119*possi[1])))
                        modebor = 0
                    cbor = 1
                elif modebor == 1 and board[man2][man1][0] != color:
                    motion += [alphabet_res[man1] + str(man2)]
                    chessman_sign=motion[0]
                    x1=alphabet[motion[1][0]]
                    y1=int(motion[1][1])
                    x2=alphabet[motion[2][0]]
                    y2=int(motion[2][1])
                    if chessman_sign=="p" and color=="B":
                        num=pawn_black(board,chessmans,chessman_sign_dict,wb_dict,hits,color,oppo_color,x1,y1,x2,y2,x_saved,y_saved)
                    if chessman_sign=="p" and color=="W":
                        num=pawn_white(board,chessmans,chessman_sign_dict,wb_dict,hits,color,oppo_color,x1,y1,x2,y2,x_saved,y_saved)
                    if chessman_sign=="n":
                        num=nerve(board,chessmans,chessman_sign_dict,wb_dict,hits,color,oppo_color,x1,y1,x2,y2)
                    if chessman_sign=="b":
                        num=bishop(board,chessmans,chessman_sign_dict,wb_dict,hits,color,oppo_color,x1,y1,x2,y2)
                    if chessman_sign=="r":
                        num=rook(board,chessmans,chessman_sign_dict,wb_dict,hits,color,oppo_color,x1,y1,x2,y2)
                    if chessman_sign=="q":
                        num=queen(board,chessmans,chessman_sign_dict,wb_dict,hits,color,oppo_color,x1,y1,x2,y2)
                    if chessman_sign=="k":
                        num=king(board,chessmans,chessman_sign_dict,wb_dict,hits,king_rook,color,oppo_color,x1,y1,x2,y2)
                    if num == 1:
                        xman = man1
                        yman = man2
                        if chessman_sign=="r":
                            king_rook.append(color+"r"+str(y1)+str(x1))
                        if chessman_sign=="k":
                            king_rook.append(color+"k")
                        x_saved=x2
                        y_saved=y2
                        color, oppo_color = oppo_color, color
                        counter += 1
                        cbor= 0
                        modebor = 0
                        c_check = 0
                        if counter % 2 == 0 :
                            img = pygame.image.load('Chess/board1.png')
                            screen.blit(img,(0,0))
                            for j in range(8):
                                for i in range(8):
                                    man = board[j][i]
                                    if man != "  ":
                                        img = pygame.image.load('Chess/320/'+wb_dict[man[0]]+chessman_sign_dict[man[1]]+'.png')
                                        img = pygame.transform.scale(img, (100, 100))
                                        screen.blit(img,(80+(119*i),80+(119*(7-j))))
                            for hb in range(len(hits["B"])):
                                img = pygame.image.load('Chess/320/'+'Black'+chessman_sign_dict[hits["B"][hb]]+'.png')
                                img = pygame.transform.scale(img, (90, 90))
                                screen.blit(img,(1077+((hb%5)*90),74+((hb//5)*90)))
                            for hw in range(len(hits["W"])):
                                img = pygame.image.load('Chess/320/'+'White'+chessman_sign_dict[hits["W"][hw]]+'.png')
                                img = pygame.transform.scale(img, (90, 90))
                                screen.blit(img,(1077+((hw%5)*90),683+((hw//5)*90)))
                        elif counter % 2 == 1 :
                            img = pygame.image.load('Chess/board2.png')
                            screen.blit(img,(0,0))
                            for j in range(8):
                                for i in range(8):
                                    man = board[j][i]
                                    if man != "  ":
                                        img = pygame.image.load('Chess/320/'+wb_dict[man[0]]+chessman_sign_dict[man[1]]+'.png')
                                        img = pygame.transform.scale(img, (100, 100))
                                        screen.blit(img,(80+(119*i),80+(119*j)))
                            for hb in range(len(hits["B"])):
                                img = pygame.image.load('Chess/320/'+'Black'+chessman_sign_dict[hits["B"][hb]]+'.png')
                                img = pygame.transform.scale(img, (90, 90))
                                screen.blit(img,(1077+((hb%5)*90),683+((hb//5)*90)))
                            for hw in range(len(hits["W"])):
                                img = pygame.image.load('Chess/320/'+'White'+chessman_sign_dict[hits["W"][hw]]+'.png')
                                img = pygame.transform.scale(img, (90, 90))
                                screen.blit(img,(1077+((hw%5)*90),74+((hw//5)*90)))
                    elif num == 0:
                        motion = motion[:-1]
    time2 = time.localtime()[5]
    if counter % 2 == 0 and (time2-time1 == 1 or time1-time2 == 59):
        s_w -= 1
        time1 = time2
        if s_w == -1:
            m_w -= 1
            s_w = 59
        if m_w < 0:
            img = pygame.image.load('Chess/checkmate'+oppo_color+'.png')
            img = pygame.transform.scale(img, (624, 312))
            screen.blit(img,((sc[0]-624)//2,(sc[1]-312)//2))
            pygame.display.flip();
            break
    elif counter % 2 == 1 and (time2-time1 == 1 or time1-time2 == 59):
        s_b -= 1
        time1 = time2
        if s_b == -1:
            m_b -= 1
            s_b = 59
        if m_b < 0:
            img = pygame.image.load('Chess/checkmate'+oppo_color+'.png')
            img = pygame.transform.scale(img, (624, 312))
            screen.blit(img,((sc[0]-624)//2,(sc[1]-312)//2))
            pygame.display.flip();
            break
    printyw = "0"*(2-len(str(m_w)))+str(m_w)+"0"*(2-len(str(s_w)))+str(s_w)
    printyb = "0"*(2-len(str(m_b)))+str(m_b)+"0"*(2-len(str(s_b)))+str(s_b)
    img = pygame.image.load('chess/timer_cl'+str(counter%2)+'.png')
    screen.blit(img,(1094,427))
    if counter % 2 == 0:
        for i in range(4):
            img = pygame.image.load('chess/numbers/'+printyw[i]+color+'.png')
            screen.blit(img,(xx[i],552))
        for i in range(4):
            img = pygame.image.load('chess/numbers/'+printyb[i]+oppo_color+'.png')
            screen.blit(img,(xx[i],439))
    elif counter % 2 == 1:
        for i in range(4):
            img = pygame.image.load('chess/numbers/'+printyb[i]+color+'.png')
            screen.blit(img,(xx[i],552))
        for i in range(4):
            img = pygame.image.load('chess/numbers/'+printyw[i]+oppo_color+'.png')
            screen.blit(img,(xx[i],439))
    pygame.display.flip();
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT or ( evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE ):
            pygame.quit()
            sys.exit(0)