# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals
import json

from model_mommy import mommy
from tastypie.test import ResourceTestCase
from characters.models import Character, Race, Skill


class CharactersApiTests(ResourceTestCase):

    def setUp(self):
        super(CharactersApiTests, self).setUp()
        mommy.make('characters.Character')
        mommy.make('characters.Skill')

    def test_get_characters(self):
        response = self.api_client.get(
            '/api/v1/characters/',
            format='json',
        )
        self.assertValidJSONResponse(response)
        characters = json.loads(response.content)
        self.assertEquals(characters['meta']['total_count'], Character.objects.count())

    def test_get_character_details(self):
        race = mommy.make('characters.Race')
        character = mommy.make('characters.Character', race=race)
        response = self.api_client.get(
            '/api/v1/characters/{}/'.format(character.pk),
            format='json',
        )
        self.assertValidJSONResponse(response)
        character = json.loads(response.content)
        self.assertTrue('strength' in character)
        self.assertTrue('dexterity' in character)
        self.assertTrue('intelligence' in character)

    def test_get_races(self):
        response = self.api_client.get(
            '/api/v1/races/',
            format='json',
        )
        self.assertValidJSONResponse(response)
        characters = json.loads(response.content)
        self.assertEquals(characters['meta']['total_count'], Race.objects.count())

    def test_post_races(self):
        prev = Race.objects.count()
        data = {
            "name": "human",
            "strength_modifier": 1,
            "dexterity_modifier": 1,
            "intelligence_modifier": 0,
        }
        response = self.api_client.post(
            '/api/v1/races/',
            format='json',
            data=data
        )
        self.assertHttpCreated(response)
        self.assertEquals(prev + 1, Race.objects.count())

    def test_get_race_details(self):
        race = mommy.make('characters.Race')
        response = self.api_client.get(
            '/api/v1/races/{}/'.format(race.pk),
            format='json',
        )
        self.assertValidJSONResponse(response)
        race = json.loads(response.content)
        self.assertTrue('strength_modifier' in race)
        self.assertTrue('dexterity_modifier' in race)
        self.assertTrue('intelligence_modifier' in race)

    def test_get_skills(self):
        response = self.api_client.get(
            '/api/v1/skills/',
            format='json',
        )
        self.assertValidJSONResponse(response)
        skills = json.loads(response.content)
        self.assertEquals(skills['meta']['total_count'], Skill.objects.count())

    def test_get_skill_details(self):
        skill = mommy.make('characters.Skill')
        response = self.api_client.get(
            '/api/v1/skills/{}/'.format(skill.pk),
            format='json',
        )
        self.assertValidJSONResponse(response)

    def test_get_skill_probe(self):
        skill = mommy.make('characters.Skill')
        character = mommy.make('characters.Character')
        data = {
            "character": character.pk,
            "difficulty": 12
        }
        response = self.api_client.get(
            '/api/v1/skills/{}/probes/'.format(skill.pk),
            data=data,
            format='json',
        )
        self.assertValidJSONResponse(response)