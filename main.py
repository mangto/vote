import pygame, sys, time
import win32api
from shaders import *
from pygame import gfxdraw
import gicon_keyboard as gk

pygame.init()

global group_list

window = pygame.display.set_mode((1440,800))
save = (1030,int(1030*210/297))
pygame.display.set_caption("자리 바꾸기")
pygame.display.set_icon(pygame.image.load('.\\data\\icon.jpg'))
ui_list = []

votes = eval(open('.\\vote.json','r',encoding='utf-8').read())

def font(fontname, size):
    return pygame.font.Font(f"C:\\Windows\\Fonts\\{fontname}.TTF",size)
def addlist(lists:list):
    result = []
    for lst in lists:
        result += lst

    return result

global btonmouse
btonmouse = False

lastleft1 = 0
lastleft2 = 0
lastright2 = 0
lastright1 = 0
lastmiddle1 = 0
class mouse:
    def middlebtdown():
        global lastmiddle1
        middle = win32api.GetKeyState(0x04)
        if int(lastmiddle1) >=0 and middle <0:
            lastmiddle1 = middle
            return True
        else:
            lastmiddle1 = middle
            return False
    def rightbtdown():
        global lastright1
        right = win32api.GetKeyState(0x02)
        if int(lastright1) >= 0 and right <0:
            lastright1 = right
            return True
        else:
            lastright1=right
            return False
    def rightbtup():
        global lastright2
        right = win32api.GetKeyState(0x02)
        if int(lastright2) < 0 and right >=0:
            lastright2 = right
            return True
        else:
            lastright2=right
            return False
    def leftbtdown():
        global lastleft1
        left = win32api.GetKeyState(0x01)
        if int(lastleft1) >=0 and left <0:
            lastleft1 = left
            return True
        else:
            lastleft1 = left
            return False
    def leftbtup():
        global lastleft2
        left = win32api.GetKeyState(0x01)
        if int(lastleft2) < 0 and left >= 0:
            lastleft2 = left
            return True
        
        else:
            lastleft2 = left
            return False
def vote(number):
    votes[number] += 1

    pad1.reset()
    pad2.reset()
    pad3.reset()

def reset():
    global votes
    votes = [0,0,0]



class System:
    clock = pygame.time.Clock()

    class draw:
        def aacircle(surface, x, y, radius, color):
            gfxdraw.aacircle(surface, x, y, radius, color)
            gfxdraw.filled_circle(surface, x, y, radius, color)
        def rrect(surface,rect,color,radius=0.4):
            rect         = pygame.Rect(rect)
            color        = pygame.Color(*color)
            alpha        = color.a
            color.a      = 0
            pos          = rect.topleft
            rect.topleft = 0,0
            rectangle    = pygame.Surface(rect.size,pygame.SRCALPHA)
            circle       = pygame.Surface([min(rect.size)*3]*2,pygame.SRCALPHA)
            pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
            circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)
            radius              = rectangle.blit(circle,(0,0))
            radius.bottomright  = rect.bottomright
            rectangle.blit(circle,radius)
            radius.topright     = rect.topright
            rectangle.blit(circle,radius)
            radius.bottomleft   = rect.bottomleft
            rectangle.blit(circle,radius)

            rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
            rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

            rectangle.fill(color,special_flags=pygame.BLEND_RGBA_MAX)
            rectangle.fill((255,255,255,alpha),special_flags=pygame.BLEND_RGBA_MIN)
            return surface.blit(rectangle,pos)
        def trirect(surface,x,y,sx,sy,tri,color,edge=(1,1,1,1)):
            if sx < tri*2:
                sx = tri*2
            if sy < tri*2:
                sy = tri*2

            pygame.draw.rect(surface,color,[x+tri,y,sx-tri*2,sy])
            pygame.draw.rect(surface,color,[x,y+tri,sx,sy-tri*2])
            if edge[0] == 1:
                pygame.draw.polygon(surface,color,[[x,y+tri],[x+tri,y],[x+tri,y+tri]])
            else:
                pygame.draw.rect(surface,color,[x,y,tri,tri])
            if edge[1] == 1:
                pygame.draw.polygon(surface,color,[[x+sx-tri,y+1],[x+sx-1,y+tri],[x+sx-tri,y+tri]])
            else:
                pygame.draw.rect(surface,color,[x+sx-tri,y,tri,tri])
            if edge[2] == 1:
                pygame.draw.polygon(surface,color,[[x,y+sy-tri],[x+tri,y+sy-1],[x+tri,y+sy-tri]])
            else:
                pygame.draw.rect(surface,color,[x,y+sy-tri,tri,tri])
            if edge[3] == 1:
                pygame.draw.polygon(surface,color,[[x+sx-1,y+sy-tri],[x+sx-tri,y+sy-1],[x+sx-tri,y+sy-tri]])
            else:
                pygame.draw.rect(surface,color,[x+sx-tri,y+sy-tri,tri,tri])
        def textsize(text, font):
            text_obj = font.render(text, True, (0,0,0))
            text_rect=text_obj.get_rect()
            return text_rect.size
        def text(text, font, window, x, y, cenleft="center", color=(0,0,0)):
            text_obj = font.render(text, True, color)
            text_rect=text_obj.get_rect()
            if(cenleft == "center"):
                text_rect.centerx = x
                text_rect.centery = y
            elif(cenleft == "left"):
                text_rect.left=x
                text_rect.top=y
            elif(cenleft == "right"):
                text_rect.right=x
                text_rect.top=y
            elif(cenleft == "cenleft"):
                text_rect.left=x
                text_rect.centery=y
            elif(cenleft == "cenright"):
                text_rect.right=x
                text_rect.centery=y
            window.blit(text_obj, text_rect)
        def gettsize(text,font):
            return font.render(text,True,(0,0,0)).get_rect().size
    
    class ui:
        ui_tag = eval(open('.\\data\\ui.json','r',encoding='utf-8').read())
        group_lst = []

        def shadow(surface, amount, opacity):
            blured, x, y = blur(surface,amount)
            shadow = change_light_color(blured,(28, 32, 64))
            shadow.set_alpha(opacity)
            return shadow, x, y
        class votepad:

            img = pygame.image.load(".\\data\\vote.png")

            def __init__(self, x, y, sx, sy):
                self.x=x
                self.y=y
                self.sx=sx
                self.sy=sy

                self.surface = pygame.Surface((sx,sy),pygame.SRCALPHA).convert_alpha()
                self.count = 0

                ui_list.append(self)


            def draw(self,mx,my):
                window.blit(self.surface,(self.x,self.y))

            def addone(self):
                self.surface.blit(System.ui.votepad.img,(60*(self.count%4),60*(self.count//4)))
                self.count += 1

            def reset(self):
                self.surface = pygame.Surface((self.sx,self.sy),pygame.SRCALPHA).convert_alpha()
                self.count = 0

        class line_shadow:
            def __init__(self,x,y,sx,sy,way,startvalue=150):
                global sshadow
                ui_list.append(self)
                self.x=x
                self.y=y
                self.sx=sx
                self.sy=sy
                self.way=way
                self.pointer=[0,0]
                self.startvalue=startvalue
                self.shadow = pygame.transform.smoothscale(pygame.transform.rotate(sshadow,(way-1)*90+180),(sx,sy))
                self.shadow.set_alpha(startvalue)
                self.mouse=pygame.SYSTEM_CURSOR_ARROW 
                if self.way >2:
                    self.startvalue = self.startvalue
            def draw(self,mx,my):
                global window
                window.blit(self.shadow,(self.x,self.y))
        class group:
            description = eval(open('.\\data\\description.json','r',encoding='utf-8').read())
            def __init__(self,name:str, des:str=" - "):
                self.name = name
                System.ui.group_lst.append(self)

                
                self.width = 400
                self.height = 500
                self.panel = System.ui.button(window,1230,150,self.width,self.height,color=(255,255,255))
                self.des = des


                ui_list.append(self)


            def draw(self, mx, my):
                self.panel.x = int((1440-self.width*len(System.ui.group_lst))/(len(System.ui.group_lst)+1))*(System.ui.group_lst.index(self)+1)  +self.width*System.ui.group_lst.index(self)
                self.vote.x = self.panel.x + int(self.width/2-self.vote.sx/2)
                System.draw.text(self.name,font("LG_SMART_UI-SEMIBOLD",30),window,self.panel.x+int(self.width/2),200,"center",(41, 42, 44))

                if (self.name in System.ui.group.description):
                    for i, descript in enumerate(System.ui.group.description[self.name]):
                        System.draw.text(f"{self.des}{descript}",font("LG_SMART_UI-SEMIBOLD",20),window,self.panel.x+15,250+22*i,"cenleft",(41, 42, 44))
        class button:
            vfont = font("LG_SMART_UI-SEMIBOLD",30)
            def __init__(self,surface:pygame.Surface, x:int, y:int, sx:int, sy:int, icon:pygame.Surface=False,
                            color=(255,255,255),edge_color=(0,0,0), edge_thick=1,opacity:int=255,round:bool=False, roundness=1.0,
                            text:str="",text_color=(0,0,0),font:font=font("LG_SMART_UI-SEMIBOLD",15),
                            addshadow=True, clickable=True,CustomCorrectionX=0,CustomCorrectionY=0,
                            showline=True,
                            tag="", vote = False
                        ):
                ui_list.append(self)

                self.surface=surface
                self.x=x
                self.y=y
                self.sx=sx
                self.sy=sy
                self.icon=icon
                self.color=color
                self.edge_color=edge_color
                self.edge_thick=edge_thick
                self.shape = round
                self.opacity = opacity
                self.text=text
                self.text_color = text_color
                self.font=font
                self.round=round
                self.roundness=roundness
                self.addshadow=addshadow
                self.clickable=clickable
                self.CustomCorrectionX=CustomCorrectionX
                self.CustomCorrectionY=CustomCorrectionY
                self.showline=showline
                self.tag=tag

                self.onmouse = False
                self.onmousecolor = (int(color[0]*0.9),int(color[1]*0.9),int(color[2]*0.9))

                self.image = pygame.Surface((sx,sy),pygame.SRCALPHA,32).convert_alpha()
                self.onmouseS = pygame.Surface((sx,sy),pygame.SRCALPHA,32).convert_alpha()
                self.omtexted = pygame.Surface((sx,sy),pygame.SRCALPHA,32).convert_alpha()
                self.texted = pygame.Surface((sx,sy),pygame.SRCALPHA,32).convert_alpha()
                self.hitbox = pygame.Surface(surface.get_size())

                if (round == False):
                    pygame.draw.rect(self.image,color,[0,0,sx,sy])
                    pygame.draw.rect(self.image,edge_color,[0,0,sx,sy],edge_thick)
                    pygame.draw.rect(self.hitbox,(255,255,255),[x,y,sx,sy])

                    pygame.draw.rect(self.onmouseS,self.onmousecolor,[0,0,sx,sy])
                    pygame.draw.rect(self.onmouseS,edge_color,[0,0,sx,sy],edge_thick)
                else:
                    System.draw.rrect(self.image,[0,0,sx,sy],edge_color,1)
                    System.draw.rrect(self.image,[edge_thick,edge_thick,sx-2*edge_thick,sy-2*edge_thick],color,roundness)
                    System.draw.rrect(self.hitbox,[x,y,sx,sy],(255,255,255),1)

                    System.draw.rrect(self.onmouseS,[0,0,sx,sy],edge_color,1)
                    System.draw.rrect(self.onmouseS,[edge_thick,edge_thick,sx-2*edge_thick,sy-2*edge_thick],self.onmousecolor,roundness)


                if (icon != False):
                    icon_size = icon.get_size()
                    self.image.blit(icon,(int((sx-icon_size[0])/2),int((sy-icon_size[1])/2)))
                    self.onmouseS.blit(icon,(int((sx-icon_size[0])/2),int((sy-icon_size[1])/2)))

                self.texted.blit(self.image,(0,0))
                self.omtexted.blit(self.onmouseS,(0,0))
                System.draw.text(text,font,self.texted,int(sx/2),int(sy/2),"center",self.text_color)
                System.draw.text(text,font,self.omtexted,int(sx/2),int(sy/2),"center",self.text_color)

                self.opacitied = self.texted
                self.omopacited = self.omtexted
                self.opacitied.set_alpha(opacity)
                self.omopacited.set_alpha(opacity)

                self.shadow, self.correctionx,self.correctiony=System.ui.shadow(self.opacitied,5,10)

                self.vote = vote
                if vote == True:
                    self.voted = pygame.Surface((1440,800),pygame.SRCALPHA).convert_alpha()
                    pygame.draw.rect(self.voted,(0,0,0,128),[0,0,1440,800])
                    System.draw.text(f"{self.text}(을)를 투표했습니다",System.ui.button.vfont,self.voted,720,400,"center",(255,255,255))

            def draw(self, mx, my):
                global btonmouse
                
                if (self.addshadow == True):
                    if (self.CustomCorrectionX==0 and self.CustomCorrectionY ==0):
                        self.surface.blit(self.shadow,(self.x-self.correctionx,self.y-self.correctiony))
                    else:
                        self.surface.blit(self.shadow,(self.x+self.CustomCorrectionX,self.y+self.CustomCorrectionY))
                self.surface.blit(self.opacitied,(self.x,self.y))

                if (self.hitbox.get_at((mx,my)) == (255,255,255) and self.clickable==True):
                    self.onmouse = True
                    System.draw.text(f"{self.text}를 투표합니다",font("LG_SMART_UI-SEMIBOLD",20),window,500,50,"center")
                    btonmouse = True
                    if (self.showline == True):
                        pygame.draw.rect(window,(56,190,128),[self.x,self.y,self.sx,self.sy],1)
                    else: self.surface.blit(self.omopacited,(self.x,self.y))

                    if (mouse.leftbtup() == True):
                        if (self.tag in System.ui.ui_tag['button']):
                            exec(f"{System.ui.ui_tag['button'][self.tag]}")

                            if (self.vote == True):
                
                                System.display()
                                window.blit(self.voted,(0,0))
                                    
                                pygame.display.update()

                                System.clock.tick(30)
                                time.sleep(1)

                else:
                    self.onmouse = False

                System.draw.text(self.text,self.font,window,self.x+int(self.sx/2),self.y+int(self.sy/2),"center",color=self.text_color)
            def set_text(self,text:str):
                self.text = text
                self.texted = pygame.Surface((self.sx,self.sy),pygame.SRCALPHA,32).convert_alpha()
                self.omtexted = pygame.Surface((self.sx,self.sy),pygame.SRCALPHA,32).convert_alpha()
                self.texted.blit(self.image,(0,0))
                self.omtexted.blit(self.onmouseS, (0,0))
                self.opacitied = self.texted
                self.opacitied.set_alpha(self.opacity)
                self.omopacited = self.omtexted
                self.omopacited.set_alpha(self.opacity)
            def set_opacity(self,opacity:int):
                self.opacity = opacity
                self.opacitied = self.texted
                self.opacitied.set_alpha(opacity)
        class textlistview:
            def __init__(self):
                pass
            def draw(self,mx,my):
                pass
        class numberinput:
            def __init__(self,surface:pygame.Surface, x,y,sx,sy,backgroundcolor,font,basetext="input box",textcolor=(255,255,255),glow=(255,255,255),warn=(255,30,30),text=""):
                ui_list.append(self)
                self.x=x
                self.y = y
                self.sx=sx
                self.sy = sy
                self.bgc = backgroundcolor
                self.font = font
                self.basetext = basetext
                self.text = text
                self.textcolor = textcolor
                self.glow = glow
                self.enabled = False
                self.canwrite = True
                self.warn = warn

                self.hitbox = pygame.Surface(surface.get_size())
                pygame.draw.rect(self.hitbox,(255,255,255),(x,y,sx,sy))
            def draw(self, mx,my):
                pressed = keyboard[0]

                if (self.hitbox.get_at((mx,my)) == (255,255,255) and mouse.leftbtup() == True):
                    self.enabled = True
                elif(self.hitbox.get_at((mx,my)) != (255,255,255) and mouse.leftbtup() == True):
                    self.enabled = False

                pygame.draw.rect(window,self.bgc,[self.x,self.y,self.sx,self.sy])
                textsize = System.draw.gettsize(self.text,self.font)
                if (self.text != ""): System.draw.text(self.text,self.font,window,self.x+int(self.sx/2),self.y+int(self.sy/2),"center",self.textcolor)
                else: System.draw.text(self.basetext,self.font,window,self.x+int(self.sx/2),self.y+int(self.sy/2),"center",self.textcolor)
                if (self.enabled == True): pygame.draw.rect(window,self.glow,[self.x,self.y,self.sx,self.sy],1)
                if (textsize[0] > self.sx-(self.sy-textsize[1])):
                    self.canwrite = False
                    pygame.draw.rect(window,self.warn,[self.x,self.y,self.sx,self.sy],1)
                else: self.canwrite = True

                for key in pressed:
                    if (key == "backspace"):
                        self.text = self.text[0:-1]
                    elif (str(key).isnumeric() == True and textsize[0] < self.sx-(self.sy-textsize[1])):
                        self.text += key

    def display():
        window.fill((235, 241, 249))

        for ui in ui_list: 
            ui.draw(mx,my)
        
        if(btonmouse == False):
            System.draw.text(f"이름을 눌러 투표합니다",font("LG_SMART_UI-SEMIBOLD",20),window,500,50,"center")

        System.draw.text(f"* 이름을 눌러 투표할 수 있습니다",font("LG_SMART_UI-SEMIBOLD",15),window,1050,120,"cenleft")
        System.draw.text(f"* 한 번 투표한 표는 바꿀 수 없으니 주의하세요!",font("LG_SMART_UI-SEMIBOLD",15),window,1050,140,"cenleft")

    def event(events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

cand1 = System.ui.button(window,120,150,240,100,color=(255,255,255),edge_thick=0,text="임영재",round=True,roundness=0.6,font=font("LG_SMART_UI-SEMIBOLD",24),tag="vote1",vote=True)
cand2 = System.ui.button(window,380,150,240,100,color=(255,255,255),edge_thick=0,text="김선아",round=True,roundness=0.6,font=font("LG_SMART_UI-SEMIBOLD",24),tag="vote2",vote=True)
cand3 = System.ui.button(window,640,150,240,100,color=(255,255,255),edge_thick=0,text="윤지유",round=True,roundness=0.6,font=font("LG_SMART_UI-SEMIBOLD",24),tag="vote3",vote=True)
num1 = System.ui.button(window,215,110,70,30,color=(56,190,128),edge_thick=0,text="기호 1번",round=True,roundness=0.6,font=font("LG_SMART_UI-SEMIBOLD",15),tag="vote1",text_color=(255,255,255),clickable=False)
num2 = System.ui.button(window,475,110,70,30,color=(56,190,128),edge_thick=0,text="기호 2번",round=True,roundness=0.6,font=font("LG_SMART_UI-SEMIBOLD",15),tag="vote2",text_color=(255,255,255),clickable=False)
num3 = System.ui.button(window,735,110,70,30,color=(56,190,128),edge_thick=0,text="기호 3번",round=True,roundness=0.6,font=font("LG_SMART_UI-SEMIBOLD",15),tag="vote3",text_color=(255,255,255),clickable=False)
setting_panel = System.ui.button(window,1030,-50,450,150,color=(255,255,255),edge_thick=0,round=True,roundness=0.1,clickable=False,CustomCorrectionX=-75,CustomCorrectionY=-150)

pad1 = System.ui.votepad(120,270,240,640)
pad2 = System.ui.votepad(380,270,240,640)
pad3 = System.ui.votepad(640,270,240,640)

AtOnce = System.ui.button(window,1055,35,290,30,color=(56,190,128),edge_thick=0,text="결과보기",text_color=(255,255,255),round=True,roundness=0.5,showline=False,tag="show")
Reset = System.ui.button(window,1355,35,60,30,color=(253, 76, 54),edge_thick=0,text="초기화",text_color=(255,255,255),round=True,roundness=0.4,showline=False,tag="Reset")

def show():
    pad1.reset()
    pad2.reset()
    pad3.reset()
    for n in range(max(votes)):
        n += 1

        for i, vote in enumerate(votes):
            if (vote >= n):
                exec(f"pad{i+1}.addone()")


        events = pygame.event.get()
        keyboard = gk.keyboard.get_input()

        mx, my = pygame.mouse.get_pos()

        System.display()
        System.event(events)

        pygame.display.update()

        System.clock.tick(30)

        time.sleep(0.3)

while True:
    btonmouse = False
    events = pygame.event.get()
    keyboard = gk.keyboard.get_input()

    mx, my = pygame.mouse.get_pos()

    System.display()
    System.event(events)
        
    pygame.display.update()

    System.clock.tick(30)