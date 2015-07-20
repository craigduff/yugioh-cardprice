# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Carousel'
        db.create_table(u'bootstrap_theme_carousel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('carousel_group', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('lead', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('ordering', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('button_text', self.gf('django.db.models.fields.CharField')(default='Learn more', max_length=30)),
            ('button_url', self.gf('django.db.models.fields.CharField')(default='list-machines', max_length=20)),
            ('button_parameter', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
        ))
        db.send_create_signal(u'bootstrap_theme', ['Carousel'])


    def backwards(self, orm):
        # Deleting model 'Carousel'
        db.delete_table(u'bootstrap_theme_carousel')


    models = {
        u'bootstrap_theme.carousel': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'Carousel'},
            'button_parameter': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'button_text': ('django.db.models.fields.CharField', [], {'default': "'Learn more'", 'max_length': '30'}),
            'button_url': ('django.db.models.fields.CharField', [], {'default': "'list-machines'", 'max_length': '20'}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'carousel_group': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'lead': ('django.db.models.fields.TextField', [], {}),
            'ordering': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['bootstrap_theme']