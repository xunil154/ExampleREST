# ExampleREST
Basic example of django + Django Rest Framework

What I did
==========

Setup:
```
$ mkvirtualenv -p /usr/bin/python2.7 examplerest
(examplerest)$ pip install -r requirements.txt
    ...
    <snip>
    ...
(examplerest)$ django-admin startproject example
(examplerest)$ cd example
(examplerest)$ django-admin startapp notes
(examplerest)$ vim settings.py
```

Update settings.py: (ignore the ... <snip> ...'s )
```
INSTALLED_APPS = (
    ... <snip> ...
    # Non Default APPS
    'rest_framework',
    'notes',
)

... <snip> ...

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../', 'example.sqlite3'),
    }
}

```

Create our model:
```
(examplerest)$ vim example/models.py
```
example/models.py :
```
from django.conf import settings

class Note(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notes')
    subject = models.CharField(max_length=100)
    note = models.TextField(blank=True,null=True)
```

Create the tables and stuff in the database:
```
(examplerest)$ ./manage.py makemigrations
(examplerest)$ ./manage.py migrate 
```

Now to create the ViewSet for RESTfullness

notes/views.py
```
from rest_framework import viewsets

from .models import Note
from .serializers import NoteSerializer

class NotesViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
```

And we need to make our NoteSerializer

notes/serializers.py (you need to create this)
```
from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
```

And now we just need to register the URL's to use them

example/urls.py
```
from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from notes.views import NotesViewSet

router = DefaultRouter()
router.register(r'notes', NotesViewSet)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
)
```

Oh, and we need to register our model with the admin site too (Not required, 
but nice to have)

notes/admin.py
```
from django.contrib import admin

from .models import Note

admin.site.register(Note)
```

DONE

Running
=======

Now that it's ready, fire it up

```
(examplerest)$ ./manage.py runserver
```

And point your browser to `http://localhost:8000`

You will see a `404 Page not found`. This is because we didn't specify a URL
for `/`. Which is not a problem. 
    
Admin
-----
Now goto the Django admin interface: `http://localhost:8000/admin` and login.

This is the Admin Interface, it's nice, but not RESTful


REST
----
Now goto the Rest interface: `http://localhost:8000/api`

ohhhh shiny.

Django Rest Framework provides us with a nice web interface for interacting
with the framework! You can also interact via curl/ajax or whatever and it
doesn't care.

```
$ curl http://localhost:8000/api/notes
[]
$ curl -X POST -H "Content-Type: application/json" -d '{"subject":"Curl Note", "note": "A note posted from curl!", "author": 1}' http://localhost:8000/api/notes/
{"id":1,"subject":"Curl Note","note":"A note posted from curl!","author":1}
```

Want to get a note?
```
$ curl http://localhost:8000/api/notes/1/
{"id":1,"subject":"Curl Note","note":"A note posted from curl!","author":1}
```

Delete?
```
$ curl -X DELETE http://localhost:8000/api/notes/1/
$ curl http://localhost:8000/api/notes/1/
{"detail":"Not Found."}
```

