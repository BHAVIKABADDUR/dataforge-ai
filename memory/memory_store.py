memory = {
    "last_question": None,
    "last_agent": None,
    "last_result": None
}


def save_memory(question, agent, result):

    memory["last_question"] = question
    memory["last_agent"] = agent
    memory["last_result"] = result


def get_memory():

    return memory