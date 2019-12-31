import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def pagination_questions(request, selection):
    """
    Subsets list of questions to fit page limit
    :Return a list of questions based on page limits
    """
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # Route handler for getting categories
    @app.route('/categories')
    def get_all_categories():
        """
        Creates a dictionary of all categories
        :return a json of succes, and category dictionary
        """
        results = Category.query.order_by(Category.id).all()
        categories = {}
        for row in results:
            categories[row.id] = row.type

        return jsonify({
            'success': True,
            'categories': categories,
            'total_categories': len(results)
        })

    # Endpoint route handler for GET request for questions
    @app.route('/questions')
    def get_all_questions():
        """
        Get all questions, categories and total questions from database
        :return paginated ten questions, categories and total questions
        """
        questions_results = Question.query.order_by(Question.id).all()
        category_results = Category.query.order_by(Category.id).all()
        current_questions = pagination_questions(request, questions_results)
        if len(current_questions) == 0:
            abort(404)
        categories = {}
        for row in category_results:
            categories[row.id] = row.type

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions_results),
            'categories': categories,
            'current_category': None
        })

    # API endpoint route handler to delete question usng question_id
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        Delete a question using question id
        :param question_id: Id of the question to be deleted
        :return: Id of the question that has been deleted
        """
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except Exception:
            abort(422)

    # API endpoint route handler for creating new question
    @app.route('/questions', methods=['POST'])
    def create_question():
        """
        Add new question to database
        :return newly added question
        """
        body = request.get_json(request)
        new_question = body.get('question')
        new_answer = body.get('answer')
        new_category = body.get('category')
        new_difficulty = body.get('difficulty')
        if (new_question == '' or new_answer == '' or
            new_category == '' or
                new_difficulty == ''):
            abort(400)
        try:
            question = Question(question=new_question, answer=new_answer,
                                category=new_category,
                                difficulty=new_difficulty)
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id
            })
        except Exception:
            abort(422)

    # API endpoint route handler for searching questions
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        """
        Search for questions using the search term
        :return: Searcheed questions and total questions
        """
        body = request.get_json()
        search_term = body.get('searchTerm', None)
        try:
            questions_results = Question.query.order_by(Question.id).filter(
                Question.question.ilike('%{}%'.format(search_term))).all()
            search_questions = [question.format()
                                for question in questions_results]
            return jsonify({
                'success': True,
                'questions': search_questions,
                'total_questions': len(questions_results),
                'current_category': None
            })
        except Exception:
            abort(422)

    # API endpoint route handler for getting questions for a category
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        """
        Gets questions from database and filters them based on category
        :param category_id: The category for which questions are to be filtered
        :return: Filtered questions, total questions and current category
        """
        # tip: https://stackoverflow.com/questions/11530196/f
        # lask-sqlalchemy-query-specify-column-names
        # seelct few columns nd aslo take care of tuples being created
        categories = [category.id for category in
                      Category.query.with_entities(Category.id)]
        if category_id not in categories:
            abort(400, 'Invalid category id')
        try:
            questions_results = Question.query.order_by(
                Question.id).filter(Question.category == category_id).all()
            category_questions = [question.format()
                                  for question in questions_results]
            return jsonify({
                'success': True,
                'questions': category_questions,
                'total_questions': len(questions_results),
                'current_category': category_id
            })
        except Exception:
            abort(422)

    # API endpoint route handler for getting quiz questions
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        """
        Gets question for quiz
        :return: Uniques quiz question or None
        """
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        quizCategory = body.get('quiz_category', None)

        if quizCategory['id'] == 0:
            questions = Question.query.order_by(Question.id).all()
        else:
            questions = Question.query.order_by(Question.id).filter(
                Question.category == quizCategory['id']).all()

            formatted_questions = [question.format() for question in questions]
        # exclude previous questions
        unasked_questions = []
        for question in formatted_questions:
            if question['id'] not in previous_questions:
                unasked_questions.append(question)

        next_question = None
        if len(unasked_questions) > 0:
            next_question = unasked_questions[0]

        return jsonify({
            'success': True,
            'question': next_question
        })

    # Error Handler
    @app.errorhandler(HTTPException)
    def http_exception_handler(error):
        """
        HTTP error handler for all endpoints
        :param error: HTTPException containing code and description
        :return: error: HTTP status code, message: Error description
        """
        return jsonify({
            'success': False,
            'error': error.code,
            'message': error.description
        }), error.code

    @app.errorhandler(Exception)
    def exception_handler(error):
        """
        Generic error handler for all endpoints
        :param error: Any exception
        :return: error: HTTP status code, message: Error description
        """
        return jsonify({
            'success': False,
            'error': 500,
            'message': f'Something went wrong: {error}'
        }), 500
    return app
