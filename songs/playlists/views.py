from django.shortcuts import render
from django.http import HttpResponse
from .models import Song, Playlist
from rest_framework.decorators import api_view, permission_classes
from .serializers import SongSerializer, PlaylistSerializer, AllPlaylistsSerializer, PlaylistAndSongSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "username" : serializer.data.get('username'),
                "email" : serializer.data.get('email'),
                "first_name" : serializer.data.get('first_name'),
                "last_name" : serializer.data.get('last_name')
                }, 
            status=status.HTTP_201_CREATED
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def songs(request):
    if request.method == 'GET':
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"Error": "the data is not in valid form"}, serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def song_details(request, id):
    try:
        song = Song.objects.get(id = id)
    except Song.DoesNotExist:
        return Response({"Error" : "song not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        playlists = Playlist.objects.all()
        for x in playlists:
            x.songs.remove(song)
        song.playlists.clear()
        song.delete()
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = SongSerializer(song, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def playlist_details(request, id):
    try:
        playlist = Playlist.objects.get(id = id)
    except Playlist.DoesNotExist:
        return Response({"Error" : "playlist not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        flag = request.GET.get('songs', None)
        if flag is not None:
            if flag == 'true':
                for x in playlist.songs.all():
                    x.playlists.clear()
                    x.delete()
        playlist.delete()
        return Response(status=status.HTTP_200_OK)
    if request.method == 'PUT':
        serializer = PlaylistSerializer(playlist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'POST'])
def playlists(request):
    if request.method == 'GET':
        all_playlists = Playlist.objects.all()
        serializer = AllPlaylistsSerializer(all_playlists, many= True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_to_playlist(request):
    serializer = PlaylistAndSongSerializer(data=request.data)
    if serializer.is_valid():
        playlistId = serializer.data.get('playlistId')
        songId = serializer.data.get('songId')
        try:
            playlist = Playlist.objects.get(id = playlistId)
        except Playlist.DoesNotExist:
            return Response({"Error": "playlist not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            song = Song.objects.get(id=songId)
        except Song.DoesNotExist:
            return Response({"Error" : "song not found"}, status=status.HTTP_404_NOT_FOUND)
        if song in playlist.songs.all():
            return Response({"Error" : "The song is already in the playlist"}, status=status.HTTP_409_CONFLICT)
        playlist.songs.add(song)
        return Response(status=status.HTTP_201_CREATED)
    return Response({"Error" : "The data is not in valid form"},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def remove_from_playlist(request):
    serializer = PlaylistAndSongSerializer(data=request.data)
    if serializer.is_valid():
        playlistId = serializer.data.get('playlistId')
        songId = serializer.data.get('songId')
        try:
            playlist = Playlist.objects.get(id = playlistId)
        except Playlist.DoesNotExist:
            return Response({"Error" : "playlist not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            song = Song.objects.get(id=songId)
        except Song.DoesNotExist:
            return Response({"Error" : "song not found"}, status=status.HTTP_404_NOT_FOUND)
        if song not in playlist.songs.all():
            return Response({"Error" : "the song is not present in the playlist" }, status=status.HTTP_404_NOT_FOUND)
        playlist.songs.remove(song)
        return Response(status=status.HTTP_200_OK)
    return Response({"Error" : "the data is not in valid form"}, status=status.HTTP_400_BAD_REQUEST)
    