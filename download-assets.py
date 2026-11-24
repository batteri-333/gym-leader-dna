import base64, concurrent.futures, hashlib, json, pathlib, urllib.request, time
root=pathlib.Path(__file__).parent

def download(item):
    target=root/item['path'];target.parent.mkdir(parents=True,exist_ok=True)
    for attempt in range(3):
        try:
            req=urllib.request.Request(item['url'],headers={'User-Agent':'GymLeaderDNA/1.0'})
            payload=base64.b64decode(item['inline_base64']) if item.get('inline_base64') else urllib.request.urlopen(req,timeout=60).read()
            if hashlib.sha256(payload).hexdigest()!=item['sha256']:
                raise ValueError('Image checksum mismatch: '+item['path'])
            target.write_bytes(payload)
            return
        except Exception:
            if attempt==2:raise
            time.sleep(2)

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    list(pool.map(download,json.loads((root/'deployment-assets.json').read_text())))
print('Verified and downloaded all official images.')
