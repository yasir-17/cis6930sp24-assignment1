import spacy
import os
import glob
import pyap
from dateutil import parser
from dateparser.search import search_dates

def replace_with_blocks(text, entities):
    for entity in entities:
        text = text.replace(entity, '\u2588' * len(entity))
    return text

def detect_information(text):
    # Load the English NER model from spacy
    nlp = spacy.load("en_core_web_md")

    # Process the text using the NER model
    doc = nlp(text)

    # Extract named entities (names, addresses, dates, and phone numbers)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    # name_nltk = extract_name(text)
    # addresses = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
    # dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    phones = [ent.text for ent in doc.ents if ent.label_ == "PHONE"]
    address = pyap.parse(text, country='US')
    dates = search_dates(text)

    # Replace entities with Unicode full block characters
    text = replace_with_blocks(text, names + addresses + dates + phones)

    return text


def process_files(file_paths):
    for file_path in file_paths:
        print(f"\nProcessing file: {file_path}")
        # Read the text file
        with open(file_path, 'r') as file:
            text_content = file.read()

        # Detect information from the text and replace with full block characters
        modified_text = detect_information(text_content)

        # Display the modified text
        print("Modified Text:", modified_text)


if __name__ == "__main__":
    # Use the glob pattern to get a list of text files
    file_pattern = os.path.join('../docs/Text_Files', "*.txt")
    file_paths = glob.glob(file_pattern)

    if file_paths:
        process_files(file_paths)
    else:
        print("No text files found in the specified folder.")
