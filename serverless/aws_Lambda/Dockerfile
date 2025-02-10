# Use the official AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.8

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}/lambda_function.py
COPY threads_downloader.py ${LAMBDA_TASK_ROOT}/threads_downloader.py
COPY ai_nsfw_detection.py ${LAMBDA_TASK_ROOT}/ai_nsfw_detection.py
COPY ai_captioning.py ${LAMBDA_TASK_ROOT}/ai_captioning.py
COPY requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt

# Install dependencies
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler
CMD ["lambda_function.lambda_handler"]
