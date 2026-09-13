"""Pruebas del inicio.

El inicio es la misma URL para los tres roles: lo unico que cambia es lo que
se le ofrece a cada uno. Un mesero no reserva como cliente, asi que el boton
no puede aparecer donde la vista lo va a rechazar.
"""

from django.test import TestCase
from django.urls import reverse

from panel.models import User


class InicioPorRolTest(TestCase):
    def setUp(self):
        # Credenciales unicas por prueba: la base de test de Mongo puede
        # arrastrar documentos de una corrida anterior.
        self.mesero = User.crear_mesero(
            username=f'mesero-{self._testMethodName}@abaroa.com',
            email=f'mesero-{self._testMethodName}@abaroa.com',
            password='1234', first_name='Ana',
        )
        self.admin = User.crear_admin(
            username=f'admin-{self._testMethodName}@abaroa.cl',
            email=f'admin-{self._testMethodName}@abaroa.cl',
            password='1234', first_name='Administradora',
        )
        self.cliente = User.objects.create_user(
            username=f'cliente-{self._testMethodName}@gmail.com',
            password='1234', first_name='Kevin',
        )

    def inicio(self, usuario):
        self.client.force_login(usuario)
        return self.client.get(reverse('home'))

    def test_el_inicio_del_mesero_cambia_reservar_por_salon(self):
        respuesta = self.inicio(self.mesero)

        self.assertNotContains(respuesta, reverse('booking:crear_reserva'))
        # El texto tampoco puede prometerle una reserva que no puede hacer.
        self.assertNotContains(respuesta, 'hacer reservas')
        # El boton grande sigue en el hero, pero lleva al salon del mesero.
        self.assertContains(
            respuesta,
            f'<a class="btn-reservar-gigante" href="{reverse("mesero")}">Salón</a>',
        )
        self.assertContains(respuesta, reverse('menu'))
        self.assertContains(respuesta, reverse('logout'))

    def test_el_inicio_del_admin_tampoco_ofrece_reservar(self):
        respuesta = self.inicio(self.admin)

        self.assertNotContains(respuesta, reverse('booking:crear_reserva'))

    def test_el_inicio_del_cliente_ofrece_reservar(self):
        respuesta = self.inicio(self.cliente)

        self.assertContains(respuesta, reverse('booking:crear_reserva'))

    def test_el_inicio_anonimo_ofrece_el_login_para_reservar(self):
        respuesta = self.client.get(reverse('home'))

        self.assertContains(respuesta, reverse('login'))
