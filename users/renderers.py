import json
from typing import Any, Optional, Dict

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data: dict, media_type:str='', renderer_context:Optional[Dict[str, Any]]=None) -> Any:
        errors = data.get('errors', None)

        token = data.get('token', None)

        if errors is not None:
            return super(UserJSONRenderer, self).render(data)

        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')

        return json.dumps({
            'user': data
        })