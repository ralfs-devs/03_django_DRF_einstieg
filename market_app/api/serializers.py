from rest_framework import request, serializers
from market_app.models import Market, Seller, Product


class MarketSerializer(serializers.ModelSerializer):

    sellers = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='seller_single')

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


class MarkethyperlinkedSerializer(MarketSerializer, serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Market
        fields = ['id', 'name', 'location',
                  'description', 'sellers', 'url', 'net_worth']


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

    sellers = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='seller_single')

    class Meta:
        model = Product
        fields = '__all__'


class ProducthyperlinkedSerializer(ProductSerializer, serializers.HyperlinkedModelSerializer):
    # def __init__(self, *args, **kwargs):
    # # Don't pass the 'fields' arg up to the superclass
    # fields = kwargs.pop('fields', None)

    # # Instantiate the superclass normally
    # super().__init__(*args, **kwargs)

    # if fields is not None:
    #     # Drop any fields that are not specified in the `fields` argument.
    #     allowed = set(fields)
    #     existing = set(self.fields)
    #     for field_name in existing - allowed:
    #         self.fields.pop(field_name)

    class Meta:
        model = Product
        fields = '__all__'
