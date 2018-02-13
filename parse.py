#!/usr/bin/python3
"""Durchsucht die lokale nodes.json auf alte Knoten mit einer Firmware aus 2016"""

import json
try:
    from terminaltables import AsciiTable
    USE_TABLE = True
except ImportError:
    USE_TABLE = False

def main():
    """the main function"""
    with open('nodes.json') as file:
        data = json.load(file)
        nodes = data['nodes']
        table_data = [['Name', 'Kontakt', 'Firmware']]
        for i in nodes:
            if data['nodes'][i]["nodeinfo"]["software"]["firmware"]["release"].startswith("2016"):
                try:
                    owner = data['nodes'][i]['nodeinfo']['owner']['contact']
                except KeyError:
                    owner = "N/A"
                table_data.append(
                    [data['nodes'][i]['nodeinfo']['hostname'],
                     owner,
                     data['nodes'][i]["nodeinfo"]["software"]["firmware"]["release"]]
                    )
        if USE_TABLE:
            table = AsciiTable(table_data)
            print(table.table)
        else:
            for i in table_data:
                print(i)
            print("für bessere Tabellen: pip install terminaltables")


if __name__ == '__main__':
    main()
