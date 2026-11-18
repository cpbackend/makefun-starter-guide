import sys, json, time, urllib.request, urllib.parse, base64
sys.path.insert(0,'D:/Tools/gig-monitor')
import scrape_prizes as sp
import websocket

url='https://github.com/cpbackend/makefun-starter-guide'
tab=sp.cdp('PUT','/json/new?'+urllib.parse.quote(url,safe=':/?=&'))
tid=tab['id']
ws=websocket.create_connection(f'ws://127.0.0.1:9222/devtools/page/{tid}',timeout=90)
i=[0]
def cmd(m,p=None,t=60):
    i[0]+=1; ws.send(json.dumps({'id':i[0],'method':m,'params':p or {}}))
    import time as _t; end=_t.time()+t
    while True:
        r=json.loads(ws.recv())
        if r.get('id')==i[0]: return r
        if _t.time()>end: raise TimeoutError(m)

cmd('Page.enable'); cmd('Runtime.enable')
cmd('Emulation.setDeviceMetricsOverride',{'width':1400,'height':1600,'deviceScaleFactor':1,'mobile':False})
cmd('Page.navigate',{'url':url})
# 等 load 事件
for _ in range(40):
    r=cmd('Runtime.evaluate',{'expression':'document.readyState','returnByValue':True})
    if r['result']['result'].get('value')=='complete': break
    time.sleep(1)
time.sleep(6)
# 滚到顶部并确认 README 文本存在
cmd('Runtime.evaluate',{'expression':'window.scrollTo(0,0)','returnByValue':True})
chk=cmd('Runtime.evaluate',{'expression':"document.body.innerText.length",'returnByValue':True})
print('body text len:',chk['result']['result'].get('value'))
has=cmd('Runtime.evaluate',{'expression':"document.body.innerText.includes('make.fun actually is')",'returnByValue':True})
print('README visible:',has['result']['result'].get('value'))
time.sleep(2)
r=cmd('Page.captureScreenshot',{'format':'png','captureBeyondViewport':False})
data=r['result']['data']
raw=base64.b64decode(data)
open('screenshot.png','wb').write(raw)
print('bytes:',len(raw))
ws.close()
