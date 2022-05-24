from multiprocessing import allow_connection_pickling
from rest_framework import serializers
from django.db import models
from .models import User, Profile, Book, Journal


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.pop('password')
        user = User(email=email)
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    bio = serializers.CharField(max_length=500, required=False, allow_blank=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def update(self, instance: Profile, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance
    

class BaseBookJournalSerializer(serializers.Serializer):
    """ Base serializer of information for Course, Lesson, Task models"""
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=300, required=True, allow_blank=False)
    price = serializers.IntegerField(min_value=0, required=True)
    desciprion = serializers.CharField(max_length=2000, required=False, allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        fields = ('id', 'name', 'price', 'description', 'created_at')


class BookSerializer(serializers.ModelSerializer, BaseBookJournalSerializer):
    num_pages = serializers.IntegerField(min_value=0, required=True)
    genre = serializers.CharField(max_length=300, required=True, allow_blank=False)
    
    class Meta:
        model = Book
        fields = BaseBookJournalSerializer.Meta.fields + ('num_pages', 'genre')
    

class JournalSerializer(serializers.ModelSerializer, BaseBookJournalSerializer):
    type = serializers.ChoiceField(choices=Journal.TYPE_CHOICES, default=Journal.BULLET)
    publisher = serializers.CharField(max_length=300, required=True, allow_blank=False)
    
    class Meta:
        model = Journal
        fields = BaseBookJournalSerializer.Meta.fields + ('type', 'publisher')
        