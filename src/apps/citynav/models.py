from django.contrib.postgres.fields import JSONField
from django.db import models, transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from .navigator import RouteNavigator


class Landmark(models.Model):
    x = models.PositiveIntegerField(_('coordinate X'))
    y = models.PositiveIntegerField(_('coordinate Y'))
    name = models.CharField(_('name'), max_length=250, db_index=True)

    class Meta:
        unique_together = (
            ('x', 'y'),
        )

    def __str__(self):
        return f'[{self.x}, {self.y}] {self.name}'


class Route(models.Model):
    start_x = models.PositiveIntegerField(_('start point coordiate X'))
    start_y = models.PositiveIntegerField(_('start point coordinate Y'))
    end_x = models.PositiveIntegerField(_('end point coordiate X'))
    end_y = models.PositiveIntegerField(_('end point coordinate Y'))
    instructions = JSONField(verbose_name=_('instructions'), default=list,
                             help_text=_('List of instructions. For example: '
                                         '[["START", [1, 2]], ["GO", ["E", 5]], ["TURN", "R"], '
                                         '["REACH", "The Bridge"], ["GO", [null, 8]]]'))

    class Meta:
        unique_together = (
            ('start_x', 'start_y'),
            ('end_x', 'end_y'),
        )

    def __str__(self):
        return f'Route from [{self.start_x}, {self.start_y}] to [{self.end_x}, {self.end_y}]'

    @classmethod
    def import_from_json(cls, data):
        """
        Import routes and landmarks from JSON-object.
        """
        added_routes = updated_routes = added_landmarks = updated_landmarks = 0
        with transaction.atomic():
            for route in data['routes']:
                # add or update landmarks
                for landmark in route['landmarks']:
                    landmark_obj, created = Landmark.objects.update_or_create(
                        x=landmark['coordinate'][0],
                        y=landmark['coordinate'][1],
                        defaults={'name': landmark['name']}
                    )
                    if created:
                        added_landmarks += 1
                    else:
                        updated_landmarks += 1

                # add or update the route
                nav = RouteNavigator(route['instructions'], landmarks_json=route['landmarks'])
                start_point = nav.get_start_point()
                end_point = nav.get_end_point()
                route_obj = Route.objects.filter(
                    start_x=start_point[0], start_y=start_point[1],
                    end_x=end_point[0], end_y=end_point[1],
                ).first()
                if route_obj is not None:
                    route_obj.instructions = route['instructions']
                    route_obj.save()
                    updated_routes += 1
                else:
                    Route.objects.create(instructions=route['instructions'])
                    added_routes += 1
        return {
            'added_routes': added_routes,
            'updated_routes': updated_routes,
            'added_landmarks': added_landmarks,
            'updated_landmarks': updated_landmarks,
        }

    def get_navigator(self):
        return RouteNavigator(self.instructions)


@receiver(pre_save, sender=Route)
def _update_denormalized_fields(instance, **kwargs):
    """
    Get start and end point from instructions and set them to the instance.
    """
    nav = RouteNavigator(instance.instructions)
    instance.start_x, instance.start_y = nav.get_start_point()
    instance.end_x, instance.end_y = nav.get_end_point()
