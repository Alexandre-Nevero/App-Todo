from fastapi import FastAPI
import os # For osgetenv protection
import boto3 # To acces AWS credentials and codes

app = FastAPI(title="Notes API ni Abu", version="1.0.0", description="API for managing notes")
              
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Abu's Notes API"}

@app.get("/health")X
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# AWS config
DYNAMO_TABLE = os.getenv("DYNAMO_TABLE","abu-todo-notes")
S3_BUCKET = os.getenv("S3_BUCKET","notes-images-bucket-abu")

# Initialize AWS resources (DynamoDB, S3, and etc.) boto3 gets resources from our AWS account
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

# models for the data
class Note:
    id: str
    title: str
    Conntent: str
    created_at: str
    updated_at: str
    images: list[str] = []
    image_urls: List[str] = []

# schemas for the models for the data


# Utility functions for signing S3 because we configured privacy
def generate_presigned_url(image_keys: List[str]) -> List[str]:
    signed_urls = []
    for image_key in image_keys:
        try:
            signed_url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': S3_BUCKET, 'Key': image_key},
                ExpiresIn=3600  # URL valid for 1 hour
            )
            signed_urls.append(signed_url)
        except Exception as e:
            print(f"Error generating presigned URL for {image_key}: {e}")
            signed_urls.append("https://{S3_BUCKET}.s3.ap-northeast-1.amazonaws.com/{image_key}")  # Fallback to public URL if needed
    return signed_urls



# Validation

# Endpoints

# Middleware allowed all for simplicity and for protection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
