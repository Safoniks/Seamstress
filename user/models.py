from django.contrib.auth.models import User, BaseUserManager


class MyUserManager(BaseUserManager):
    def new_user(self, **kwargs):
        password = kwargs.pop('password')
        user = self.model(**kwargs)

        user.set_password(password)
        return user

    def create_worker(self, **kwargs):
        user = self.new_user(**kwargs)
        user.save()
        return user

    def create_admin(self, **kwargs):
        user = self.new_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class MyUser(User):
    objects = MyUserManager()

    class Meta:
        proxy = True

    def is_worker(self):
        return hasattr(self, 'worker')
