"""
Management command to populate the database with sample data.
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import Book, Review, UserProfile, ReadingList
import random


BOOKS = [
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "genre": "fiction",
        "description": "A gripping tale of racial injustice and childhood innocence in the American South.",
        "published_year": 1960,
        "isbn": "978-0-06-112008-4",
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "genre": "sci-fi",
        "description": "A chilling dystopia where Big Brother watches your every move and truth is whatever the Party says it is.",
        "published_year": 1949,
        "isbn": "978-0-452-28423-4",
    },
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "genre": "fiction",
        "description": "A portrait of the Jazz Age in all its decadence and excess, exploring themes of wealth and the American Dream.",
        "published_year": 1925,
        "isbn": "978-0-7432-7356-5",
    },
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "genre": "sci-fi",
        "description": "An epic science fiction saga set on the desert planet Arrakis, exploring politics, religion, and ecology.",
        "published_year": 1965,
        "isbn": "978-0-441-17271-9",
    },
    {
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author": "Douglas Adams",
        "genre": "sci-fi",
        "description": "A hilarious journey through space that begins with the demolition of Earth to make way for a hyperspace bypass.",
        "published_year": 1979,
        "isbn": "978-0-345-39180-3",
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "genre": "romance",
        "description": "A witty and romantic story exploring love, class, and society through the Bennet family.",
        "published_year": 1813,
        "isbn": "978-0-14-143951-8",
    },
    {
        "title": "The Name of the Wind",
        "author": "Patrick Rothfuss",
        "genre": "fantasy",
        "description": "A legendary wizard recounts his extraordinary life: an orphan who becomes the most feared magician in the land.",
        "published_year": 2007,
        "isbn": "978-0-7564-0474-1",
    },
    {
        "title": "Sapiens: A Brief History of Humankind",
        "author": "Yuval Noah Harari",
        "genre": "history",
        "description": "A sweeping survey of human history from the Stone Age to the Silicon Age, exploring what makes us uniquely human.",
        "published_year": 2011,
        "isbn": "978-0-06-231609-7",
    },
    {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "genre": "fiction",
        "description": "A young shepherd's journey to the Egyptian pyramids in search of treasure reveals profound life lessons.",
        "published_year": 1988,
        "isbn": "978-0-06-112241-5",
    },
    {
        "title": "Gone Girl",
        "author": "Gillian Flynn",
        "genre": "mystery",
        "description": "On their fifth anniversary, Nick Dunne's wife Amy disappears, pulling readers into a tale of dark obsession.",
        "published_year": 2012,
        "isbn": "978-0-307-58836-4",
    },
    {
        "title": "Atomic Habits",
        "author": "James Clear",
        "genre": "self-help",
        "description": "Practical strategies for forming good habits, breaking bad ones, and mastering tiny behaviors that lead to big results.",
        "published_year": 2018,
        "isbn": "978-0-7352-1129-2",
    },
    {
        "title": "The Shadow of the Wind",
        "author": "Carlos Ruiz Zafón",
        "genre": "mystery",
        "description": "Barcelona, 1945: a boy discovers a mysterious book and embarks on an adventure to find the author.",
        "published_year": 2001,
        "isbn": "978-0-14-303490-9",
    },
]

REVIEWS = [
    ("Absolutely Unforgettable", "One of the most powerful books I've ever read. The storytelling is masterful and the characters feel completely real. I found myself unable to put it down.", 5),
    ("A Timeless Classic", "This book has earned its place in the literary canon. Every page is beautifully crafted and the themes remain incredibly relevant today.", 5),
    ("Surprisingly Deep", "I picked this up not expecting much, but was completely blown away. The layers of meaning and the prose are exceptional.", 4),
    ("Good But Overhyped", "It's a well-written book, but I'm not sure it deserves quite all the praise it receives. Still worth reading, just temper your expectations.", 3),
    ("Changed My Perspective", "After finishing this I sat quietly for a long time. It challenged my assumptions and made me see the world differently.", 5),
    ("Excellent Start to Finish", "Gripping from the first page to the last. The pacing is perfect and every scene builds on the last brilliantly.", 4),
    ("Dense but Rewarding", "Takes some work to get into, but the payoff is immense. Patient readers will be richly rewarded.", 4),
    ("A Bit Slow in the Middle", "The beginning and end are fantastic, but the middle section drags a bit. Overall still a very worthwhile read.", 3),
    ("Technically Brilliant", "The craft on display here is extraordinary. Flawlessly plotted with characters that feel utterly authentic.", 5),
    ("Not For Everyone", "I can see why people love this, but it wasn't quite my cup of tea. The style is unique but takes getting used to.", 3),
]

USERNAMES = [
    ("alice_reads", "alice@example.com", "Avid reader of literary fiction and historical novels."),
    ("bookworm_ben", "ben@example.com", "I read everything, but especially love sci-fi and fantasy."),
    ("carol_pages", "carol@example.com", "Mystery addict and coffee shop regular."),
    ("dan_the_reader", "dan@example.com", "Former literature teacher. I review what I read."),
    ("emma_litpicks", "emma@example.com", "Romance and contemporary fiction are my happy place."),
]


class Command(BaseCommand):
    help = 'Seeds the database with sample books, users, and reviews'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding database...')

        # Create admin if not exists
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@folio.com', 'admin123')
            self.stdout.write(f'  ✅ Created superuser: admin / admin123')

        # Create users
        created_users = []
        for username, email, bio in USERNAMES:
            user, created = User.objects.get_or_create(username=username, defaults={'email': email})
            if created:
                user.set_password('password123')
                user.save()
                profile, _ = UserProfile.objects.get_or_create(user=user)
                profile.bio = bio
                profile.reading_goal = random.randint(12, 36)
                profile.save()
                self.stdout.write(f'  ✅ Created user: {username}')
            created_users.append(user)

        # Create books
        created_books = []
        admin_user = User.objects.get(username='admin')
        for book_data in BOOKS:
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults={**book_data, 'added_by': random.choice(created_users + [admin_user])}
            )
            if created:
                self.stdout.write(f'  📚 Added book: {book.title}')
            created_books.append(book)

        # Create reviews
        review_count = 0
        for book in created_books:
            num_reviewers = random.randint(1, min(len(created_users), 5))
            reviewers = random.sample(created_users, num_reviewers)
            for user in reviewers:
                if not Review.objects.filter(book=book, user=user).exists():
                    title, body, rating = random.choice(REVIEWS)
                    Review.objects.create(
                        book=book, user=user, rating=rating,
                        title=title, body=body,
                    )
                    review_count += 1

        self.stdout.write(f'  💬 Created {review_count} reviews')

        # Create some reading list entries
        rl_count = 0
        statuses = ['want', 'reading', 'read']
        for user in created_users:
            sample_books = random.sample(created_books, min(6, len(created_books)))
            for book in sample_books:
                entry, created = ReadingList.objects.get_or_create(
                    user=user, book=book,
                    defaults={'status': random.choice(statuses)}
                )
                if created:
                    rl_count += 1

        self.stdout.write(f'  📌 Created {rl_count} reading list entries')
        self.stdout.write(self.style.SUCCESS('\n✨ Database seeded successfully!'))
        self.stdout.write('  🔑 Admin login: admin / admin123')
        self.stdout.write('  👤 User login: alice_reads / password123')
        self.stdout.write('  🌐 Run: python manage.py runserver')
