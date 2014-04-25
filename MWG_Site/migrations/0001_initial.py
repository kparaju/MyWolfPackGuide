# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MWGUser'
        db.create_table(u'MWG_Site_mwguser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('_picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, db_column='picture', blank=True)),
        ))
        db.send_create_signal(u'MWG_Site', ['MWGUser'])

        # Adding model 'MWGAdmin'
        db.create_table(u'MWG_Site_mwgadmin', (
            (u'mwguser_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['MWG_Site.MWGUser'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'MWG_Site', ['MWGAdmin'])

        # Adding model 'Address'
        db.create_table(u'MWG_Site_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('state_abbrev', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=5, null=True)),
        ))
        db.send_create_signal(u'MWG_Site', ['Address'])

        # Adding model 'Event'
        db.create_table(u'MWG_Site_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('_picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, db_column='picture', blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['MWG_Site.Address'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'MWG_Site', ['Event'])


    def backwards(self, orm):
        # Deleting model 'MWGUser'
        db.delete_table(u'MWG_Site_mwguser')

        # Deleting model 'MWGAdmin'
        db.delete_table(u'MWG_Site_mwgadmin')

        # Deleting model 'Address'
        db.delete_table(u'MWG_Site_address')

        # Deleting model 'Event'
        db.delete_table(u'MWG_Site_event')


    models = {
        u'MWG_Site.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'state_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'})
        },
        u'MWG_Site.event': {
            'Meta': {'object_name': 'Event'},
            '_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'db_column': "'picture'", 'blank': 'True'}),
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['MWG_Site.Address']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'MWG_Site.mwgadmin': {
            'Meta': {'object_name': 'MWGAdmin', '_ormbases': [u'MWG_Site.MWGUser']},
            u'mwguser_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['MWG_Site.MWGUser']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'MWG_Site.mwguser': {
            'Meta': {'object_name': 'MWGUser'},
            '_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'db_column': "'picture'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['MWG_Site']