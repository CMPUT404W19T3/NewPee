from rest_framework.decorators import renderer_classes, api_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
import coreapi
from rest_framework import response

@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    schema = coreapi.Document(
    title='NewPee API Documentation',
    url='https://newpee.herokuapp.com/',
    content={
        'search': coreapi.Link(
            url='api/posts/',
            action='get',
            fields=[
                coreapi.Field(
                    name='UUID',
                    required=True,
                    location='query',
                    description='A string that represents a UUID'
                ),
            ],
            description='Return all authors'
        )
    }
)
    # schema = generator.get_schema(request)
    return response.Response(schema)