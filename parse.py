#!/usr/bin/python3
"""Durchsucht die lokale nodes.json auf alte Knoten mit einer Firmware aus 2016"""

import json
import argparse
import re

PARSER = argparse.ArgumentParser()
PARSER.add_argument("-j" "--json", metavar="Path", dest="json_path",
                    help="Path to the nodes.json file", required=True)
PARSER.add_argument("-s" "--search", metavar="search", dest="search",
                    help="pattern to search in firmware", required=True)
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
    except KeyError:
        print("fehler")

    table_data = [['Name', 'Kontakt', 'Firmware']]
    for node in nodes:
        try:
            if re.search(ARGS.search, node["nodeinfo"]["software"]["firmware"]["release"]) is not None:
                try:
                    owner = node["nodeinfo"]['owner']['contact']
                except TypeError:
                    owner = "N/A"
                table_data.append(
                    [node["nodeinfo"]['hostname'],
                     owner,
                     node["nodeinfo"]["software"]["firmware"]["release"]]
                )
        except KeyError:
            pass

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
                html_table = '<table border=1 id="nodestable" align="center">{}</table>'.format(html_content)
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
