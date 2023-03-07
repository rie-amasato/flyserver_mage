import numpy as np
import random
from PIL import Image, ImageDraw
import io

def Reset(N):
    map=[]
    for i in range(N):
        map.append([0 for i in range(N)])
    for y in range(N):
        for x in range(N):
            if x==0 or y==0 or x==N-1 or y==N-1:
                map[x][y]=1
    return map

def mkVW(x,y,MP):
    N=len(MP)
    if x==0:
        xU=[-1]
        xL=[0,2]
        xR=[0,2]
        xD=[1,3]
    elif x==1:
        xU=[0,1]
        xL=[0,3]
        xR=[0,3]
        xD=[2,4]
    elif x==N-1:
        xU=[x-2,x]
        xL=[N-2,N]
        xR=[N-2,N]
        xD=[-1]
    elif x==N-2:
        xU=[x-2,x]
        xL=[N-3,N]
        xR=[N-3,N]
        xD=[N-1,N]
    else:
        xU=[x-2,x]
        xL=[x-1,x+2]
        xR=[x-1,x+2]
        xD=[x+1,x+3]
    if y==0:
        yU=[0,2]
        yL=[-1]
        yR=[1,3]
        yD=[0,2]
    elif y==1:
        yU=[0,3]
        yL=[0,1]
        yR=[2,4]
        yD=[0,3]
    elif y==N-1:
        yU=[y-1,y+1]
        yL=[N-3,N-1]
        yR=[-1]
        yD=[N-2,N]
    elif y==N-2:
        yU=[y-1,y+2]
        yL=[y-2,y]
        yR=[y+1,y+2]
        yD=[y-1,y+2]
    else:
        yU=[y-1,y+2]
        yL=[y-2,y]
        yR=[y+1,y+3]
        yD=[y-1,y+2]
    return(xU,xL,xR,xD,yU,yL,yR,yD)

def WCheck(x,y,mp):
    #0:地面 1:伸ばせる壁 2:伸ばせない壁
    Sosuu=[2,3,5,7]
    R=mkVW(x,y,mp)
    C=1
    for i in range(0, 4):
        if R[i]!=[-1] and R[i+4]!=[-1]:
            if (sum(sum(np.array(mp)[R[i][0]:R[i][1],R[i+4][0]:R[i+4][1]]))!=0):
                C*=Sosuu[i]
        else:
            C*=Sosuu[i]
    #print(C,x,y)
    return C

def mkMage(N):
    random.seed()
    # cnt=1
    m=Reset(N)
    while True:
        cnt=0
        for x in range(len(m)):
            for y in range(len(m[0])):
                if m[x][y]==1:
                    if WCheck(x,y,m)==210:
                        m[x][y]=2
                    else:
                        cnt+=1

        if cnt==0:
            break
        WStart=random.randint(1,cnt)

        for x in range(len(m)):
            for y in range(len(m[0])):
                if m[x][y]==1:
                    WStart-=1
                if WStart==0:
                    while (WCheck(x,y,m)!=210):
                        WVertical=WCheck(x,y,m)
                        CVertical=0
                        if WVertical%2!=0:
                            #print("うえ")
                            CVertical+=1
                        if WVertical%3!=0:
                            #print("ひだ")
                            CVertical+=1
                        if WVertical%5!=0:
                            #print("みぎ")
                            CVertical+=1
                        if WVertical%7!=0:
                            #print("した")
                            CVertical+=1
                        Vertical=random.randint(1,CVertical)
                        #print(CVertical)

                        if WVertical%2!=0:
                            Vertical-=1
                            if Vertical==0:
                                #print("うえ")
                                x-=1
                        if WVertical%3!=0:
                            Vertical-=1
                            if Vertical==0:
                                #print("ひだ")
                                y-=1
                        if WVertical%5!=0:
                            Vertical-=1
                            if Vertical==0:
                                #print("みぎ")
                                y+=1
                        if WVertical%7!=0:
                            Vertical-=1
                            if Vertical==0:
                                #print("した")
                                x+=1
                        m[x][y]=1
                    WStart-=1

    STGen=0
    for x in range(1,len(m)-1):
        for y in range(1,len(m[0])-1):
            if m[x][y]==0:
                WAW=0
                for dx,dy in zip([-1,1,0,0],[0,0,1,-1]):
                    if m[x+dx][y+dy]==0:
                        WAW+=1
                if WAW==1:
                   STGen+=1

    ST=1#random.randint(1,STGen) 
    G=STGen-1#random.randint(1,STGen)-1
    #print(ST,G)
    for x in range(1,len(m)-1):
        for y in range(1,len(m[0])-1):
            if m[x][y]==0:
                WAW=0
                for dx,dy in zip([-1,1,0,0],[0,0,1,-1]):
                    if m[x+dx][y+dy]==0:
                        WAW+=1
                if WAW==1:
                    ST-=1
                    if ST==0:
                        m[x][y]=3
                        ST-=1
                    else:
                        G-=1
                    if G==0:
                        m[x][y]=4
                        G-=1
    return m

def mkImg(length):
    m=mkMage(int(length))
    im = Image.new('RGB', (len(m)*10, len(m[0])*10), (256,256,256))
    draw = ImageDraw.Draw(im)
    for x in range(len(m)):
        for y in range(len(m[0])):
            if m[x][y]==2:
                draw.rectangle((x*10,y*10,x*10+10,y*10+10),fill=(0,0,0))
            if m[x][y]==3:
                draw.rectangle((x*10,y*10,x*10+10,y*10+10),fill=(256,0,0))
            if m[x][y]==4:
                draw.rectangle((x*10,y*10,x*10+10,y*10+10),fill=(0,256,0))

    im_bytes=io.BytesIO()
    im.save(im_bytes, format='PNG')
    return im_bytes.getvalue()

def mkSvg(length):
    m = mkMage(int(length))
    h = 10
    w = 10
    im_svgstring = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="'+str(w*len(m[0]))+'" height="'+str(h*len(m))+'">'

    c = ["#badcad", "-", "#3f312b", "#d7003a", "#0095d9"]
    #地面、なし、壁、Start、Goal
    for x in range(len(m)):
        for y in range(len(m[0])):
            im_svgstring+=\
                '<rect x="'+str(x*w)+'" '\
                +'y="'+str(y*h)+'" '\
                +'height="'+str(h)+'" '\
                +'width="'+str(w)+'" '\
                +'fill="'+c[m[x][y]]+'" '\
                +'/>'

    im_svgstring+="</svg>"

    #print(im_svgstring)
    return im_svgstring
