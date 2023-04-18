from time import sleep

from django.core.management.base import BaseCommand

from Bot.management.commands.fucn_trader import check_users


class Command(BaseCommand):
    help = 'бот'

    def handle(self, *args, **options):
        while True:
            sleep(500)
            check_users()
            # follows_js()
            # pair_list_update()
