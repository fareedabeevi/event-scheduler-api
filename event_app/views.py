
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from django.shortcuts import render
from.serializer import EventSerializerAdd,EventSerializerGet,SessionSerializer,SpeakerSerializer
from.models import CustomUser,Events,Speakers
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]  # Allow anyone to access login API


def home(request):
    return JsonResponse({"message": "Welcome to the Event App API"})


@api_view(['POST'])
def register_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    if not (email and password and first_name and last_name):
       return Response({"error": "All fields are required"}, status=400)
    
    if CustomUser.objects.filter(email=email).exists():
       return Response({"error": "User already exists"}, status=400)
    
    user = CustomUser.objects.create_user(
        email=email, password=password, first_name=first_name, last_name=last_name
    )
    return Response({"message": "User created successfully"}, status=201)

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
      refresh = RefreshToken.for_user(user)
      return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
})
    return Response({"error": "Invalid credentials"}, status=401)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": f"Hello {request.user.email}, this is a protected view!"}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_event(request):
    serializer = EventSerializerAdd(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": f"Event Created" },status= status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_event(request):
    events = Events.objects.all().order_by('date')
    serializer = EventSerializerAdd(events,many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_event(request, pk):
    try:
        event = Events.objects.get(id=pk)
    except Events.DoesNotExist:
        return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

    # Use the serializer with partial=True to allow partial updates
    serializer = EventSerializerAdd(event, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Event updated successfully", "event": serializer.data}, status=status.HTTP_200_OK)
    
    # Handle invalid data
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event(request, pk):
    try:
        event = Events.objects.get(id=pk)
        event.delete()
        return Response({"message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Events.DoesNotExist:
        return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_session(request):
    serializer = SessionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": f"Session Created" },status= status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_speaker(request):
    serializer = SpeakerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": f"Speaker Created" },status= status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_sessions(request):
    events = Events.objects.select_related()
    serializer = EventSerializerGet(events,many=True)
    print(serializer.data)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_speakers(request):
    speakers=Speakers.objects.all()
    print(Speakers.objects.all())
    serializer = SpeakerSerializer(speakers,many=True)
    print(serializer.data)
    return Response(serializer.data)