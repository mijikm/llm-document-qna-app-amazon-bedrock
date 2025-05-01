# Use the native inference API to send a text message to Anthropic Claude.

import boto3
import json

from botocore.exceptions import ClientError

# Step 1. Invoke the Bedrock Runtime client.
# Create a Bedrock Runtime client in the AWS Region of your choice.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Step 2: Set the model ID (Claude 2.1)
# This is the identifier for the specific model you want to use.
model_id = "anthropic.claude-v2:1"

# Step 3: Define and embed the prompt for the model.
prompt = """
    Analyze this customer feedback: 'I’ve been waiting too long for my loan approval, and the staff was not helpful.'
    And summarize the top 3 areas of improvement based on these customer feedback responses.
"""

# Step 4: Format the request payload (using the model's native structure).
native_request = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 512,
    "temperature": 0.5,
    "messages": [
        {
            "role": "user",
            "content": [{"type": "text", "text": prompt}],
        }
    ],
}

# Step 5: Convert the native request to JSON 
request = json.dumps(native_request)

try:
    # Step 6: Invoke the model with the request. (This send the request to the model.)
    response = client.invoke_model(modelId=model_id, body=request)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)

# Step 7: Decode the response body and print the response text.
model_response = json.loads(response["body"].read())

# Extract and print the response text.
response_text = model_response["content"][0]["text"]
print(response_text)


