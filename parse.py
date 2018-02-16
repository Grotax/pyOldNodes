#!/usr/bin/python3
"""Durchsucht die lokale nodes.json auf alte Knoten mit einer Firmware aus 2016"""

import json
import argparse

PARSER = argparse.ArgumentParser()
PARSER.add_argument("-j" "--json", metavar="Path", dest="json_path",
                    help="Path to the nodes.json file", required=True)
PARSER.add_argument("--html", metavar="Path", dest="html_path", default=False,
                    help="Path where to store HTML output")

#ja pfad zur nodes.json erzwungen und
#optional html für eine noch zu implementierende html ausgabe

ARGS = PARSER.parse_args()


try:
    from terminaltables import AsciiTable
    USE_TABLE = True
except ImportError:
    USE_TABLE = False

def main():
    """the main function"""
    with open(ARGS.json_path) as file:
        data = json.load(file)
    try:
        nodes = data['nodes']
        node_info = True
    except KeyError:
        nodes = data
        node_info = False
    table_data = [['Name', 'Kontakt', 'Firmware']]
    if node_info:
        for i in nodes:
            if nodes[i]["nodeinfo"]["software"]["firmware"]["release"].startswith("2016"):
                try:
                    owner = nodes[i]["nodeinfo"]['owner']['contact']
                except KeyError:
                    owner = "N/A"
                table_data.append(
                    [nodes[i]["nodeinfo"]['hostname'],
                     owner,
                     nodes[i]["nodeinfo"]["software"]["firmware"]["release"]]
                    )
    else:
        for i in nodes:
            if nodes[i]["software"]["firmware"]["release"].startswith("2016"):
                try:
                    owner = nodes[i]['owner']['contact']
                except KeyError:
                    owner = "N/A"
                table_data.append(
                    [nodes[i]['hostname'],
                     owner,
                     nodes[i]["software"]["firmware"]["release"]]
                    )
    if USE_TABLE:
        table = AsciiTable(table_data)
        print(table.table)
        if ARGS.html_path:
            with open(ARGS.html_path, "w") as file:
                html_content = ""
                html_row = ""
                for row in table_data:
                    html_cell = ""
                    for cell in row:
                        html_cell += "<th>{}</th>".format(cell)
                    html_row = "<tr>{}</tr>".format(html_cell)
                    html_content += html_row
                html_table = '<table border=1 align="center">{}</table>'.format(html_content)
                file.write(html_table)
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
