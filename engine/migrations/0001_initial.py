# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'list_object'
        db.create_table('engine_list_object', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('engine', ['list_object'])

        # Adding model 'object_object'
        db.create_table('engine_object_object', (
            ('master_list', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['engine.list_object'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('engine', ['object_object'])

        # Adding model 'parameter_object'
        db.create_table('engine_parameter_object', (
            ('default', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('master_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['engine.object_object'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('engine', ['parameter_object'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'list_object'
        db.delete_table('engine_list_object')

        # Deleting model 'object_object'
        db.delete_table('engine_object_object')

        # Deleting model 'parameter_object'
        db.delete_table('engine_parameter_object')
    
    
    models = {
        'engine.list_object': {
            'Meta': {'object_name': 'list_object'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'engine.object_object': {
            'Meta': {'object_name': 'object_object'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'master_list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['engine.list_object']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'engine.parameter_object': {
            'Meta': {'object_name': 'parameter_object'},
            'default': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'master_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['engine.object_object']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }
    
    complete_apps = ['engine']
