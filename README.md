# Campus Opportunity Hub

#### Video Demo: https://youtu.be/heeb261DtZE

#### Description:

Campus Opportunity Hub is a web application that I created to help college students find and keep track of different opportunities in one place. Students usually find internships, hackathons, scholarships, workshops, and placement opportunities through different websites, college groups, and social media. Because of this, it can be difficult to keep track of everything and remember application deadlines.

The main idea behind this project is to provide a simple website where students can browse opportunities, search for something specific, filter opportunities by type, save opportunities they are interested in, and keep track of the opportunities they have applied for.

The application is built using Python and Flask. I used SQLite as the database because it is simple to set up and works well for this project without requiring a separate database server. The front end uses HTML, CSS, and Jinja templates, with JavaScript used for a small amount of interaction.

Users can create an account and log in to the application. After logging in, they can view the available opportunities and search or filter them. Each opportunity has its own details page. From there, a user can save an opportunity for later or update its application status. Saved opportunities can be viewed separately, and the application tracker allows users to see the opportunities they have applied for.

The project also allows users to add new opportunities. This makes the application more useful because opportunities are not limited to the initial data included in the database.

## Files

`app.py` is the main Python file for the project. It contains the Flask application, routes, login and registration logic, database operations, and the functions used for opportunities, saved opportunities, and application tracking.

`schema.sql` contains the SQL statements used to create the database tables.

`database.db` is the SQLite database used by the application. It stores users, opportunities, saved opportunities, and application information.

`templates/layout.html` contains the common layout of the website, including the navigation bar, flash messages, and other shared elements.

`templates/index.html` is the home page.

`templates/login.html` contains the login form.

`templates/register.html` contains the registration form.

`templates/opportunities.html` displays the available opportunities and provides search and filtering.

`templates/opportunity_detail.html` displays the details of a selected opportunity and provides options to save it and update its application status.

`templates/saved.html` displays opportunities saved by the logged-in user.

`templates/applications.html` displays the user's application tracker.

`templates/add.html` contains the form used to add a new opportunity.

`templates/404.html` is displayed when a requested page cannot be found.

`static/style.css` contains the styling for the website, including the layout, forms, buttons, cards, and responsive design.

`static/script.js` contains JavaScript used for small interface interactions, such as handling flash messages.

`requirements.txt` contains the Python packages required to run the application.

## Database

The application uses four main tables.

The `users` table stores the registered users and their password hashes.

The `opportunities` table stores information about internships, hackathons, scholarships, workshops, and other opportunities.

The `saved_opportunities` table connects users with the opportunities they have saved.

The `applications` table stores the application status of opportunities for each user.

I used these separate tables so that one user can save or apply to multiple opportunities and each opportunity can be associated with multiple users.

## Design Choices

I chose Flask because I wanted to use Python for the backend and Flask provided a simple way to connect Python code with HTML pages and a database.

I chose SQLite because it is easy to use and does not require setting up a separate database server. It was suitable for the size of this project.

I used Jinja templates and a shared `layout.html` file so that common parts of the website, such as the navigation bar, did not have to be written again on every page.

For user accounts, passwords are stored as password hashes instead of plain text. Flask sessions are used to remember logged-in users.

I also used SQL placeholders when passing user input into database queries instead of directly joining strings into SQL statements.

The website includes sample opportunity data so that the application can be tested and demonstrated without having to manually add every opportunity first.

## How to Run

Install the required packages with:

    pip install -r requirements.txt

Run the application with:

    python app.py

The Flask server will show a local address in the terminal. Open that address in a browser to use the application.

## AI Disclosure

I used AI tools during the development of this project for learning, explanations, brainstorming, debugging, and help understanding parts of the implementation. I reviewed and tested the code and made changes while developing the project. The final project and its implementation are my responsibility.

## 📸 Screenshots

### 🏠 Home Page

![Home Page](Screenshot%202026-09-10%20184944.png)

### 🔎 Opportunities

![Opportunities](Screenshot%202026-09-10%20185105.png)

### 📝 Registration

![Registration](Screenshot%202026-09-10%20185032.png)

### ➕ Add Opportunity

![Add Opportunity](Screenshot%202026-09-10%20185127.png)
