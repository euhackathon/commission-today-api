import datetime
from haystack import indexes
from backend.models import Meeting


class MeetingIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='description')
    member = indexes.CharField(model_attr='member')
    date = indexes.DateTimeField(model_attr='date')

    def get_model(self):
        return Meeting
