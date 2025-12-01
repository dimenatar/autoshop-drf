from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ViewBase(APIView):
    def __init__(self):
        super().__init__()
        self.entity_name = ''

    def get_entity_id_from_request(self, request: Request) -> int | None:
        try:
            found_id = int(request.data.get(f'{self.entity_name}_id'))
            return found_id
        except TypeError:
            return None
        except ValueError:
            return None

    def get(self, request: Request) -> Response:
        pass

    def generate_message_response_by_id(self) -> Response:
        return Response(f"Error with entity {self.entity_name}. Does not exists")

    def generate_final_response_to_single_entity(self, request: Request, func: Any) -> Response:
        found_id = self.get_entity_id_from_request(request)
        return Response(func(found_id)) if found_id else self.generate_message_response_by_id()