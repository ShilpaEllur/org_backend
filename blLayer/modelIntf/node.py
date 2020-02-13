import random
import string

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404

from blLayer.modelIntf.client import OrgClient
from blLayer.modelIntf.orgUtils import OrgUtils
from blLayer.validators import Validators
from dbLayer.models import OrgNodeTypes, OrgModel


class Node(OrgUtils, Validators):
    """
    Handles Organization Model
    """
    def __init__(self, client_id, pk):
        """
        Initialize a node
        :param client_id: client for which node belongs
        :param pk: primary key of node
        """
        super(Node, self).__init__(OrgModel, client_id, pk)

    # Function which handles create, update and delete operations related to Node/sub-nodes
    def update_node(self, **kwargs):
        if 'del_ind' in kwargs:
            # first check action is delete/update
            self.base.del_ind = kwargs.get('del_ind')
            if self.base.del_ind:
                if not self.delete_possible():
                    self.base.del_ind = False
            self.base.name = self.get_node_name(kwargs.get('name', self.base.name))
            return
        else:
            # Action is create
            for k, v in kwargs.items():
                if k == 'name':
                    self.set_base_props(k, self.get_node_name(v))
                elif k == 'node_type':
                    self.set_base_props(k, self.get_node_type(v))
                elif k == 'parent_node':
                    self.set_base_props(k, self.get_parent_node(v))
                elif k == 'map_id':
                    self.set_base_props(k, self.get_node_map_id(v))

    def delete_possible(self):
        """
        Checks for existence of children for the node
        :return: True/False
        """
        nodes = OrgModel.objects.filter(parent_node=self.base.node, del_ind=False)
        if nodes.count() != 0:
            self.set_error("Delete children first")
            return False
        return True

    def get_node_name(self, name):
        """
        Node name validation
        :param name: Name of the node
        :return: Node name
        """
        if self.name_valid(name):
            return name
        self.set_error("Invalid node name")
        return None

    def get_node_type(self, pk):
        """
        Get the node-type of a node
        :param pk: primary key of a node
        :return: Response object
        """
        if (pk is None) or (pk == ""):
            # Find ROOTNODE type
            return get_object_or_404(OrgNodeTypes, client=self.base.client, node_type='ROOTNODE', del_ind=False)
        return get_object_or_404(OrgNodeTypes, ~Q(node_type='ROOTNODE'), client=self.base.client, pk=pk, del_ind=False)

    # Checks the node-type position where should it exist
    def check_node_type(self):

        # Don't allow root node below the nodes
        if self.base.node_type.node_type == 'ROOTNODE':
            if self.base.parent_node is not None:
                self.set_error("Cannot create root node underneath the node")
            return
        tree_types = Node.read_tree_up(self.base)

        # Don't allow any nodes under P_GROUP except NODE
        if self.base.node_type.node_type != 'NODE':
            if 'P_GROUP' in tree_types:
                self.set_error("Cannot create this node under P_GROUP")

        # Allow P_GROUP only under P_ORG
        if self.base.node_type.node_type == 'P_GROUP':
            if 'P_ORG' not in tree_types:
                self.set_error("P_GROUP should be created under P_ORG")

        # Don't allow any nodes under P_ORG except NODE and P_GROUP
        if self.base.node_type.node_type != 'NODE':
            if self.base.node_type.node_type != 'P_GROUP':
                if self.base.node_type.node_type != 'CC':
                    if 'P_ORG' in tree_types:
                        self.set_error("Cannot create this node under P_ORG")

        # Don't allow CC under CC
        if self.base.node_type.node_type == 'CC':
            if 'CC' in tree_types:
                self.set_error("Can't create CC under CC")

        # Don't allow P_ORG under P_ORG
        if self.base.node_type.node_type == 'P_ORG':
            if 'P_ORG' in tree_types:
                self.set_error("Can't create P_ORG under P_ORG")

    # To get the parent node of the current node
    def get_parent_node(self, guid):
        try:
            if guid is not None:
                parent_node = OrgModel.objects.filter(client=self.base.client, pk=guid, del_ind=False)
                if parent_node.count() != 0:
                    return guid
                self.set_error("Parent node doesn't exist")
        except ValidationError:
            self.set_error("Invalid parent")
        return None

    # To get the map-id for the node
    def get_node_map_id(self, map_id):
        if map_id is None:
            while True:
                # Generate random string of alphanumeric format 'ROOT_XXX' where XXX is calculated dynamically
                tmp_str = "ROOT_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
                # Check if map_id already exists in the particular client
                if not self.check_map_id_exist(tmp_str):
                    return tmp_str
        if self.alpha_num(map_id):
            if not self.check_map_id_exist(map_id):
                if len(map_id) <= 8:
                    return map_id
                else:
                    self.set_error("Map_id length should not be lesser than 8")
            else:
                self.set_error("Map id already exist")
        else:
            self.set_error("Invalid map id")
        return None

    # To check whether map-id already exist for that client or not
    def check_map_id_exist(self, name):
        tmp_node = OrgModel.objects.filter(client=self.base.client, map_id=name, del_ind=False)
        print(tmp_node)
        if tmp_node.count() == 0:
            return False
        return True

    # To set node name
    def set_node_name(self):
        if self.base.node_type.node_type == 'ROOTNODE':
            self.base.name = self.base.name.upper()
        else:
            self.base.name = self.base.name.capitalize()

    def \
            save_node(self):
        """
        Saves the node
        """
        if not(
            self.base.client is None or
            self.base.node is None or
            self.base.name is None or
            self.base.node_type is None or
            self.base.map_id is None
        ):
            self.set_node_name()
            if self.base.node_type.node_type == 'ROOTNODE':
                if self.base.parent_node is not None:
                    self.set_error("Parent should be null for root node")
            else:
                if self.base.parent_node is not None:
                    if self.alpha_num(self.base.map_id):
                        self.check_node_type()
                    else:
                        self.set_error("Invalid map id")
                else:
                    self.set_error("No parent found")
            if not self.error:
                self.base.save()
                return True
        return False

    @staticmethod
    def read_tree_up(cur_node):
        tree_struct = []
        while cur_node.parent_node is not None:
            cur_node = OrgModel.objects.get(pk=cur_node.parent_node)
            tree_struct.append(cur_node)
        tree_types = []
        for item in tree_struct:
            tree_types.append(item.node_type.node_type)
        return tree_types

    # To get node types of a client
    @staticmethod
    def get_node_types(client_id):
        client = OrgClient.get_client(client_id)
        return OrgNodeTypes.objects.filter(~Q(node_type='ROOTNODE'), client=client)

    @staticmethod
    def get_node(client_id, guid):
        try:
            client = OrgClient.get_client(client_id)
            node = get_object_or_404(OrgModel, client=client, node=guid, del_ind=False)
            return node
        except:
            return '{"error": "No node found"}'

    @staticmethod
    def get_children(client_id, guid):
        try:
            client = OrgClient.get_client(client_id)
            node = OrgModel.objects.filter(client=client, parent_node=guid, del_ind=False)
            if node.exists():
                return node
            else:
                return ['{"error": "No children found"}']
        except:
            return ['{"error": "no valid input"}']
