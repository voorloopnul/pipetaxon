from rest_framework import serializers
from taxonomy.models import Taxonomy


class TaxonomySerializer(serializers.ModelSerializer):

    class Meta:
        model = Taxonomy
        fields = ('taxid', 'rank', 'name', 'parent', 'division')


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, taxonomy):
        # prevent lineage to keep iterating over taxid 1 ( because it is it own parent )
        if taxonomy.taxid == 1:
            return None
        serializer = self.parent.__class__(taxonomy, context=self.context)
        return serializer.data


class NestedTaxonomySerializer(serializers.ModelSerializer):
    parent = RecursiveSerializer(many=False)

    class Meta:
        model = Taxonomy
        fields = ('taxid', 'rank', 'name', 'division', 'parent')
