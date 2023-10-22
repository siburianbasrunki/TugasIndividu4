import jwt
from pyramid.view import view_config
from pyramid.response import Response
from ..models import User

# Kunci rahasia untuk tanda tangan JWT (sebaiknya simpan dalam variabel lingkungan)
SECRET_KEY = 'secret_key'

@view_config(route_name='register', renderer='json', request_method='POST')
def register(request):
    email = request.json_body.get('email')
    password = request.json_body.get('password')

    # Cek apakah email sudah digunakan
    existing_user = request.dbsession.query(User).filter_by(email=email).first()
    if existing_user:
        return Response('Email already in use', status=400)

    # Buat pengguna baru dan simpan dalam basis data
    new_user = User(email=email, name='', role='user')
    new_user.set_password(password)
    request.dbsession.add(new_user)

    # Buat token JWT
    token = jwt.encode({'sub': new_user.email}, SECRET_KEY, algorithm='HS256')

    return Response('Registered and logged in', headers={'Authorization': 'Bearer ' + token})
