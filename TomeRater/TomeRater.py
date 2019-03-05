class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def __repr__(self):
        return 'User: {name}, email: {email}, books read: {total}'.format(name=self.name, email=self.email, total=self.get_number_of_books_read())

    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.email

    def __hash__(self):
        return hash((self.name, self.email))

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print('UPDATE: The email of user {name} has been changed to {email}'.format(name=self.name, email=self.email))

    def read_book(self, book, rating=None):
        try:
            if rating >= 0 and rating <= 4:
                self.books[book] = rating
                book.add_rating(rating)
            else:
                print('INVALID RATING: The ratings was not a number from 0 to 4, no rating was added.')
                self.books[book] = None
        except TypeError:
            self.books[book] = rating

    def get_average_rating(self):
        total = [rating for rating in self.books.values() if rating != None]
        return sum(total) / len(total)
    
    def get_number_of_books_read(self):
        return len(list(self.books.keys()))

class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def __repr__(self):
        return self.title

    def __eq__(self, other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn

    def __hash__(self):
        return hash((self.title, self.isbn))
    
    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn
    
    def set_isbn(self, number):
        self.isbn = number
        print('UPDATE: The ISBN of {title} has been changed to {isbn}'.format(title=self.title, isbn=self.isbn))

    def add_rating(self, rating):
        try:
            if rating>=0 and rating<=4:
                self.ratings.append(rating)
            else:
                print('Invalid Rating')
        except TypeError:
            pass
    
    def get_average_rating(self):
        if self.ratings != []:
            return sum(self.ratings) / len(self.ratings)
        else:
            print('{title} has not received any ratings'.format(title=self.title))

class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def __repr__(self):
        return '{title} by {author}'.format(title=self.title, author=self.author)

    def get_author(self):
        return self.author

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def __repr__(self):
        return '{title}, {determiner} {level} manual on {subject}'.format(title=self.title, determiner=self.a_or_an(self.level),level=self.level, subject=self.subject)

    def get_subject(self):
        return self.subject
        
    def get_level(self):
        return self.level

    def a_or_an(self, word):
        if word[0] in 'aeiouy':
            return 'an'
        else:
            return 'a'

class TomeRater:
    def __init__(self):
        # Keys = Email addresses, Values = User objects
        self.users = {}
        # Keys = Book objects, Values = Number of users the book has been read by
        self.books = {}

    def create_book(self, title, isbn):
        return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating=None):
        if email in self.users.keys():
            self.users[email].read_book(book, rating)
            book.add_rating(rating)
        else:
            print('No user with email {email}'.format(email=email))
        
        if book in self.books.keys():
            self.books[book] += 1
        else:
            self.books[book] = 1
    
    def add_user(self, name, email, user_books=None):
        self.users[email] = User(name, email)
        if user_books != None:
            for book in user_books:
                self.add_book_to_user(book, email)

    def print_catalog(self):
        print('-----------------------Catalog---------------------------')
        for book in self.books:
            print(book)
    
    def print_users(self):
        print('-----------------------Users-----------------------------')
        for email in self.users:
            print(self.users[email])

    def most_read_book(self):
        most_read = list(self.books.keys())[0]
        for book in self.books:
            if self.books[book] > self.books[most_read]:
                most_read = book
        return most_read

    def highest_rated_book(self):
        highest_rated = list(self.books.keys())[0]
        for book in self.books:
            if book.get_average_rating() != None and book.get_average_rating() > highest_rated.get_average_rating():
                highest_rated = book
        return highest_rated
    
    def most_positive_user(self):
        most_positive = list(self.users.values())[0]
        for user in self.users.values():
            if user.get_average_rating() > most_positive.get_average_rating():
                most_positive = user
        return most_positive
    
    # Sophisticated analysis methods:
    def get_n_most_read_books(self, n):
        sorted_books_dict = sorted(self.books.items(), key=lambda x: x[1])
        sorted_books = [item[0] for item in list(reversed(sorted_books_dict))]
        return sorted_books[:n]

    def get_n_most_prolific_readers(self, n):
        readers_dict = {}
        for user in self.users.values():
            readers_dict.update({user: user.get_number_of_books_read()})
        sorted_readers_dict = sorted(readers_dict.items(), key=lambda x: x[1])
        sorted_readers = [item[0] for item in list(reversed(sorted_readers_dict))]
        return sorted_readers[:n]