from django.urls import path

from apiLayer.views import HandleOrg, HandleNode, HandleUsers, HandleNodeTypes, HandleDetails, HandleBasicData

urlpatterns = [
    path('org/<str:action>', HandleOrg.as_view(), name="org_handle"),                  # Refers to org related actions
    path('node/<str:action>', HandleNode.as_view(), name="node_handle"),               # Refers to node related actions
    path('users/<str:action>', HandleUsers.as_view(), name="user_handle"),             # Refers to users related actions
    path('node-types/getall', HandleNodeTypes.as_view(), name="node_types_handle"),    # Refers to node-types
    path('basic-data/<str:action>', HandleBasicData.as_view(), name="basicdata_tab"),  # Refers to basic data tab
    path('details/<str:action>', HandleDetails.as_view(), name="details_tab"),         # Refers to details tab
]
