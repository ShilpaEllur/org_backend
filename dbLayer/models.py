# All database tables are defined here
import uuid
from django.db import models


class OrgClients(models.Model):
    """
    Table contains client details
    """
    client = models.CharField(primary_key=True, max_length=5)
    description = models.CharField(max_length=30, null=False)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "ORG_CLIENTS"
        managed = True

    def __str__(self):
        return self.pk


class OrgNames(models.Model):
    """
    Table contains all organizations
    """
    client = models.ForeignKey(OrgClients, on_delete=models.PROTECT, null=False)
    name = models.CharField(max_length=20, null=False)
    root_node = models.UUIDField(unique=True, null=True)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        unique_together = ('client', 'name')
        db_table = "ORG_NAMES"
        managed = True

    def __str__(self):
        return self.name


class OrgNodeTypes(models.Model):
    """
    Table contains node types/functions
    """
    client = models.ForeignKey(OrgClients, on_delete=models.PROTECT, null=False)
    node_type = models.CharField(max_length=8, null=False)
    description = models.CharField(max_length=30, null=False)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        unique_together = ('client', 'node_type')
        db_table = "ORG_NODETYPES"
        managed = True

    def __str__(self):
        return self.description


class OrgModel(models.Model):
    """
    Table contains all nodes of org structure
    """
    client = models.ForeignKey(OrgClients, on_delete=models.PROTECT, null=False)
    node = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=20, null=False)
    node_type = models.ForeignKey(OrgNodeTypes, on_delete=models.PROTECT, null=False)
    parent_node = models.UUIDField(default=None, null=True)
    map_id = models.CharField(max_length=8, null=False)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        unique_together = ('client', 'map_id')
        db_table = "ORG_MODEL"
        managed = True

    def __str__(self):
        return self.name


class OrgCompanies(models.Model):
    """
    Contains company code description
    """
    client = models.ForeignKey(OrgClients, on_delete=models.PROTECT, null=False)
    company_id = models.CharField(max_length=8, null=False)
    name1 = models.CharField(max_length=20, null=False)
    name2 = models.CharField(max_length=20, null=False)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        unique_together = ('client', 'company_id')
        db_table = "ORG_COMPANIES"
        managed = True

    def __str__(self):
        return self.company_id


class OrgPorg(models.Model):
    """
    Contains purchase organization description
    """
    client = models.ForeignKey(OrgClients, on_delete=models.PROTECT, null=False)
    porg_id = models.CharField(max_length=8, null=False)
    description = models.CharField(max_length=30, null=False)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        unique_together = ('client', 'porg_id')
        db_table = "ORG_PORG"
        managed = True

    def __str__(self):
        return self.porg_id


class OrgPGroup(models.Model):
    """
    Contains purchase group description
    """
    client = models.ForeignKey(OrgClients, on_delete=models.PROTECT, null=False)
    pgroup_id = models.CharField(max_length=8, null=False)
    description = models.CharField(max_length=30, null=False)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        unique_together = ('client', 'pgroup_id')
        db_table = "ORG_PGROUP"
        managed = True

    def __str__(self):
        return self.pgroup_id


class OrgUsers(models.Model):
    """
    Contains organization users
    """
    client = models.ForeignKey(OrgClients, on_delete=models.PROTECT, null=False)
    map_id = models.CharField(max_length=8, null=True)
    user_id = models.CharField(max_length=12, null=False)
    name1 = models.CharField(max_length=20, null=False)
    name2 = models.CharField(max_length=20, null=True)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        unique_together = ('client', 'user_id')
        db_table = "ORG_USERS"
        managed = True

    def __str__(self):
        return self.user_id


class OrgAttributes(models.Model):
    """
    Contains different possible attributes in organization
    """
    client = models.ForeignKey(OrgClients, on_delete=models.PROTECT, null=False)
    attr_name = models.CharField(max_length=20, null=False)
    description = models.CharField(max_length=40, null=False)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        unique_together = ('client', 'attr_name')
        db_table = "ORG_ATTRIBUTES"
        managed = True

    def __str__(self):
        return self.attr_name


class OrgAttrMap(models.Model):
    """
    Contains attributes mapping to nodes via map_id
    """
    client = models.ForeignKey(OrgClients, on_delete=models.PROTECT, null=False)
    map_id = models.CharField(max_length=8, null=False)
    attr_name = models.ForeignKey(OrgAttributes, on_delete=models.PROTECT, null=False)
    value = models.CharField(max_length=20, null=False)
    attr_def = models.BooleanField(default=False, null=False)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "ORG_ATTR_MAP"
        managed = True

    def __str__(self):
        return self.value


class OrgCostCtr(models.Model):
    """
    Contains Cost center details
    """
    client = models.ForeignKey(OrgClients, on_delete=models.PROTECT, null=False)
    cost_ctr = models.CharField(max_length=10, null=False)
    description = models.CharField(max_length=40, null=False)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        unique_together = ('client', 'cost_ctr')
        db_table = "ORG_COST_CTR"
        managed = True

    def __str__(self):
        return self.cost_ctr


class OrgGlAcc(models.Model):
    """
    Contains GL account details
    """
    client = models.ForeignKey(OrgClients, on_delete=models.PROTECT, null=False)
    gl_account = models.CharField(max_length=10, null=False)
    description = models.CharField(max_length=40, null=False)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        unique_together = ('client', 'gl_account')
        db_table = "ORG_GL_ACC"
        managed = True

    def __str__(self):
        return self.gl_account


class OrgAddress(models.Model):
    """
    Contains address details
    """
    client = models.ForeignKey(OrgClients, on_delete=models.PROTECT, null=False)
    address = models.CharField(max_length=10, null=False)
    description = models.CharField(max_length=40, null=False)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        unique_together = ('client', 'address')
        db_table = "ORG_ADDRESS"
        managed = True

    def __str__(self):
        return self.address
