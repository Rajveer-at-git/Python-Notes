from survey import Anonymous_Survey

question = "What was the first language you learned? (Enter 'q' to exit.)"
survey = Anonymous_Survey(question)

survey.show_question()


while True:
    response = input("Enter your answer: ")
    if response == 'q':
        break
    survey.store_response(response)

print("Thank you to everyone who participated in the survey.")
survey.show_results()