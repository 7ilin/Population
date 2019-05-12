#-*- coding: utf-8 -*-

import os
import sys
import json
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from district.models import Region, City


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-p",
                    "--path",
                    dest='path_to_json',
                    help="Path to json file."),)
    def handle(self, *args, **options):
        if not options.get('path_to_json'):
            raise CommandError('You need specify --path (path to json file). See --help for more info.')
        
        path = options.get('path_to_json')

        if not os.path.exists(path):
            raise CommandError('File %s does not exists.' % path)

        print 'LOAD FROM FILE:'
        with open(path) as json_file:
            json_data = json.load(json_file)

        counter = 0
        for region_name, cities in json_data.items():
            region, _ = Region.objects.get_or_create(name=region_name)
            for city_name, people in cities.items():
                try:
                    city = City.objects.get(name=city_name, region=region)
                    city.people = people
                    city.save()
                except City.DoesNotExist:
                    city = City(name=city_name, region=region, people=people)
                    city.save()
                    
                counter += 1
                sys.stdout.flush()
                sys.stdout.write('\r\tCities: %s loaded' % counter)
        print