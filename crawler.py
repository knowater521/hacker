import requests

def request(url):
    try:
        return requests.get("http://"+url, timeout=1)
    except Exception as e: 
        if e == requests.exceptions.ConnectionError:
            pass
        elif e == requests.exceptions.InvalidURL:
            print(f"[-] Invalid URL:{url}")
    
target_url = "scut.edu.cn"

with open("wordlist.txt",'r') as wordlist:
    for i, line in enumerate(wordlist):
        print(f"\r\r\rThe {i} domain:" , end="")
        test_url = line.strip() + '.' + target_url
        response = request(test_url)
        if response:
            print("[+] Discover submain --> "+test_url)
