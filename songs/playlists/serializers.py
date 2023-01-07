from django.db import models
from rest_framework import serializers
from .models import Song, Playlist
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        write_only_fields = ['password']
        extra_kwargs = {
            'first_name' : {'required' : False},
            'last_name' : {'required' : False}
        }
        
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        first_name = validated_data.get('first_name')
        if first_name is not None:
            user.first_name = first_name
        last_name = validated_data.get('last_name')
        if last_name is not None:
            user.last_name = last_name
        user.save()
        return user

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'artist', 'album']

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'name', 'songs']
        depth = 1
class AllPlaylistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'name']
        
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['songs'] = instance.songs.count()
        return representation


class PlaylistAndSongSerializer(serializers.Serializer):
    playlistId = serializers.IntegerField()
    songId = serializers.IntegerField()
    
    