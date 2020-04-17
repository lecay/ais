import datetime
import os
import json
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

filepath = './'
# now = datetime.datetime.now()
now = datetime.datetime(2020,4,14,15,10,10)
if now.hour<4:
    dt = datetime.timedelta(hours=-9-now.hour)
elif now.hour>=15:
    dt = datetime.timedelta(hours=15-now.hour)
else:
    dt = datetime.timedelta(hours=4-now.hour)
intimenum = now+dt
intime = intimenum.strftime('%y%m%d%H')
print(intime)
if os.path.exists(filepath+intime+'.json'):
    with open(filepath+intime+'.json', 'rb') as f:
        data = json.load(f)
allrow = len(data.keys())*2+1

ysize = allrow*0.2+1.4    #图片长度
fig = plt.figure(figsize=(8,ysize),dpi=130)
ax1 = fig.add_axes([0.05,0.6/(ysize),0.9,allrow*0.2/(ysize)])
font = fm.FontProperties(fname=r"C:/Windows/Fonts/msyh.ttc")

#fcx = 1.25      #机场四字码与中文名分割线x坐标
cnx = 1.4        #机场中文名与跑道号分割线x坐标
anx = 1.9        #跑道号与通告号分割线x坐标
stawx = 2.8    #通告号与通告展示区分割线x坐标
allx = 11.2    #x轴总长度

ax1.plot([cnx,cnx],[allrow,0],color='lightgrey',linewidth=0.5)    #机场中文名与跑道号分割线
ax1.plot([anx,anx],[allrow,0],color='lightgrey',linewidth=0.5)    #跑道号与通告号分割线
ax1.plot([stawx,stawx],[allrow,0],color='dimgray',linewidth=1)    #通告号与通告展示区分割线
# for x in range(1,24):
#     ax1.plot([stawx+x*0.35,stawx+x*0.35],[0,allrow],color='lightgrey',linewidth=0.5)    #画纵向网格线
for x in range(1,allrow):
    ax1.plot([0,allx],[x*2,x*2],color='dimgray',linewidth=1)    #机场分割线
    ax1.plot([stawx,allx],[x*2-1,x*2-1],color='lightgrey',linewidth=0.5)    #画横向网格线

# h小时，wy填充下边界y坐标，wid填色宽度，height填色高度，color填色颜色，rim是否画右边界，dheight填色下边高度，isstr是否填写字符，fstr字符内容
def drawwx(timestr,wy,wid,height,color,dheight=0,isstr=False,fstr='',alpha=1):
    if timestr[0:2]==intime[4:6]:
        h = int(timestr[2:])-int(intime[6:])
    else:
        h = int(timestr[2:])+24-int(intime[6:])
    ax1.fill_between([stawx+(h+1-wid)*0.35,stawx+(h+1)*0.35],wy+height,wy+dheight,facecolor=color,alpha=alpha)
    if isstr:
        ax1.text(stawx+(h+1-wid)*0.35+wid*0.175,wy+0.4,fstr,ha='center', va='center',fontproperties=font, size=8)

x = 0
for sta,detail in data.items():
    x = x+1
    wy = allrow-x
    stainfo = sta.split(); staid = stainfo[0]; rwy = ''.join(stainfo[1:-1])
    ax1.text(0.1,wy+0.4,staid,ha='left', va='center',fontproperties=font, size=8)    #机场四字码
    ax1.text((anx+cnx)/2,wy+0.4,rwy[3:],ha='center', va='center',fontproperties=font, size=8)    #跑道号
    ax1.text((stawx+anx)/2,wy+0.4,stainfo[-1],ha='center', va='center',fontproperties=font, size=8, color='dimgrey')    #通告号
    ax1.text(stawx+0.1,wy+0.4,detail['notamContent'],ha='left', va='center',fontproperties=font, size=8)    #通告内容
    if detail['style'] == 'EST':
        fillcolor = 'orange'
    else:
        fillcolor = 'tomato'
    for t in detail['time']:   #时间填充
        drawwx(t,wy,1,1,fillcolor,alpha=0.5)

ax1.set_xlim((0,allx))
ax1.set_ylim((0,allrow))
ax1.set_xticks([stawx-0.6]+list(np.arange(stawx+0.175,allx,0.35)))
#ax1.set_xticklabels(['时间']+np.arange(0,24,1),fontsize=8.5, fontproperties=font1)
ax1.set_xticklabels(['时间 ->']+list(np.arange(0,24,1)), fontproperties=font, size=8.5)
ax1.set_yticks([])
ax1.tick_params(axis='x', labeltop='True', length=0.01, pad=2)

plt.savefig(filepath+intime+'.png')
plt.show()