from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

import commonware.log

from applications.models import Application, AppVersion
import amo.models

class Command(BaseCommand):
    help = ('Add a new version to a Application. Syntax: \n'
            '    ./manage.py addnewversion <applicarion_name> <version>')
    log = commonware.log.getLogger('z.appversions')

    def handle(self, *args, **options):

        try:
            do_addnewversion(args[0], args[1])
            msg = 'Adding %s to %s'%(args[1], args[0])
            self.log.info(msg)
            self.stdout.write(msg)

        except IndexError:
            raise CommandError(self.help)

def do_addnewversion(application, version):

    try:    
        apps = amo.APPS_ALL
        shorts = [ a.short for a in apps.values() ]
        if application in shorts:
            guids = dict((a.short, a.guid) for a in apps.values())
            app_id = guids.get(application)
        else:
            raise CommandError('Application %s does not exist'% application)

        app = Application.objects.get(guid=app_id)
        AppVersion.objects.create(application=app, version=version)

    except IntegrityError, e:
        raise CommandError('version %s already exist? %s'% (version, e))
