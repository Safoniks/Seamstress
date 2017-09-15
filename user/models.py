from django.contrib.auth.models import User, BaseUserManager

from simple_history.models import HistoricalRecords


class MyUserManager(BaseUserManager):
    def all_directors(self, **kwargs):
        return self.get_queryset().filter(is_superuser=True, is_staff=True)

    def all_technologists(self, **kwargs):
        return self.get_queryset().filter(is_superuser=False, is_staff=True)

    def all_workers(self, **kwargs):
        return self.get_queryset().filter(is_superuser=False, is_staff=False)

    def new_user(self, **kwargs):
        password = kwargs.pop('password')
        user = self.model(**kwargs)

        user.set_password(password)
        return user

    def create_worker(self, **kwargs):
        user = self.new_user(**kwargs)
        user.save()
        return user

    def create_technologist(self, **kwargs):
        user = self.new_user(**kwargs)
        user.is_staff = True
        user.save()
        return user

    def create_director(self, **kwargs):
        user = self.new_user(**kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class MyUser(User):
    WORKER = 'worker'
    TECHNOLOGIST = 'technologist'
    DIRECTOR = 'director'

    history = HistoricalRecords(table_name='user_history')

    objects = MyUserManager()

    class Meta:
        proxy = True

    def is_worker(self):
        return hasattr(self, 'worker') or self.is_staff is False and self.is_superuser is False

    def is_technologist(self):
        return self.is_staff is True and self.is_superuser is False

    def is_director(self):
        return self.is_superuser is True

    def get_scope(self):
        if MyUser.is_worker(self):
            return MyUser.WORKER
        elif MyUser.is_technologist(self):
            return MyUser.TECHNOLOGIST
        elif MyUser.is_director(self):
            return MyUser.DIRECTOR

