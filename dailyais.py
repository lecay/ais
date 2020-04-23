import datetime
import os
import json
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import patches
import numpy as np
import pandas as pd

filepath = './'
pypath = 'J:/影响天气/lecay/ais/'
now = datetime.datetime.now()
#now = datetime.datetime(2020,4,14,15,10,10)
if now.hour<7:
    dt = datetime.timedelta(hours=-9-now.hour)
elif now.hour>=15:
    dt = datetime.timedelta(hours=15-now.hour)
else:
    dt = datetime.timedelta(hours=7-now.hour)
intimenum = now+dt
intime = intimenum.strftime('%y%m%d%H')
if os.path.exists(filepath+intime+'.json'):
    with open(filepath+intime+'.json', 'rb') as f:
        data = json.load(f)
allrow = len(data.keys())+1

ysize = allrow*0.21+1.4    #图片长度
fig = plt.figure(figsize=(8,ysize),dpi=130)
ax1 = fig.add_axes([0.05,0.6/(ysize),0.9,allrow*0.21/(ysize)])
font = fm.FontProperties(fname=r"C:/Windows/Fonts/msyh.ttc")

fcx = 0.8     #机场四字码与中文名分割线x坐标
cnx = 1.7        #机场中文名与跑道号分割线x坐标
anx = 2.3        #跑道号与通告号分割线x坐标
stawx = 3.3    #通告号与通告展示区分割线x坐标
allx = 11.7    #x轴总长度

ax1.plot([cnx,cnx],[allrow,0],color='grey',linewidth=0.5)    #机场中文名与跑道号分割线
ax1.plot([anx,anx],[allrow,0],color='grey',linewidth=0.5)    #跑道号与通告号分割线
ax1.plot([stawx,stawx],[allrow,0],color='dimgray',linewidth=1)    #通告号与通告展示区分割线
for x in range(1,24):    #画纵向网格线
    #ax1.plot([stawx+x*0.35,stawx+x*0.35],[allrow,allrow-1],color='lightgrey',linewidth=0.5)
    for y in range(0,allrow+1):
        ax1.plot([stawx+x*0.35,stawx+x*0.35],[allrow-y,allrow-y-0.1],color='gray',linewidth=1)
for x in range(1,allrow):
    ax1.plot([0,stawx],[x,x],color='dimgray',linewidth=1)    #机场分割线
    ax1.plot([stawx,allx],[x,x],color='gray',linewidth=1)    #画横向网格线

# h小时，wy填充下边界y坐标，wid填色宽度，height填色高度，color填色颜色，rim是否画右边界，dheight填色下边高度，isstr是否填写字符，fstr字符内容
def drawwx(timestr,wy,wid,height,color,dheight=0,isstr=False,fstr='',alpha=1):
    if timestr[0:2]==intime[4:6]:    #当日
        h = int(timestr[2:])-int(intime[6:])
    else:                            #第二日
        h = int(timestr[2:])+24-int(intime[6:])
    if h!=0:
    	ax1.fill_between([stawx+(h-wid)*0.35,stawx+(h)*0.35],wy+height,wy+dheight,facecolor=color,alpha=alpha)
    if isstr:
        ax1.text(stawx+(h-wid)*0.35+wid*0.175,wy+0.4,fstr,ha='center', va='center',fontproperties=font, size=8)

ax1.text(cnx/2,allrow-0.59,'机场',ha='center', va='center',fontproperties=font, size=8)    #机场四字码
ax1.text((anx+cnx)/2,allrow-0.63,'跑道',ha='center', va='center',fontproperties=font, size=8)    #跑道号
ax1.text((stawx+anx)/2,allrow-0.6,'通告号',ha='center', va='center',fontproperties=font, size=8)    #通告号
ax1.text((allx+stawx)/2,allrow-0.6,'时间及详情',ha='center', va='center',fontproperties=font, size=8)    #通告内容
cnsta = pd.read_csv(pypath+'stationcn.txt', header=None, sep=r'[\s]+', engine='python', 
    names=['cnname'])
x = 0
estcolor = 'tomato'
infocolor = 'orange'
for sta in sorted(data,reverse=True):
    x = x+1
    wy = allrow-1-x
    stainfo = sta.split(); staid = stainfo[0]; rwy = ''.join(stainfo[1:-1])
    ax1.text(fcx/2,wy+0.4,staid,ha='center', va='center',fontproperties=font, size=8)    #机场四字码
    if staid in cnsta.index:
    	ax1.text((cnx+fcx)/2-0.05,wy+0.4,cnsta.loc[staid,'cnname'][:5],ha='center', va='center',fontproperties=font, size=8)    #机场四字码
    ax1.text((anx+cnx)/2,wy+0.4,rwy[3:],ha='center', va='center',fontproperties=font, size=8)    #跑道号
    ax1.text((stawx+anx)/2,wy+0.4,stainfo[-1],ha='center', va='center',fontproperties=font, size=8)    #通告号
    ax1.text(stawx+0.1,wy+0.4,data[sta]['notamContent'],ha='left', va='center',fontproperties=font, size=8)    #通告内容
    if data[sta]['style'] == 'EST':
        ax1.fill_between([anx,stawx],wy+1,wy,facecolor=estcolor,alpha=0.5)
    for ti,t in enumerate(data[sta]['time']):   #时间填充
        if ti>0:
        	drawwx(t,wy,1,1,infocolor,alpha=0.5)
        
ax1.set_xlim((0,allx))
ax1.set_ylim((0,allrow))
ax1.set_xticks([stawx-1.2,stawx-0.4]+list(np.arange(stawx,allx+0.35,0.35)))
#ax1.set_xticklabels(['时间']+np.arange(0,24,1),fontsize=8.5, fontproperties=font1)
secday = intimenum + datetime.timedelta(days=1)
#ax1.set_xticklabels(['北京时间 ->',intime[4:6]+'日']+list(np.arange(intimenum.hour,24,1))+[secday.strftime('%d')+'日']+list(np.arange(1,intimenum.hour+1,1)), fontproperties=font, size=8.5)
ax1.set_xticklabels(['北京时间 ->',intime[4:6]+'日']+list(np.arange(intimenum.hour,24,1))+['0']+list(np.arange(1,intimenum.hour+1,1)), fontproperties=font, size=8.5)
ax1.set_yticks([])
ax1.tick_params(axis='x', labeltop='True', length=0.01, pad=2)
ax1.annotate('*本图表每日07时和15时更新，仅供整体参考，动态及时信息请以情报处数据为准。', (0.05,0.25/ysize), xycoords='figure fraction', fontproperties=font, fontsize=8, color='dimgrey')
ax1.annotate('*标有预估时间(EST)的通告，请随时关注情报处动态更新。', (0.05,0.1/ysize), xycoords='figure fraction', fontproperties=font, fontsize=8, color='dimgrey')

ax2 = fig.add_axes([0.05,(ysize-0.6)/ysize,0.9,0.6/ysize])
lx = 9.5    #图例最左边x坐标
ax2.text(1,0.6,'重要情报通告（涉及气象标准变更）',ha='left', va='center',fontproperties=font, size=12)
ax2.text(1,0.2,'小飞象%d年%d月%d日%02d时制作'% (now.year,now.month,now.day,now.hour),ha='left', va='center',fontproperties=font, size=8, color='grey')
ax2.fill_between([lx,lx+0.5],0.7,0.5,facecolor=estcolor,alpha=0.5)     #est图例
ax2.text(lx+0.6,0.6,'预估时间(EST)', ha='left', va='center',fontproperties=font, size=7)
ax2.fill_between([lx,lx+0.5],0.4,0.2,facecolor=infocolor,alpha=0.5)    #影响时段图例
ax2.text(lx+0.6,0.3,'影响时段', ha='left', va='center',fontproperties=font, size=7)

ax2.set_xlim((0,allx))
ax2.set_ylim((0,1))
ax2.axis('off')

ax3 = fig.add_axes([0.04,(ysize-0.59)/ysize,0.08,0.53/ysize])
logoimg = plt.imread(pypath+'logo.png')
im = ax3.imshow(logoimg,interpolation='bilinear')
patch = patches.Circle((200, 200), radius=200, transform=ax3.transData)
im.set_clip_path(patch)
ax3.axis('off')

plt.savefig(filepath+intime+'.png')
#plt.savefig(filepath+infocolor+'.png')
plt.show()