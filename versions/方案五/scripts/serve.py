"""Project-owned static preview with video and Framer CMS byte-range support."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from io import BytesIO
import re, argparse

ROOT = Path(__file__).resolve().parents[1]

class Handler(SimpleHTTPRequestHandler):
    def guess_type(self,path):
        if path.endswith(('.js','.mjs')): return 'text/javascript'
        return super().guess_type(path)
    def send_head(self):
        path=Path(self.translate_path(self.path))
        if not path.is_file():return super().send_head()
        size=path.stat().st_size
        ranges=parse_qs(urlsplit(self.path).query).get('range') if path.suffix=='.framercms' else None
        if ranges:
            data=[]
            for segment in ranges[0].split(','):
                m=re.fullmatch(r'(\d+)-(\d+)',segment)
                if not m or int(m[1])>int(m[2]) or int(m[2])>=size:self.send_error(416);return None
                with path.open('rb') as f:f.seek(int(m[1]));data.append(f.read(int(m[2])-int(m[1])+1))
            body=b''.join(data);self.remaining=len(body);self.send_response(200);self.send_header('Content-Length',str(len(body)));self.end_headers();return BytesIO(body)
        start,end=0,size-1
        header=self.headers.get('Range')
        if header:
            m=re.fullmatch(r'bytes=(\d*)-(\d*)',header)
            if not m or not any(m.groups()):self.send_error(416);return None
            if m[1]:start=int(m[1]);end=min(int(m[2]),size-1) if m[2] else size-1
            else:start=max(0,size-int(m[2]))
            if start>end or start>=size:self.send_error(416);return None
        f=path.open('rb');f.seek(start);self.remaining=end-start+1
        self.send_response(206 if header else 200)
        self.send_header('Content-Type',self.guess_type(str(path)))
        self.send_header('Content-Length',str(self.remaining));self.send_header('Accept-Ranges','bytes');self.send_header('Cache-Control','no-cache')
        if header:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
        self.end_headers();return f
    def copyfile(self,source,output):
        remaining=getattr(self,'remaining',None)
        if remaining is None:return super().copyfile(source,output)
        try:
            while remaining:
                data=source.read(min(65536,remaining))
                if not data:break
                output.write(data);remaining-=len(data)
        except (BrokenPipeError,ConnectionResetError):pass
    def log_message(self,fmt,*args):
        if len(args)>1 and str(args[1]) not in ('200','206','304'):super().log_message(fmt,*args)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=3005);args=p.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',args.port),partial(Handler,directory=str(ROOT)))
    print(f'Influx scheme 5: http://127.0.0.1:{args.port}/',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:server.server_close()
