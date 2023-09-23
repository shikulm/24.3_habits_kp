from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, telegram, password):

        if not telegram:
            raise TypeError('Users must have an telegram.')

        if not password:
            raise TypeError('Users must have a telegram.')

        user = self.model(telegram=telegram)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, telegram, password):

        user = self.create_user(telegram, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
