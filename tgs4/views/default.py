from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import SQLAlchemyError

from ..models.user import User
from ..models.movie import Movie

@view_config(route_name='home', renderer='pwl_tugas4:templates/mytemplate.jinja2')
def my_view(request):
    try:
        user = request.dbsession.query(User).filter_by(name='one').one()
    except SQLAlchemyError:
        return Response('error', content_type='text/plain', status=500)
    
    return {'user': user, 'project': 'pwl tugas4'}
