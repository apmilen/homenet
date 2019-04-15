import uuid

from django.db import models

from .utils import get_short_uuid


class BaseModel(models.Model):
    model_id = models.UUIDField(primary_key=True,
                                default=uuid.uuid4,
                                editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def short_id(self):
        return get_short_uuid(self.model_id)

    def attrs(self, *attrs):
        """
        get a dictionary of attr:val for a list of attrs, defaults to all fields
        """
        if attrs is None:
            attrs = (f.name for f in self._meta.fields)
        return {attr: getattr(self, attr) for attr in attrs}

    def __json__(self, *attrs):
        return {
            'model_id': self.model_id,
            'str': str(self),
            **self.attrs(*attrs),
        }

    def __str__(self):
        return f'{self.__class__.__name__}:{self.short_id}'

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.short_id}>'

    class Meta:
        abstract = True


class SingletonModel(BaseModel):
    """
    Inherit from this to create a Singleton Model, (a model for which there
    should only ever be one row)
    """
    ID = '00' * 16
    id = models.UUIDField(primary_key=True, default=ID, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # make sure the inheriting model sets a real uuid (not default value)
        if self.ID is None or str(self.ID) == '00' * 16:
            raise NotImplementedError('Please provide a default singleton ID ')

        # make sure the ID they are trying to save matches the singleton's only
        #   allowed ID
        if str(self.id) != str(self.ID):
            raise ValueError('This is intended to be a singleton.')

        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create()
        return obj
