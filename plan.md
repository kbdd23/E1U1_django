Vamos a re-organizar de manera más prolija el proyecto de un restaurante con gestión de reservas, atención de mesas y administración de carta y usuarios a partir del borrador ubicado en .../django-project-AFM/django_projectAFM

0.-Organizar las configs en settings.py en base a las del proyecto AFM [Done]
1.-Conectar Mongo al backend para que la BD sea remota. [Done]
2.-Crear las vistas del landing 'home' [Done]
3.-Crear la app 'panel' que contenga el modelo de usuario [Done]
4.-La app de 'booking' [Done]
5.-App 'menú' y 'orders' [Donde]
6.-Unir todo [Done]
7.-Añadir la nueva caracteristica del panel de administración [DONE]
8.-Añadir y pulir nuevas feats [DONE]
    -drawers pulidos
    -feat: ahora los meseros puede "sentar" invitados en una mesa

***

En el proyecto borrador, la app "pages" se ha inflado con login, gestión de mesas, y landing, por eso abstraer los roles en "panel" para determinar que página mostrar es más estable.

