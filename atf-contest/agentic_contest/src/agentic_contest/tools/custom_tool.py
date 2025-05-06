from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import requests as re
import time

class DatabricksSQLInput(BaseModel):
    """Input for the DatabricksSQLTool."""
    query: str = Field(..., description="SQL command to execute.")

class DatabricksSQLTool(BaseTool):
    name: str = "DatabricksSQLTool"
    description: str = "Tool for executing SQL queries against Databricks using the REST API."
    args_schema: Type[BaseModel] = DatabricksSQLInput

    host: str
    token: str
    warehouse_id: str
    endpoints: dict = {
        "execute_sql": "/api/2.0/sql/statements",
        "get_statement_status": "/api/2.0/sql/statements/{statement_id}"
    }

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def _run(self, query: str) -> str:
        try:
            query = query.strip()
            response = self.execute_sql(query)
            statement_id = response.get("statement_id")

            if not statement_id:
                return f"Failed to submit SQL query. Response: {response}"

            for _ in range(15):
                status_response = self.get_statement_status(statement_id)
                state = status_response.get("status", {}).get("state")

                if state == "SUCCEEDED":
                    result = status_response.get("result", {})
                    return result.get("data_array", [])
                elif state == "FAILED":
                    return f"Query execution failed: {status_response}"
                time.sleep(2)

            return "Query execution timed out."

        except Exception as e:
            return f"Databricks SQL tool error: {str(e)}"

    def execute_sql(self, query: str) -> dict:
        self.host = self.host.strip().replace("host = ", "")
        url = f"{self.host}{self.endpoints['execute_sql']}"
        payload = {
            "statement": query,
            "warehouse_id": self.warehouse_id
        }
        response = re.post(url, headers=self._headers(), json=payload)
        return response.json()

    def get_statement_status(self, statement_id: str) -> dict:
        self.host = self.host.strip().replace("host = ", "")
        url = f"{self.host}{self.endpoints['get_statement_status'].format(statement_id=statement_id)}"
        response = re.get(url, headers=self._headers())
        return response.json()
