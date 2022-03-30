from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from .managers import UserManager
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'Username', unique=True, db_index=True, max_length=255,
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    deposit = models.IntegerField(default=0)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.',
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    USERNAME_FIELD = 'username'

    create_objects = UserManager()
    objects = models.Manager()

    class Meta:
        """
            allowing users with a “seller” role to add,
            update or remove products, while users with a “buyer” role can deposit coins into the
            machine and make purchases
        """
        permissions = (('can_add_product', 'Can Add Product'),
                       ('can_update_product', 'Can Update Product'),
                       ('can_delete_product', 'Can Delete Product'),
                       ('is_seller', 'Is Seller'),
                       ('is_buyer', 'Is Buyer'),
                       ('can_deposit', 'Can Deposit'),)

    def reset_deposit(self):
        self.deposit = 0
        self.save()
