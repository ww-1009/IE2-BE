from django.db import models

# Create your models here.
class NasdaqIndex3(models.Model):
    prompt = models.TextField(blank=True, null=True)
    index = models.CharField(max_length=255, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'nasdaq_index_3'

    # __str__方法
    def __str__(self):
        return "index:%s\tprompt:%s" % (self.index, self.prompt)

class NasdaqIndex5(models.Model):
    index = models.CharField(max_length=255, blank=True, null=True)
    prompt = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nasdaq_index_5'
        # __str__方法

    def __str__(self):
        return "index:%s\tprompt:%s" % (self.index, self.prompt)


class NasdaqIndex7(models.Model):
    index = models.CharField(max_length=255, blank=True, null=True)
    prompt = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nasdaq_index_7'
        # __str__方法

    def __str__(self):
        return "index:%s\tprompt:%s" % (self.index, self.prompt)

class NasdaqDepth(models.Model):
    target = models.CharField(max_length=255, db_collation='utf8_bin', blank=True, null=True)
    depth = models.CharField(max_length=255, db_collation='utf8_bin', blank=True, null=True)
    name = models.CharField(max_length=255, db_collation='utf8_bin', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nasdaq_depth'

class NasdaqSpo3(models.Model):
    s = models.CharField(max_length=255, db_collation='utf8_bin', blank=True, null=True)
    p = models.CharField(max_length=255, db_collation='utf8_bin', blank=True, null=True)
    o = models.CharField(max_length=255, db_collation='utf8_bin', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nasdaq_spo_3'





