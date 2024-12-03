# Use the official Python image from the Docker Hub
FROM public.ecr.aws/lambda/python:3.13
# Copy the requirements file into the container
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . ${LAMBDA_TASK_ROOT}

CMD ["handler.handler"]
