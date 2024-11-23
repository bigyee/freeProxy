import requests
import yaml
from starlette.responses import PlainTextResponse


def writeYaml(proxyies):
    filepath = "~/.config/clash.meta/freeNode/freeproxy.yaml"
    proxy = {"proxies": proxyies}
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(proxy, stream=f, indent=2, sort_keys=False, allow_unicode=True)
def genYaml(proxyies):
    proxy = {"proxies": proxyies}
    return yaml.dump(proxy, indent=2, sort_keys=False, allow_unicode=True)

def json2yaml(jdata, filepath: str):
    addr = jdata["server"].split(':')
    port = addr[1].split(',')
    hy2 = {"name": filepath, "type": "hysteria2", "server": addr[0], "port": int(port),
           "password": jdata["auth"],
           "sni": jdata["tls"]["sni"], "skip-cert-verify": jdata["tls"]['insecure']
           }
    return hy2

def getConfig(url, f):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "sec-ch-ua": ''''"Chromium";v = "118", "Google Chrome";v = "118", "Not=A?Brand";v = "99"''',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "macOS"
    }
    rsp = requests.get(url, headers=headers)
    if rsp.ok and rsp.status_code == 200:
        return json2yaml(rsp.json(), f)
    else:
        print("rsp: "+str(rsp.content))
        print(rsp.status_code)
        print(rsp.headers)
        return None

from fastapi import FastAPI

app = FastAPI()

@app.get("/freeproxy/hy2", response_class=PlainTextResponse)
async def free_proxy():
    urls = { "tw": "https://www.githubip.xyz/Alvin9999/pac2/master/hysteria2/config.json",
             "us": "https://www.gitlabip.xyz/Alvin9999/pac2/master/hysteria2/1/config.json"}
    proxy = []
    for k,v in urls.items():
        p = getConfig(v, k)
        if p is not None:
            proxy.append(p)

    return genYaml(proxy)
