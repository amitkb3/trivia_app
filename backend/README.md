# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API endpoint Documentation

* GET '/categories'
  - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
  - Request Arguments: None
  - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

```json5
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

* GET '/questions'
  - Fetches the questions to be displayed. 
  - Request Arguments: None. If 'page' parameter is provided, the questions will be paginated
  - Returns: The response body contains
    `questions`: List of questions
    `categories`: dictionary of categories
    `total_questions`: Total number of  questions

```json5
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```
* POST "/questions"
    - Adds a question to the database
    - Request Body:

      `question`: Question statement    
      `answer`: Answer statement
      `category`: Category ID
      `difficulty`: Difficulty Level

```json5
{
  "question": "Capital of India?",
  "answer": "New Delhi",
  "difficulty": 1,
  "category": 3
}
```
  - Response Body:

      `created`:  Question Id of new question saved to the database

```json5
{
  "success": true,
  "created": 22
}
```
* DELETE "/questions/<int:question_id>"
    - Deletes a question from the database
    - Request Parameters: `question_id`: Question ID to delete
    - Response Body:

      `deleted`: Question ID that is deleted

```json5
{
  "success": true,
  "deleted": 22
}
```
* POST "/questions/search"
    - search questions based on search term
    - Request Body:
    
      `searchTerm`: Search term

```json5
{
  "searchTerm": "movie"
}
```

  - Response Body:
    
    `questions`: List of questions found in search
    
    `total_questions`: Total number of  questions

```json5
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": " What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```
* GET "/categories/<int:category_id>/questions"
    - Fetches questions for the requested category
    - Request Parameters: `category_id`: Category ID for questions
    - Response Body:

    `questions`: List of category questions

    `total_questions`: Total number of  questions
    
    `current_category`: Current category ID
```json5
{
  "questions": [{
    "answer": "Apollo 13",
    "category": 5,
    "difficulty": 4,
    "id": 2,
    "question": " What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  }],
  "total_questions": 1,
  "current_category": 1
}
```

* POST "/quizzes"
    - Fetches a unique question for the quiz on selected category
    - Request Body:
    
    `previous_questions`: List of previously answered questions

    `quiz_category`: Category object of the quiz
    - Response Body:
    
    `question`: question of requested category

```json5
{
  "question": {
    "answer": "Apollo 13",
    "category": 5,
    "difficulty": 4,
    "id": 2,
    "question": " What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  }
}
```



## Testing
To run the tests, run

```json5
dropdb trivia_test

createdb trivia_test

psql trivia_test < trivia.psql

python test_flaskr.py

```