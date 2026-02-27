# from rest_framework import serializers
# from learning.profile_model import Portfolio,Instrument,PortfolioInstrument


# class InstrumentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Instrument
#         fields = ['id','name','symbol']

# class PortfolioInstrumentSerializer(serializers.ModelSerializer):
#     instrument = InstrumentSerializer(read_only=True)

#     class Meta:
#         model = PortfolioInstrument
#         fields = ['id','portfolio','instrument','quantity','date_added']

# class PortfolioSerializer(serializers.ModelSerializer):
#     instruments = PortfolioInstrumentSerializer(source='portfolioinstrument_set', many=True)
#     class Meta:
#         model = Portfolio
#         fields = ['id','name','instruments']
