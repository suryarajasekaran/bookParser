import json
import logging

class Regenerator(object):

    def __init__(self, json_file_path):
        self.json_file_path = json_file_path

    def get_data(self):
        json_file = open(self.json_file_path)
        json_str = json_file.read()
        json_data = json.loads(json_str)
        return json_data

    # organizes the data back to a file from json
    def process_data(self):
        data = self.get_data()
        total_books = len(data["books"])
        logging.info("regenerating the book, requesting books data")
        out_str = ""
        for book_num in xrange(0, total_books):
            total_chapters = len(data["books"][str(book_num)]["chapters"])
            logging.info("regenerating the chapter, requesting chapters data")
            book = ""
            for chapter_num in xrange(0, total_chapters):
                total_paragraphs = len(data["books"][str(book_num)]["chapters"][str(chapter_num)]["paragraphs"])
                logging.info("regenerating the paragraph, requesting paragraphs data")
                chapter = ""
                for paragraph_num in xrange(0, total_paragraphs):
                    total_sentences = len(data["books"][str(book_num)]["chapters"][str(chapter_num)]["paragraphs"][str(paragraph_num)]["sentences"])
                    logging.info("regenerating the sentence, requesting sentences data")
                    paragraph = ""
                    for sentences_num in xrange(0, total_sentences):
                        total_words = len(data["books"][str(book_num)]["chapters"][str(chapter_num)]["paragraphs"][str(paragraph_num)]["sentences"][str(sentences_num)]["words"])
                        sentence = ""
                        logging.info("regenerating the word, requesting words data")
                        for words_num in xrange(0, total_words):
                            sentence = sentence + data["books"][str(book_num)]["chapters"][str(chapter_num)]["paragraphs"][str(paragraph_num)]["sentences"][str(sentences_num)]["words"][str(words_num)] + " "
                        paragraph = paragraph + sentence + "."
                    chapter = chapter + paragraph + "\r\n\r\n"
                book = book + "\r\n\r\n\r\n\r\n\r\n\r\n" + str(data["books"][str(book_num)]["chapters"][str(chapter_num)]["chapter_name"]) + "\r\n" + chapter
            out_str = out_str + "\r\n\r\n\r\n\r\n\r\n\r\n" + str(data["books"][str(book_num)]["book_name"]) + book
        return out_str

    def write_to_file(self, file_path):
        file = open(file_path, "w")
        file.write(self.process_data().encode("utf-8"))
        file.close()
        return True

