# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright (c) 2014

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from __future__ import unicode_literals, absolute_import
from tastypie import fields

from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from characters.models import Character, Race


class RaceResource(ModelResource):

    class Meta:
        object_class = Race
        queryset = Race.objects.all()
        resource_name = "races"
        authorization = Authorization()
        authentication = Authentication()
        always_return_data = True


class CharacterResource(ModelResource):

    race = fields.ToOneField(RaceResource, attribute='race')

    class Meta:
        object_class = Character
        queryset = Character.objects.all()
        resource_name = "characters"
        authorization = Authorization()
        authentication = Authentication()
        always_return_data = True

    def dehydrate(self, bundle):
        bundle.data['strength'] = bundle.obj.strength()
        bundle.data['dexterity'] = bundle.obj.dexterity()
        bundle.data['intelligence'] = bundle.obj.intelligence()
        return bundle