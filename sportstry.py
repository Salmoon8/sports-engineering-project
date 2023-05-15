from vpython import *
import numpy as np
running=False
scene = canvas()
def Run(b):
  global running
  running= not running
  if running:
    b.text="Pause"
  else:
    b.text="Run"

runbutton=button(text="Run",pos=scene.title_anchor,bind=Run)

def reset(b):
    global scene, running , ground , ball ,line ,theta,v0,labeldist,velocitys,anglelabel,labelv,angles,distances,at_goal_height,maxheight
    running=False
    runbutton.text="Run"    
    scene.delete()
    scene = canvas()
    scene.select() 
    #these two lines make the ground 
    ground=box(pos=vector(0,0,0), size=vector(10,.2,50), color=color.green)
    line=box(pos=vector(0,.1,0), size=vector(.1,.2,50), color=color.white)
    #the soccer ball
    ball=sphere(pos=vector(0,.45,24.5), radius=.4, color=color.white, make_trail=True)
    #calculate the mass of the soccer ball
    ball.m=(rhosoccer*4*pi*ball.radius**3)/3
    labeldist.text="ditsance to goal:"+'50'
    distances.value=50
    #launch speed in m/s - YOU CAN CHANGE THIS
    v0=15
    velocitys.value=15
    labelv.text='firing velocity: 15'
    #launch angle - YOU CAN CHANGE THIS
    theta = 22*pi/180
    angles.value=22
    anglelabel.text='firing angle: 22'
    #initial velocity vector
    ball.v=v0*vector(0,sin(theta),-cos(theta))
    #initial momentum vector
    ball.p=ball.m*ball.v
    at_goal_height.text=('Max Height: ')
    maxheight.text=('At Goal Height :')


reset=button(text="reset",pos=scene.title_anchor,bind=reset)

#gravitational field vector
g=vector(0,-9.8,0)

#these two lines make the ground 
ground=box(pos=vector(0,0,0), size=vector(10,.2,50), color=color.green)
line=box(pos=vector(0,0.1,0), size=vector(.1,.2,50), color=color.white)

#the soccer ball
ball=sphere(pos=vector(0,.55,24.5), radius=.5, color=color.white, make_trail=True)
#density of soccer ball
rhosoccer=74*1.02 #74 times the density of air
#calculate the mass of the soccer ball
ball.m=(rhosoccer*4*pi*ball.radius**3)/3

#launch speed in m/s - YOU CAN CHANGE THIS
v0=15
#launch angle - YOU CAN CHANGE THIS
theta = 22*pi/180

#initial velocity vector
ball.v=v0*vector(0,sin(theta),-cos(theta))
#initial momentum vector
ball.p=ball.m*ball.v


t=0
dt=0.001

scene.append_to_title('\n\n')

def ball_kick_calculations(distance_from_goal, angle, i_speed):
    # calculating time untill ball reach max height
    t1 = (i_speed * np.sin(angle*(np.pi/180))) / 9.81
    # calculating max height
    max_height = (i_speed * t1 * np.sin(angle*(np.pi/180))) - (0.5 * 9.81 * t1**2)
    # distance travelled untill  max height
    d1 = i_speed * t1 * np.cos(angle*(np.pi/180))
    # distance from max height to goal line
    d2 = distance_from_goal - d1
    # time from max height to goal line
    t2 = d2 / (i_speed * np.cos(angle*(np.pi/180)))
    # height at goal line
    at_goal_height = max_height - (0.5 * 9.81 * t2**2)
    
    if at_goal_height < 0:
        at_goal_height = np.float64(0)
    
    return max_height.round(2), at_goal_height.round(2)

def distance(s):
    global labeldist ,ball
    labeldist.text="ditsance to goal:"+str((s.value+25))
    ball.make_trail=False
    ball.pos=vector(0,0.5,s.value)

    
    
distances=slider(pos=scene.title_anchor
,min=-25,max=25,step=1, bind=distance,value=25 )
labeldist=wtext(pos=scene.title_anchor)
labeldist.text="ditsance to goal:50"
scene.append_to_title('\n\n')


def velocity(s):
   global v0,labelv,ball
   labelv.text="firing velocity:"+str(s.value)
   v0=int(s.value)
   ball.v=v0*vector(0,sin(theta),-cos(theta))
   ball.p=ball.m*ball.v
    
velocitys=slider(pos=scene.title_anchor
,min=0,max=100,step=1, bind=velocity ,value=15)
labelv=wtext(pos=scene.title_anchor)
labelv.text='firing velocity: 15'
#labelv.pos=scene.title_anchor
scene.append_to_title('\n\n')

def angle(s):
   global theta ,anglelabel,ball
   anglelabel.text="firing angle: "+str(s.value)
   theta=int(s.value)*pi/180
   ball.v=v0*vector(0,sin(theta),-cos(theta))
   ball.p=ball.m*ball.v
    
angles=slider( pos=scene.title_anchor
,min=0,max=180,step=1,bind=angle,value=22 )
anglelabel=wtext(pos=scene.title_anchor)
anglelabel.text='firing angle: 22'
#anglelabel.pos=scene.title_anchor

scene.append_to_title('\n\n')


maxheight=wtext(pos=scene.title_anchor)
maxheight.text=('Max Height: ')
scene.append_to_title('\n\n')
at_goal_height=wtext(pos=scene.title_anchor)
at_goal_height.text=('At Goal Height :')









while True:
    if running:
        ball.make_trail=True
        while ( ball.pos.y>=0 )and running:
            rate(300)
            
        #calculate the force
            F=ball.m*g
            #update the momentum
            ball.p=ball.p+F*dt
            #update the position
            ball.pos=ball.pos+ball.p*dt/ball.m
            #update the time
            t=t+dt
        print(distances.value+25,angles.value,v0)
        maxh,at_goal_h=ball_kick_calculations(distances.value+25,angles.value,v0)
        print(maxh,at_goal_h)
        maxheight.text=(('Max Height:  ' + str(maxh)))
        at_goal_height.text=(('At Goal Height :'+str(at_goal_h)))



