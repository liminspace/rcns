import datetime
import msgpack
import pytz
from django.utils.dateparse import parse_datetime, parse_date, parse_time
from django_redis.serializers.msgpack import MSGPackSerializer
from django.utils.timezone import is_aware


class ExtendedMSGPackSerializer(MSGPackSerializer):
    def dumps(self, value):
        return msgpack.dumps(value, use_bin_type=True, default=self._encoder)

    def loads(self, value):
        return msgpack.loads(value, raw=False, object_hook=self._decoder)

    @classmethod
    def _custom_obj(cls, custom_type, val):
        return {'@__TYPE__': custom_type, '@__VALUE__': val}

    @classmethod
    def _parse_custom_obj(cls, obj):
        if isinstance(obj, dict) and '@__TYPE__' in obj and '@__VALUE__' in obj:
            return obj['@__TYPE__'], obj['@__VALUE__']

    @classmethod
    def _encoder(cls, obj):
        if isinstance(obj, datetime.datetime):
            if is_aware(obj):
                obj = obj.astimezone(pytz.utc)
            return cls._custom_obj('datetime', obj.isoformat())
        elif isinstance(obj, datetime.date):
            return cls._custom_obj('date', obj.isoformat())
        elif isinstance(obj, datetime.time):
            return cls._custom_obj('time', obj.isoformat())
        return obj

    @classmethod
    def _decoder(cls, obj):
        custom_data = cls._parse_custom_obj(obj)
        if custom_data:
            if custom_data[0] == 'datetime':
                return parse_datetime(custom_data[1])
            elif custom_data[0] == 'date':
                return parse_date(custom_data[1])
            elif custom_data[0] == 'time':
                return parse_time(custom_data[1])
        return obj


class SimpleMSGPackSerializer:
    def dumps(self, value):
        return msgpack.dumps(value, use_bin_type=True)

    def loads(self, value):
        return msgpack.loads(value, raw=False)
