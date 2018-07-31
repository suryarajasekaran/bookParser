import re
import logging


# HEART of the whol program, any changes here should be well tested !!
class RuleEngine(object):

    def __init__(self, file_data):
        self.file_data = file_data
        pass

    # this will extract books
    def get_books(self):
        out_list = []
        pattern_1 = r"\r\n\r\n\r\n\r\n\r\nBOOK [0-9A-Za-z: -]+\r\n\r\n\r\n\r\n\r\n"
        re_compile_1 = re.compile(pattern=pattern_1)
        pattern_2 = r"\r\n\r\n\r\n\r\n\r\n[0-9A-Za-z]* EPILOGUE[:0-9A-Za-z -]*\r\n\r\n\r\n\r\n\r\n"
        re_compile_2 = re.compile(pattern=pattern_2)
        results = re_compile_1.findall(self.file_data)
        for result in results:
            out_list.append(result.replace("\r\n\r\n\r\n\r\n\r\n",""))
        results = re_compile_2.findall(self.file_data)
        for result in results:
            out_list.append(result.replace("\r\n\r\n\r\n\r\n\r\n", ""))
        logging.debug("books data {}".format(out_list))
        return out_list

    # this will extract chapters in a book
    def get_chapters(self, book, next_book=None):
        if next_book is None:
            chapters_data = self.file_data.split("\r\n\r\n\r\n\r\n\r\n"+book+"\r\n\r\n\r\n\r\n\r\n")[1].split("\r\n\r\n\r\n\r\n\r\nBOOK")[0]
        else:
            chapters_data = self.file_data.split("\r\n\r\n\r\n\r\n\r\n"+book+"\r\n\r\n\r\n\r\n\r\n")[1].split("\r\n\r\n\r\n\r\n\r\n"+next_book)[0]
        out_list = []
        pattern = r"CHAPTER [0-9A-Za-z]*\r\n"
        re_compile = re.compile(pattern=pattern)
        results = re_compile.findall(chapters_data)
        for result in results:
            out_list.append(result.replace("\r\n", ""))
        logging.debug("book {} chapters data {}".format(book, out_list))
        return out_list, chapters_data

    # this will extract paragraphs in a chapter
    def get_paragraphs(self, chapter, chapters_data):
        paragraphs_data = chapters_data.split(chapter+"\r\n")[1].split("\r\n\r\n\r\n\r\n\r\nCHAPTER")[0]
        out_list = []
        results = paragraphs_data.split("\r\n\r\n")
        for result in results:
            out_list.append(result)
        logging.debug("chapter {} paragraphs data {}".format(chapter, out_list))
        return out_list

    # this will extract sentences in a paragraph
    def get_sentences(self, paragraph):
        out_list = []
        results = paragraph.split(".")
        for result in results:
            out_list.append(result)
        logging.debug("paragraph {} sentences data {}".format(paragraph, out_list))
        return out_list

    # this will extract words in a sentence
    def get_words(self, sentence):
        out_list = []
        results = sentence.split(" ")
        for result in results:
            out_list.append(result)
        logging.debug("sentence {} words data {}".format(sentence, out_list))
        return out_list
