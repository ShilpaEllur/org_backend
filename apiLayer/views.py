import json
from json import JSONDecodeError

from django.core import serializers
from django.http import HttpResponse
from django.views import View

from blLayer.apiHandler import ApiHandler


class JsonParser:
    """
    Used for dealing with JSON format
    """
    def get_json_from_req(self, req):
        """
        Converts requests body content to JSON object
        :param req: Http requestget_children object
        :return: JSON object
        """
        try:
            return json.loads(req.body.decode('utf-8'))
        except JSONDecodeError:
            return json.loads('{"error": "Incorrect input"}')

    def get_json_from_obj(self, obj):
        """
        Converts any iterable object to JSON
        :param obj: Any object
        :return: Http response with content type JSON
        """
        try:
            # Try to serialize the object
            data = serializers.serialize('json', obj)
        except AttributeError:
            # Attribute error if the object is a dictionary (already a key value pair)
            data = obj
        return HttpResponse(data, content_type='application/json')


class HandleOrg(View, JsonParser):
    """
    Handle Organization related API calls
    """
    def post(self, req, action):
        """
        Handles POST request
        :param req: Http request object
        :param action: Action to be performed on org
        :return: Http response
        """
        # Get JSON data from request's body
        data = self.get_json_from_req(req)
        if action == "create":
            # Create new organization
            res = ApiHandler.create_org(data)
            return self.get_json_from_obj(res)
        elif action == "getall":
            res = ApiHandler.get_all_org(data)
            return self.get_json_from_obj(res)
        return HttpResponse("Invalid request")


class HandleNode(View, JsonParser):
    """
    Handle Node related API calls
    """
    def post(self, req, action):
        """
        Handles POST request
        :param req: Http request object
        :param action: Action to be performed on node
        :return: Http response
        """
        # Get JSON data from request's body
        data = self.get_json_from_req(req)
        if action == "create":
            # Create new node
            res = ApiHandler.create_node(data)
            return self.get_json_from_obj(res)
        elif action == "edit":
            res = ApiHandler.edit_node(data)
            return self.get_json_from_obj(res)
        elif action == "delete":
            res = ApiHandler.delete_node(data)
            return self.get_json_from_obj(res)
        elif action == "get":
            res = ApiHandler.get_node(data)
            return self.get_json_from_obj(res)
        elif action == "getchilds":
            res = ApiHandler.get_children(data)
            return self.get_json_from_obj(res)
        return HttpResponse("Invalid request")


class HandleUsers(View, JsonParser):
    """
    Handle user related API calls
    """
    def post(self, req, action):
        """
        Handles POST request
        :param req: Http request object
        :param action: Action to be performed on users
        :return: Http response
        """
        data = self.get_json_from_req(req)
        if action == 'assign':
            resp = ApiHandler.assign_users(data)
            return self.get_json_from_obj(resp)
        elif action == 'edit':
            pass
        elif action == 'unassign':
            pass
        return HttpResponse("Invalid request")


class HandleNodeTypes(View, JsonParser):
    """
    Handle node-types related API calls
    """
    def post(self, req):
        """
        Handles POST request
        :param req: Http request object
        :return: Http response
        """
        data = self.get_json_from_req(req)
        res = ApiHandler.get_node_types(data)
        return self.get_json_from_obj(res)


class HandleDetails(View, JsonParser):
    """
    Handle details tab related API calls
    """
    def post(self, req, action):
        """
        Handles POST request
        :param req: Http request object
        :param action: Action to be performed on details
        :return: Http response
        """
        data = self.get_json_from_req(req)
        if action == "get":
            res = ApiHandler.get_node_details(data)
            return self.get_json_from_obj(res)
        # elif action == "create":
        #     res = ApiHandler.create_node_details(data)
        #     return self.get_json_from_obj(res)
        elif action == "edit":
            res = ApiHandler.modify_node_details(data)
            return self.get_json_from_obj(res)
        return HttpResponse("Invalid request")


class HandleBasicData(View, JsonParser):
    """
    Handle basic data tab related API calls
    """
    def post(self, req, action):
        """
        Handles POST request
        :param req: Http request object
        :param action: Action to be performed on basic data tab
        :return: Http response
        """
        data = self.get_json_from_req(req)
        if action == "get":
            res = ApiHandler.get_node_basic_data(data)
            return self.get_json_from_obj(res)
        elif action == "edit":
            res = ApiHandler.edit_node_basic_data(data)
            return self.get_json_from_obj(res)
        return HttpResponse("Invalid request")
