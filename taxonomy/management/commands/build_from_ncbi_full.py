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

    def _build_mappings(self, path):
        self.parent_mapping = {}
        self.rank_mapping = {}

        reader = csv.reader(open(join(path, "nodes.dmp")), delimiter="\t")
        for row in reader:
            taxid = int(row[0])
            parent = int(row[2])
            rank = row[4]
            self.parent_mapping[taxid] = parent
            self.rank_mapping[taxid] = rank

        for taxid in self.parent_mapping:
            parent = self.parent_mapping[taxid]
            parent_rank = self.rank_mapping[parent]
            if VALID_RANKS:
                if parent_rank in VALID_RANKS:
                    pass
                else:
                    while parent != 1:
                        parent = self.parent_mapping[parent]
                        parent_rank = self.rank_mapping[parent]
                        if parent_rank in VALID_RANKS:
                            break
            self.parent_mapping[taxid] = parent

    @staticmethod
    def build_division_table(path):
        print("# building division table...")
        reader = csv.reader(open(join(path, "division.dmp")), delimiter="\t")

        for line in reader:
            _id = line[0]
            _short = line[2]
            _long = line[4]
            Division.objects.get_or_create(id=_id, short=_short, long=_long)

        #Taxonomy.objects.create(name='no rank', rank='no rank', division_id=0, taxid=1)

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

    def build_lineage(self):
        if VALID_RANKS:
            _VALID_RANKS = VALID_RANKS
        else:
            _VALID_RANKS = list(set(Taxonomy.objects.all().values_list('rank', flat=True)))

        for rank in _VALID_RANKS:
            entries = Taxonomy.objects.filter(rank=rank).count()
            print("\n# Building taxonomy lineage for rank {0} ( {1} entries )".format(rank, entries))
            taxonomies_to_update = (Taxonomy.objects.filter(rank=rank, parent=None).count())

            total = 0
            with transaction.atomic():
                for taxonomy in Taxonomy.objects.filter(rank=rank).iterator(100000):
                    total += 1
                    sys.stdout.write("\r -> Progress: {0:.1f}%".format((total/taxonomies_to_update)*100))
                    sys.stdout.flush()

                    taxonomy.parent_id = self.parent_mapping[taxonomy.taxid]
                    taxonomy.save()
        print("")

    @staticmethod
    def clear_database():
        print("Removing all taxonomies entries...")
        Taxonomy.objects.all().delete()
        print("Removing all division entries...")
        Division.objects.all().delete()

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
            self._build_mappings(path)
            self.build_lineage()
            delta = (datetime.datetime.now() - start_time).seconds
            print("--lineage option took: {0}".format(delta))

        elif clear:
            self.clear_database()
