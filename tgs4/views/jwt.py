import jwt
from pyramid.view import view_config
from pyramid.response import Response
from ..models import User

# Kunci rahasia untuk tanda tangan JWT (sebaiknya simpan dalam variabel lingkungan)
SECRET_KEY = 'secret_key'

@view_config(route_name='login', renderer='json', request_method='POST')
def login(request):
    email = request.json_body.get('email')
    password = request.json_body.get('password')

    # Cari pengguna dengan email yang sesuai dalam basis data
    user = request.dbsession.query(User).filter_by(email=email).first()

    if user and user.check_password(password):
        # Jika autentikasi berhasil, buat token JWT
        token = jwt.encode({'sub': user.email}, SECRET_KEY, algorithm='HS256')

        return Response('Logged in', headers={'Authorization': 'Bearer ' + token})
    else:
        return Response('Login failed', status=401)

@view_config(route_name='register', renderer='json', request_method='POST')
def register(request):
    # Ambil data pendaftaran dari permintaan
    email = request.json_body.get('email')
    password = request.json_body.get('password')
    name = request.json_body.get('name')

    # Periksa apakah pengguna sudah terdaftar
    existing_user = request.dbsession.query(User).filter_by(email=email).first()

    if existing_user:
        return Response('Email already registered', status=400)

    # Jika pengguna belum terdaftar, buat pengguna baru
    new_user = User(email=email, name=name, role='user')
    new_user.set_password(password)

    # Simpan pengguna baru ke basis data
    request.dbsession.add(new_user)

    # Buat token JWT untuk pengguna baru
    token = jwt.encode({'sub': new_user.email}, SECRET_KEY, algorithm='HS256')

    return Response('Registered and logged in', headers={'Authorization': 'Bearer ' + token})
