from django.http import JsonResponse
from django.utils.text import slugify
from rest_framework import status
from rest_framework.views import APIView
from ..models import Character, Stat, Ability, Information, StatToAbility
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

TYPE_MAP_DROPDOWN = {
    # 'type_name': (model_class, data_func_name, complexity, items, default_option)
    # model_class is the model class for the dropdown
    # data_func_name is the name of the function that will return the data for the dropdown
    # complexity is whether the dropdown is simple or complex
    #       #complex the input id is dynamic 'id_dynamic_stat' + str(stat.name)
    # items is the list of fields to return from the model_class
    # default option for the dropdown
    'StatToAbilityForm':    (StatToAbility,
                             'stat_to_ability_data',
                             ['stat', 'ability'],
                             ['id', 'name'],
                             [' --- ',  0]),
    'CharacterForm':        (Character,
                             'character_data',
                             False,
                             ['id', 'name'],
                             {'id': 0, 'name': 'New Character'}),
    'StatForm':             (Stat,
                             'stat_data',
                             False,
                             ['id', 'name'],
                             {'id': 0, 'name': 'New Stat'}),
    'AbilityForm':          (Ability,
                             'ability_data',
                             False,
                             ['id', 'name'],
                             {'id': 0, 'name': 'New Ability'}),
    'InformationForm':      (Information,
                             'information_data',
                             False,
                             ['id', 'name'],
                             {'id': 0, 'name': 'New Information'}),
}


@permission_classes([IsAuthenticated])
class GetDropdownItems(APIView):
    """ API for getting the dropdown items for the page"""

    def get_not_complex_data(self, model_class, model_field, default_item):
        queryset_data = model_class.objects.all().values(*model_field)

        array_data = []
        array_data.append(default_item)
        for item in queryset_data:
            array_data.append(item)
        return JsonResponse(array_data, safe=False)

    def get_complext_data(self, model_class, data_func_name, complex, model_field, default_item):
        queryset_data = model_class.objects.all().prefetch_related(*complex)
        data_func = getattr(self, data_func_name, None)
        array_data = data_func(queryset_data, default_item)

        return JsonResponse(array_data, safe=False)

    # def stat_to_ability_data(self, queryset_data, default_item):
    #     print('stat to ability')
    #     ability_to_stat = {'ability': {**default_item}}
    #     print(ability_to_stat)
    #     for item in queryset_data:
    #         if item.ability.name not in ability_to_stat['ability']:
    #             ability_to_stat['ability'][item.ability.name] = {
    #                 'ability_id': item.ability.id, 'stats': []}

    #         ability_to_stat['ability'][item.ability.name]['stats'].append({'stat_id': item.stat.id,
    #                                                                        'stat_name': item.stat.name,
    #                                                                        'weight': item.weight
    #                                                                        })
    #     print(ability_to_stat)

    #     return ability_to_stat

    def stat_to_ability_data(self, queryset_data, default_item):
        print('stat to ability')
        ability_to_stat = {}
        ability_to_stat[default_item[0]] = default_item[1]
        print(ability_to_stat)
        for item in queryset_data:
            if item.ability.name not in ability_to_stat:
                ability_to_stat[item.ability.name] = item.ability.id

        print(ability_to_stat)

        return ability_to_stat

    def get(self, request, type_name):
        model_class, data_func_name, complex, model_field, default_item = TYPE_MAP_DROPDOWN.get(
            type_name, (None, None))
        if not model_class:
            return JsonResponse({'model_class not found': f"Invalid type name: {type_name}"}, status=status.HTTP_400_BAD_REQUEST)

        if not complex:
            return self.get_not_complex_data(model_class, model_field, default_item)

        return self.get_complext_data(model_class, data_func_name, complex, model_field, default_item)


@permission_classes([IsAuthenticated])
class DropdownUpdateAPI(APIView):
    """ API for updating dropdowns on the page"""

    def add_character_properties(self, character, property_relation, related_set_name, field_prefix, data):
        # Fetch the related properties with prefetch_related for efficiency
        properties = getattr(
            character, property_relation).prefetch_related(related_set_name)

        for property_item in properties:
            # Access the related set and get the specific property for this character
            property_value = getattr(property_item, related_set_name).get(
                character=character).value

            # Format the field name and set the value in the data dictionary
            field_name = f'#id_dynamic_{field_prefix}_{slugify(property_item.name)}'
            data['formFields'][field_name] = property_value

    def character_data(self, character, sent_id):
        # NAMING CONVENTION FOR DATA DICTIONARY
        # data = {
        #             'formFields': {
        #             },
        #             'checkboxGroups': {
        #             }
        #         }
        data = {
            'formFields': {
                # '#id_' + pk_id . pk_id being from pk_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
                '#id_pk_id': sent_id,
                # '#id_' + name . name being from name = forms.CharField(....
                '#id_name': character.name,
                # '#id_' + player . player being from player = forms.ModelChoiceField(....
                '#id_player': character.player.id,
                # we need to add '#id_stat_1' and '#id_stat_2' and so on
            },
            'checkboxGroups': {
                'known_information': list(character.known_information.values_list('id', flat=True)),
            }
        }
        self.add_character_properties(
            character, 'stats', 'characterstat_set', 'stat', data)
        self.add_character_properties(
            character, 'abilities', 'characterability_set', 'ability', data)

        return data

    def stat_data(self, stat, sent_id, complex=False):
        return {
            'formFields': {
                '#id_pk_id': sent_id,
                '#id_name': stat.name,
                '#id_description': stat.description,
            },
            'checkboxGroups': {}
        }

    def ability_data(self, ability, sent_id, complex=False):
        return {
            'formFields': {
                '#id_pk_id': sent_id,
                '#id_name': ability.name,
                '#id_description': ability.description,
            },
            'checkboxGroups': {}
        }

    def information_data(self, information, sent_id, complex=False):
        return {
            'formFields': {
                '#id_pk_id': sent_id,
                '#id_name': information.name,
            },
            'checkboxGroups': {}
        }

    def stat_to_ability_data(self, stat_to_ability, sent_id, complex=False, **kwargs):
        if not complex:
            return {'error': 'stat_to_ability_data must be complex'}

        data = {
            'formFields': {
                '#id_pk_id': sent_id,
            },
            'checkboxGroups': {}
        }
        model_class = kwargs.get('model_class')
        stats = model_class.objects.filter(ability=sent_id)

        for stat in stats:
            data['formFields']['#id_dynamic_stat_' +
                               str(stat.stat)] = stat.weight

        return data

    def get_object_data(self, model_class, obj_id):
        return model_class.objects.filter(id=obj_id).first()

    def get(self, request, type_name, sent_id):
        obj = None
        model_class, data_func_name, complexity, _, _ = TYPE_MAP_DROPDOWN.get(
            type_name, (None, None))
        if sent_id == 0:
            return JsonResponse({})

        if not model_class:
            return JsonResponse({'error': f"Invalid type name: {type_name}"}, status=status.HTTP_400_BAD_REQUEST)
        if not complexity:
            obj = self.get_object_data(model_class, sent_id)

            if not obj:
                return JsonResponse({'error': f"{type_name[:-4]} not found"}, status=status.HTTP_404_NOT_FOUND)

        # Use getattr to get the method from its name
        data_func = getattr(self, data_func_name, None)

        if not data_func:
            return JsonResponse({'error': f"Data function for {type_name} not found"}, status=status.HTTP_400_BAD_REQUEST)
        if complexity:
            data = data_func(
                obj, sent_id, **{'model_class': model_class, 'type_name': type_name, 'complex': True})
        else:
            data = data_func(obj, sent_id)
        return JsonResponse(data)
