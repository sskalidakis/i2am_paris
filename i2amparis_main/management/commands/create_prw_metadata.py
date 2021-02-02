from django.core.management.base import BaseCommand, CommandError
from i2amparis_main.models import ResultsComp, PRWMetaData


class Command(BaseCommand):
    help = 'Created metadata for Paris Reinforce Workspace'

    def handle(self, *args, **options):
        PRWMetaData.objects.all().delete()
        data = ResultsComp.objects.values('model__name', 'scenario__name', 'region__name', 'variable__name').distinct()
        md_length = len(data)
        count = 0
        self.stdout.write('Passing all metadata of prw...')
        for d in data:
            try:
                md_obj = PRWMetaData(model_name=d['model__name'], scenario_name=d['scenario__name'],
                                     region_name=d['region__name'], variable_name=d['variable__name'])
                md_obj.save()
                count = count + 1
            except:
                raise CommandError('{} out of {} passed'.format(count, md_length))
        print(data)
        self.stdout.write('Successfully created metadata for prw!')
