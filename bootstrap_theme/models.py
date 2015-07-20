from django.db import models

class Carousel(models.Model):
    carousel_group = models.SlugField(help_text='Use the same group name for carousels that display together.')
    caption = models.CharField(max_length=40, help_text='The large caption text.')
    lead = models.TextField(help_text='The marketing text just below the caption.')
    image = models.ImageField(upload_to='carousel', help_text='The big banner image to display.')
    ordering = models.PositiveSmallIntegerField(help_text='The carousel items are sorted by this number.')
    button_text = models.CharField(max_length=30, default='Learn more', help_text='The text to place on the button.')
    button_url = models.CharField(max_length=20, default='list-machines', help_text='The destination of the button.')
    button_parameter = models.CharField(max_length=40, blank=True, null=True, help_text='A special parameter for the URL, leave blank if unsure.')
    def __unicode__(self):
        return u"%s" % self.caption
    class Meta:
        ordering = ['ordering']
