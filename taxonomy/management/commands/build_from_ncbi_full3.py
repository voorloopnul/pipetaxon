import csv
import datetime
import sys
from itertools import islice
from django.core.management import BaseCommand
from os.path import join
from django.db import transaction
from django.db.models import Case, When

from taxonomy.models import Taxonomy, Division, VALID_RANKS


class Command(BaseCommand):
    help = 'Build the database taxonomy from NCBI data'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

        parser.add_argument(
            '--clear',
            action='store_true',
            dest='clear',
            default=False,
            help='Clear database',
        )

        parser.add_argument(
            '--lineage',
            action='store_true',
            dest='lineage',
            default=False,
            help='Do not rebuild the taxonomy database',
        )

        parser.add_argument(
            '--taxonomy',
            action='store_true',
            dest='taxonomy',
            default=False,
            help='Add taxonomy from NCBI taxdump',
        )

        parser.add_argument(
            '--division',
            action='store_true',
            dest='division',
            default=False,
            help='Add division',
        )

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

    def rebuild_division_table(self, path):
        print("# rebuild division table")
        reader = csv.reader(open(join(path, "division.dmp")), delimiter="\t")

        for line in reader:
            _id = line[0]
            _short = line[2]
            _long = line[4]
            Division.objects.get_or_create(id=_id, short=_short, long=_long)

    def rebuild_taxonomy_base(self, path):
        print("# rebuild taxonomy database")
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
                if rank in VALID_RANKS:
                    taxonomy_object_list.append(Taxonomy(taxid=taxid, rank=rank, division_id=division, name=name))
            Taxonomy.objects.bulk_create(taxonomy_object_list)
        print("Total entries: {0}".format(Taxonomy.objects.count()))

    def rebuild_lineage(self):
        print("# rebuild taxonomy lineage")
        print(Taxonomy.objects.filter(rank='species').count())
        print(Taxonomy.objects.filter(rank='species', parent=None).count())

        total = 0
        with transaction.atomic():
            for taxonomy in Taxonomy.objects.filter(rank='species'):
                total +=1
                sys.stdout.write("\r{0}".format(total))
                sys.stdout.flush()

                taxid_list = []
                parent_taxid = taxonomy.taxid
                while parent_taxid !=1:
                    parent_taxid = self.parent_mapping[parent_taxid]
                    taxid_list.append(parent_taxid)

                preserved = Case(*[When(taxid=pk, then=pos) for pos, pk in enumerate(taxid_list)])

                #lineage = Taxonomy.objects.filter(taxid__in=taxid_list).order_by(preserved)
                #for parent in lineage:
                #    taxonomy.parent = parent
                #    if parent.parent:
                #        break
                #    taxonomy.save()
                #    taxonomy = parent

                #parent = Taxonomy.objects.filter(taxid__in=taxid_list).order_by(preserved).first()


        print("")

    def _clear_database(self):
        print("Clear database")
        Taxonomy.objects.all().delete()

    def handle(self, *args, **options):
        path = options['path']
        lineage = options['lineage']
        taxonomy = options['taxonomy']
        division = options['division']
        clear = options['clear']

        if lineage:
            start_time = datetime.datetime.now()
            self._build_mappings(path)
            self.rebuild_lineage()
            seconds = (datetime.datetime.now() - start_time).seconds
            print("Lineage took: {0}".format(seconds))
        elif taxonomy:
            start_time = datetime.datetime.now()
            self.rebuild_taxonomy_base(path)
            seconds = (datetime.datetime.now() - start_time).seconds
            print("Taxonomy took: {0}".format(seconds))
        elif division:
            self._clear_database()
            self.rebuild_division_table(path)
        elif clear:
            self._clear_database()
