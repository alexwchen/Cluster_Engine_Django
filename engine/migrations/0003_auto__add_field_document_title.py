# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Document.title'
        db.add_column('engine_document', 'title', self.gf('django.db.models.fields.CharField')(default=1, max_length=200), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'Document.title'
        db.delete_column('engine_document', 'title')
    
    
    models = {
        'engine.document': {
            'Meta': {'object_name': 'Document'},
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
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
