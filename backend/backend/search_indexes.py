import datetime
from haystack import indexes
from backend.models import Meeting


class MeetingIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='description',
                             use_template=True)

    def get_model(self):
        return Meeting
