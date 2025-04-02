import os
from datetime import datetime
import re
from task_4 import fix_misspelling
from task_4 import text_normalize
import csv
import string
import json

# File to store the records
FILE_NAME = 'news_feed.txt'
DEFAULT_INPUT_FILE = 'input_records.txt'
DEFAULT_INPUT_JSON = 'input_json.json'


class Record:
    """Base class for all records."""
    # Class-level variable to accumulate text from all records
    accumulated_text = ""

    def __init__(self, text):
        self.text = text
        self.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # The current date and time when the record is created

    def publish(self):
        """Publishes the record and updates accumulated text."""
        # Add the current record's text to the accumulated text
        Record.accumulated_text += " " + self.text

    @classmethod
    def finalize_and_update_csvs(cls):
        """Finalize the accumulated text and generate word and letter count CSVs."""
        cls.generate_word_count_csv(cls.accumulated_text)
        cls.generate_letter_count_csv(cls.accumulated_text)

    @staticmethod
    def generate_word_count_csv(text, file_path='word_count.csv'):
        """Generate CSV with word counts."""

        words = text.lower().split()
        word_count = {}

        for word in words:
            word = word.strip(string.punctuation)
            if word:
                word_count[word] = word_count.get(word, 0) + 1

        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Word', 'Count'])
            for word, count in word_count.items():
                writer.writerow([word, count])

    @staticmethod
    def generate_letter_count_csv(text, file_path='letter_count.csv'):
        """Generate CSV with letter counts, uppercase counts, and percentage of uppercase."""

        letter_count = {letter: 0 for letter in string.ascii_lowercase}
        uppercase_count = {letter: 0 for letter in string.ascii_uppercase}

        total_letters = 0
        for char in text:
            if char.isalpha():
                total_letters += 1
                lowercase_char = char.lower()
                letter_count[lowercase_char] += 1
                if char.isupper():
                    uppercase_count[char] += 1

        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Letter', 'Count All', 'Count Uppercase', 'Percentage Uppercase'])
            for letter in string.ascii_lowercase:
                count_all = letter_count[letter]
                count_uppercase = uppercase_count[letter.upper()]
                percentage = (count_uppercase / count_all * 100) if count_all > 0 else 0
                writer.writerow([letter, count_all, count_uppercase, f'{percentage:.2f}%'])

    def _write_to_file(self, record):
        with open(FILE_NAME, 'a') as file:
            file.write(record)  # Append the record to the file


class News(Record):
    """Class for News records."""
    def __init__(self, text, city):
        super().__init__(text)
        self.city = city  # The city where the news is related to

    def publish(self):
        """Override publish method to include city information."""
        record = f"News\nDate: {self.date}\nCity: {self.city}\n{self.text}\n\n"
        self._write_to_file(record)  # Write the record to the file
        super().publish()  # Accumulate the text in the Record class
        return record  # Return the record for reporting


class PrivateAd(Record):
    """Class for Private Ad records."""
    def __init__(self, text, expiration_date_str):
        super().__init__(text)
        self.expiration_date_str = expiration_date_str  # Store the date as-is before validation
        self.expiration_date_str = self.validate_date(expiration_date_str)  # Validate and format date
        if not self.expiration_date_str:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")  # Raise an error if the date is invalid
        self.days_left = self.calculate_days_left()  # Calculate days left until expiration

    @staticmethod
    def validate_date(date_str):
        """Checks the date format and returns a valid formatted date string or None if incorrect."""
        date_str = date_str.replace("/", "-")  # Replace slashes with dashes to handle user input errors

        # Validate the final formatted date
        try:
            datetime.strptime(date_str, '%Y-%m-%d')  # Check if the format is correct (YYYY-MM-DD)
            return date_str  # Return formatted date if it's valid
        except ValueError:
            return None  # Return None for invalid input

    def calculate_days_left(self):
        """Calculates the number of days until the expiration date."""
        expiration_date = datetime.strptime(self.expiration_date_str, '%Y-%m-%d')
        today = datetime.now()  # Get the current date
        return max((expiration_date - today).days, 0)  # Ensure the value is not negative

    def publish(self):
        """Publishes the Private Ad record."""
        record = f"Private Ad\nDate: {self.date} | Expiration: {self.expiration_date_str} | {self.days_left} days left\n{self.text}\n\n"
        self._write_to_file(record)  # Write the record to the file
        super().publish()  # Accumulate the text in the Record class
        return record  # Return the record for reporting


class Comment(Record):
    """Class for unique records."""
    def __init__(self, nickname, text):
        super().__init__(text)
        self.nickname = nickname  # The nickname of the commenter
        self.words_num = self.words_count()  # Calculate the number of words in the comment

    def words_count(self):
        """Counts the number of words in the comment, excluding punctuation."""
        if isinstance(self.text, str):
            # Remove punctuation and split the text into words
            cleaned_text = re.sub(r'[^\w\s]', '', self.text)  # Remove all non-word characters except spaces
            words = cleaned_text.split()  # Split the cleaned text into words
            return len(words)  # Return the number of words
        else:
            return 0  # Return 0 if the text is not a string

    def publish(self):
        """Publish Comment record."""
        record = f"Nickname: {self.nickname}\nDate: {self.date}\n{self.text}\nWords count: {self.words_num}\n\n"
        self._write_to_file(record)  # Write the record to the file
        super().publish()  # Accumulate the text in the Record class
        return record  # Return the record for reporting


class FileReader:
    """Class to read records from a text file and process them."""
    def __init__(self, file_path=DEFAULT_INPUT_FILE):
        self.file_path = file_path

    def process_file(self):
        if not os.path.exists(self.file_path):
            print(f"File '{self.file_path}' does not exist.")
            return

        with open(self.file_path, 'r') as file:
            data = file.read().strip().split('---')

        for record_data in data:
            record_lines = record_data.strip().split('\n')
            if not record_lines:
                continue
            record_type = record_lines[0].strip()
            if record_type == 'News':
                text = record_lines[1].split(':', 1)[1].strip()
                city = record_lines[2].split(':', 1)[1].strip()
                record = News(text_normalize(text), text_normalize(city))
            elif record_type == 'Private Ad':
                text = record_lines[1].split(':', 1)[1].strip()
                expiration_date_str = record_lines[2].split(':', 1)[1].strip()
                record = PrivateAd(text_normalize(text), expiration_date_str)
            elif record_type == 'Comment':
                nickname = record_lines[1].split(':', 1)[1].strip()
                text = record_lines[2].split(':', 1)[1].strip()
                text = fix_misspelling(text)
                record = Comment(text_normalize(nickname), text_normalize(text))
            else:
                print(f"Unknown record type: {record_type}")
                continue

            record.publish()
            print(f"Processed record: {record_type}")

        # Remove file after successful processing
        os.remove(self.file_path)
        print(f"File '{self.file_path}' processed and removed.")


class JsonReader:
    """Class to read records from a json file and process them."""
    def __init__(self, file_path=DEFAULT_INPUT_JSON):
        self.file_path = file_path

    def process_json(self):
        if not os.path.exists(self.file_path):
            print(f"File '{self.file_path}' does not exist.")
            return

        with open(self.file_path, 'r') as file:
            data = json.load(file)

        for record_type, records in data.items():
            if record_type == 'News':
                for news in records:
                    text = news.get("Text")
                    city = news.get("City")
                    record = News(text_normalize(text), text_normalize(city))
                    record.publish()
                    print(f"Processed record: {record_type}")
            elif record_type == 'PrivateAd':
                for ads in records:
                    text = ads.get("Text")
                    expiration_date_str = ads.get("Expires")
                    record = PrivateAd(text_normalize(text), expiration_date_str)
                    record.publish()
                    print(f"Processed record: {record_type}")
            elif record_type == 'Comment':
                for comment in records:
                    nickname = comment.get("Nickname")
                    text = comment.get("Text")
                    record = Comment(text_normalize(nickname), text_normalize(text))
                    record.publish()
                    print(f"Processed record: {record_type}")
            else:
                print(f"Unknown record type: {record_type}")

        # Remove file after successful processing
        os.remove(self.file_path)
        print(f"File '{self.file_path}' processed and removed.")

def main():
    """Main function to interact with the user and handle their input."""
    # List to keep track of records added during the session
    records = []

    while True:
        # Menu options for the user
        print("\nSelect the type of record you want to add:")
        print("1. News")
        print("2. Private Ad")
        print("3. Comment")
        print("4. Process records from txt file")
        print("5. Process records from json file")
        print("6. Exit")

        choice = input("Enter your choice (1/2/3/4/5/6): ")

        if choice == '1':  # Add News
            text = input("Enter the news text: ")  # Get the news text from the user
            city = input("Enter the city: ")  # Get the city related to the news
            news_record = News(text, city)  # Create a News record
            record = news_record.publish()  # Publish the news
            records.append(record)  # Add the record to the list

        elif choice == '2':  # Add PrivateAd
            text = input("Enter the ad text: ")  # Get the ad text from the user

            while True:  # Keep asking for a valid date
                expiration_date_str = input("Enter the expiration date (YYYY-MM-DD): ")
                # Validate date before creating an object
                validated_date = PrivateAd.validate_date(expiration_date_str)
                if validated_date:
                    private_ad_record = PrivateAd(text, validated_date)  # Create PrivateAd instance
                    break  # Exit the loop if date is valid
                print("Invalid date format. Please enter the date again in the correct format (YYYY-MM-DD).")

            record = private_ad_record.publish()  # Publish the PrivateAd
            records.append(record)  # Add the record to the list

        elif choice == '3':  # Add Comment
            nickname = input("Enter your nickname: ")  # Get the user's nickname
            text = input("Enter your comment: ")  # Get the comment text
            comments = Comment(nickname, text)  # Create a Comment record
            record = comments.publish()  # Publish the comment
            records.append(record)  # Add the record to the list

        elif choice == '4':  # Process records from txt file
            # Prompt user to enter file path; if left empty, use the default file
            file_path = input(f"Enter the txt file path (default: {DEFAULT_INPUT_FILE}): ").strip() or DEFAULT_INPUT_FILE
            file_reader = FileReader(file_path)  # Create FileReader with the given file path
            file_reader.process_file()  # Process the file

        elif choice == '5':  # Process records from json file
            file_path = input(f"Enter the json file path (default: {DEFAULT_INPUT_JSON}): ").strip() or DEFAULT_INPUT_JSON
            file_reader = JsonReader(file_path)  # Create JsonReader with the given file path
            file_reader.process_json()  # Process the file

        elif choice == '6':  # Exit the program
            print("Exiting...")
            Record.finalize_and_update_csvs()
            break  # Exit the loop

        else:
            print("Invalid choice. Please try again.")  # Handle invalid menu choices

    # Print results of all records added during the session
    print(f"Summary of records added:")
    for record in records:
        print(record.strip())


if __name__ == "__main__":
    main()   # Run the main function
