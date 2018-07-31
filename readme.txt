# USAGE

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Question

Large body of semi structured text: Parser and fuzzing
Download a plain text (UTF-8) version of Tolstoy’s War and Peace (http://www.gutenberg.org/ebooks/2600)

Using Python, perform the following:
	• Write a robust scanner and parser that:
		• Separates the body of the book's text from the header and footer of the text file
		• Detects books, chapters and paragraphs.
		• Structures the text into the following nested format

Book number and year
	-> Chapter index (within a given book)
		-> Paragraph index (within a given chapter)
			-> Sentence index (within a given paragraph)
				-> Sentence text
				-> Word index (within a given sentence)
					-> Word (only alphanumeric)

2. Choose an appropriate container to store the extracted dataset and efficiently serialize into a file (think working with thousands or millions of copies of books like this in a distributed fashion)
    DONE

3. Assume this book is following a format template. Come up with tests/rules to enforce the format template you see in this book (imagine you’d be processing a data stream of data like this book, wanting to verify it’s the same format)
    DONE

4. Write or at least outline fuzzing methods to validate these tests
    DONE

Additional notes: Assume you might not see the whole book at once, instead you might get partial data. Handle this assumption with concise logging.
    DONE

The result you should return back to us should be:
	• Documented python code (including all parser, serialization and analysis functionality). Provide a command line interface including usage help with an option to feed a text file to parse and output path to serialize the structured dataset.
	    DONE

2. A representative PDF slide deck (think presenting it to a group of Apple engineers) with a summary of your methodology and a walk-through of the functionality. Feel free to include your thought process in the deck.
    DONE

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Project Setup

- `cd book`
- `source venv.sh`
    this will setup the python virtual environment, and the code can run there.
    this was tested with py2.7
- `python book.py --help`
    this shows the command-line-interface for how to run or execute this program

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Project Structure

    |_ book.py (Entry point, main function)
    |_ FileReader.py (helper to read data from file)
    |_ FileWriter.py (helper to write data to file)
    |_ RuleEngine.py (Rules defined to extract sections from the file, this is the HEART of the program)
    |_ Parser.py (Uses the rule engine and then parses and structures the data) **can be paralellized easily if decided to perform distributed computing
    |_ Regenerator.py (Regenerates the book file from the json data)
    |_ Compare.py (Compares regenerated file with actual file for accuracy match, uses the standard shingling approach to compare documents)
    |_ readme.txt (READ ME for the project)

    generated files
    |_ log-data.txt (generated log file)
    |_ out.json (generated parsed json file)
    |_ regenerate.txt (this is the regenerated file from the json)

    sample files
    |_ sample.regenerate.txt (shows how reconstruction would look)
    |_ sample.out.json (shows how out json would look)



------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Output Structure ("out.json")

I have decided to use the `json` structure for parsing as follows :
{
    "books": {
        "0": {
            "book_name": "$BOOK_NAME",
            "chapters": {
                "0": {
                    "chapter_name": "$CHAPTER_NAME",
                    "paragraphs": {
                        "0": {
                            "sentences": {
                                "0": {
                                    "words": {
                                        "0": "$WORD",
                                        "1": "$WORD"
                                    }
                                },
                                "1": {
                                    "words": {
                                        "0": "$WORD",
                                        "1": "$WORD"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}


This above example is more of a schema setting I have in place. This supports multiple books with multiple chapters with multiple paragraphs with multiple sentences with multiple words.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## How to run the program

- PARSE
    `python book.py parse -f book.txt`

    this command basically creates the above "out.json" structure.

- REGENERATE
    `python book.py regenerate -f book.txt`

    this command creates regenerate.txt, which is a reconstructed book file from the "out.json"
    the intention to do this is to see if there are any differences with the actual file as i was developing this
    this helped me to perform tests quickly, but its still manual - had to move to a more automated testing approach - which is where I decided to use shingling approach in the next step

- COMPARE
    `python book.py compare -f book.txt`

    this command does a parse->regenerate->compare all in one go.
    this outputs a response like this : "Accuracy Score 99.7790111599%"
    this accuracy gets computed by using the generated file and comparing that with actual file using shingling approach for document comparison

- Logging
    log data is generated in the same folder as "log-data.txt"

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

