# cis6930sp24 -- Assignment1 -- Template

Name: Yasir Khan

# Assignment Description (in your own words)
In this project, the task is to censor sensitive information like name, address, date, phone no. from the text files.

# How to install
pipenv install

## How to run
For running the project use the following command
1) pipenv run python censoror.py --input './docs/Text_Files/*.txt' --names --dates --phones --address --output 'docs/output' --stats stderr

For running the testcase use the following command
1) pipenv run python -m pytest

![](https://github.com/yasir-17/cis6930sp24-assignment1/blob/main/Recording%202024-03-10%20202646.gif)


## Functions
1)  main() - This function defines the main entry point for the code. It parses command line arguments and then do the processing of files based on user-provided inputs. It ensures proper input and output handling, facilitating the overall execution of the code.

2) filter_out_4_digit_numbers(list) - This function takes a list of strings as a parameter and filters out any four-digit numbers from the list. Its purpose is to exclude specific numeric entities with four digits from further processing.

3) replace_with_blocks(text, entities) - Given a text string and a list of entities, this function replaces the specified entities in the text with Unicode full block characters. It serves the purpose of visually censoring sensitive information by substituting identified entities with block characters.

4) analyze_entities(text_content) - This function takes text as input. This function utilizes spaCy and Google Cloud Natural Language API to extract named entities like addresses, dates, and phone numbers. It provides valuable information about the types and counts of entities present in the text.

5) print_stats(count) - This function takes a list of entity counts as input. This function prints statistics on the number of censored names, addresses, dates, and phone numbers.

6) detect_information(text) - This function takes a text string, combines entity extraction, and censorship processes. It replaces identified entities in the text with Unicode full block characters and prints statistics on the counts of censored entities, providing a comprehensive integration of entity processing.

7) process_files(file_paths, output_dir) - Given a list of file paths and an output directory, this function iterates through the files, reads, processes, and writes modified versions based on specified censor flags. It serves as the main pipeline orchestrator, handling the processing of multiple files.

## Testings
For testing, I am testing to see that each function is perfoming as expected

1) test_analyze_entities_name - This test case aims to validate the analyze_entities function's ability to accurately extract and return named entities (PERSON) from the input text. The test creates a mock spaCy NLP object, configures it with mock entities representing names ("John Doe" and "Jane Smith"), and ensures that the function correctly identifies and returns these entities when analyzing the provided text containing these names.

2) test_empty_input - This test verifies the behavior of the analyze_entities function when given with an empty input text. By calling the function with an empty string, the test ensures that the function gracefully handles this edge case, returning an empty list as expected.

3) test_no_entities - The purpose of this test is to confirm that the analyze_entities function appropriately handles input text without relevant entities. Using a sample text devoid of entities ("The quick brown fox..."), the test ensures that the function correctly returns an empty list, indicating the absence of identified entities.

4) test_entitites - This test case aims to validate the analyze_entities function's correct identification and extraction of relevant entities (DATE, ADDRESS, PHONE_NUMBER) from the input text. The test involves analyzing a text containing a mix of relevant entities, such as a date, an address, and a phone number. By comparing the identified entities to the expected output, the test ensures the function's accuracy in extracting the specified types of information.


## Bugs and Assumptions
1) The bug is that the function is not detecting name for all the cases since the spacy librray does not have 100% accuracy.
2) I have test the code for usa phone number, but there is a chance it won't work for non usa phone number as other countries have phone no. in different format and some countries even have phone no. which are less than or more than 10 digits long.
3) The assumption is that that while running the code we are censoring all the name, address, phone no, and date and we are not censoring any more entitites than the one specified above.
