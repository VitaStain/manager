from django.db import transaction
from rest_framework import serializers

from .models import Balance, Category, Profile, Transaction


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        password2 = validated_data['password2']
        if (email and Profile.objects.filter(email=email).exclude(username=username).exists()):
            raise serializers.ValidationError(
                {'email': 'Email addresses must be unique.'}
            )
        if password != password2:
            raise serializers.ValidationError({'password': 'The two passwords differ.'})
        user = Profile(username=username, email=email)
        user.set_password(password)
        user.save()
        return user


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['balance']


class TransactionSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Transaction
        fields = ['action', 'summa', 'time', 'category', 'organization', 'description', 'status']

    def create(self, validated_data):
        user = self._kwargs['context']['request'].user
        validated_data['user'] = user
        with transaction.atomic():
            sp = transaction.savepoint()
            obj = Transaction.objects.create(**validated_data)
            balance = user.balance
            if obj.action == 'debit':
                balance.balance -= obj.summa
            elif obj.action == 'replenish':
                balance.balance += obj.summa
            balance.save()
            if balance.balance < 0:
                obj.status = '403'
                transaction.savepoint_rollback(sp)
        return obj


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def create(self, validated_data):
        user = self._kwargs['context']['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    balance = BalanceSerializer(read_only=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'balance', 'categories']
