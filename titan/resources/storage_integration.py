from dataclasses import dataclass

from .resource import Resource, ResourceSpec
from ..enums import ParseableEnum, ResourceType
from ..scope import AccountScope
from ..props import Props, StringProp, BoolProp, EnumProp, StringListProp


class StorageProvider(ParseableEnum):
    S3 = "S3"
    AZURE = "AZURE"
    GCS = "GCS"


@dataclass
class _S3StorageIntegration(ResourceSpec):
    name: str
    enabled: bool
    storage_aws_role_arn: str
    storage_allowed_locations: list[str]
    storage_blocked_locations: list[str] = None
    storage_provider: StorageProvider = StorageProvider.S3
    storage_aws_object_acl: str = None
    owner: str = "ACCOUNTADMIN"
    comment: str = None


class S3StorageIntegration(Resource):
    """
    CREATE [ OR REPLACE ] STORAGE INTEGRATION [IF NOT EXISTS]
      <name>
      TYPE = EXTERNAL_STAGE
      cloudProviderParams
      ENABLED = { TRUE | FALSE }
      STORAGE_ALLOWED_LOCATIONS = ('<cloud>://<bucket>/<path>/' [ , '<cloud>://<bucket>/<path>/' ... ] )
      [ STORAGE_BLOCKED_LOCATIONS = ('<cloud>://<bucket>/<path>/' [ , '<cloud>://<bucket>/<path>/' ... ] ) ]
      [ COMMENT = '<string_literal>' ]

    cloudProviderParams (for Amazon S3) ::=
      STORAGE_PROVIDER = 'S3'
      STORAGE_AWS_ROLE_ARN = '<iam_role>'
      [ STORAGE_AWS_OBJECT_ACL = 'bucket-owner-full-control' ]
    """

    resource_type = ResourceType.STORAGE_INTEGRATION
    props = Props(
        _start_token="type = external_stage",
        storage_provider=EnumProp("storage_provider", [StorageProvider.S3]),
        storage_aws_role_arn=StringProp("storage_aws_role_arn"),
        storage_aws_object_acl=StringProp("storage_aws_object_acl"),
        enabled=BoolProp("enabled"),
        storage_allowed_locations=StringListProp("storage_allowed_locations", parens=True),
        storage_blocked_locations=StringListProp("storage_blocked_locations", parens=True),
        comment=StringProp("comment"),
    )
    scope = AccountScope()
    spec = _S3StorageIntegration

    def __init__(
        self,
        name: str,
        enabled: bool,
        storage_aws_role_arn: str,
        storage_allowed_locations: list[str],
        storage_blocked_locations: list[str] = None,
        storage_aws_object_acl: str = None,
        owner: str = "ACCOUNTADMIN",
        comment: str = None,
        **kwargs,
    ):
        kwargs.pop("storage_provider", None)
        super().__init__(**kwargs)
        self._data = _S3StorageIntegration(
            name=name,
            enabled=enabled,
            storage_aws_role_arn=storage_aws_role_arn,
            storage_allowed_locations=storage_allowed_locations,
            storage_blocked_locations=storage_blocked_locations,
            storage_aws_object_acl=storage_aws_object_acl,
            owner=owner,
            comment=comment,
        )


@dataclass
class _GCSStorageIntegration(ResourceSpec):
    name: str
    enabled: bool
    storage_allowed_locations: list[str]
    storage_blocked_locations: list[str] = None
    storage_provider: StorageProvider = StorageProvider.GCS
    owner: str = "ACCOUNTADMIN"
    comment: str = None


class GCSStorageIntegration(Resource):
    """
    CREATE [ OR REPLACE ] STORAGE INTEGRATION [IF NOT EXISTS]
      <name>
      TYPE = EXTERNAL_STAGE
      cloudProviderParams
      ENABLED = { TRUE | FALSE }
      STORAGE_ALLOWED_LOCATIONS = ('<cloud>://<bucket>/<path>/' [ , '<cloud>://<bucket>/<path>/' ... ] )
      [ STORAGE_BLOCKED_LOCATIONS = ('<cloud>://<bucket>/<path>/' [ , '<cloud>://<bucket>/<path>/' ... ] ) ]
      [ COMMENT = '<string_literal>' ]

    cloudProviderParams (for Google Cloud Storage) ::=
      STORAGE_PROVIDER = 'GCS'

    """

    resource_type = ResourceType.STORAGE_INTEGRATION
    props = Props(
        _start_token="type = external_stage",
        storage_provider=EnumProp("storage_provider", [StorageProvider.GCS]),
        enabled=BoolProp("enabled"),
        storage_allowed_locations=StringListProp("storage_allowed_locations", parens=True),
        storage_blocked_locations=StringListProp("storage_blocked_locations", parens=True),
        comment=StringProp("comment"),
    )
    scope = AccountScope()
    spec = _GCSStorageIntegration

    def __init__(
        self,
        name: str,
        enabled: bool,
        storage_allowed_locations: list[str],
        storage_blocked_locations: list[str] = None,
        owner: str = "ACCOUNTADMIN",
        comment: str = None,
        **kwargs,
    ):
        kwargs.pop("storage_provider", None)
        super().__init__(**kwargs)
        self._data = _GCSStorageIntegration(
            name=name,
            enabled=enabled,
            storage_allowed_locations=storage_allowed_locations,
            storage_blocked_locations=storage_blocked_locations,
            owner=owner,
            comment=comment,
        )


@dataclass
class _AzureStorageIntegration(ResourceSpec):
    name: str
    enabled: bool
    azure_tenant_id: str
    storage_allowed_locations: list[str]
    storage_blocked_locations: list[str] = None
    storage_provider: StorageProvider = StorageProvider.AZURE
    owner: str = "ACCOUNTADMIN"
    comment: str = None


class AzureStorageIntegration(Resource):
    """
    CREATE [ OR REPLACE ] STORAGE INTEGRATION [IF NOT EXISTS]
      <name>
      TYPE = EXTERNAL_STAGE
      cloudProviderParams
      ENABLED = { TRUE | FALSE }
      STORAGE_ALLOWED_LOCATIONS = ('<cloud>://<bucket>/<path>/' [ , '<cloud>://<bucket>/<path>/' ... ] )
      [ STORAGE_BLOCKED_LOCATIONS = ('<cloud>://<bucket>/<path>/' [ , '<cloud>://<bucket>/<path>/' ... ] ) ]
      [ COMMENT = '<string_literal>' ]

    cloudProviderParams (for Microsoft Azure) ::=
      STORAGE_PROVIDER = 'AZURE'
      AZURE_TENANT_ID = '<tenant_id>'
    """

    resource_type = ResourceType.STORAGE_INTEGRATION
    props = Props(
        _start_token="type = external_stage",
        storage_provider=EnumProp("storage_provider", [StorageProvider.AZURE]),
        azure_tenant_id=StringProp("azure_tenant_id"),
        enabled=BoolProp("enabled"),
        storage_allowed_locations=StringListProp("storage_allowed_locations", parens=True),
        storage_blocked_locations=StringListProp("storage_blocked_locations", parens=True),
        comment=StringProp("comment"),
    )
    scope = AccountScope()
    spec = _AzureStorageIntegration

    def __init__(
        self,
        name: str,
        enabled: bool,
        azure_tenant_id: str,
        storage_allowed_locations: list[str],
        storage_blocked_locations: list[str] = None,
        owner: str = "ACCOUNTADMIN",
        comment: str = None,
        **kwargs,
    ):
        kwargs.pop("storage_provider", None)
        super().__init__(**kwargs)
        self._data = _AzureStorageIntegration(
            name=name,
            enabled=enabled,
            azure_tenant_id=azure_tenant_id,
            storage_allowed_locations=storage_allowed_locations,
            storage_blocked_locations=storage_blocked_locations,
            owner=owner,
            comment=comment,
        )


StorageIntegrationMap = {
    StorageProvider.S3: S3StorageIntegration,
    StorageProvider.GCS: GCSStorageIntegration,
    StorageProvider.AZURE: AzureStorageIntegration,
}


class StorageIntegration:
    def __new__(cls, storage_provider: StorageProvider, **kwargs) -> Resource:
        if isinstance(storage_provider, str):
            storage_provider = StorageProvider(storage_provider)
        storage_integration_cls = StorageIntegrationMap[storage_provider]
        return storage_integration_cls(**kwargs)

    # @classmethod
    # def from_sql(cls, sql):
    #     resource_cls = Resource.classes[_resolve_resource_class(sql)]
    #     return resource_cls.from_sql(sql)
