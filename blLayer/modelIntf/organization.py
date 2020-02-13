from django.shortcuts import get_object_or_404
from blLayer.modelIntf.client import OrgClient
from blLayer.modelIntf.orgUtils import OrgUtils
from blLayer.validators import Validators
from dbLayer.models import OrgNames


class Organization(OrgUtils, Validators):
    """
    Handles Organization
    """
    def __init__(self, client_id, pk):
        """
        Initialize a organization
        :param client_id: client for which organization belongs
        :param pk: primary key of org
        """
        super(Organization, self).__init__(OrgNames, client_id, pk)

    # Function which handles create, update and delete operations related to org name
    def update_org(self, **kwargs):
        if self.base.pk is not None:
            # Action is update / delete
            if 'del_ind' in kwargs:
                self.base.del_ind = kwargs.get('del_ind')
            else:
                self.base.name = self.get_org_name(kwargs.get('name', self.base.name))
            return
        else:
            # Action is create
            for k, v in kwargs.items():
                if k == 'name':
                    self.set_base_props(k, self.get_org_name(v))
                elif k == 'root_node':
                    self.set_base_props(k, v)

    # To get a Org name
    def get_org_name(self, name):
        # Check if org_name already exist
        tmp_list = OrgNames.objects.filter(client=self.base.client, name=name, del_ind=False)
        if tmp_list.count() == 0:
            # Check for org_name validity
            if not self.name_valid(name):
                self.set_error("Invalid org name")
                return None
            return name.upper()
        self.set_error("Org name already exist")
        return None

    # To get a org by root-node
    @staticmethod
    def get_org_by_rootnode(client_id, guid):
        client = OrgClient.get_client(client_id)
        return get_object_or_404(OrgNames, client=client, root_node=guid, del_ind=False)

    # To get all org
    @staticmethod
    def get_all_org(client_id):
        """
        Get all the organization for client
        :param client_id: client which org belongs to
        :return: Queryset containing org list
        """
        client = OrgClient.get_client(client_id)
        orgs = OrgNames.objects.filter(client=client, del_ind=False)
        if orgs.count() == 0:
            return ['{"info": "No organizations found"}']
        return orgs

    # To save the org
    def save_org(self):
        """
        Save the organization
        """
        if not(self.base.name is None or self.base.root_node is None or self.error):
            self.base.save()
            return True
        return False
