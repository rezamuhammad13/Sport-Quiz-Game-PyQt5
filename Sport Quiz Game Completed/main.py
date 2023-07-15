from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5 import QtCore
from urllib.request import urlopen
import json
import pandas as pd
import random

#open api link to database
with urlopen("https://opentdb.com/api.php?amount=50&category=21&difficulty=medium&type=multiple") as webpage:
    #read JSON file & extract data
    data = json.loads(webpage.read().decode())
    df = pd.DataFrame(data["results"])

#load 1 instance of questions & answers at a time from the database
def preload_data(idx):
    #idx parm: selected randomly time and again at function call
    question = df["question"][idx]
    correct = df["correct_answer"][idx]
    wrong = df["incorrect_answers"][idx]

    #fixing charecters with bad formatting
    formatting = [
        ("#039;", "'"),
        ("&'", "'"),
        ("&quot;", '"'),
        ("&lt;", "<"),
        ("&gt;", ">")
        ]

    #replace bad charecters in strings
    for tuple in formatting:
        question = question.replace(tuple[0], tuple[1])
        correct = correct.replace(tuple[0], tuple[1])
    #replace bad charecters in lists
    for tuple in formatting:
        wrong = [char.replace(tuple[0], tuple[1]) for char in wrong]

    #store local values globally
    parameters["question"].append(question)
    parameters["correct"].append(correct)

    all_answers = wrong + [correct]
    random.shuffle(all_answers)

    parameters["answer1"].append(all_answers[0])
    parameters["answer2"].append(all_answers[1])
    parameters["answer3"].append(all_answers[2])
    parameters["answer4"].append(all_answers[3])

    #print correct answer to the terminal (for testing)
    print(parameters["correct"][-1])

#dictionary to store local pre-load parameters on a global level
parameters = {
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "correct": [],
    "score": [],
    "total_correct": [],
    "total_false": [],
    "number_quest": [],
    "index": []
    }

#global dictionary of dynamically changing widgets
widgets = {
    "logo": [],
    "button": [],
    "score": [],
    "number_quest": [],
    "total_correct": [],
    "total_false": [],
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "message": [],
    "message2": []
}

#initialliza grid layout
grid = QGridLayout()

def clear_widgets():
    ''' hide all existing widgets and erase
        them from the global dictionary'''
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()

def clear_parameters():
    #clear the global dictionary of parameters
    for parm in parameters:
        if parameters[parm] != []:
            for i in range(0, len(parameters[parm])):
                parameters[parm].pop()
    #populate with initial index & score values
    parameters["index"].append(random.randint(0,49))
    parameters["score"].append(0)
    parameters["number_quest"].append(1)
    parameters["total_correct"].append(0)
    parameters["total_false"].append(0)

def start_game():
    #start the game, reset all widgets and parameters
    clear_widgets()
    clear_parameters()
    preload_data(parameters["index"][-1])
    #display the game frame
    frame2()

def create_buttons(answer, l_margin, r_margin):
    #create identical buttons with custom left & right margins
    button = QPushButton(answer)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(485)
    button.setStyleSheet(
        #setting variable margins
        "*{margin-left: " + str(l_margin) +"px;"+
        "margin-right: " + str(r_margin) +"px;"+
        '''
        border: 4px solid '#201c1c';
        color: '#ea3a3a';
        font-family: 'poppins';
        font-size: 20px;
        border-radius: 25px;
        padding: 15px 0px;
        margin-top: 20px;
        }
        *:hover{
            background: '#201c1c';
        }
        '''
    )
    button.clicked.connect(lambda x: is_correct(button))
    return button

def is_correct(btn):
    #a function to evaluate wether user answer is correct
    if btn.text() == parameters["correct"][-1]:
        # CORRECT ANSWER

        #update score (+10 points)
        temp_score = parameters["score"][-1]
        parameters["score"].pop()
        parameters["score"].append(temp_score + 10)

        #update number of question
        temp_quest = parameters["number_quest"][-1]
        parameters["number_quest"].pop()
        parameters["number_quest"].append(temp_quest + 1)

        #update number of correct answer
        temp_correct = parameters["total_correct"][-1]
        parameters["total_correct"].pop()
        parameters["total_correct"].append(temp_correct + 1)

        #select a new random index and replace the old one
        parameters["index"].pop()
        parameters["index"].append(random.randint(0,49))
        #preload data for new index value
        preload_data(parameters["index"][-1])

        #update the text of all widgets with new data
        widgets["score"][-1].setText(str(parameters["score"][-1]))
        widgets["question"][0].setText(parameters["question"][-1])
        widgets["answer1"][0].setText(parameters["answer1"][-1])
        widgets["answer2"][0].setText(parameters["answer2"][-1])
        widgets["answer3"][0].setText(parameters["answer3"][-1])
        widgets["answer4"][0].setText(parameters["answer4"][-1])
        widgets["number_quest"][-1].setText(str(parameters["number_quest"][-1]) + "/50")

        if parameters["score"][-1] == 100 or parameters["score"][-1] > 100:
            # WON THE GAME
            clear_widgets()
            frame3()
        if parameters["number_quest"][-1] == 50 :
            # LOSE THE GAME
            clear_widgets()
            frame4()

    else:
        # update score (-5 points)
        temp_score = parameters["score"][-1]
        parameters["score"].pop()
        parameters["score"].append(temp_score - 5)

        # update number of question
        temp_quest = parameters["number_quest"][-1]
        parameters["number_quest"].pop()
        parameters["number_quest"].append(temp_quest + 1)

        # update number of false answer
        temp_false = parameters["total_false"][-1]
        parameters["total_false"].pop()
        parameters["total_false"].append(temp_false + 1)

        # select a new random index and replace the old one
        parameters["index"].pop()
        parameters["index"].append(random.randint(0, 49))
        # preload data for new index value
        preload_data(parameters["index"][-1])

        # update the text of all widgets with new data
        widgets["score"][-1].setText(str(parameters["score"][-1]))
        widgets["question"][0].setText(parameters["question"][-1])
        widgets["answer1"][0].setText(parameters["answer1"][-1])
        widgets["answer2"][0].setText(parameters["answer2"][-1])
        widgets["answer3"][0].setText(parameters["answer3"][-1])
        widgets["answer4"][0].setText(parameters["answer4"][-1])
        widgets["number_quest"][-1].setText(str(parameters["number_quest"][-1]) + "/50")

        if parameters["score"][-1] == -50 or parameters["score"][-1] < -50 or parameters["number_quest"][-1] == 50 :
            # LOSE THE GAME
            clear_widgets()
            frame4()

#*********************************************
#                  FRAME 1
#*********************************************

def frame1():
    clear_widgets()
    clear_parameters()
    #logo widget
    image = QPixmap("images/QUIZ.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 10px;")
    widgets["logo"].append(logo)

    #button widget
    button = QPushButton("PLAY")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
        '''
        *{
            border: 4px solid '#201c1c';
            border-radius: 45px;
            font-size: 35px;
            color: '#ea3a3a';
            padding: 25px 0;
            margin: 150px 50px;
        }
        *:hover{
            background: '#201c1c';
        }
        '''
    )
    #button callback
    button.clicked.connect(start_game)
    widgets["button"].append(button)

    #place global widgets on the grid
    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 1, 0, 1, 2)

#*********************************************
#                  FRAME 2
#*********************************************

def frame2():
    #score widget
    score = QLabel(str(parameters["score"][-1]))
    score.setAlignment(QtCore.Qt.AlignLeft)
    score.setStyleSheet(
        '''
        font-size: 35px;
        font-family: 'poppins';
        color: '#201c1c';
        padding: 15px 25px;
        margin: 60px 200px;
        background: '#ea3a3a';
        border: 1px solid '#201c1c';
        border-radius: 35px;
        '''
    )
    widgets["score"].append(score)

    #number_question_widget
    num_quest = QLabel(str(parameters["number_quest"][-1]) + "/50")
    num_quest.setAlignment(QtCore.Qt.AlignRight)
    num_quest.setStyleSheet(
        '''
        font-size: 15px;
        font-family: 'poppins';
        color: '#201c1c';
        margin: 60px 300px;
        '''
    )
    widgets["number_quest"].append(num_quest)

    #question widget
    question = QLabel(parameters["question"][-1])
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet(
        '''
        font-family: 'poppins';
        font-size: 25px;
        color: '#ea3a3a';
        padding: 75px;
        '''
    )
    widgets["question"].append(question)

    #answer button widgets
    button1 = create_buttons(parameters["answer1"][-1], 5, 5)
    button2 = create_buttons(parameters["answer2"][-1], 5, 5)
    button3 = create_buttons(parameters["answer3"][-1], 5, 5)
    button4 = create_buttons(parameters["answer4"][-1], 5, 5)

    widgets["answer1"].append(button1)
    widgets["answer2"].append(button2)
    widgets["answer3"].append(button3)
    widgets["answer4"].append(button4)

    # instruction message
    message = QLabel("get 100 points to win this game")
    message.setAlignment(QtCore.Qt.AlignCenter)
    message.setStyleSheet(
        "font-family: 'poppins'; font-size: 15px; color: 'grey';margin-top: 45px; margin-bottom: 10px;"
    )
    widgets["message"].append(message)

    #logo widget
    image = QPixmap("images/logo.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 15px; margin-bottom: 30px;")
    widgets["logo"].append(logo)


    #place widget on the grid
    grid.addWidget(widgets["score"][-1], 0, 1)
    grid.addWidget(widgets["number_quest"][-1], 0, 0)
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["answer1"][-1], 2, 0)
    grid.addWidget(widgets["answer2"][-1], 2, 1)
    grid.addWidget(widgets["answer3"][-1], 3, 0)
    grid.addWidget(widgets["answer4"][-1], 3, 1)
    grid.addWidget(widgets["message"][-1],4, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 5, 0, 1, 2)

#*********************************************
#             FRAME 3 - WIN GAME
#*********************************************

def frame3():
    #congratulation widget
    message2 = QLabel("Congratulations! You\nare a true sport fans")
    message2.setAlignment(QtCore.Qt.AlignCenter)
    message2.setStyleSheet(
        "font-family: 'poppins'; font-size: 30px; color: '#201c1c'; margin-top:10px; margin-bottom:100px;"
        )
    widgets["message2"].append(message2)

    #button widget
    button = QPushButton('TRY AGAIN')
    button.setStyleSheet(
        "*{background:'#eeeded'; padding:25px 0px; border: 1px solid '#201c1c'; color: '#ea3a3a'; font-family: 'poppins'; font-size: 25px; border-radius: 40px; margin: 50px 200px;} *:hover{background:'#201c1c';}"
        )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(frame1)

    widgets["button"].append(button)

    # total correct_widget
    correct = QLabel("Total Correct Answer = " + str(parameters["total_correct"][-1]))
    correct.setAlignment(QtCore.Qt.AlignCenter)
    correct.setStyleSheet(
        '''
        font-size: 15px;
        font-family: 'poppins';
        color: '#201c1c';
        margin-top : 20px;
        '''
    )
    widgets["total_correct"].append(correct)

    # total false_widget
    false = QLabel("Total False Answer = " + str(parameters["total_false"][-1]))
    false.setAlignment(QtCore.Qt.AlignCenter)
    false.setStyleSheet(
        '''
        font-size: 15px;
        font-family: 'poppins';
        color: '#201c1c';
        margin-bottom: 30px;
        '''
    )
    widgets["total_false"].append(false)

    # logo widget
    pixmap = QPixmap('images/QUIZ.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:25px; margin-bottom: 20px;"
    )
    widgets["logo"].append(logo)

    #place widgets on the grid
    grid.addWidget(widgets["message2"][-1], 0, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["total_correct"][-1], 2, 0, 1, 2)
    grid.addWidget(widgets["total_false"][-1], 3, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 4, 0, 2, 2)


#*********************************************
#                  FRAME 4 - FAIL
#*********************************************
def frame4():
    #sorry widget
    message = QLabel("Sorry,feel free to try again your score is:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'poppins'; font-size: 35px; color: '#201c1c'; margin: 50px 10px; padding:20px;"
        )
    widgets["message"].append(message)

    #score widget
    score = QLabel(str(parameters["score"][-1]))
    score.setStyleSheet("font-size: 100px; color: '#201c1c'; margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    # total correct_widget
    correct = QLabel("Total Correct Answer = " + str(parameters["total_correct"][-1]))
    correct.setAlignment(QtCore.Qt.AlignCenter)
    correct.setStyleSheet(
        '''
        font-size: 15px;
        font-family: 'poppins';
        color: '#201c1c';
        margin-top : 100px;
        '''
    )
    widgets["total_correct"].append(correct)

    # total false_widget
    false = QLabel("Total False Answer = " + str(parameters["total_false"][-1]))
    false.setAlignment(QtCore.Qt.AlignCenter)
    false.setStyleSheet(
        '''
        font-size: 15px;
        font-family: 'poppins';
        color: '#201c1c';
        margin-bottom: 10px;
        '''
    )
    widgets["total_false"].append(false)

    #button widget
    button = QPushButton('TRY AGAIN')
    button.setStyleSheet(
        '''*{
            padding: 25px 0px;
            background: '#eeeded';
            color: '#ea3a3a';
            font-family: 'poppins';
            font-size: 35px;
            border: 1px solid '#201c1c';
            border-radius: 40px;
            margin-bottom: 130px;
            margin-right: 25px;
            margin-left: 25px
        }
        *:hover{
            background: '#201c1c';
        }'''
        )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(frame1)

    widgets["button"].append(button)

    #logo widget
    pixmap = QPixmap('images/QUIZ.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :5px;" +
        "margin-bottom : 150px;"
    )
    widgets["logo"].append(logo)

    #place widgets on the grid
    grid.addWidget(widgets["message"][-1], 0, 0)
    grid.addWidget(widgets["score"][-1], 0, 1)
    grid.addWidget(widgets["total_correct"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["total_false"][-1], 2, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 3, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 4, 0, 1, 2)