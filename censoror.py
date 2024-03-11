import argparse
import spacy.cli
import spacy
import os
import glob
from google.cloud import language_v1
import re
import sys

# Download the spaCy large English model
spacy.cli.download("en_core_web_lg")

# Function to filter out 4-digit numbers from the list
def filter_out_4_digit_numbers(strings):
    return [s for s in strings if not re.match(r'^\d{4}$', s)]

def replace_with_blocks(text, entities):
    ent = filter_out_4_digit_numbers(entities)
    for replace_str in ent:
        full_block = "\u2588" * len(replace_str)  # Unicode full block character
        text = text.replace(replace_str, full_block)
    return text

def find_names(text_content):
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text_content)
    return [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

def find_addresses(text_content):
    client = language_v1.LanguageServiceClient.from_service_account_json('services.json')
    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(document=document, encoding_type=language_v1.EncodingType.UTF8)
    entities = response.entities
    return [entity.name for entity in entities if language_v1.Entity.Type(entity.type_).name == 'ADDRESS']

def find_dates(text_content):
    client = language_v1.LanguageServiceClient.from_service_account_json('services.json')
    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(document=document, encoding_type=language_v1.EncodingType.UTF8)
    entities = response.entities
    return [entity.name for entity in entities if language_v1.Entity.Type(entity.type_).name == 'DATE']

def find_phone_numbers(text_content):
    client = language_v1.LanguageServiceClient.from_service_account_json('services.json')
    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(document=document, encoding_type=language_v1.EncodingType.UTF8)
    entities = response.entities
    return [entity.name for entity in entities if language_v1.Entity.Type(entity.type_).name == 'PHONE_NUMBER']

def analyze_entities(text_content, censor_flags):
    entities = []
    count = []  # count variable for stats [name, address, phone no., date]

    if censor_flags["names"]:
        names = find_names(text_content)
        entities.extend(names)
        count.append(len(names))
    else:
        count.append(0)

    if censor_flags["address"]:
        addresses = find_addresses(text_content)
        entities.extend(addresses)
        count.append(len(addresses))
    else:
        count.append(0)

    if censor_flags["dates"]:
        dates = find_dates(text_content)
        entities.extend(dates)
        count.append(len(dates))
    else:
        count.append(0)

    if censor_flags["phones"]:
        phone_numbers = find_phone_numbers(text_content)
        entities.extend(phone_numbers)
        count.append(len(phone_numbers))
    else:
        count.append(0)

    return entities, count

def print_stats(count, stats_file=None):
    if stats_file:
        # Write stats to the specified file
        with open(stats_file, 'a') as f:
            f.write(f"Number of name censored - {count[0]}\n")
            f.write(f"Number of address censored - {count[1]}\n")
            f.write(f"Number of date censored - {count[2]}\n")
            f.write(f"Number of phone no. censored - {count[3]}\n")
    else:
        # Print stats to stderr or stdout
        print("Number of name censored - ", count[0], file=sys.stderr if args.stats == "stderr" else sys.stdout)
        print("Number of address censored - ", count[1], file=sys.stderr if args.stats == "stderr" else sys.stdout)
        print("Number of date censored - ", count[2], file=sys.stderr if args.stats == "stderr" else sys.stdout)
        print("Number of phone no. censored - ", count[3], file=sys.stderr if args.stats == "stderr" else sys.stdout)

def detect_information(text, censor_flags):
    # Extract entities based on the specified flags
    entities, count = analyze_entities(text, censor_flags)

    # Replace entities with Unicode full block characters
    text = replace_with_blocks(text, entities)

    # Print stats
    if args.stats == "stderr" or args.stats == "stdout":
        print_stats(count)
    else:
        print_stats(count, stats_file=args.stats)

    return text

def process_files(file_paths, output_dir, censor_flags):
    for file_path in file_paths:
        print(f"\nProcessing file: {file_path}")
        try:
            # Read the text file
            with open(file_path, 'r') as file:
                text_content = file.read()

            # Detect information from the text and replace with full block characters
            modified_text = detect_information(text_content, censor_flags)

            # Generate the output file path with the .censored suffix
            output_file_name = os.path.basename(file_path) + ".censored"
            output_file_path = os.path.join(output_dir, output_file_name)

            # Create the output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)

            # Write the modified text to the output file
            with open(output_file_path, 'w') as output_file:
                output_file.write(modified_text)

            print(f"Output file saved to: {output_file_path}")

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Censor files based on specified entity types.")
    parser.add_argument("--input", nargs="+", help="Glob patterns representing input files.")
    parser.add_argument("--output", required=True, help="Directory to store censored files.")
    parser.add_argument("--names", action="store_true", help="Censor names.")
    parser.add_argument("--dates", action="store_true", help="Censor dates.")
    parser.add_argument("--phones", action="store_true", help="Censor phone numbers.")
    parser.add_argument("--address", action="store_true", help="Censor addresses.")
    parser.add_argument("--stats", help="Output statistics to a file or stderr/stdout.")

    args = parser.parse_args()

    if not args.input:
        print("Please provide input files using --input flag.")
    else:
        # Use the glob pattern to get a list of text files
        file_paths = []
        for file_glob in args.input:
            file_paths.extend(glob.glob(os.path.join('./', file_glob)))

        if not file_paths:
            print("No matching files found with the specified patterns.")
        else:
            # Create the output directory if it doesn't exist
            os.makedirs(args.output, exist_ok=True)

            # Process the files based on the specified censor flags
            censor_flags = {"names": args.names, "dates": args.dates, "phones": args.phones, "address": args.address}
            selected_flags = [flag for flag, value in censor_flags.items() if value]

            if selected_flags:
                process_files(file_paths, args.output, censor_flags)
            else:
                print("Please specify at least one censor flag (--names, --dates, --phones, --address).")

