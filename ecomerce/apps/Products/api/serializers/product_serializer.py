from apps.Products.models import Product
from rest_framework import serializers



class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ('state','created_date','modified_date','deleted_date')

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name':instance.name,
            'descripcion':instance.description,
            'image': instance.image if instance.image != "" else "",
            'category': instance.category.description,
            'Measue_unit':instance.Measue_unit.description
        }