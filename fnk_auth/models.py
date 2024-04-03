from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserAccountDetails(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return super().__str__()


class Stat(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Ability(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    stats = models.ManyToManyField(
        'Stat', through='StatToAbility', related_name='abilities')

    def __str__(self):
        return self.name


class StatToAbility(models.Model):
    stat = models.ForeignKey(Stat, on_delete=models.CASCADE)
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        # Enforces unique combination of stat and ability
        unique_together = ('stat', 'ability')

    def __str__(self):
        return f"{self.stat.name} affects {self.ability.name} with weight {self.weight}"


class Information(models.Model):
    name = models.TextField()
    discovered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name[:50] + '...'


class Player(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Character(models.Model):
    name = models.CharField(max_length=255)
    player = models.ForeignKey(
        Player, related_name='characters', on_delete=models.CASCADE,
    )
    stats = models.ManyToManyField(Stat, through='CharacterStat')
    abilities = models.ManyToManyField(Ability, through='CharacterAbility')
    known_information = models.ManyToManyField(
        Information,
        blank=True,
        through='CharacterInformation'
    )

    def __str__(self):
        return self.name

    def print_all(self):
        return f"{self.name}-{self.player}-{self.stats}-{self.abilities}-{self.known_information}"


class CharacterInformation(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name='character_information')
    information = models.ForeignKey(Information, on_delete=models.CASCADE)
    value = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.character.name}'s {self.information.name} = {self.value}"


class CharacterStat(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name='character_stats')
    stat = models.ForeignKey(Stat, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    class Meta:
        # Enforces unique combination of stat and ability
        unique_together = ('character', 'stat')

    def __str__(self):
        return f"{self.character.name}'s {self.stat.name} = {self.value}"


class CharacterAbility(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name='character_abilities')
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE)
    value = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)

    def calculate_level(self):
        # Placeholder for the calculation logic based on related stats and their weights.
        return sum([
            stat_to_ability.weight * character_stat.value
            for stat_to_ability in StatToAbility.objects.filter(ability=self.ability)
            for character_stat in CharacterStat.objects.filter(character=self.character, stat=stat_to_ability.stat)
        ])

    def save(self, *args, **kwargs):
        # Update calculated_level before saving
        self.value = self.calculate_level()
        super(CharacterAbility, self).save(*args, **kwargs)

    def __str__(self):
        calculated_level = self.calculate_level()
        return f"{self.character.name}'s {self.ability.name} level = {calculated_level}"
