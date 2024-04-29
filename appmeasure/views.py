# Create your views here.
import json
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from injector import inject
from rest_framework import request
from rest_framework.views import APIView

from appmeasure.HandledError import HandledError
from appmeasure.messages import ApiMessages as msg
from appmeasure.serializer import (InUnitMeasureSerializer,
                                   OutInitMeasureWithIdSerializer)
from appmeasure.services.unitmeasure import UnitMeasureService
from unitmeasure.logger import logger


class UnitMeasureAPIView(APIView):
    """
        A view class that handles HTTP requests for various methods such as GET, POST,
        PUT, DELETE, etc. related to 'UnitMeasure' operations.
    """
    @inject
    def __init__(self, unit_measure_service: UnitMeasureService, *arg,
                 **kwargs):
        super().__init__()
        self.unit_measure_service = unit_measure_service

    def get(self, request: request.Request, unit_measure_id: str = None):
        name = request.query_params.get("name")
        if unit_measure_id is not None:
            serializer_class = OutInitMeasureWithIdSerializer(
                self.unit_measure_service.query_by_id(unit_measure_id),
                many=False
            )
        elif name is not None:
            serializer_class = OutInitMeasureWithIdSerializer(
                self.unit_measure_service.query_by_name(name), many=True

            )
        else:
            serializer_class = OutInitMeasureWithIdSerializer(
                self.unit_measure_service.query_all(), many=True

            )
        if serializer_class.data:
            return JsonResponse(
                {
                    "Code": msg.SUCCESSFUL_QUERY_CODE,
                    "Message": msg.SUCCESSFUL_QUERY_MESSAGE,
                    "unitmeasure": serializer_class.data
                }
            )
        else:
            return JsonResponse(
                {
                    "Code": msg.SUCCESSFUL_QUERY_CODE,
                    "Message": msg.SUCCESSFUL_QUERY_NO_RECORDS_FOUND
                }
            )

    def post(self, request: request.Request):
        logger.info("View: post method::: ")
        try:
            data = json.loads(request.body)
            serialized_unitmeasue = InUnitMeasureSerializer(
                data=data,
                many=False
            )
            serialized_unitmeasue.is_valid()
            self.unit_measure_service.create(
                serialized_unitmeasue.validated_data)
            return JsonResponse(
                {
                    "Code": msg.SUCCESSFUL_CREATION_CODE,
                    "Message": msg.SUCCESSFUL_CREATION_MESSAGE,
                }
            )
        except ValueError:
            logging.critical("A critical error occurred", exc_info=True)
            handled_error = HandledError()
            return JsonResponse(handled_error.get_value_error())
        except Exception:
            logging.critical("A critical error occurred", exc_info=True)
            handled_error = HandledError()
            return JsonResponse(handled_error.get_exception())

    def delete(self, _request, unit_measure_id: str):
        logger.info("View - delete method ::: ")
        try:
            result = self.unit_measure_service.delete(unit_measure_id)
            if result is True:
                return JsonResponse(
                    {
                        "Code": msg.SUCCESSFUL_DELETION_CODE,
                        "Message": msg.SUCCESSFUL_DELETION_MESSAGE,
                    }
                )
        except ObjectDoesNotExist:
            logging.critical("A critical error occurred", exc_info=True)
            handled_error = HandledError()
            return JsonResponse(handled_error.get_object_doesnot_exist())
        except Exception:
            logging.critical("A critical error occurred", exc_info=True)
            handled_error = HandledError()
            return JsonResponse(handled_error.get_exception())

    def put(self, request: request.Request, unit_measure_id: str):
        logger.info("View - put method")
        try:
            request_data = request.data
            serialized_unit_measure = InUnitMeasureSerializer(
                data=request_data,
                many=False,
            )
            if serialized_unit_measure.is_valid():
                unit_measure = self.unit_measure_service.update(
                    serialized_unit_measure.validated_data, unit_measure_id)
                return JsonResponse(
                    {
                        "Code": msg.SUCCESSFUL_UPDATE_CODE,
                        "description": msg.SUCCESSFUL_UPDATE_MESSAGE,
                        "UnitMeasure": unit_measure
                    }
                )
            else:
                handled_error = HandledError()
                value_error = handled_error.get_value_error()
                value_error["Message"] += str(serialized_unit_measure.errors)
                return JsonResponse(value_error)
        except ObjectDoesNotExist:
            logging.critical("A critical error occurred", exc_info=True)
            handled_error = HandledError()
            return JsonResponse(handled_error.get_object_doesnot_exist())
        except ValueError:
            logging.critical("A critical error occurred", exc_info=True)
            handled_error = HandledError()
            return JsonResponse(handled_error.get_value_error())
        except Exception:
            logging.critical("A critical error occurred", exc_info=True)
            handled_error = HandledError()
        return JsonResponse(handled_error.get_exception())
