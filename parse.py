#!/usr/bin/python3

import json

def main():
    with open('nodes.json') as file:
        data = json.load(file)
        nodes = data['nodes']
        for i in nodes:
            if data['nodes'][i]["nodeinfo"]["software"]["firmware"]["release"].startswith("2016"):
                try:
                    owner = data['nodes'][i]['nodeinfo']['owner']['contact']
                except KeyError:
                    owner = "N/A"
                print("%s: %s" % (data['nodes'][i]['nodeinfo']['hostname'], owner))


if __name__ == '__main__':
    main()
