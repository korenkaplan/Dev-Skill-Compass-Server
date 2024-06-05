from django.core.management.base import BaseCommand
from init_db.init_database_functions import initialize_pipeline
from init_db.data.data import get_tech_dict, get_roles_dict


class Command(BaseCommand):
    help = "Initialize the database"
    tech_dict = get_tech_dict()
    roles: dict = get_roles_dict()

    def handle(self, *args, **options):
        # Call your initialization function here
        res_message = initialize_pipeline(self.tech_dict, self.roles)
        self.stdout.write(res_message)
        self.stdout.write("Initialize the database command executed")
