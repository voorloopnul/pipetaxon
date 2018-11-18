from django.db import models
from django.utils.functional import cached_property


DIVISION = (
    (0, "BCT"),   # Bacteria
    (1, "INV"),   # Invertebrates
    (2, "MAM"),   # Mammals
    (3, "PHG"),   # Phages
    (4, "PLN"),   # Plants and Fungi
    (5, "PRI"),   # Primates
    (6, "ROD"),   # Rodents
    (7, "SYN"),   # Synthetic and Chimeric
    (8, "UNA"),   # Unassigned
    (9, "VRL"),   # Viruses
    (10, "VRT"),  # Vertebrates
    (11, "ENV"),  # Environmental Samples
)

RANK = (
    (0, "no rank"),
    (1, "superkingdom"),
    (2, "kingdom"),
    (3, "phylum"),
    (4, "class"),
    (5, "order"),
    (6, "family"),
    (7, "genus"),
    (8, "species"),

)


def rank_container():
    return {
        "kingdom": None,
        "phylum": None,
        "class": None,
        "order": None,
        "family": None,
        "genus": None,
        "species": None
    }


class Division(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=False)
    short = models.CharField(max_length=3)
    long = models.CharField(max_length=30)


class Taxonomy(models.Model):
    class Meta:
        ordering = ("taxid", )

    taxid = models.IntegerField(null=False, primary_key=True, auto_created=False)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    rank = models.CharField(max_length=50, db_index=True)
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    updated_at = models.DateField(null=True, auto_now=True)

    def __str__(self):
        return "{0}:{1}".format(self.rank, self.taxid)

    @cached_property
    def lineage(self):
        entry = self
        lineage = [self]
        while entry.parent.taxid != 1:
            lineage.append(entry.parent)
            entry = entry.parent
        return lineage

    def show_tree(self):
        return self.lineage

    def _check_rank(self, rank):
        for entry in self.lineage:
            if entry.rank == rank:
                return entry
        return False

    def species(self):
        return self._check_rank('species')

    def genus(self):
        return self._check_rank('genus')

    def family(self):
        return self._check_rank('family')

    def order(self):
        return self._check_rank('order')

    def klass(self):
        return self._check_rank('class')

    def phylum(self):
        return self._check_rank('phylum')

    def kingdom(self):
        return self._check_rank('kingdom')

    def superkingdom(self):
        return self._check_rank('superkingdom')