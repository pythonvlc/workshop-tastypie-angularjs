# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Race'
        db.create_table(u'characters_race', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('strength_modifier', self.gf('django.db.models.fields.IntegerField')()),
            ('dexterity_modifier', self.gf('django.db.models.fields.IntegerField')()),
            ('intelligence_modifier', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'characters', ['Race'])

        # Adding model 'Skill'
        db.create_table(u'characters_skill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('attribute', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal(u'characters', ['Skill'])

        # Adding model 'Profession'
        db.create_table(u'characters_profession', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'characters', ['Profession'])

        # Adding M2M table for field skills on 'Profession'
        m2m_table_name = db.shorten_name(u'characters_profession_skills')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profession', models.ForeignKey(orm[u'characters.profession'], null=False)),
            ('skill', models.ForeignKey(orm[u'characters.skill'], null=False))
        ))
        db.create_unique(m2m_table_name, ['profession_id', 'skill_id'])

        # Adding model 'Character'
        db.create_table(u'characters_character', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('base_strength', self.gf('django.db.models.fields.IntegerField')()),
            ('base_dexterity', self.gf('django.db.models.fields.IntegerField')()),
            ('base_intelligence', self.gf('django.db.models.fields.IntegerField')()),
            ('race', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['characters.Race'])),
            ('profession', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['characters.Profession'])),
        ))
        db.send_create_signal(u'characters', ['Character'])


    def backwards(self, orm):
        # Deleting model 'Race'
        db.delete_table(u'characters_race')

        # Deleting model 'Skill'
        db.delete_table(u'characters_skill')

        # Deleting model 'Profession'
        db.delete_table(u'characters_profession')

        # Removing M2M table for field skills on 'Profession'
        db.delete_table(db.shorten_name(u'characters_profession_skills'))

        # Deleting model 'Character'
        db.delete_table(u'characters_character')


    models = {
        u'characters.character': {
            'Meta': {'object_name': 'Character'},
            'base_dexterity': ('django.db.models.fields.IntegerField', [], {}),
            'base_intelligence': ('django.db.models.fields.IntegerField', [], {}),
            'base_strength': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'profession': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['characters.Profession']"}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['characters.Race']"})
        },
        u'characters.profession': {
            'Meta': {'object_name': 'Profession'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['characters.Skill']", 'symmetrical': 'False'})
        },
        u'characters.race': {
            'Meta': {'object_name': 'Race'},
            'dexterity_modifier': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intelligence_modifier': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'strength_modifier': ('django.db.models.fields.IntegerField', [], {})
        },
        u'characters.skill': {
            'Meta': {'object_name': 'Skill'},
            'attribute': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['characters']