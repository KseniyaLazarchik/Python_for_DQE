from datetime import datetime
import re

# File to store the records
FILE_NAME = 'news_feed.txt'


class Record:
    """Base class for all records."""
    def __init__(self, text):
        self.text = text
        self.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # The current date and time when the record is created

    def publish(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def _write_to_file(self, record):
        with open(FILE_NAME, 'a') as file:
            file.write(record) # Append the record to the file


class News(Record):
    """Class for News records."""
    def __init__(self, text, city):
        super().__init__(text)
        self.city = city # The city where the news is related to

    def publish(self):
        record = f"News\nDate: {self.date}\nCity: {self.city}\n{self.text}\n\n"
        self._write_to_file(record) # Write the record to the file
        return record # Return the record for reporting


class PrivateAd(Record):
    """Class for Private Ad records."""
    def __init__(self, text, expiration_date_str):
        super().__init__(text)
        self.expiration_date_str = expiration_date_str  # Store the date as-is before validation
        self.expiration_date_str = self.validate_date(expiration_date_str)  # Validate and format date
        if not self.expiration_date_str:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")  # Raise an error if the date is invalid
        self.days_left = self.calculate_days_left() # Calculate days left until expiration

    @staticmethod
    def validate_date(date_str):
        """Checks the date format and returns a valid formatted date string or None if incorrect."""
        date_str = date_str.replace("/", "-") # Replace slashes with dashes to handle user input errors

        # Validate the final formatted date
        try:
            datetime.strptime(date_str, '%Y-%m-%d') # Check if the format is correct (YYYY-MM-DD)
            return date_str  # Return formatted date if it's valid
        except ValueError:
            return None  # Return None for invalid input

    def calculate_days_left(self):
        """Calculates the number of days until the expiration date."""
        expiration_date = datetime.strptime(self.expiration_date_str, '%Y-%m-%d')
        today = datetime.now() # Get the current date
        return max((expiration_date - today).days, 0)  # Ensure the value is not negative

    def publish(self):
        """Publishes the Private Ad record."""
        record = f"Private Ad\nDate: {self.date} | Expiration: {self.expiration_date_str} | {self.days_left} days left\n{self.text}\n\n"
        self._write_to_file(record) # Write the record to the file
        return record  # Return the record for reporting


class Comment(Record):
    """Class for unique records."""
    def __init__(self, nickname, text):
        super().__init__(text)
        self.nickname = nickname # The nickname of the commenter
        self.words_num = self.words_count() # Calculate the number of words in the comment

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
        record = f"Nickname: {self.nickname}\nDate: {self.date}\n{self.text}\nWords count: {self.words_num}\n\n"
        self._write_to_file(record) # Write the record to the file
        return record  # Return the record for reporting


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
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1': # Add News
            text = input("Enter the news text: ") # Get the news text from the user
            city = input("Enter the city: ") # Get the city related to the news
            news_record = News(text, city) # Create a News record
            record = news_record.publish() # Publish the news
            records.append(record) # Add the record to the list


        elif choice == '2':  # Add PrivateAd
            text = input("Enter the ad text: ") # Get the ad text from the user
            while True:  # Keep asking for a valid date
                expiration_date_str = input("Enter the expiration date (YYYY-MM-DD): ")
                # Validate date before creating an object
                validated_date = PrivateAd.validate_date(expiration_date_str)
                if validated_date:
                    private_ad_record = PrivateAd(text, validated_date)  # Create PrivateAd instance
                    break # Exit the loop if date is valid
                print("Invalid date format. Please enter the date again in the correct format (YYYY-MM-DD).")
            record = private_ad_record.publish() # Publish the PrivateAd
            records.append(record) # Add the record to the list

        elif choice == '3': # Add Comment
            nickname = input("Enter your nickname: ") # Get the user's nickname
            text = input("Enter your comment: ") # Get the comment text
            comments = Comment(nickname, text) # Create a Comment record
            record = comments.publish() # Publish the comment
            records.append(record) # Add the record to the list

        elif choice == '4': # Exit the program
            print("Exiting...")
            break # Exit the loop

        else:
            print("Invalid choice. Please try again.") # Handle invalid menu choices

    # Print results of all records added during the session
    print(f"Summary of records added:")
    for record in records:
        print(record.strip())

if __name__ == "__main__":
    main() # Run the main function
