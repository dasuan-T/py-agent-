import requests
from urllib.parse import urlparse

from Demos.win32ts_logoff_disconnected import session


def download_image(session,url):
    print("发生请求:",url)
    resp=session.get(url)#发送网络请求
    parse_result=urlparse(resp.url)#返回一个 ParseResult 对象，里面包含 scheme、netloc、path、query 等字段。
    filename = parse_result.path.split("/")[-1]#取出路径字符串，转化为列表，拿到2026-04-06-12-55-34-576x434.jpg
    with open(f"./图片/{filename}", "wb") as f:
        f.write(resp.content)
        #content拿到二进制字节
        #text自动按编码（比如 utf-8）把二进制转成文本,拿到字符串
    print("下载完成：",url)
if __name__ == '__main__':
    url_list = [
        'https://pixnio.com/free-images/2026/04/06/2026-04-06-12-55-34-576x434.jpg',
        'https://pixnio.com/free-images/2026/08/07/2026-08-07-12-18-08-576x324.jpg',
        'https://pixnio.com/free-images/2026/08/21/2026-08-21-09-16-43-576x434.jpg'
    ]
    session=requests.Session()#管理连接池
    for item in url_list:
        download_image(session,item)
