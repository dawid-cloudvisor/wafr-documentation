#!/bin/bash

AWS_PROFILE="default"  # AWS_PROFILE for AWS CLI
REGION="eu-central-1"
REPLICATION_REGION="eu-west-1"
REGISTRY_ID=""  # AWS account ID

cat > replication.json << EOF
{ 
    "rules": [ 
        { 
            "destinations": [ 
                {
                    "region": "$REPLICATION_REGION", 
                    "registryId": "$REGISTRY_ID" 
                } 
            ] 
        } 
    ] 
} 
EOF

aws ecr put-replication-configuration --replication-configuration file://replication.json --region $REGION

REPOSITORY_LIST=$(aws ecr describe-repositories --region $REGION --output json --query repositories[*].repositoryName | tr -d '[],"')

for REPO in $REPOSITORY_LIST; do
	
	IMAGE_LIST=$(aws ecr list-images --region $REGION --repository-name $REPO --output json --filter tagStatus="TAGGED" --query imageIds[*].imageTag | tr -d '[],"')
	
	for IMAGE_TAG in $IMAGE_LIST; do

		TEMP_TAG=$IMAGE_TAG-temp
		IMAGE_MANIFEST=$(aws ecr batch-get-image --region $REGION --repository-name $REPO --image-ids imageTag=$IMAGE_TAG --output json | jq -r ".images[0].imageManifest")
			
		echo $IMAGE_MANIFEST > manifest.json
		
		aws ecr put-image --region $REGION --repository-name $REPO --image-manifest file://manifest.json --image-tag $TEMP_TAG

		sleep 30   # otherwise it throws "LayersNotFoundException", the bigger the image is the more time it needs to replicate layers

		aws ecr put-image --region $REPLICATION_REGION --repository-name $REPO --image-manifest file://manifest.json --image-tag $IMAGE_TAG

		aws ecr batch-delete-image --region $REGION --repository-name $REPO --image-ids imageTag=$TEMP_TAG

		aws ecr batch-delete-image --region $REPLICATION_REGION --repository-name $REPO --image-ids imageTag=$TEMP_TAG 

	done

done

rm manifest.json replication.json
