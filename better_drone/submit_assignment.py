from csci_utils.assignment_submitter.submitter import AssignmentSubmitter


def get_answers(questions):
    raise NotImplementedError("Implement answers for the associated quiz")


def submit():
    submitter = AssignmentSubmitter(
        assignment_name="Name of the assignment",
        quiz_title=None
    )
    submitter.attempt(get_answers=get_answers)
