from rest_framework import serializers
from .models import UserWallet, TokenLedger
from django.contrib.auth.models import User
from django.db import models

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        fields = ['user', 'public_key', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    public_key = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[('student', 'Student'), ('validator', 'Validator')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'public_key', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        UserWallet.objects.create(
            user=user,
            public_key=validated_data['public_key'],
            role=validated_data['role']
        )
        return user
    
class UserInfoSerializer(serializers.ModelSerializer):
    wallet = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    transactions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'wallet', 'balance', 'transactions']

    def get_wallet(self, user):
        try:
            wallet = user.userwallet
            return {
                "public_key": wallet.public_key,
                "role": wallet.role,
                "created_at": wallet.created_at
            }
        except UserWallet.DoesNotExist:
            return None

    def get_balance(self, user):
        wallet = getattr(user, "userwallet", None)
        if wallet:
            total = wallet.transactions.aggregate(total=models.Sum('amount'))['total'] or 0
            return total
        return 0

    def get_transactions(self, user):
        wallet = getattr(user, "userwallet", None)
        if not wallet:
            return []

        return [
            {
                "amount": tx.amount,
                "source_block_index": tx.source_block_index,
                "timestamp": tx.timestamp,
                "reason": tx.reason
            }
            for tx in wallet.transactions.order_by('-timestamp')
        ]
