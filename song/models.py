from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.urls import reverse
# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Song.Status.PUBLISHED)

class Song(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    CATEGORY_CHOICES = [
        ('A', 'స్తుతి, ఆరాధన, సిలువ ద్యానం'),
        ('B', 'హెచ్చరిక, దిద్దుబాటు'),
        ('C', 'ప్రార్థన, విజ్ఞాపన, యాచన'),
        ('D', 'లేఖన విలువ '),
        ('E', 'సేవా పిలుపు, సేవా సమర్పణ'),
        ('F', 'ఆధరణ, ప్రోత్సాహము'),
        ('G', 'యవనస్థులు'),
        ('H', 'సోదరీలు'),
        ('I', 'సువార్త సందేశం, సువార్త పిలుపు'),
        ('J', 'ప్రభువు రాకడ, రాకడ సిద్ధపాటు '),
        ('K', 'అనుబంధ కీర్తనలు'),

    ]

    number = models.IntegerField(verbose_name= 'Song Number')
    index = models.IntegerField(verbose_name= 'Song Index')
    title = models.CharField(max_length=100 , verbose_name= 'Song Title')
    body = models.TextField( verbose_name= 'Lyrics of the Song')
    slug = models.SlugField(max_length=100, unique=True, blank=True, allow_unicode=True , verbose_name= 'Slug (Part of URL)')
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT,
                              )
    author = models.CharField(max_length=100, verbose_name= 'Author', null=True, blank=True)
    objects = models.Manager()
    published = PublishedManager()
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='A' , verbose_name= 'Content Category')
    tags = TaggableManager( verbose_name= 'Tags (Keywords)', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('song_detail',
                       args=[self.number, self.slug])