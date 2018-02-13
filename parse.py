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
        try:
            nodes = data['nodes']
        except KeyError:
            nodes = json.load(file)
        table_data = [['Name', 'Kontakt', 'Firmware']]
        for i in nodes:
            if nodes[i]["nodeinfo"]["software"]["firmware"]["release"].startswith("2016"):
                try:
                    owner = nodes[i]['nodeinfo']['owner']['contact']
                except KeyError:
                    owner = "N/A"
                table_data.append(
                    [nodes[i]['nodeinfo']['hostname'],
                     owner,
                     nodes[i]["nodeinfo"]["software"]["firmware"]["release"]]
                    )
        if USE_TABLE:
            table = AsciiTable(table_data)
            print(table.table)
        else:
            maxlengths = [max([len(row[col]) for row in table_data]) for col in range(3)]
            for row in table_data:
                print("{} | {} | {}".format(
                    row[0].ljust(maxlengths[0]),
                    row[1].ljust(maxlengths[1]),
                    row[2].ljust(maxlengths[2])))
            print("für bessere Tabellen: pip install terminaltables")


if __name__ == '__main__':
    main()
