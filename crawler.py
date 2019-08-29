# MyCurl
# By Judah Goff

import urllib.request
import sys


def is_http(url):
    return url[0:len("http://")] == "http://" or url[0:len("https://")] == "https://"


def curl():
    if len(sys.argv) > 0:
        # Remove the file name
        del sys.argv[0]
        if len(sys.argv) == 0:
            print("MyCurl: Supply a URL to retrieve")
            return

    if sys.argv[0] == '-I':
        # Only headers
        if len(sys.argv) > 1:
            if is_http(sys.argv[1]):
                print(urllib.request.urlopen(sys.argv[1]).info())
            else:
                print("MyCurl: Only http or https URLs can be requested")
        else:
            print("MyCurl: Supply a URL to retrieve")
    elif sys.argv[0] == '-i':
        # Header and body
        if len(sys.argv) > 1:
            if is_http(sys.argv[1]):
                request = urllib.request.urlopen(sys.argv[1])
                html = request.read()
                try:
                    html = str(html, encoding='utf-8')
                    print(request.info())
                    print(html)
                except Exception:
                    print("NON-TEXTUAL CONTENT")
            else:
                print("MyCurl: Only http or https URLs can be requested")
        else:
            print("MyCurl: Supply a URL to retrieve")
    else:
        # Just body
        if '-' in sys.argv[0]:
            print("MyCurl: Only -i and -I arguments are supported")
        else:
            if is_http(sys.argv[0]):
                html = urllib.request.urlopen(sys.argv[0]).read()
                try:
                    html = str(html, encoding='utf-8')
                    print(html)
                except Exception:
                    print("NON-TEXTUAL CONTENT")
            else:
                print("MyCurl: Only http or https URLs can be requested")


curl()
