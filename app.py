from flask import Flask, request, jsonify
import boto3
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Initialize AWS SageMaker runtime client
sagemaker_runtime = boto3.client('sagemaker-runtime', region_name="us-west-2")

# SageMaker model endpoint name
ENDPOINT_NAME = "your-sagemaker-endpoint"

@app.route('/')
def health_check():
    """
    Health check endpoint.
    """
    return jsonify({"message": "Service is up and running!"})

@app.route('/predict', methods=['POST'])
def predict():
    """
    Prediction endpoint.
    Accepts JSON input and returns predictions from the SageMaker model.
    """
    try:
        # Get input data from the request
        input_data = request.json.get("data")
        if not input_data:
            return jsonify({"error": "Invalid input data"}), 400

        # Prepare payload for SageMaker
        payload = np.array(input_data).astype("float32").tobytes()

        # Invoke SageMaker endpoint
        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType="application/x-recordio-protobuf",
            Body=payload
        )

        # Decode and return the result
        result = response["Body"].read().decode("utf-8")
        return jsonify({"prediction": result})
    except Exception as e:
        # Log and return the error
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
