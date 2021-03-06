import json

from sanic import Blueprint
from sanic import response
from sanic.log import logger
from sanic_openapi import doc

from .manager import DatasetManager

dataset_svc = Blueprint('dataset_svc')


@dataset_svc.get('/datasets', strict_slashes=True)
@doc.summary('list all datasets')
@doc.produces(
    [{"name": str, "id": str, "type": str, "description": str}], content_type="application/json"
)
async def list_datasets(request):
    try:
        datasets = DatasetManager.list_datasets()
        return response.json(datasets, status=200)
    except Exception:
        logger.exception('faile to list dataset')
        return response.json({}, status=500)


@dataset_svc.post('/datasets', strict_slashes=True)
@doc.summary('creat a dataset')
@doc.produces({}, content_type="application/json")
@doc.consumes(
    doc.JsonBody({"name": str, "id": str, "type": str, "file": str, "description": str}),
    content_type="application/json",
    location="body",
)
async def create_datasets(request):
    logger.debug(f'create dataset with payload={request.body}')
    try:
        request_body = json.loads(request.body)
        DatasetManager.add_dataset(request_body)
        return response.json({}, status=201)
    except Exception:
        logger.exception('faile to create dataset')
        return response.json({}, status=500)


@dataset_svc.get('/datasets/<id>', strict_slashes=True)
@doc.summary('get one dataset')
@doc.produces(
    {"name": str, "id": str, "cols": [str], "rows": [[object]]}, content_type="application/json"
)
async def get_dataset(request, id):
    try:
        dataset = DatasetManager.get_dataset(id)
        payload = dataset.get_payload()
        return response.json(payload, status=200)
    except Exception:
        logger.exception('faile to get dataset')
        return response.json({}, status=500)


@dataset_svc.delete('/datasets/<id>', strict_slashes=True)
@doc.summary('delete one dataset')
async def delete_dataset(request, id):
    try:
        DatasetManager.delete_dataset(id)
        return response.json({}, status=204)
    except Exception:
        logger.exception('faile to delete dataset')
        return response.json({}, status=500)


@dataset_svc.post('/datasets/<id>/query', strict_slashes=True)
@doc.summary('run a dataset query')
@doc.produces({"cols": [str], "rows": [[object]]}, content_type="application/json")
@doc.consumes(
    doc.JsonBody({"type": str, "query": str}), content_type="application/json", location="body"
)
async def query_dataset(request, id):
    logger.debug(f'query dataset query payload={request.body} on {id}')
    try:
        dataset = DatasetManager.get_dataset(id)
        request_body = json.loads(request.body)
        query_result = dataset.query(request_body['query'], request_body['type'], True)
        return response.json(query_result, status=200)
    except Exception:
        logger.exception('faile to query dataset')
        return response.json({}, status=500)


@dataset_svc.post('/dataset_upload', strict_slashes=True)
@doc.summary('upload a dataset file')
async def upload_dataset(request):
    name = request.files["file"][0].name
    try:
        DatasetManager.upload_dataset(name, request.files["file"][0].body)
        return response.json({}, status=200)
    except Exception:
        logger.exception('faile to query dataset')
        return response.json({}, status=500)


@dataset_svc.post('/query2dataset', strict_slashes=True)
@doc.summary('export a query result as dataset')
@doc.produces({}, content_type="application/json")
@doc.consumes(
    doc.JsonBody(
        {
            "source_dataset_id": str,
            "query_type": str,
            "query": str,
            "dataset_id": str,
            "dataset_name": str,
            "dataset_description": str,
        }
    ),
    content_type="application/json",
    location="body",
)
async def query2dataset(request):
    try:
        request_body = json.loads(request.body)
        DatasetManager.query2dataset(**request_body)
        return response.json({}, status=200)
    except Exception:
        logger.exception('faile to query dataset')
        return response.json({}, status=500)
