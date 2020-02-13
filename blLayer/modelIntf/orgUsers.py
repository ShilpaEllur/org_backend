from django.shortcuts import get_object_or_404

from blLayer.modelIntf.orgUtils import OrgUtils
from blLayer.validators import Validators
from dbLayer.models import OrgUsers, OrgModel


class OrgUser(OrgUtils, Validators):
    """
    Handles Users
    """
    def __init__(self, client_id, pk):
        """
        Initialize a user
        :param client_id: client for which node belongs
        :param pk: primary key of user
        """
        super(OrgUser, self).__init__(OrgUsers, client_id, pk)

    # Function which handles create, update and delete operations related to users
    def update_user(self, **kwargs):
        if self.base.pk is not None:
            # Action is update / delete
            if 'del_ind' in kwargs:
                self.base.del_ind = kwargs.get('del_ind')
            else:
                self.base.user_id = self.get_user_id(kwargs.get('user_id', self.base.user_id))
                self.base.name1 = self.get_name(kwargs.get('name1', self.base.name1))
                self.base.name2 = self.get_name(kwargs.get('name2', self.base.name2))
            return
        else:
            # Action is create
            for k, v in kwargs.items():
                if k == 'user_id':
                    self.set_base_props(k, self.get_user_id(v))
                elif k == 'name1':
                    self.set_base_props(k, self.get_name(v))
                elif k == 'name2':
                    self.set_base_props(k, self.get_name(v))
                elif k == 'map_id':
                    self.set_base_props(k, self.get_map_id(v))

    # To get the user-id and to validate the user-id
    def get_user_id(self, val):
        if self.alpha_num(val):
            tmp_usrs = OrgUsers.objects.filter(client=self.base.client, user_id=val, del_ind=False)
            if tmp_usrs.count() == 0:
                return val
            self.set_error("User id already exist")
        else:
            self.set_error("Invalid user id")
        return None

    # To get the user name and to validate the user name
    def get_name(self, val):
        if self.alphabets(val):
            return val
        return None

    # To get the map-id for users from the node
    def get_map_id(self, val):
        node = get_object_or_404(OrgModel, client=self.base.client, map_id=val, del_ind=False)
        if node.node_type.node_type == 'NODE':
            return val
        self.set_error("Users cannot be assigned under this node")
        return None

    # To save the users to user table
    def save_user(self):
        """
        Saves the users
        """
        if not (
                self.base.client is None or
                self.base.user_id is None or
                self.base.name1 is None or
                self.base.name2 is None or
                self.base.map_id is None or
                self.error
        ):
            self.base.save()
            return True
        return False
