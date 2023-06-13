from typing import Dict, List

import inflection as inflection
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.responses import Response
from fastapi.routing import APIRouter

from backend.container import Container
from backend.models import PlotResponseModel, PlotMetaData

rest_v1_router = APIRouter(prefix="/v1")
Id = str


@rest_v1_router.get("/visualizations", response_model=List[str])
@inject
async def list_visualizations(plotters: Dict = Depends(Provide[Container.plotters])):
    print([p.get_metadata() for k, p in plotters.items()])
    return [p.get_metadata() for k, p in plotters.items()]


@rest_v1_router.post("/visualizations/{id}/plot", response_model=PlotResponseModel)
@inject
async def plot(id: Id, config: Dict, plotters: Dict = Depends(Provide[Container.plotters])):
    plotter = plotters.get(id)
    plot_kwargs = {inflection.underscore(k): v for k, v in config.items()}
    plot = plotter.plot(**plot_kwargs)
    return PlotResponseModel(metadata=plotter.get_metadata(), data=[plot])


@rest_v1_router.post("/ingest/{id}")
@inject
async def injest(id: Id, config: Dict, ingestors: Dict = Depends(Provide[Container.ingestors])):
    ingestor = ingestors.get(id)
    ingestor_kwargs = {inflection.underscore(k): v for k, v in config.items()}
    response = ingestor.ingest(**ingestor_kwargs)
    return response


@rest_v1_router.get("/hello")
async def hello_world():
   return {"message": "mamama"}