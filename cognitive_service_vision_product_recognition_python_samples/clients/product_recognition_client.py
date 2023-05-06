import logging
import time

from cognitive_service_vision_model_customization_python_samples.clients import Client
from ..models import ProductRecognition, ProductRecognitionResponse, ProductRecognitionStatus

logger = logging.getLogger(__name__)

class ProductRecognitionClient(Client):
    def __init__(self, resource_type, resource_name: str, multi_service_endpoint, resource_key: str) -> None:
        super().__init__(resource_type, resource_name, multi_service_endpoint, resource_key)

    def evaluate(self, evaluation: ProductRecognition) -> ProductRecognitionResponse:
        json_response = self.request_put(f'/models/{evaluation.model_name}/evaluations/{evaluation.name}', json=evaluation.params)
        return ProductRecognitionResponse.from_response(json_response)

    def query_run(self, name, model_name) -> ProductRecognitionResponse:
        json_response = self.request_get(f'/models/{model_name}/evaluations/{name}')
        return ProductRecognitionResponse.from_response(json_response)

    def wait_for_completion(self, name: str, model_name: str, check_wait_in_secs: int = 60) -> ProductRecognitionResponse:
        start_time = time.time()
        while True:
            run = self.query_run(name, model_name)
            status = run.status
            if status in [ProductRecognitionStatus.FAILED, ProductRecognitionStatus.SUCCEEDED]:
                break
            time.sleep(check_wait_in_secs)
            total_elapsed = time.time() - start_time
            logging.info(f'Product recognition running {name} for {total_elapsed} seconds. Status {status}.')

        logger.info(f'Product recognition finished with state {run.status}.')

        if run.status == ProductRecognitionStatus.FAILED:
            logger.warning(f'Product recognition failed: {run.error}.')
        else:
            logger.info(f'Wall-clock time {total_elapsed / 60} minutes.')
            logger.info(f'Product recognition result: {run.result}')

        return run