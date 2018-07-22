#Endpoints


#### Framework for API Rest

```
I decided to use falcon because it's a micro-framework that is designed for building very 
fast micro-services. It is very flexible as it permits us to install add-ons and other 
libraries (e.g. Jinja2, SqlAlchemy, etc) easily. It encourages the REST architectural style, 
and tries to do as little as possible while remaining highly effectivem and its documentation 
is not so extensive and it's very understanble.

A good explanation:
https://eshlox.net/2017/08/27/do-you-want-to-use-django-for-rest-api-consider-it/
```

### Instación

Ver archivo Instalacion.pdf

### Documentación

Ver archivo Documentación y Ejemplos API-Enpoint.pdf

### Librerias y Frameworks

Marshmallow: Para realizar validaciones y la serializacion de objetos, tiene buena documentación. [is an ORM/ODM/framework-agnostic library for converting complex datatypes, such as objects, to and from native Python datatypes.]

SQLAlchemy: Por el tiempo corto, un ORM puede ayudar para la comunicación con la bd. [SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

It provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.]

Pygogo: Para logging, para realizar los logs. [pygogo is a Python logging library and command-line interface with super powers. pygogo leverages the standard Python logging module under the hood, so there's no need to learn yet-another logging library. The default implementation sends all messages to stdout, and any messages at level WARNING or above also to stderr]


PyJWT: Para la creación de tokens JWT y cumple con los standares y es de las mas utilizadas, por lo que cuenta con mucha documentación . [is a Python library which allows you to encode and decode JSON Web Tokens (JWT). JWT is an open, industry-standard (RFC 7519) for representing claims securely between two parties.]

PyTest: Para las pruebas unitarias, existe mucha documentación y es mas sencilla que la que viene con python (unittest). [The pytest framework makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries.]
### TODO

- TESTS Unitarios
- Actualiza, Eliminar y Busqueda por ID (Course, User, Lesson, Role, Question)