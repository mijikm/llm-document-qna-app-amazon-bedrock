# Use the native inference API to send a text message to Meta Llama 3.

import boto3
import json

from botocore.exceptions import ClientError

# Step 1. Invoke the Bedrock Runtime client.
# Creates a client object for the Bedrock Runtime API in the AWS region us-east-1. 
# The client allows the code to interact with the Bedrock Runtime service, which is used to invoke foundation models like Meta Llama 3.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Step 2: Set the model ID (Llama 3.2 3B Instruct)
# e.g., Llama 3 3b, Llama 70b Instruct.
model_id = "us.meta.llama3-2-3b-instruct-v1:0"

# Step 3: Define and embed the prompt for the model.
prompt = """
    Analyze this customer feedback: 'I’ve been waiting too long for my loan approval, and the staff was not helpful.'
    And summarize the top 3 areas of improvement based on these customer feedback responses.
"""

# Embed the prompt in Llama 3's instruction format.
# It is important to keep the formatted_prompt as the model (Meta Llama 3) expects the input to follow a specific structure or format.
# The formatted_prompt wraps the raw prompt in a predefined instruction format that the model is trained to understand. 
# This format includes markers like <|begin_of_text|>, <|start_header_id|>, and <|end_header_id|> to indicate different sections of the input, 
# such as user input and assistant response.
formatted_prompt = f"""
<|begin_of_text|><|start_header_id|>user<|end_header_id|>
{prompt}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
"""

# Step 4: Format the request payload (using the model's native structure).
# The model expects a JSON object with the prompt and other parameters.
# This is the payload format for Llama 3.
native_request = {
    "prompt": formatted_prompt,
    "max_gen_len": 512,
    "temperature": 0.5,
}

# Step 5: Convert the native request to JSON (as the request body must be a JSON string).
request = json.dumps(native_request)

try:
    # Step 6: Invoke the model with the request. (This send the request to the model.)
    response = client.invoke_model(modelId=model_id, body=request)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)

# Step 7: Decode the response body and print the response text.
model_response = json.loads(response["body"].read())

# Extract and print the response text (the key called generation).
response_text = model_response["generation"]
print(response_text)


