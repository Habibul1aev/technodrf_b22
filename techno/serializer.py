from rest_framework import serializers
from techno.models import Product
from account.serializer import DataUserSerializer

class CategorySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)

class CharacteristicSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=50)
#     price = serializers.DecimalField(max_digits=10, decimal_places=2,)
#     category = CategorySerializer()
#     characteristic = CharacteristicSerializer(many=True)




class ProductSerializer(serializers.ModelSerializer):
    user = DataUserSerializer()
    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Product
        fields = '__all__'

        

    # def create(self, validated_data):
    #     characteristic = validated_data.pop('characteristic', [])
    #     product = Product.objects.create(**validated_data)
    #     product.characteristic.set(characteristic)
    #     return product

    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.category = validated_data.get('category', instance.category)
    #     instance.price = validated_data.get('price', instance.price)
    #     characteristic = validated_data.get('characteristic')
    #     instance.save()
    #     if characteristic is not None:
    #         instance.characteristic.set(characteristic)

    #     return instance



        

