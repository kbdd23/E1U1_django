"""Script de insercion de datos de prueba.

Define usuarios cliente, meseros y administradores. Todas las funciones son
idempotentes: si el correo ya existe, se salta. El username es el correo,
igual que en signup_view: asi el login por email funciona con los mismos datos.

Ademas crea dos clientes de demo que ocupan una mesa 24/7 (00:00 a 23:59,
todos los dias): Mr Everytime la mesa 1 y Mr Copycat la mesa 2. Sirven para
ver el drawer de disponibilidad lleno y las mesas siempre ocupadas.

Uso (desde la carpeta donde vive manage.py):
    ./.venv/bin/python dataseed.py
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

import django

django.setup()

from datetime import time, timedelta

from django.utils import timezone

from booking.models import Mesa, Reserva
from panel.models import User

CLIENTES = [
    ('Fernando Reveco', 'profesor.reveco@gmail.com', '1234'),
    ('Ana García', 'ana.garcia@gmail.com', '1234'),
    ('Luis Lazo', 'luis.lazo@gmail.com', '1234'),
    ('Rodrigo Pradenas', 'rodrigo.pradenas@gmail.com', '1234'),
    ('Gonzalo Rojas', 'gonza.rojas@gmail.com', '1234'),
    ('Lucía Cuevas', 'lucy.cave@gmail.com', '1234'),
    ('Marianne Raine', 'mary.raine@gmail.com', '1234'),
    ('Ziora Deen', 'zora.dee@gmail.com', '1234'),
    ('Lexis Null', 'lexnull@gmail.com', '1234'),
    ('Kevin Wayne', 'kevin.wayne@gmail.com', '1234'),
    ('Usuario', 'usuario@gmail.com', '1234'),
    ('Mr Everytime', 'mr.everytime@gmail.com', '1234'), #Este usuario es "imposible", pide reservas para todo el año las 24 horas, no se deberia poder, pero existe por motivos demostrativos
    ('Mr Copycat', 'mr.copycat@gmail.com', '1234'), #Este otro usuario imita lo que hace mr everytime, para demostrar el mismo caso pero con otro usuario. (ej: 2 meseros pueden ver la disponibilidad de las diferentes mesas.)
]

MESEROS = [
    ('Ana Barrientos', 'ana@abaroa.com', '1234'),
    ('Francisco Vera', 'goated@abaroa.com', '1234'),
    ('Matías Cáceres', 'matias@abaroa.com', '1234'),
]

ADMINISTRADORES = [
    ('Ana Barrientos', 'ana@abaroa.cl', '1234'),
    ('Francisco Vera', 'fran@abaroa.cl', '1234'),
    ('Matías Cáceres', 'matias@abaroa.cl', '1234'),
    ('Administrador', 'admin@abaroa.cl', '1234'),
]

# Demo de ocupacion 24/7: cliente -> numero de la mesa que mantiene ocupada.
DEMO_OCUPACION = [
    ('mr.everytime@gmail.com', 1),
    ('mr.copycat@gmail.com', 2),
]

# Cuantos dias hacia adelante dura la ocupacion de la demo.
DIAS_OCUPADOS = 365

# El restaurante atiende 08:00-16:00, pero la demo ocupa el dia completo
# (00:00 a 23:59) para que la mesa nunca se libere en el drawer.
APERTURA_DEMO = time(0, 0)
CIERRE_DEMO = time(23, 59)


def crear_clientes():
    """Alta de clientes. create_user impone el rol cliente por defecto."""
    creados = 0
    for nombre, correo, clave in CLIENTES:
        if User.objects.filter(username=correo).exists():
            continue
        User.objects.create_user(
            username=correo,
            email=correo,
            password=clave,
            first_name=nombre,
        )
        creados += 1
    return creados


def crear_meseros():
    """Alta de meseros por la via controlada (User.crear_mesero)."""
    creados = 0
    for nombre, correo, clave in MESEROS:
        if User.objects.filter(username=correo).exists():
            continue
        User.crear_mesero(
            username=correo,
            email=correo,
            password=clave,
            first_name=nombre,
        )
        creados += 1
    return creados


def crear_admins():
    """Alta de administradores por la via controlada (User.crear_admin)."""
    creados = 0
    for nombre, correo, clave in ADMINISTRADORES:
        if User.objects.filter(username=correo).exists():
            continue
        User.crear_admin(
            username=correo,
            email=correo,
            password=clave,
            first_name=nombre,
        )
        creados += 1
    return creados


def crear_reservas_demo():
    """Ocupa 24/7 las mesas de la demo: Mr Everytime la 1, Mr Copycat la 2.

    Cada dia lleva una reserva de 00:00 a 23:59 que cubre todos los bloques
    del horario, asi el drawer de disponibilidad se ve lleno. Idempotente:
    solo crea los dias que faltan.
    """
    hoy = timezone.localdate()
    ultimo_dia = hoy + timedelta(days=DIAS_OCUPADOS)
    creadas = 0

    for correo, numero in DEMO_OCUPACION:
        cliente = User.objects.filter(username=correo).first()
        mesa = Mesa.objects.filter(numero=numero).first()
        if cliente is None or mesa is None:
            continue

        ya_ocupados = set(
            Reserva.objects.filter(cliente=cliente, mesa=mesa)
            .values_list('fecha', flat=True)
        )

        nuevas = []
        dia = hoy
        while dia <= ultimo_dia:
            if dia not in ya_ocupados:
                nuevas.append(Reserva(
                    cliente=cliente,
                    mesa=mesa,
                    fecha=dia,
                    hora_inicio=APERTURA_DEMO,
                    hora_fin=CIERRE_DEMO,
                ))
            dia += timedelta(days=1)

        if nuevas:
            Reserva.objects.bulk_create(nuevas)
        creadas += len(nuevas)

    return creadas


def poblar():
    """Corre todas las cargas y reporta cuantos registros nuevos entraron."""
    print('clientes nuevos:', crear_clientes())
    print('meseros nuevos:', crear_meseros())
    print('admins nuevos:', crear_admins())
    print('reservas demo nuevas:', crear_reservas_demo())
    print('total de usuarios:', User.objects.count())
    print('total de reservas:', Reserva.objects.count())


if __name__ == '__main__':
    poblar()
