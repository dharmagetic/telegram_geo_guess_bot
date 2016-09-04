# -*- coding: utf-8 -*-

import json
import telepot

from django.http.response import HttpResponseForbidden, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.conf import settings

from bot.models import Country
from bot.storage import get_user_state, set_user_state

TOKEN = settings.TELEGRAM_BOT_TOKEN
BOT = telepot.Bot(TOKEN)

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
    capital = Country.objects.get(country=country).capital
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


class CommandReceiveView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        bot_token = kwargs.get('bot_token')
        if bot_token != TOKEN:
            return HttpResponseForbidden('Invalid bot token!')
        try:
            payload = json.loads(request.body)
        except:
            return HttpResponseForbidden('Invalid request body')
        else:
            chat_id = payload.get('message').get('chat').get('id')
            message = payload.get('message').get('text')
            command = COMMANDS.get(message)
            if command:
                response = command(chat_id)
                BOT.sendMessage(chat_id, response['message'], reply_markup=response['reply_markup'])
            else:
                response = check_answer(chat_id, message)
                BOT.sendMessage(chat_id, response['message'], reply_markup=response['reply_markup'])

            return JsonResponse({}, status=200)
