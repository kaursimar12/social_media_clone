from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Thread, ThreadLike, Repost
from .serializers import ThreadSerializer, LikeSerializer
import uuid

# View for listing all threads
class ThreadListView(ListAPIView):
    queryset = Thread.objects.all().order_by('-created_at')
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]

# View for creating a new thread
class ThreadCreateView(CreateAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# View for retrieving a specific thread by UUID
class ThreadRetrieveView(RetrieveAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Override to handle UUIDs
        uuid_value = self.kwargs.get('pk')
        return Thread.objects.get(pk=uuid_value)

# View for updating a specific thread by UUID
class ThreadUpdateView(UpdateAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Override to handle UUIDs
        uuid_value = self.kwargs.get('pk')
        return Thread.objects.get(pk=uuid_value)

    def perform_update(self, serializer):
        thread = self.get_object()
        if thread.user != self.request.user:
            raise PermissionDenied('You do not have permission to edit this thread.')
        serializer.save()

# View for deleting a specific thread by UUID
class ThreadDeleteView(DestroyAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Override to handle UUIDs
        uuid_value = self.kwargs.get('pk')
        return Thread.objects.get(pk=uuid_value)

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied('You do not have permission to delete this thread.')
        instance.delete()

# View for toggling like/unlike a thread by UUID
class ThreadLikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, thread_id):
        user = request.user
        try:
            thread = Thread.objects.get(id=thread_id)
        except Thread.DoesNotExist:
            return Response({'detail': 'Thread not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        like, created = ThreadLike.objects.get_or_create(user=user, thread=thread)
        
        if not created:
            # If the like already exists, delete it (unlike)
            like.delete()
            return Response({'detail': 'Like removed.'}, status=status.HTTP_204_NO_CONTENT)
        
        # If the like did not exist, create it (like)
        return Response({'detail': 'Thread liked.'}, status=status.HTTP_201_CREATED)


# class RepostThreadView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, thread_id):
#         user = request.user
#         try:
#             thread = Thread.objects.get(id=thread_id)
#         except Thread.DoesNotExist:
#             return Response({'detail': 'Thread not found.'}, status=status.HTTP_404_NOT_FOUND)
        
#         # Check if the user has already reposted this thread
#         if Repost.objects.filter(original_thread=thread, reposting_user=user).exists():
#             return Response({'detail': 'You have already reposted this thread.'}, status=status.HTTP_400_BAD_REQUEST)

#         # Create a new repost
#         Repost.objects.create(original_thread=thread, reposting_user=user)
#         return Response({'detail': 'Thread reposted.'}, status=status.HTTP_201_CREATED)


class RepostThreadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, thread_id):
        user = request.user
        try:
            thread = Thread.objects.get(id=thread_id)
        except Thread.DoesNotExist:
            return Response({'detail': 'Thread not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is trying to repost their own thread
        if thread.user == user:
            return Response({'detail': 'You cannot repost your own thread.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the user has already reposted this thread
        if Repost.objects.filter(original_thread=thread, reposting_user=user).exists():
            return Response({'detail': 'You have already reposted this thread.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new repost
        Repost.objects.create(original_thread=thread, reposting_user=user)
        return Response({'detail': 'Thread reposted.'}, status=status.HTTP_201_CREATED)
    
    