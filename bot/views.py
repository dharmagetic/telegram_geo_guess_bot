# -*- coding: utf-8 -*-

import json
import telepot

from django.http.response import HttpResponseForbidden, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.conf import settings

from bot.commands import COMMANDS, check_answer

TOKEN = settings.TELEGRAM_BOT_TOKEN
BOT = telepot.Bot(TOKEN)


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
            else:
                response = check_answer(chat_id, message)

            BOT.sendMessage(chat_id, response['message'], reply_markup=response['reply_markup'])

            return JsonResponse({}, status=200)
