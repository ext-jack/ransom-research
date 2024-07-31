import requests
import re
import js2py


def main():

    regex = r"\(\(.*\)\)"
    session = requests.Session()
     
    ### impersonate Tor headers
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate, br', 'Upgrade-Insecure-Requests': '1', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site'})

    ### sending requests to act like Tor, favicon.ico is logged in the ransom page logic
    response = session.get("http://fpwwt67hm3mkt6hdavkfyqi42oo3vkaggvjj4kxdr2ivsbzyka5yr2qd.onion/")
    resp = session.get("http://fpwwt67hm3mkt6hdavkfyqi42oo3vkaggvjj4kxdr2ivsbzyka5yr2qd.onion/favicon.ico")

    matches = re.findall(regex, response.text)
    ### evaluate obfusctaed code via js2py
    calc = int(js2py.eval_js(matches[0])) + int(js2py.eval_js(matches[1]))
    cookies = response.cookies

    ### update calculations via cookies
    session.cookies.set('_k2', str(calc))
    session.cookies.set('_k1', cookies.get_dict()["_k1"])

    ### check its worked
    response = session.get("http://fpwwt67hm3mkt6hdavkfyqi42oo3vkaggvjj4kxdr2ivsbzyka5yr2qd.onion/")

    print(response.text)
    print(response.status_code)



if __name__ == "__main__":
    main()
