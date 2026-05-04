from rest_framework import serializers
from market_app.models import Market, Seller, Product


class MarketSerializer(serializers.ModelSerializer):

    sellers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Seller.objects.all())

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
    markets_ids = serializers.PrimaryKeyRelatedField(
        queryset=Market.objects.all(), many=True, write_only=True, source='markets')
    market_count = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ['id', 'name', 'contact_info',
                  'market_count', 'markets_ids', 'markets']

    def get_market_count(self, obj):
        return obj.markets.count()


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
