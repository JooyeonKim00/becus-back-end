from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    # for creating all user
    def create_user(self, email, name, phone, password=None, **extra_fields):
        if email is None:
            raise TypeError('Users must have an email address')
        if name is None:
            raise TypeError('Users must have a username')
        if phone is None:
            raise TypeError('Users must have an phone')
        if password is None:
            raise TypeError('Users must have a password')
        
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
            **extra_fields
        )
        user.role = 'USER'
        user.set_password(password)
        user.save(using=self._db)
        return user

    # for creating admin user
    def create_superuser(self, email, name, phone, password, **extra_fields):
        if password is None:
            raise TypeError('Superuser must have a password')
        user = self.create_user(
            email,
            name,
            phone,
            password,
            **extra_fields
        )
        user.is_superuser = True
        user.is_staff = True
        user.role = 'ADMIN'
        user.approval = 'ACCEPT'
        user.save(using=self._db)
        return user