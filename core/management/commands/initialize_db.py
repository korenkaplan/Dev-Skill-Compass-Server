from django.core.management.base import BaseCommand
from init_db.init_database_functions import initialize_pipeline
from init_db.data.data import get_tech_dict, get_roles_list


class Command(BaseCommand):
    help = 'Initialize the database'
    tech_dict = get_tech_dict()
    roles = get_roles_list()

    def handle(self, *args, **options):
        # Call your initialization function here
        initialize_pipeline(self.tech_dict, self.roles)
        self.stdout.write("Initialize the database command executed")
