from .models import Candidate
from .serializers import CandidateSerializer 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Sum, Case, When, IntegerField

class CandidateAPIView(APIView):
    """
    Note: We could have simply used ModelViewSet from rest_framework.viewsets, but I wanted to handle exceptions seperately for each and show you how to create API using APIView.
    This API is created for CRUD operations on Candidate model.
    """

    def get(self, request):
        candidates = Candidate.objects.all()
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            serializer = CandidateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            candidate = Candidate.objects.get(pk=pk)
            serializer = CandidateSerializer(candidate, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Candidate.DoesNotExist:
            return Response({'error': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            candidate = Candidate.objects.get(pk=pk)
            candidate.delete()
            return Response({'msg': 'Candidate Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Candidate.DoesNotExist:
            return Response({'error': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        



class SearchCandidateAPIView(APIView):
    """
    API to search candidates by name
    """

    def get(self, request):
        name = request.query_params.get('name')
        if not name:
            return Response({'error': 'Please provide a name to search'}, status=status.HTTP_400_BAD_REQUEST)

        search_terms = name.split()
        query = Q(*[Q(name__icontains=term) for term in search_terms], _connector=Q.OR)

        candidates = Candidate.objects.filter(query).annotate(
            relevancy=Sum(
                Case(*(When(name__icontains=term, then=1) for term in search_terms), 
                     default=0, output_field=IntegerField())
            )
        ).order_by('-relevancy')

        return Response(CandidateSerializer(candidates, many=True).data)


