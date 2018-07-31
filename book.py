"""
book.py

entry point to start the program.

follows the pattern :
`python book.py bookparse -f $FILEPATH`
    - this spits out a `out.json` file with structured data

there are other options as well to perform fuzzy testing

- regenerate option helps reconstruct the book
    `python book.py regenerate -f $FILEPATH`

- compare option compares the reconstructed book and original book with a crude shingling method.
    `python book.py regenerate -f $FILEPATH`

there are helpers setup to facilitate cli navigation.
`python book.py --help`

the function `book_parse_task` masks the parsing section
"""

# inbuilt imports
import argparse
import logging
import time
import os

# custom imports
from FileReader import FileReader
from FileWriter import FileWriter
from Parser import Parser
from Regenerator import Regenerator
from Compare import Compare


# parsing function
def book_parse_task():
    logging.info("starting book parse task")
    file_reader_obj = FileReader(file_path=args.filepath)
    file_data = file_reader_obj.get_content()
    parser_obj = Parser(file_data=file_data)
    data = parser_obj.get_json()
    file_writer_obj = FileWriter(file_path="out.json")
    file_writer_obj.write_content(data=data)


# regenerate function
def book_regenerate_task():
    logging.info("starting book regenerate task")
    file_reader_obj = FileReader(file_path=args.filepath)
    file_data = file_reader_obj.get_content()
    parser_obj = Parser(file_data=file_data)
    data = parser_obj.get_json()
    file_writer_obj = FileWriter(file_path="out.json")
    file_writer_obj.write_content(data=data)
    regenerator_obj = Regenerator(json_file_path="out.json")
    regenerator_obj.write_to_file("regenerate.txt")


# regenerate function
def book_compare_task():
    logging.info("starting book compare task")
    file_reader_obj = FileReader(file_path=args.filepath)
    file_data = file_reader_obj.get_content()
    parser_obj = Parser(file_data=file_data)
    data = parser_obj.get_json()
    file_writer_obj = FileWriter(file_path="out.json")
    file_writer_obj.write_content(data=data)
    regenerator_obj = Regenerator(json_file_path="out.json")
    regenerator_obj.write_to_file("regenerate.txt")
    compare_obj = Compare(actual_file_data=parser_obj.file_data, regenerate_file_data=regenerator_obj.process_data())
    percent_match = compare_obj.compare_data()
    print("Accuracy Score {}%".format(percent_match))


# main
if __name__ == '__main__':

    fmt = '%(asctime)s %(levelname)s %(process)d %(filename)s %(funcName)s %(message)s'
    logging.basicConfig(
        filename=os.path.join("log-data.txt"),
        filemode='w',
        format=fmt,
        level=logging.DEBUG
    )

    logging.info("*************EXECUTION START TIME {}*************".format(time.strftime('%Y%m%d%H%M%S')))

    # parser setup
    parser = argparse.ArgumentParser(description='INFO : book parser')
    subparsers = parser.add_subparsers()

    # args -> parse book
    book_parse = subparsers.add_parser('bookparse', description='used to parse the book into a json struct')
    book_parse.add_argument('-f', '--filepath', required=True, help='book file path')
    book_parse.set_defaults(func=book_parse_task)

    # args -> regenerate
    regenerate = subparsers.add_parser('regenerate', description='used to regenerate the book from json struct, this produces almost similar book structure')
    regenerate.add_argument('-f', '--filepath', required=True, help='book file path')
    regenerate.set_defaults(func=book_regenerate_task)

    # args -> compare
    compare = subparsers.add_parser('compare', description='used to compre the book & its regenerate to show % similarity, score > 80% is deemed accurate')
    compare.add_argument('-f', '--filepath', required=True, help='book file path')
    compare.set_defaults(func=book_compare_task)

    # parser close
    args = parser.parse_args()
    args.func()
