from django.shortcuts import get_object_or_404

from blLayer.modelIntf.client import OrgClient
from blLayer.modelIntf.node import Node
from blLayer.modelIntf.orgUsers import OrgUser
from blLayer.modelIntf.organization import Organization
from dbLayer.models import OrgCompanies, OrgPorg, OrgPGroup, OrgUsers, OrgModel


class ApiHandler:
    """
    Contains methods for handling all APIs
    """

    @staticmethod
    def create_org(data):
        """
        Creates new organization for client
        :param data: Organization data (should contain client and org_name)
        :return: Response object/message
        """
        try:
            # Get client and org_name from data
            client = data['client']
            org_name = data['org_name']
            org_obj = Organization( client, None )
            org_obj.update_org( name=org_name )
            if not org_obj.error:
                root_node = Node( client, None )
                root_node.update_node( name=org_name, node_type=None, parent_node=None, map_id=None )
                if root_node.save_node( ):
                    org_obj.update_org( root_node=root_node.base.node )
                    if org_obj.save_org( ):
                        return [org_obj.base]
                    return [org_obj.message]
                return [root_node.message]
            return [org_obj.message]
        except KeyError:
            # Raised when client or org_name not found
            return ['{"error": "No valid inputs found"}']

    # @staticmethod
    # def edit_org(data):
    #     """
    #     Edit existing organization
    #     :param data: Organization data
    #     :return: Response data
    #     """
    #     try:
    #         client = data['client']
    #         org_name = data['org_name']
    #         pk = data['pk']
    #         org_obj = Organization(client, pk)
    #         org_obj.update_org(name=org_name)
    #         if not org_obj.error:
    #             if org_obj.save_org():
    #                 return [org_obj.base]
    #             return [org_obj.message]
    #         return [org_obj.message]
    #     except KeyError:
    #         return [{'error': 'No valid inputs found'}]

    # To get all organizations
    @staticmethod
    def get_all_org(data):
        """
        Get all the organizations
        :param data: Organization data(should contain client)
        :return: Response object/message
        """
        try:
            client = data['client']
            return Organization.get_all_org( client )
        except KeyError:
            return ['{"error": "No valid inputs found"}']

    @staticmethod
    def create_node(data):
        """
        Create new node
        :param data: Node data
        :return: Response object/message
        """
        try:
            client = data['client']
            name = data['name']
            node_type = data['node_type']
            parent_node = data['parent_node']
            map_id = data['map_id']
            new_node = Node( client, None )
            new_node.update_node( name=name, node_type=node_type, parent_node=parent_node, map_id=map_id )
            res = new_node.save_node( )
            if res:
                return [new_node.base]
            else:
                return [new_node.message]
        except KeyError:
            return ['{"error": "No valid inputs found"}']

    @staticmethod
    def edit_node_basic_data(data):
        """
        Edit node
        :param data: Node data
        :return: Response object/message
        """
        try:
            client = data['client']
            pk = data['pk']
            new_name = data['name']
            node = Node( client, pk )
            node.update_node( name=new_name, del_ind=False )
            if not node.error:
                # Update org name if root node changed
                if node.base.node_type.node_type == 'ROOTNODE':
                    # Get org by root node and update both org and root node
                    org = Organization.get_org_by_rootnode( client, node.base.node )
                    edit_org = Organization( client, None )
                    edit_org.base = org
                    edit_org.update_org( name=node.base.name )
                    if edit_org.error:
                        return [edit_org.message]
                    if node.save_node( ) and edit_org.save_org( ):
                        return [node.base]
                    return ['{"error": "Something went wrong"}']
                else:
                    if node.save_node( ):
                        return [node.base]
            return [node.message]
        except KeyError:
            return ['{"error": "No valid inputs found"}']

    @staticmethod
    def delete_node(data):
        """
        Node deletion
        :param data: Node data
        :return: Response message
        """
        try:
            client = data['client']
            pk = data['pk']
            node = Node( client, pk )
            node.update_node( del_ind=True )
            if not node.error:
                # Delete org if root node is deleted
                if node.base.node_type.node_type == 'ROOTNODE':
                    org = Organization.get_org_by_rootnode( client, node.base.node )
                    del_org = Organization( client, None )
                    del_org.base = org
                    del_org.update_org( del_ind=True )
                    if del_org.error:
                        return [del_org.message]
                    if node.save_node( ) and del_org.save_org( ):
                        return ['{"message": "Deletion successfull"}']
                    return ['{"error": "Something went wrong"}']
                else:
                    if node.save_node( ):
                        return ['{"message": "Deletion successfull"}']
            return [node.message]
        except KeyError:
            return ['{"error": "No valid inputs found"}']

    @staticmethod
    def get_node_types(data):
        """
        Get different node types available in client (except ROOTNODE)
        :param data: Client data
        :return: Response object
        """
        try:
            client = data['client']
            n_types = Node.get_node_types( client )
            if not n_types.count( ) == 0:
                return n_types
            else:
                return ['{"info": "Node types not found"}']
        except KeyError:
            return ['{"error""": "No client found"}']

    @staticmethod
    def assign_users(data):
        """
        User creation
        :param data: User data
        :return: Response object/message
        """
        try:
            client = data['client']
            map_id = data['map_id']
            user_id = data['user_id']
            name1 = data['name1']
            name2 = data['name2']
            new_user = OrgUser( client, None )
            new_user.update_user( map_id=map_id, user_id=user_id, name1=name1, name2=name2 )
            res = new_user.save_user( )
            if res:
                return [new_user.base]
            else:
                return [new_user.message]
        except KeyError:
            return ['{"error": "No valid inputs found"}']

    @staticmethod
    def get_node(data):
        try:
            client = data['client']
            guid = data['guid']
            return [Node.get_node( client, guid )]
        except KeyError:
            return ['{"error": "Invalid inputs found"}']

    @staticmethod
    def get_children(data):
        try:
            client = data['client']
            guid = data['guid']
            return Node.get_children( client, guid )
        except KeyError:
            return ['{"error": "Invalid inputs found"}']

    @staticmethod
    def get_node_details(data):
        try:
            client = data['client']
            pk = data['pk']
            n_type = data['node_type']
            clnt = OrgClient.get_client(client)
            obj = None
            sel = {'client': clnt, 'del_ind': False}
            if n_type != "":
                # Get the node
                node = Node.get_node( client, pk )
                node_type = node.node_type.node_type
                if node_type == 'ROOTNODE' or node_type == 'NODE':
                    return []
                elif node_type == "CC":
                    obj = OrgCompanies
                    sel['company_id'] = node.map_id
                elif node_type == "P_ORG":
                    obj = OrgPorg
                    sel['porg_id'] = node.map_id
                elif node_type == "P_GROUP":
                    obj = OrgPGroup
                    sel['pgroup_id'] = node.map_id
                node_det = get_object_or_404( obj, **sel )
                return [node_det]
            else:
                # Get the user
                sel['pk'] = pk
                user = get_object_or_404(OrgUsers, **sel)
                return [user]
        except KeyError:
            return ['{"error": "Invalid inputs found"}']

    @staticmethod
    def modify_node_details(data):
        try:
            client = data['client']
            pk = data['pk']
            n_type = data['node_type']
            clnt = OrgClient.get_client(client)
            obj = None
            sel = {'client': clnt, 'del_ind': False}
            inp = {'client': clnt}
            if n_type != "":
                # Get the node
                node = Node.get_node(client, pk)
                node_type = node.node_type.node_type
                if node_type == 'ROOTNODE' or node_type == 'NODE':
                    return []
                elif node_type == "CC":
                    obj = OrgCompanies
                    sel['company_id'] = node.map_id
                    inp['name1'] = data['name1']
                    inp['name2'] = data['name2']
                elif node_type == "P_ORG":
                    obj = OrgPorg
                    sel['porg_id'] = node.map_id
                    inp['description'] = data['description']
                elif node_type == "P_ORG":
                    obj = OrgPGroup
                    sel['pgroup_id'] = node.map_id
                    inp['description'] = data['description']
                try:
                    node_det = obj.objects.filter(**sel).update(**inp)
                    return [node_det]
                except obj.DoesNotExist:
                    node_det = obj( )
                    node_det.objects.modify(**inp)
                    node_det.save( )
                    return [node_det]
            else:
                # Get the user
                sel['pk'] = pk
                user = get_object_or_404(OrgUsers, **sel)
                inp['name1'] = data['name1']
                inp['name2'] = data['name2']
                user.objects.modify(**inp)
                return [user]
                pass
        except KeyError:
            return ['{"error": "Invalid inputs found"}']

    @staticmethod
    def get_node_basic_data(data):
        """
        Handles basic data tab details
        :param data: Node data
        :return: Response object/message
        """
        try:
            client = data['client']
            pk = data['pk']
            node_type = data['node_type']
            clnt = OrgClient.get_client( client )
            temp = {'client': clnt, 'del_ind': False}
            if node_type != "" and node_type is not None:
                node = Node.get_node(client, pk)
                obj = OrgModel
                temp['map_id'] = node.map_id
                node_detail = get_object_or_404(obj, **temp)
                return [node_detail]
            else:
                temp['pk'] = pk
                user = get_object_or_404(OrgUsers, **temp)
                return [user]
        except KeyError:
            return ['{"error": "Invalid inputs found"}']


