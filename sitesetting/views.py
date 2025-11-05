from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contact
from .serializers import ContactSerializer

class ContactView(APIView):
    # Fetch all contacts
    def get(self, request, pk=None):
        try:
            if pk:  # Fetch single contact
                contact = Contact.objects.get(pk=pk)
                serializer = ContactSerializer(contact)
                return Response({
                    "success": True,
                    "message": "Contact fetched successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            else:  # Fetch all contacts
                contacts = Contact.objects.all().order_by('-created_at')
                serializer = ContactSerializer(contacts, many=True)

                if contacts.exists():
                    return Response({
                        "success": True,
                        "message": "Contacts fetched successfully",
                        "count": contacts.count(),
                        "data": serializer.data
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "success": True,
                        "message": "No contacts found",
                        "count": 0,
                        "data": []
                    }, status=status.HTTP_200_OK)

        except Contact.DoesNotExist:
            return Response({
                "success": False,
                "message": f"Contact with id {pk} not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "success": False,
                "message": "Something went wrong while fetching contacts",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Create a new contact
    def post(self, request):
        try:
            serializer = ContactSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True,
                    "message": "Contact created successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "success": False,
                    "message": "Validation failed",
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "success": False,
                "message": "Something went wrong while creating contact",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        try:
            contact = Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            return Response({
                "success": False,
                "message": f"Contact with id {pk} not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Only update 'status'
        status_value = request.data.get('status')
        if not status_value:
            return Response({
                "success": False,
                "message": "Status field is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        contact.status = status_value
        contact.save()

        serializer = ContactSerializer(contact)
        return Response({
            "success": True,
            "message": "Contact status updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        try:
            contact = Contact.objects.get(pk=pk)
            contact.delete()
            return Response({
                "success": True,
                "message": "Contact deleted successfully"
            }, status=status.HTTP_200_OK)
        except Contact.DoesNotExist:
            return Response({
                "success": False,
                "message": f"Contact with id {pk} not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "success": False,
                "message": "Something went wrong while deleting contact",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)