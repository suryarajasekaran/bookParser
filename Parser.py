import logging

from RuleEngine import RuleEngine


class Parser(object):

    def __init__(self, file_data):
        self.file_data = file_data
        self.pre_process_data()
        self.rule_engine_obj = RuleEngine(file_data=self.file_data)

    def pre_process_data(self):
        logging.info("pre processing file data to remove headers & footers")
        self.file_data = "\r\n\r\n\r\n\r\n\r\n"+self.file_data.split("\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n")[1].split("\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n")[0]

    # top level requestor
    def get_json(self):
        logging.info("request to generate full json struct")
        return self.get_structure_books()

    # book data requestor => can be parallelized
    def get_structure_books(self):
        logging.info("request to generate books json struct")
        out_json = {}
        books = self.rule_engine_obj.get_books()
        for location, book in enumerate(books):
            if location == len(books) - 1:
                out_json[location] = self.get_structure_chapters(book=book)
            else:
                out_json[location] = self.get_structure_chapters(book=book, next_book=books[location+1])
        return {"books": out_json}

    # chapter data requestor => can be parallelized
    def get_structure_chapters(self, book, next_book=None):
        logging.info("request to generate chapters json struct for book {}".format(book))
        out_json = {}
        chapters, chapters_data = self.rule_engine_obj.get_chapters(book=book, next_book=next_book)
        for location, chapter in enumerate(chapters):
            out_json[location] = self.get_structure_paragraphs(chapter=chapter, chapters_data=chapters_data)
        return {"chapters": out_json, "book_name": book}

    # paragraph data requestor => can be parallelized
    def get_structure_paragraphs(self, chapter, chapters_data):
        logging.info("request to generate paragraphs json struct for chapter {}".format(chapter))
        out_json = {}
        paragraphs = self.rule_engine_obj.get_paragraphs(chapter=chapter, chapters_data=chapters_data)
        for location, paragraph in enumerate(paragraphs):
            out_json[location] = self.get_structure_sentences(paragraph=paragraph)
        return {"paragraphs": out_json, "chapter_name": chapter}

    # sentence data requestor => can be parallelized
    def get_structure_sentences(self, paragraph):
        logging.info("request to generate sentence json struct for paragraph {}".format(paragraph))
        out_json = {}
        sentences = self.rule_engine_obj.get_sentences(paragraph=paragraph)
        for location, sentence in enumerate(sentences):
            out_json[location] = self.get_structure_words(sentence=sentence)
        return {"sentences": out_json}

    # word data requestor => can be parallelized
    def get_structure_words(self, sentence):
        logging.info("request to generate word json struct for sentence {}".format(sentence))
        out_json = {}
        words = self.rule_engine_obj.get_words(sentence=sentence)
        for location, word in enumerate(words):
            out_json[location] = word
        return {"words": out_json}
