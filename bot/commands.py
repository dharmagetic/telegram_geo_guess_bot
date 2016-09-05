# -*- coding: utf-8 -*-
from bot.models import Country
from bot.storage import set_user_state, get_user_state

START = u"/start"
GUESS_COUNTRIES = u"Угадывать страны"
NEXT_COUNTRY = u"Следующая страна"
GUESS_CAPITALS = u"Угадывать столицы"
NEXT_CAPITAL = u"Следующая столица"


def _start(chat_id):
    message = u"Привет! Я робот, который поможет тебе прошариться в географии. Попробуй угадать страну или столицу!"
    reply_markup = {"keyboard": [[u"Угадывать столицы"], [u"Угадывать страны"]], "one_time_keyboard": True}
    response = {
        'message': message,
        'reply_markup': reply_markup
    }
    return response


def _guess_capital(chat_id):
    country = Country.random.country()
    capital = Country.objects.get(name=country).capital
    message = u"Назовите столицу %s" % (country)
    reply_markup = {"keyboard": [[u"Следующая столица"], [u"Угадывать страны"]], "one_time_keyboard": True}
    state = {
        'correct_answer': capital,
        'current_command': GUESS_CAPITALS
    }
    set_user_state(chat_id, state)
    return {
        'message': message,
        'reply_markup': reply_markup
    }


def _guess_country(chat_id):
    capital = Country.random.capital()
    country = Country.objects.get(capital=capital).name
    message = u"Назовите страну, чья столица %s" % (capital)
    reply_markup = {"keyboard": [[u"Следующая страна"], [u"Угадывать столицы"]], "one_time_keyboard": True}
    state = {
        'correct_answer': country,
        'current_command': GUESS_COUNTRIES
    }
    set_user_state(chat_id, state)
    return {
        'message': message,
        'reply_markup': reply_markup
    }

COMMANDS = {
    START: _start,
    GUESS_COUNTRIES: _guess_country,
    NEXT_COUNTRY: _guess_country,
    GUESS_CAPITALS: _guess_capital,
    NEXT_CAPITAL: _guess_capital,
}


def check_answer(chat_id, chat_message):
    state = get_user_state(str(chat_id))
    if not state:
        message = u"Привет! Я робот, который поможет тебе прошариться в географии. Попробуй угадать страну или столицу!"
        reply_markup = {"keyboard": [[u"Угадывать столицы"], [u"Угадывать страны"]], "one_time_keyboard": True}
        response = {
            'message': message,
            'reply_markup': reply_markup
        }
        return response
    else:
        correct_answer = state.get('correct_answer')
        current_command = state.get('current_command')
        if chat_message == correct_answer:
            message = u"Правильно!"
        else:
            message = u"Не верно :( Правильный ответ: %s" % (correct_answer)
        response = COMMANDS.get(current_command)(chat_id)
        response['message'] = message
        return response