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
from django.db import models
from characters import CHARACTER_ATTRIBUTES


class Race(models.Model):
    """
    Race model. A race modifies characters values.
    """
    name = models.CharField(max_length=200)
    strength_modifier = models.IntegerField()
    dexterity_modifier = models.IntegerField()
    intelligence_modifier = models.IntegerField()

    def __unicode__(self):
        return self.name


class Skill(models.Model):
    """
    Skill model. An action a character can do.
    """

    name = models.CharField(max_length=200)
    description = models.TextField()
    attribute = models.CharField(choices=CHARACTER_ATTRIBUTES, max_length=16)

    def __unicode__(self):
        return self.name


class Profession(models.Model):
    """
    Class model. Give skills to characters
    """
    name = models.CharField(max_length=200)
    skills = models.ManyToManyField(Skill)

    def __unicode__(self):
        return self.name


class Character(models.Model):
    """
    Character model.
    """
    name = models.CharField(max_length=200)
    base_strength = models.IntegerField()
    base_dexterity = models.IntegerField()
    base_intelligence = models.IntegerField()
    race = models.ForeignKey(Race)
    profession = models.ForeignKey(Profession)

    def __unicode__(self):
        return self.name

    def strength(self):
        return self.base_strength + self.race.strength_modifier

    def dexterity(self):
        return self.base_dexterity + self.race.dexterity_modifier

    def intelligence(self):
        return self.base_dexterity + self.race.dexterity_modifier