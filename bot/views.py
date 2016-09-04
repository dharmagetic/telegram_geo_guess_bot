# -*- coding: utf-8 -*-

import json
import telepot

from django.http.response import HttpResponseForbidden, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.conf import settings

from bot.models import Country

TOKEN = settings.TELEGRAM_BOT_TOKEN
BOT = telepot.Bot(TOKEN)

GUESS_COUNTRIES = u"Угадывать страны"
NEXT_COUNTRY = u"Следующая страна"
GUESS_CAPITALS = u"Угадывать столицы"
NEXT_CAPITAL = u"Следующая столица"


def _guess_capital(chat_id):
    reply_markup = {"keyboard": [[u"Следующая столица"], [u"Угадывать страны"]], "one_time_keyboard": True}
    country = Country.random.country()
    message = u"Назовите столицу %s" % (country)
    return {
        'message': message,
        'reply_markup': reply_markup
    }


def _guess_country(chat_id):
    reply_markup = {"keyboard": [[u"Следующая страна"], [u"Угадывать столицы"]], "one_time_keyboard": True}
    capital = Country.random.capital()
    message = u"Назовите страну, чья столица %s" % (capital)
    return {
        'message': message,
        'reply_markup': reply_markup
    }

COMMANDS = {
    GUESS_COUNTRIES: _guess_country,
    NEXT_COUNTRY: _guess_country,
    GUESS_CAPITALS: _guess_capital,
    NEXT_CAPITAL: _guess_capital
}


class CommandReceiveView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        bot_token = kwargs.get('bot_token')
        # import pdb
        # pdb.set_trace()
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
                pass

            return JsonResponse({}, status=200)
