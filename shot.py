import sys, json, time, urllib.request, urllib.parse, base64
sys.path.insert(0,'D:/Tools/gig-monitor')
import scrape_prizes as sp
import websocket

url='https://github.com/cpbackend/makefun-starter-guide'
tab=sp.cdp('PUT','/json/new?'+urllib.parse.quote(url,safe=':/?=&'))
tid=tab['id']
print('tab',tid)
time.sleep(12)
ws=websocket.create_connection(f'ws://127.0.0.1:9222/devtools/page/{tid}',timeout=60)
i=[0]
def cmd(m,p=None):
    i[0]+=1; ws.send(json.dumps({'id':i[0],'method':m,'params':p or {}}))
    while True:
        r=json.loads(ws.recv())
        if r.get('id')==i[0]: return r
cmd('Runtime.enable')
cmd('Page.enable')
# 视口设大一点，把 README 露出来
cmd('Emulation.setDeviceMetricsOverride',{'width':1280,'height':1400,'deviceScaleFactor':1,'mobile':False})
time.sleep(2)
t=cmd('Runtime.evaluate',{'expression':'document.title','returnByValue':True})
print('title:',t['result']['result'].get('value'))
r=cmd('Page.captureScreenshot',{'format':'png'})
data=r['result']['data']
open('D:/Tools/repro/makefun/guide/screenshot.png','wb').write(base64.b64decode(data))
print('screenshot bytes:',len(data))
ws.close()
try: sp.cdp('GET',f'/json/close/{tid}')
except Exception: pass
