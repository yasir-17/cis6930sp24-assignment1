import argparse
import spacy.cli
import spacy
import os
import glob
import pyap
from dateutil import parser
from dateparser.search import search_dates

# Download the spaCy large English model
spacy.cli.download("en_core_web_lg")

def replace_with_blocks(text, entities):
    for entity in entities:
        text = text.replace(entity, '\u2588' * len(entity))
    return text

def detect_information(text, nlp):
    # Process the text using the NER model
    doc = nlp(text)

    # Extract named entities (names, addresses, dates, and phone numbers)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    addresses = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
    phones = [ent.text for ent in doc.ents if ent.label_ == "PHONE"]
    
    # Extract only the string part of the tuple for dates
    dates = [date[0] if isinstance(date, tuple) else date for date in search_dates(text)]

    # Replace entities with Unicode full block characters
    text = replace_with_blocks(text, names + addresses + dates + phones)

    return text

def process_files(file_paths, output_dir, censor_flags):
    # Load the English NER model from spacy
    nlp = spacy.load("en_core_web_lg")

    for file_path in file_paths:
        print(f"\nProcessing file: {file_path}")
        try:
            # Read the text file
            with open(file_path, 'r') as file:
                text_content = file.read()

            # Detect information from the text and replace with full block characters
            modified_text = detect_information(text_content, nlp)

            # Generate the output file path with the .censored suffix
            output_file_name = os.path.basename(file_path) + ".censored"
            output_file_path = os.path.join(output_dir, output_file_name)
            
            # Create the output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)

            # Write the modified text to the output file
            with open(output_file_path, 'w') as output_file:
                output_file.write(modified_text)

            # Display the modified text
            print("Modified Text:", modified_text)
            print(f"Output file saved to: {output_file_path}")

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

if __name__ == "__main__":
    
    if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Censor files based on specified entity types.")
        parser.add_argument("--input", nargs="+", help="Glob patterns representing input files.")
        parser.add_argument("--output", required=True, help="Directory to store censored files.")
        parser.add_argument("--names", action="store_true", help="Censor names.")
        parser.add_argument("--dates", action="store_true", help="Censor dates.")
        parser.add_argument("--phones", action="store_true", help="Censor phone numbers.")
        parser.add_argument("--address", action="store_true", help="Censor addresses.")
        parser.add_argument("--stats", choices=["stdout", "stderr"], default="stderr", help="Output statistics to stdout or stderr.")
    
        args = parser.parse_args()

        if not args.input:
            print("Please provide input files using --input flag.")
        else:
            # Use the glob pattern to get a list of text files
            file_paths = []
            for file_glob in args.input:
                file_paths.extend(glob.glob(os.path.join('docs/Text_Files', file_glob)))

            if not file_paths:
                print("No matching files found with the specified patterns.")
            else:
                # Create the output directory if it doesn't exist
                os.makedirs(args.output, exist_ok=True)

                # Set up spaCy model
                nlp = spacy.load("en_core_web_lg")

                # Process the files based on the specified censor flags
                censor_flags = {"names": args.names, "dates": args.dates, "phones": args.phones, "address": args.address}
                selected_flags = [flag for flag, value in censor_flags.items() if value]

                if selected_flags:
                    process_files(file_paths, args.output, nlp)
                else:
                    print("Please specify at least one censor flag (--names, --dates, --phones, --address).")

