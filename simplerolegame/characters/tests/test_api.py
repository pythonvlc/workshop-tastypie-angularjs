# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals
import json

from model_mommy import mommy
from tastypie.test import ResourceTestCase
from characters.models import Character


class CharactersApiTests(ResourceTestCase):

    def setUp(self):
        super(CharactersApiTests, self).setUp()
        mommy.make('characters.Character')

    def test_get_characters(self):
        response = self.api_client.get(
            '/api/v1/characters/',
            format='json',
        )
        self.assertValidJSONResponse(response)
        characters = json.loads(response.content)
        self.assertEquals(characters['meta']['total_count'], Character.objects.count())

    def test_get_characters_details(self):
        character = mommy.make('characters.Character')
        response = self.api_client.get(
            '/api/v1/characters/{}/'.format(character.pk),
            format='json',
        )
        self.assertValidJSONResponse(response)
        character = json.loads(response.content)
        self.assertTrue('strength' in character)
        self.assertTrue('dexterity' in character)
        self.assertTrue('intelligence' in character)
