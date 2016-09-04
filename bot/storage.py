import shelve


def set_user_state(chat_id, state):
    d = shelve.open('shelve.db')
    d[chat_id] = state
    d.close()


def get_user_state(chat_id):
    d = shelve.open('shelve.db')
    state = d[chat_id]
    d.close()
    return state