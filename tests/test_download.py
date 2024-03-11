import unittest
from unittest.mock import patch, MagicMock
from google.cloud import language_v1
from censoror import filter_out_4_digit_numbers, replace_with_blocks, find_names, find_addresses, find_dates, find_phone_numbers, analyze_entities

class TestCensoringFunctions(unittest.TestCase):

    def test_filter_out_4_digit_numbers(self):
        test_strings = ['1234', 'word', '5678', 'anotherword', '9012']
        expected_result = ['word', 'anotherword']
        self.assertEqual(filter_out_4_digit_numbers(test_strings), expected_result)

    def test_replace_with_blocks(self):
        text = "Hello John Doe"
        entities = ["John", "Doe"]
        expected_result = "Hello \u2588\u2588\u2588\u2588 \u2588\u2588\u2588"
        self.assertEqual(replace_with_blocks(text, entities), expected_result)

    @patch('censoror.spacy.load')
    def test_find_names(self, mock_spacy_load):
        mock_nlp = mock_spacy_load.return_value
        mock_doc = mock_nlp.return_value
        mock_doc.ents = [MockEntity(text='John Doe', label_='PERSON')]
        text_content = "Hello John Doe"
        expected_result = ['John Doe']
        self.assertEqual(find_names(text_content), expected_result)

    @patch('censoror.language_v1.LanguageServiceClient.from_service_account_json')
    def test_find_addresses(self, mock_client):
        mock_client.return_value.analyze_entities.return_value = MockResponse(entity_type='LOCATION', entity_text=['1400 Smith Street Houston, TX  77002-7311'])
        text_content = "Send this to 1400 Smith Street Houston, TX  77002-7311"
        expected_result = ['1400 Smith Street Houston, TX  77002-7311']
        self.assertEqual(find_addresses(text_content), expected_result)

    @patch('censoror.language_v1.LanguageServiceClient.from_service_account_json')
    def test_find_dates(self, mock_client):
        mock_client.return_value.analyze_entities.return_value = MockResponse(entity_type='DATE', entity_text=['January 1, 2020'])
        text_content = "The event is on January 1, 2020"
        expected_result = ['January 1, 2020']
        self.assertEqual(find_dates(text_content), expected_result)

    @patch('censoror.language_v1.LanguageServiceClient.from_service_account_json')
    def test_find_phone_numbers(self, mock_client):
        mock_client.return_value.analyze_entities.return_value = MockResponse(entity_type='PHONE_NUMBER', entity_text=['555-1234-980'])
        text_content = "Call me at 555-1234-980"
        expected_result = ['555-1234-980']
        self.assertEqual(find_phone_numbers(text_content), expected_result)

# Helper mock class for testing spaCy entities
class MockEntity:
    def __init__(self, text, label_):
        self.text = text
        self.label_ = label_

# Helper mock class for simulating Google Cloud Language API responses
class MockResponse:
    def __init__(self, entity_type, entity_text):
        self.entities = [MockGoogleEntity(name=text, type_=entity_type) for text in entity_text]

class MockGoogleEntity:
    def __init__(self, name, type_):
        self.name = name
        self.type_ = {
            'LOCATION': language_v1.Entity.Type.LOCATION,
            'DATE': language_v1.Entity.Type.DATE,
            'PHONE_NUMBER': language_v1.Entity.Type.PHONE_NUMBER,
            # Add more types as needed
        }.get(type_, language_v1.Entity.Type.UNKNOWN)

if __name__ == '__main__':
    unittest.main()
