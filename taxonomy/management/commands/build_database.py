import csv
import datetime
import sys
from os.path import join
from itertools import islice
from django.core.management import BaseCommand
from django.db import transaction
from pipetaxon.settings import VALID_RANKS
from taxonomy.models import Taxonomy, Division


class Command(BaseCommand):
    help = 'Build the database taxonomy from NCBI data'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)
        parser.add_argument('--clear', action='store_true', dest='clear', default=False, help='Missing help',)
        parser.add_argument('--lineage', action='store_true', dest='lineage', default=False, help='Missing help',)
        parser.add_argument('--taxonomy', action='store_true', dest='taxonomy', default=False, help='Missing help',)

    def _build_names_dict(self, path):
        """
        This method exclude any taxonomy that is not a scientific name

        :param path: full path for NCBI taxonomy folder
        :return: a dictionary with tax_id as key and taxonomy as value
        """

        name_reference = {}
        with open(join(path, "names.dmp")) as fh:
            for line in fh:
                line = line.replace("\t", '').replace("\n",'')
                _taxid, _name, _, _flag, _ = line.split("|")
                if _flag == 'scientific name':
                    name_reference[int(_taxid)] = _name

        return name_reference

    @staticmethod
    def build_division_table(path):
        print("# building division table...")
        reader = csv.reader(open(join(path, "division.dmp")), delimiter="\t")

        for line in reader:
            _id = line[0]
            _short = line[2]
            _long = line[4]
            Division.objects.get_or_create(id=_id, short=_short, long=_long)

    def build_taxonomy_base(self, path):
        print("# building taxonomy table...")
        lookup_table = self._build_names_dict(path)
        reader = csv.reader(open(join(path, "nodes.dmp")), delimiter="\t")  # has 1879344 entries

        while True:
            taxonomy_object_list = []
            next_n_lines = list(islice(reader, 400000))
            if not next_n_lines:
                break

            print("processing the next {0} lines".format(len(next_n_lines)))
            for line in next_n_lines:
                taxid = int(line[0])
                rank = line[4]  # string
                division = int(line[8])
                name = lookup_table[taxid]
                if VALID_RANKS:
                    if rank in VALID_RANKS:
                        taxonomy_object_list.append(Taxonomy(taxid=taxid, rank=rank, division_id=division, name=name))
                else:
                    taxonomy_object_list.append(Taxonomy(taxid=taxid, rank=rank, division_id=division, name=name))

            Taxonomy.objects.bulk_create(taxonomy_object_list)
        print("Total entries: {0}".format(Taxonomy.objects.count()))

    @staticmethod
    def clear_database():
        print("Removing all taxonomies entries...")
        Taxonomy.objects.all().delete()
        print("Removing all division entries...")
        Division.objects.all().delete()

    def build_lineage(self, path):
        lookup_table = self._build_names_dict(path)
        reader = csv.reader(open(join(path, "taxidlineage.dmp")), delimiter="\t")  # has 1879344 entries
        total = 0
        taxonomies_to_update = (Taxonomy.objects.filter().count())
        with transaction.atomic():
            for line in reader:
                taxid = int(line[0])
                lineage = line[2]
                if taxid in lookup_table:
                    lineage = lineage.split(" ")
                    if lineage != ['']:
                        parent = int(lineage[-2])
                        while parent not in lookup_table:
                            parent = int(lineage.pop())
                        Taxonomy.objects.filter(taxid=taxid).update(parent_id=parent)

                        total += 1
                        sys.stdout.write("\r -> Progress: {0:.1f}%".format((total / taxonomies_to_update) * 100))
                        sys.stdout.flush()

        Taxonomy.objects.filter(parent=None).update(parent_id=1)

    def handle(self, *args, **options):
        path = options['path']
        lineage = options['lineage']
        taxonomy = options['taxonomy']
        clear = options['clear']

        if taxonomy:
            start_time = datetime.datetime.now()
            self.clear_database()
            self.build_division_table(path)
            self.build_taxonomy_base(path)
            delta = (datetime.datetime.now() - start_time).seconds
            print("--taxonomy option took: {0}".format(delta))

        elif lineage:
            start_time = datetime.datetime.now()
            self.build_lineage(path)
            delta = (datetime.datetime.now() - start_time).seconds
            print("--lineage option took: {0}".format(delta))

        elif clear:
            self.clear_database()
