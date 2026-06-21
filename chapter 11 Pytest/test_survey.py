from survey import Anonymous_Survey

def test_store_single_response():
    question = "What language did you first learned to speak?"
    language_survey = Anonymous_Survey(question)
    language_survey.store_response("English")
    assert "English" in language_survey.responses

def test_store_multiple_response():
    question = "What language did you first learned to speak?"
    language_survey = Anonymous_Survey(question)
    responses = ['English', 'Hindi', 'Mandarian']
    for response in responses:
        language_survey.store_response(response)

    # check for multiple responses correctly stored in the responses array
    for response in responses:
        assert response in language_survey.responses

        












