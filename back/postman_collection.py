# postman_collection.py
import json
import os

from fastapi.openapi.utils import get_openapi

from main import app


def generate_postman_collection():
    """
    Genera una colección de Postman a partir de la especificación OpenAPI de la aplicación.

    La colección se guarda en un archivo llamado `postman_collection.json`.
    """
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    collection = {
        "info": {
            "name": app.title,
            "_postman_id": os.urandom(16).hex(),
            "description": app.description,
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "item": [],
    }

    for path, path_item in openapi_schema["paths"].items():
        for method, operation in path_item.items():
            item = {
                "name": operation.get("summary", f"{method.upper()} {path}"),
                "request": {
                    "method": method.upper(),
                    "header": [],
                    "url": {
                        "raw": f"{{{{base_url}}}}{path}",
                        "host": ["{{base_url}}"],
                        "path": path.strip("/").split("/"),
                    },
                    "description": operation.get("description", ""),
                },
                "response": [],
            }

            if "requestBody" in operation:
                item["request"]["body"] = {
                    "mode": "raw",
                    "raw": json.dumps(
                        operation["requestBody"]["content"]["application/json"]["schema"].get(
                            "example", {}
                        ),
                        indent=2,
                    ),
                    "options": {"raw": {"language": "json"}},
                }

            collection["item"].append(item)

    with open("postman_collection.json", "w") as f:
        json.dump(collection, f, indent=2)


if __name__ == "__main__":
    generate_postman_collection()
    print("✅ Colección de Postman generada en `postman_collection.json`")

