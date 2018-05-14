import requests
import sys
from threading import Thread, Lock
from Queue import Queue
from random import choice, randint
sys.path.append("config")


def readproxyfile(proxyfile):
    with open(proxyfile, "r") as raw_proxies:
        proxies = raw_proxies.read().split("\n")
        proxies_list = []
        for individual_proxies in proxies:
            if individual_proxies.strip() != "":
                p_splitted = individual_proxies.split(":")
                if len(p_splitted) == 2:
                    proxies_list.append("http://" + individual_proxies)
                if len(p_splitted) == 4:
                    # ip0:port1:user2:pass3
                    # -> username:password@ip:port
                    p_formatted = "http://{}:{}@{}:{}".format(p_splitted[2], p_splitted[3], p_splitted[0], p_splitted[1])
                    proxies_list.append(p_formatted)
        proxies_list.append(None)
    return proxies_list


def load_accounts():
    with open("config/Accounts.txt", "r+") as CONTENTS:
        CONTENTS = CONTENTS.readlines()
    all_accs = {}
    for acc in CONTENTS:
        acc = acc.strip()
        if ":" in acc:
            user = acc.split(":")
            email = user[0]
            pw = user[1]
            if not email in all_accs:
                all_accs[email] = pw
    return all_accs.items()  # acc tuple


def remove_account(account):
    global GLOBAL_LOCKS
    if account in GLOBAL_LOCKS["accounts"]:
        with GLOBAL_LOCKS["account"]:
            GLOBAL_LOCKS["accounts"].remove(account)


def unlock_p(proxy):
    global GLOBAL_LOCKS
    if proxy in GLOBAL_LOCKS["pll"]:
        with GLOBAL_LOCKS["proxy"]:
            GLOBAL_LOCKS["pll"].remove(proxy)


def log_in():
    global GLOBAL_LOCKS
    while GLOBAL_LOCKS["queue"].qsize() > 0:
        GLOBAL_LOCKS["queue"].get()
        proxy = choice(GLOBAL_LOCKS["proxies"])
        if not proxy in GLOBAL_LOCKS["pll"]:
            with GLOBAL_LOCKS["proxy"]:
                GLOBAL_LOCKS["pll"].append(proxy)
            try:
                acc = choice(GLOBAL_LOCKS["accounts"])
                with GLOBAL_LOCKS["account"]:
                    GLOBAL_LOCKS["accounts"].remove(acc)
            except:
                pass
            with requests.Session() as s:
                resp = s.post("https://kith.com/account/recover", headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Host": "kith.com",
                    "Origin": "https://kith.com",
                    "Referer": "https://kith.com/account/login",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36"
                }, data={
                    "form_type": "recover_customer_password",
                    "email": acc[0],
                }, proxies={"https": proxy}, timeout=30)  # false for captcha
            if resp.status_code == 200:  # proxy not banned
                if resp.url == "https://kith.com/account/login":  # acc exists
                    print("Verified: {}".format(str(acc[0])))
                    with open("config/Verified.txt", "a+") as verified_file:
                        verified_file.write("{}:{}\n".format(acc[0], acc[1]))
                else:  # acc doesn't exist
                    print("Unverified: {}".format(str(acc[0])))
                    with open("config/Unverified.txt", "a+") as unverified_file:
                        unverified_file.write("{}:{}\n".format(acc[0], acc[1]))
                unlock_p(proxy)
            else:
                unlock_p(proxy)
                with GLOBAL_LOCKS["q_l"]:
                    GLOBAL_LOCKS["queue"].put(1)
        else:
            with GLOBAL_LOCKS["q_l"]:
                GLOBAL_LOCKS["queue"].put(1)


def wrapper():
    global GLOBAL_LOCKS
    for _ in range(len(GLOBAL_LOCKS["accounts"])):
        with GLOBAL_LOCKS["q_l"]:
            GLOBAL_LOCKS["queue"].put(1)
    for _ in range(10):
        Thread(target=log_in).start()


if __name__ == "__main__":
    GLOBAL_LOCKS = {"pen": Lock(), "proxy": Lock(), "account": Lock(), "accounts": load_accounts(), "queue": Queue(), "q_l": Lock(), "proxies": readproxyfile("config/Proxies.txt"), "pll": []}
    wrapper()
