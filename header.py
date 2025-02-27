#!/usr/bin/env python3

from sys import path
from os.path import expanduser
path.append(expanduser("~/modules/python/"))

#SVG generation wrapper - www.github.com/JoeyShepard
import svg

from math import sqrt
from random import random

DEBUG_FONT=False

IMG_WIDTH=1280
IMG_HEIGHT=200

COLOR_BG="#000040"
COLOR_FONT="orange"
COLOR_TRACE="#203080"

FONT_SIZE=60
TITLE_SIZE=48
FONT_WEIGHT=200
FONT_NAME="Ubuntu"
FONT_FAMILY=FONT_NAME+", sans-serif"

NAME_X=int(IMG_WIDTH/2)
NAME_Y=int((IMG_HEIGHT)*0.3)

TITLE_X=NAME_X
TITLE_Y=int((IMG_HEIGHT)*0.7)

TRACE_WIDTH=3

TRACE_ON=3      #seconds
TRACE_FADE=1    #seconds
TRACE_SPEED=150

CYCLE_TIME=8    #seconds - time of full animation cycle

VIA_RADIUS=6
VIA_STROKE=4
VIA_FADE=0.2

traces=[
    #Left side
    #=========
    #Top left corner
    {"origin":(0,0),"segments":((35,35),),"via":(1,1),"delay":0},
    #Left side then up
    {"origin":(0,110),"segments":((75,0),(40,-40),(0,-25)),"via":(0,-1),"delay":1},
    #Parallel traces from left
    {"origin":(0,140),"segments":((120,0),),"via":(1,0),"delay":2},
    {"origin":(0,170),"segments":((120,0),),"via":(1,0),"delay":2},
    #Straight up from bottom
    {"origin":(175,IMG_HEIGHT),"segments":((0,-75),),"via":(0,-1),"delay":3},
    #Bottom then diagonal right
    {"origin":(220,IMG_HEIGHT),"segments":((0,-50),(75,-75),(0,-30)),"via":(0,-1),"delay":4},
    #Loop with no via
    {"origin":(260,IMG_HEIGHT),"segments":((0,-40),(25,-25),(40,0),(25,25),(0,40)),"via":(0,1.2),"delay":5},
    #Two connected from top
    {"origin":(200,0),"segments":((0,40),(-20,20)),"via":(-1,1),"delay":6},
    {"origin":(200,0),"segments":((0,40),(20,20)),"via":(1,1),"delay":6},
    #Two on bottom on right of loop
    {"origin":(390,IMG_HEIGHT),"segments":((0,-115),(-40,-40)),"via":(-1,-1),"delay":7},
    {"origin":(390,IMG_HEIGHT),"segments":((0,-90),(-40,0)),"via":(-1,0),"delay":7},
    #Three from top to left of name
    {"origin":(430,0),"segments":((0,40),(-20,0)),"via":(-1,0),"delay":8},
    {"origin":(430,0),"segments":((0,110),(20,0)),"via":(1,0),"delay":8},
    {"origin":(430,0),"segments":((0,170),(20,0)),"via":(1,0),"delay":8},

    #Right side
    #==========
    #Top left corner
    {"origin":(IMG_WIDTH,IMG_HEIGHT),"segments":((-35,-35),),"via":(-1,-1),"delay":9},
    #Left side then up
    {"origin":(IMG_WIDTH,IMG_HEIGHT-110),"segments":((-75,0),(-40,40),(0,25)),"via":(0,1),"delay":10},
    #Parallel traces from left
    {"origin":(IMG_WIDTH,IMG_HEIGHT-140),"segments":((-120,0),),"via":(-1,0),"delay":11},
    {"origin":(IMG_WIDTH,IMG_HEIGHT-170),"segments":((-120,0),),"via":(-1,0),"delay":11},
    #Straight up from bottom
    {"origin":(IMG_WIDTH-175,0),"segments":((0,75),),"via":(0,1),"delay":12},
    #Bottom then diagonal right
    {"origin":(IMG_WIDTH-220,0),"segments":((0,50),(-75,75),(0,30)),"via":(0,1),"delay":13},
    #Loop with no via
    {"origin":(IMG_WIDTH-260,0),"segments":((0,40),(-25,25),(-40,0),(-25,-25),(0,-40)),"via":(0,-1.2),"delay":14},
    #Two connected from top
    {"origin":(IMG_WIDTH-200,IMG_HEIGHT),"segments":((0,-40),(20,-20)),"via":(1,-1),"delay":15},
    {"origin":(IMG_WIDTH-200,IMG_HEIGHT),"segments":((0,-40),(-20,-20)),"via":(-1,-1),"delay":15},
    #Two on bottom on right of loop
    {"origin":(IMG_WIDTH-390,0),"segments":((0,162),(40,0)),"via":(1,0),"delay":16},
    {"origin":(IMG_WIDTH-390,0),"segments":((0,90),(40,0)),"via":(1,0),"delay":16},
    #Two to right of name
    {"origin":(IMG_WIDTH-430,0),"segments":((0,110),(-20,0)),"via":(-1,0),"delay":17},
    {"origin":(IMG_WIDTH-430,0),"segments":((0,150),(-20,15)),"via":(-1,1),"delay":17},
    ]

#Assign random delays for beginning of trace animation
delays=[]
for trace in traces:
    delays+=[random()]

for i,trace in enumerate(traces):
    trace["delay"]=delays[trace["delay"]]

f=svg.writer("output/header.svg",width=IMG_WIDTH,height=IMG_HEIGHT)

#Background
f.rect(width=IMG_WIDTH,height=IMG_HEIGHT,fill=COLOR_BG);

#Traces
ID=0
for trace in traces:
    ID+=1
    length=0
    x,y=trace["origin"]
    f.write(f'<path d="M{x},{y} ')    
    for seg_width,seg_height in trace["segments"]:
        f.write(f"l {seg_width},{seg_height} ")
        length+=sqrt(abs(seg_width)**2+abs(seg_height)**2)
        x+=seg_width
        y+=seg_height
    f.write(f'" ')
    f.write(f'stroke="{COLOR_BG}" fill="none" stroke-width="{TRACE_WIDTH}" stroke-dasharray="{length}" stroke-dashoffset="0">\n')

    #Animation steps for each trace
    delay=trace["delay"]
    trace_dur=length/TRACE_SPEED
    f.write(f'\t<animate id="trace{ID}" attributeName="stroke-dashoffset" begin="{delay}s;trace{ID}.begin+{CYCLE_TIME}" dur="{trace_dur}s" values="{length};0" />\n')
    f.write(f'\t<set attributeName="stroke" begin="trace{ID}.begin;via{ID}.end" to="{COLOR_TRACE}" />\n')
    f.write(f'\t<animate attributeName="stroke" begin="via{ID}.begin" dur="{VIA_FADE}s" values="white;{COLOR_TRACE}" />\n')
    f.write(f'\t<animate id="fade{ID}" attributeName="stroke" begin="via{ID}.end+{TRACE_ON}s" dur="{TRACE_FADE}s" values="{COLOR_TRACE};{COLOR_BG}" />\n')
    f.write(f'\t<set attributeName="stroke" begin="fade{ID}.end" to="{COLOR_BG}" />\n')
    f.write('</path>\n')

    #Via at end of trace
    vx,vy=trace["via"]
    x+=vx*VIA_RADIUS
    y+=vy*VIA_RADIUS
    f.write(f'<circle cx="{x}" cy="{y}" r="{VIA_RADIUS}" fill="none" stroke-width="{VIA_STROKE}" stroke="{COLOR_BG}">\n')

    #Animation steps for via
    f.write(f'\t<animate id="via{ID}" attributeName="stroke" begin="trace{ID}.end" dur="{VIA_FADE}s" values="white;{COLOR_TRACE}" />\n')
    f.write(f'\t<set attributeName="stroke" begin="via{ID}.end" to="{COLOR_TRACE}" />\n')
    f.write(f'\t<animate attributeName="stroke" begin="via{ID}.end+{TRACE_ON}s" dur="{TRACE_FADE}s" values="{COLOR_TRACE};{COLOR_BG}" />\n')
    f.write(f'\t<set attributeName="stroke" begin="fade{ID}.end" to="{COLOR_BG}" />\n')
    f.write('</circle>\n')


if DEBUG_FONT:
    #Text - only used here to compare to prerendered text inserted below
    f.text("Joey Shepard",NAME_X,NAME_Y,
        fill=COLOR_FONT,
        font_size=FONT_SIZE,
        font_weight=FONT_WEIGHT,
        font=FONT_FAMILY,
        baseline="middle",
        anchor="middle")

    f.text("Programmer",TITLE_X,TITLE_Y,
        fill=COLOR_FONT,
        font_size=TITLE_SIZE,
        font_weight=FONT_WEIGHT,
        font=FONT_FAMILY,
        baseline="middle",
        anchor="middle")

#Insert text converted to path in Inkscape
with open("prerendered/name.svg","rt") as p:
    f.write(p.read())
with open("prerendered/programmer.svg","rt") as p:
    f.write(p.read())


#Done generating file
f.close()
