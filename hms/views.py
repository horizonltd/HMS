from datetime import datetime, timedelta

from django.db.models import Sum
from rest_framework import viewsets, generics

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from hms.models import *
from hms.serializers import *


class CompanyViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            company = Company.objects.all()
            serializer = CompanySerializer(company, many=True, context={"request": request})
            response_dict = {"error": False, "message": "All Company Data List", "data": serializer.data}
        except:
            response_dict = {"error": True, "message": "Data Can't be Fetched"}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = CompanySerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Data Save Successfully."}
        except:
            dict_response = {"error": True, "message": "Data Can't be Save Due to Data Entry Issues."}
        return Response(dict_response)

    def update(self, request, pk=None):
        try:
            queryset = Company.objects.all()
            company = get_object_or_404(queryset, pk=pk)
            serializer = CompanySerializer(company, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Data Updated Successfully."}
        except:
            dict_response = {"error": True, "message": "Data Can't be Updated Due to Data Entry Issues."}
        return Response(dict_response)


class CompanyBankViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = CompanyBankSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Data Save Successfully."}
        except:
            dict_response = {"error": True, "message": "Data Can't be Save Due to Data Entry Issues."}
        return Response(dict_response)

    def list(self, request):
        try:
            companybank = CompanyBank.objects.all()
            serializer = CompanyBankSerializer(companybank, many=True, context={"request": request})
            response_dict = {"error": False, "message": "Data fetched successfully", "data": serializer.data}
        except:
            response_dict = {"error": True, "message": "Data can't be fetched"}
        return Response(response_dict)

    def retrieve(self, request, pk=None):
        try:
            queryset = CompanyBank.objects.all()
            companybank = get_object_or_404(queryset, pk=pk)
            serializer = CompanyBankSerializer(companybank, context={"request": request})
            response_dict = {"error": False, "message": "Record fetched successfully.", "data": serializer.data}
        except:
            response_dict = {"error": True, "message": "Record  can't fetched."}
        return Response(response_dict)

    def update(self, request, pk=None):
        try:
            queryset = CompanyBank.objects.all()
            companybank = get_object_or_404(queryset, pk=pk)
            serializer = CompanySerializer(companybank, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Data Updated Successfully."}
        except:
            dict_response = {"error": True, "message": "Data Can't be Updated Due to Data Entry Issues."}
        return Response(dict_response)


class CompanyNameViewSet(generics.ListAPIView):
    serializer_class = CompanySerializer

    def get_queryset(self):
        name = self.kwargs["name"]
        return Company.objects.filter(name=name)


class MedicineViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = MedicineSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Accessing Serializer ID of the current inserted data
            medicine_id = serializer.data['id']
            print(medicine_id)

            medicine_details_list = []

            print("Medicine Data Details")
            for medicine_detail in request.data["medicine_details"]:
                medicine_detail["medicine_id"] = medicine_id
                medicine_details_list.append(medicine_detail)
                print(medicine_detail)

            serializer2 = MedicalDetailsSerializer(data=medicine_details_list, many=True, context={"request": request})
            serializer2.is_valid(raise_exception=True)
            serializer2.save()

            dict_response = {"error": False, "message": "Data Save Successfully."}
        except:
            dict_response = {"error": True, "message": "Data can't be save due to data entry issues."}
        return Response(dict_response)

    def list(self, request):
        try:
            medicine = Medicine.objects.all()
            serializer = MedicineSerializer(medicine, many=True, context={"request": request})

            medicine_data = serializer.data
            new_medicine_list = []

            # Getting all the medicineDetails of the current medicineID
            for medicine in medicine_data:
                medicine_details = MedicalDetails.objects.filter(medicine_id=medicine["id"])
                medicine_details_serializers = SimpleMedicalDetailsSerializer(medicine_details, many=True)
                medicine["medicine_details"] = medicine_details_serializers.data
                new_medicine_list.append(medicine)

            response_dict = {"error": False, "message": "Data fetched successfully", "data": serializer.data}
        except:
            response_dict = {"error": True, "message": "Data can't be fetched"}
        return Response(response_dict)

    def retrieve(self, request, pk=None):
        try:
            queryset = Medicine.objects.all()
            medicine = get_object_or_404(queryset, pk=pk)
            serializer = MedicineSerializer(medicine, context={"request": request})

            # Fetching Single DATA
            serializer_data = serializer.data

            medicine_details = MedicalDetails.objects.filter(medicine_id=serializer_data["id"])
            medicine_details_serializers = SimpleMedicalDetailsSerializer(medicine_details, many=True)
            serializer_data["medicine_details"] = medicine_details_serializers.data

            response_dict = {"error": False, "message": "Record fetched successfully.", "data": serializer_data}
            return Response(response_dict)
        except:
            response_dict = {"error": True, "message": "Record  can't fetched."}
        return Response(response_dict)

    def update(self, request, pk=None):
        try:
            queryset = Medicine.objects.all()
            medicine = get_object_or_404(queryset, pk=pk)
            serializer = MedicineSerializer(medicine, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Data Updated Successfully."}
        except:
            dict_response = {"error": True, "message": "Data can't be updated due to data entry issues."}
        return Response(dict_response)


company_list = CompanyViewSet.as_view({"get": "list"})
company_create = CompanyViewSet.as_view({"post": "create"})
company_update = CompanyViewSet.as_view({"put": "update"})

