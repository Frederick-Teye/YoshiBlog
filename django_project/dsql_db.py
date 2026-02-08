import os
import boto3
from django.db.backends.postgresql.base import DatabaseWrapper as PgWrapper


class DatabaseWrapper(PgWrapper):
    def get_connection_params(self):
        params = super().get_connection_params()
        host = params.get("host", "") or ""

        if "dsql" in host and host.endswith(".on.aws"):
            region = os.environ.get("AWS_REGION", "us-east-1")
            parts = host.split(".")
            if len(parts) >= 3:
                region = parts[2] or region

            client = boto3.client("dsql", region_name=region)
            if hasattr(client, "generate_db_connect_auth_token"):
                token = client.generate_db_connect_auth_token(
                    Hostname=host,
                    Region=region,
                )
            else:
                token = client.generate_db_connect_admin_auth_token(
                    Hostname=host,
                    Region=region,
                )
            params["password"] = token

        return params
