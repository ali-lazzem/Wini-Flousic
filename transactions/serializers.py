from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
    
    def validate(self, data):
        if data['type'] == 'expense' and not data.get('category'):
            raise serializers.ValidationError({"category": "Category is required for expenses."})
        return data