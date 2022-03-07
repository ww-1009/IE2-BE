# from django.db import models
from elasticsearch_dsl import DocType, Keyword, Text,Nested,Completion
# Create your models here.

from elasticsearch_dsl.analysis import CustomAnalysis as _CustomAnalysis
from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])

class CustomAnalyzer(_CustomAnalysis):
    def get_analysis_definition(self):
        return {}

ik_analyzer=CustomAnalyzer("ik_max_word")


class NasdaqGraph(DocType):
    imgUrl=Keyword()
    node=Nested(
            properties={
            'level0': Text(),
            'level1': Text(),
            'level2': Text(),
            'level3': Text(),
        })
    relatedType=Text()
    link=Nested(properties={
            'level1': Text(),
            'level2': Text(),
            'level3': Text(),
        })
    name=Text(analyzer="ik_max_word")
    abstract=Text()
    id=Keyword()
    namesuggest=Completion(analyzer=ik_analyzer,max_input_length=50,preserve_position_increments=True,preserve_separators=True)

    class Meta:
        index="index"
        doc_type="GraphType"






