import ipywidgets as widgets
from IPython.display import display
import json

class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.user_responses = []
        self.current_question = 0
        self.question_text = widgets.HTML()
        self.choices_radio = widgets.RadioButtons(options=[], layout={'width': 'max-content'})
        self.submit_button = widgets.Button(description='Submit')
        self.submit_button.on_click(self.submit_response)
        self.feedback_text = widgets.HTML()
        self.result_displayed = False
        self.widget_container = widgets.VBox()
        self.display_question()

    def display_question(self):
        question = self.questions[self.current_question]
        self.question_text.value = f'<strong>Question {self.current_question + 1}:</strong> {question["question"]}'
        self.choices_radio.options = question['choices']

        # Clear the previous widget display
        self.widget_container.children = []
        self.widget_container.children = [self.question_text, self.choices_radio, self.submit_button]
        display(self.widget_container)

    def submit_response(self, b):
        user_response = self.choices_radio.value
        self.user_responses.append(user_response)
        
        question = self.questions[self.current_question]
        if user_response == question['answer']:
            feedback = '<strong style="color: green;">Correct!</strong>'
        else:
            feedback = '<strong style="color: red;">Incorrect.</strong>'
        
        self.feedback_text.value = feedback
        self.current_question += 1

        # Check if there are more questions or if results should be displayed
        if self.current_question < len(self.questions):
            self.display_question()
        elif not self.result_displayed:
            self.display_result()
            self.result_displayed = True

    def display_result(self):
        correct_answers = sum(response == question['answer'] for response, question in zip(self.user_responses, self.questions))
        total_questions = len(self.questions)
        result_text = f'You got {correct_answers} out of {total_questions} questions correct!<br><br>'

        # Create a list to store the incorrect questions and their details
        incorrect_questions = []

        for i, (user_response, question) in enumerate(zip(self.user_responses, self.questions)):
            if user_response != question['answer']:
                incorrect_questions.append({
                    'question_text': question['question'],
                    'correct_answer': question['answer'],
                    'user_response': user_response
                })

        if len(incorrect_questions) > 0:
            result_text += '<strong>Incorrect Questions:</strong><br>'
            for i, incorrect_question in enumerate(incorrect_questions, 1):
                question_text = incorrect_question['question_text']
                correct_answer = incorrect_question['correct_answer']
                user_response = incorrect_question['user_response']
                result_text += f'{i}. {question_text}<br>'
                result_text += f'   Correct Answer: <span style="color: green;">{correct_answer}</span><br>'
                result_text += f'   Your Answer: <span style="color: red;">{user_response}</span><br>'

        self.feedback_text.value = result_text

        # Clear the previous widget display and display the result
        self.widget_container.children = []
        self.widget_container.children = [self.feedback_text]

# Import the questions from JSON file to a variable
with open('questions.json', 'r') as f:
    quiz_questions = json.load(f)

# Create a global instance of the Quiz class
quiz_instance = Quiz(quiz_questions)
