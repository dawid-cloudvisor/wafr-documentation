#!/usr/bin/env python3

import boto3

session = boto3.Session(profile_name='default',region_name='eu-central-1')
ecr = session.client('ecr')

registryId=""  # AWS account ID

repositories_list = ecr.describe_repositories(
    registryId=registryId,
    maxResults=1000
)

for repository in repositories_list['repositories']:
    repositoryName=repository['repositoryName']
    imagesList = ecr.list_images(
        registryId=registryId,
        repositoryName=repositoryName,
        maxResults=1000,
        filter={
            'tagStatus': 'TAGGED'
        }
    )
    for image in imagesList['imageIds']:
        imageTag=image['imageTag']
        imageData = ecr.batch_get_image(
            registryId=registryId,
            repositoryName=repositoryName,
            imageIds=[
                {
                    'imageTag': imageTag
                },
            ],
        )
        print("reuploading: ",repositoryName,":",imageTag, end=" ")
        for image in imageData['images']:
            tempTag=imageTag+"-temp"
            imageManifest=image['imageManifest']
            ecr.put_image(
                registryId=registryId,
                repositoryName=repositoryName,
                imageManifest=imageManifest,
                imageTag=tempTag
            )
            ecr.batch_delete_image(
                registryId=registryId,
                repositoryName=repositoryName,  
                imageIds=[
                    {
                    'imageTag': imageTag
                    },
                ]
            )
            ecr.put_image(
                registryId=registryId,
                repositoryName=repositoryName,
                imageManifest=imageManifest,
                imageTag=imageTag
            )
            ecr.batch_delete_image(
                registryId=registryId,
                repositoryName=repositoryName,  
                imageIds=[
                    {
                    'imageTag': tempTag
                    },
                ]
            )
            print("OK")