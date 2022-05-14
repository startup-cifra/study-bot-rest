import time
import logging
from typing import Callable
from fastapi import HTTPException, Request, Response
from fastapi.routing import APIRoute
from logging import getLogger
from fastapi.responses import JSONResponse
from app.exceptions import CommonException, NotFoundException

logger = getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


class log_stuff(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            logger.info("******INFO*****")
            logger.info(f"Date time: {time.ctime()}")
            logger.info(f"Start request path={request.url.path} Method {request.method}")
            logger.info(f"Body requst { await request.body()} ")
            start_time = time.time()
            exception_object = None
            try:
                response: Response = await original_route_handler(request)
            except NotFoundException as ex:
                body = await request.body()
                detail = {"errors": ex.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)
            process_time = (time.time() - start_time) * 1000
            formatted_process_time = '{0:.2f}'.format(process_time)
            logger.info(f"Completed_in = {formatted_process_time}ms status_code = { response.status_code}")
            logger.info(f"Message: {response.body}")
            return response

        return custom_route_handler

        
