from rest_framework import request, serializers
from market_app.models import Market, Seller, Product


class MarketSerializer(serializers.HyperlinkedModelSerializer):
    
    sellers = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='seller_single')
    
    class Meta:
        model = Market
        fields = '__all__'
    def validate_name(self, value):
        errors = []
        if 'X' in value:
            errors.append("Der Name darf kein 'X' enthalten.")
        if 'Y' in value:
            errors.append("Der Name darf kein 'Y' enthalten.")
        if errors:
            raise serializers.ValidationError(errors)

        return value
    
class SellerSerializer(serializers.ModelSerializer):
    markets = MarketSerializer(read_only=True, many=True)
    markets_ids = serializers.PrimaryKeyRelatedField(queryset=Market.objects.all(), many=True, write_only=True, source='markets')
    market_count = serializers.SerializerMethodField()
    class Meta:
        model = Seller
        fields = ['id', 'name','contact_info','market_count', 'markets_ids', 'markets']
        
    def get_market_count(self, obj):
        return obj.markets.count()   
        
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    description = serializers.CharField()
    seller_id = serializers.IntegerField(write_only=True)
    market_id = serializers.IntegerField(write_only=True)
    
    def validate_seller_id(self, value):
        if not Seller.objects.filter(id=value).exists():
            raise serializers.ValidationError("Der Verkäufer existiert nicht.")
        return value
    
    def validate_market_id(self, value):
        if not Market.objects.filter(id=value).exists():
            raise serializers.ValidationError("Der Markt existiert nicht.")
        return value
    
    def create(self, validated_data):
        seller_id = validated_data.pop('seller_id')
        market_id = validated_data.pop('market_id')
        product = Product.objects.create(**validated_data, seller_id=seller_id, market_id=market_id)
        return product
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        seller_id = validated_data.get('seller_id')
        market_id = validated_data.get('market_id')
        
        if seller_id:
            if not Seller.objects.filter(id=seller_id).exists():
                raise serializers.ValidationError("Der Verkäufer existiert nicht.")
            instance.seller_id = seller_id
        
        if market_id:
            if not Market.objects.filter(id=market_id).exists():
                raise serializers.ValidationError("Der Markt existiert nicht.")
            instance.market_id = market_id
        
        instance.save()
        return instance