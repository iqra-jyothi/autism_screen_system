def convert(answer):
    """
    Convert questionnaire answers into numerical values.

    Yes   -> 1
    Maybe -> 1
    No    -> 0
    """

    if answer in ["Yes", "Maybe"]:
        return 1

    return 0


def convert_questions(answers):
    """
    Convert a list of questionnaire answers into numbers.
    """

    return [convert(answer) for answer in answers]


def create_features(answers, age):
    """
    Create ML feature vector.

    Only A1-A10 are used for prediction.
    Age is added as the final feature.

    Total features = 11
    """

    encoded_answers = convert_questions(answers)

    # First 10 questions are ML features
    features = encoded_answers[:10]

    # Add age
    features.append(age)

    return features