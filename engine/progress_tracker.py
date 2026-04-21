def update_progress(skill, correct, state):

    if "skills" not in state:
        state.skills = {}

    if skill not in state.skills:
        state.skills[skill] = {"correct": 0, "wrong": 0}

    if correct:
        state.skills[skill]["correct"] += 1
    else:
        state.skills[skill]["wrong"] += 1
