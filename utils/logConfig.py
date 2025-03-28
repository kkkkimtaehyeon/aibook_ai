import logging


logging.basicConfig(
    level=logging.DEBUG,  # 디버그 레벨까지 출력되도록 설정
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger("aibook")
logger.setLevel(logging.DEBUG)
