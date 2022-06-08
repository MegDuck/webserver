import grequests
import requests

running = True
actions = []

print("type \"help\" for commands")


def main():
    while running:
        action = input("action: ").split(" ")
        if action[0] == "download":
            grequests.map([grequests.post("http://127.0.0.1:5000/archive", json={"url": action[1]})])
        if action[0] == "status":
            print(requests.get("http://127.0.0.1:5000/archive/" + action[1]).text)


main()
