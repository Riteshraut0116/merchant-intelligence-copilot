# Multi-stage build for Lambda container image
FROM public.ecr.aws/lambda/python:3.12 as builder

# Install build dependencies
RUN dnf install -y gcc gcc-c++ make cmake

# Copy requirements and install dependencies
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -t /asset

# Final stage
FROM public.ecr.aws/lambda/python:3.12

# Copy installed dependencies from builder
COPY --from=builder /asset ${LAMBDA_TASK_ROOT}

# Copy application code
COPY src/ ${LAMBDA_TASK_ROOT}/

# Set the CMD to your handler
CMD ["handlers.health.lambda_handler"]
