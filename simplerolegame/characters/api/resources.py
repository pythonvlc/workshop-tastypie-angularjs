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
import json

from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponse
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.http import HttpNotFound, HttpMultipleChoices
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from characters.models import Character, Race, Profession, Skill


class RaceResource(ModelResource):

    class Meta:
        object_class = Race
        queryset = Race.objects.all()
        resource_name = "races"
        authorization = Authorization()
        authentication = Authentication()
        always_return_data = True


class SkillResource(ModelResource):

    class Meta:
        object_class = Skill
        queryset = Skill.objects.all()
        resource_name = "skills"
        probes_allowed_methods = ['get']
        authorization = Authorization()
        authentication = Authentication()
        always_return_data = True

    def prepend_urls(self):
        return [
            url(
                r"^(?P<resource_name>%s)/(?P<%s>.+)/probes%s$" % (
                    self._meta.resource_name, self._meta.detail_uri_name, trailing_slash()
                ),
                self.wrap_view('dispatch_probes'),
                name="api_dispatch_probes"
            ),
        ]

    def dispatch_probes(self, request, **kwargs):
        return self.dispatch('probes', request, **kwargs)

    def get_probes(self, request, **kwargs):
        basic_bundle = self.build_bundle(request=request)
        try:
            obj = self.cached_obj_get(bundle=basic_bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpNotFound()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at this URI.")
        try:
            character = Character.objects.get(pk=request.GET.get('character'))
        except Character.DoesNotExist:
            return HttpNotFound()
        result = obj.probe(character, request.GET.get('difficulty'))
        response = {"result": result}
        return HttpResponse(json.dumps(response), content_type='application/json')


class ProfessionResource(ModelResource):

    skills = fields.ToManyField(SkillResource, attribute='skills', full=True, null=True)

    class Meta:
        object_class = Profession
        queryset = Profession.objects.all()
        resource_name = "professions"
        authorization = Authorization()
        authentication = Authentication()
        always_return_data = True


class CharacterResource(ModelResource):

    race = fields.ToOneField(RaceResource, attribute='race', full=True, null=True)
    profession = fields.ToOneField(ProfessionResource, attribute='race', full=True, null=True)

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
