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
For testing, I am testing to see that each function is perfoming as expected using mocking

1) test_filter_out_4_digit_numbers - This test ensures the correct functioning of the filter_out_4_digit_numbers function, which aims to filter out 4-digit numbers from a list of strings. The test provides a scenario with a list containing a mix of words and 4-digit numbers, asserting that the function correctly identifies and removes the numerical elements, leaving only the words in the final result.

2) test_replace_with_blocks - The replace_with_blocks function is subjected to testing in this case, where it is expected to replace specified entities within a given text with Unicode block characters. The test supplies a sample text and a list of entities, evaluating whether the function accurately obscures sensitive information by replacing the identified entities with block characters.

3) test_find_names - This test focuses on the find_names function, which utilizes spaCy entity recognition to extract names from a provided text. The scenario involves a greeting containing a person's full name, and the test verifies that the function correctly identifies and returns the name as a list within the expected result.

4) test_find_addresses - The find_addresses function undergoes scrutiny in this test, checking its ability to identify and extract addresses from a given text using the Google Cloud Language API. The test supplies a text with an embedded address and asserts that the function accurately recognizes and returns the address within the expected result.

5) test_find_dates - This test assesses the capability of the find_dates function, which is designed to recognize and extract date entities from a provided text. The scenario presents a sentence mentioning a specific date, and the test confirms that the function correctly identifies and returns the date information as part of the expected result.

6) test_find_phone_numbers - The functionality of the find_phone_numbers function is tested in this scenario, focusing on its accuracy in identifying and extracting phone numbers using the Google Cloud Language API. The test supplies a text with a phone number and checks that the function successfully recognizes and returns the phone number within the expected result.


## Bugs and Assumptions
1) The bug is that the function is not detecting name for all the cases since the spacy librray does not have 100% accuracy.
2) I have test the code for usa phone number, but there is a chance it won't work for non usa phone number as other countries have phone no. in different format and some countries even have phone no. which are less than or more than 10 digits long.
3) The assumption is that that while running the code we are censoring only the entity which is mentioned in the running command and we are not censoring any more entitites than the one specified in the assignment(name, address, date, phone no.).
