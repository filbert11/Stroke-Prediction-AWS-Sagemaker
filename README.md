# Automated Cloud Pipeline for Stroke Prediction
## Introduction
Stroke is Singapore's fourth leading cause of death which comprises 6.8% of all deaths and is the seventh leading cause of adult disability. Awareness of stroke risk factors and symptoms in Singapore is poor (only 40-50% of Singapore residents are able to identify stroke risk factors or stroke symptoms). This raises conserns as residents have poor awareness of identifying or detecting stroke despite it being a major debilitating health problem. Thus, this project aims to develop and deploy a Machine Learning (ML) model to predict whether Singapore residents are likely to get stroke based on their demographic, lifestyle and pre-existing health conditions such as hypertension and heart disease information. This project can assist residents in identifying if they are likely to get stroke so that they can pre-emptively seek medical advice to identify stroke and treat it.

The dataset used in this project is "Stroke Prediction dataset" which is obtained from Kaggle (https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset). 

AWS Sagemaker was used to create a Machine Learning Engineering pipeline (AWS pipeline) to predict Stroke. The ultimate idea was to deploy Telegram chatbot on AWS cloud instance for seamless interaction with our end users, allowing them to conveniently access our service through their mobile devices. The ability to bring the prediction service directly to the users would allow users to take better control of their health and gain greater awareness.

This is the overall project architecture.
![ProjectArchitecture](https://github.com/filbert11/Stroke-Prediction-AWS-Sagemaker/blob/main/plot/ProjectArchitecture.jpg)

However, as this project used AWS learner account. API integration of Telegram chatbot API with AWS API getaway was unable to be accomplished. Instead, a mock-up telegram chatbot was used to give idea on how the end product looks like and how it interacts with the users.

## Workflow Pipeline
The workflow steps performed in this project are as follows::
1. Processing step: to preprocess the input data
2. Tuning and evaluation step: to tune the model based on the best hyperparameters and evaluate the trained model
3. Condition step: to conduct evaluation, bias and explanability check on the trained model
4. Model step: to register the eligible model to model registry and deploy the model via Lambda step
![WorkflowPipeline](https://github.com/filbert11/Stroke-Prediction-AWS-Sagemaker/blob/main/plot/WorkflowPipelinesjpg.jpg)

The pipeline was deployed using the serverless hosting option. Since this is not an essential service, we might expect intermittent traffic patterns or periods of no traffic, for example at night. Choosing the serverless inference hosting option would grant us the benefits of real-time inference hosting such as low-latency results while keeping costs efficient during expected periods of downtime

The architecture for our inference pipeline would comprise a single inference container that runs the input processing, model loading, and prediction functionalities sequentially. A single container would suffice as the same programming language (Python) is used across all three functions. Additionally, the model that will be implemented is a single standalone model, not a model ensemble. Thus, it will not evoke considerations on having to load-balance the resources consumed by multiple models within the same container.

## Telegram Chatbot Mock up
The chatbot would ask a series of predefined questions to which the users can provide their inputs. These replies will be pre-processed and mapped to the corresponding features of our model. This will result in a prediction which will indicate if the user is at risk of getting a stroke. If the user is at risk, a link would be provided to redirect users to the Ministry of Health’s Stroke Hub. This will allow the users to self-help on the possible next steps for prevention and interventions to manage their stroke risk. This links back to our business proposition where early detection of symptoms will help with stroke management and reduce the risk of occurrence.
<br> ![TelegramChatbot1](https://github.com/filbert11/Stroke-Prediction-AWS-Sagemaker/blob/main/plot/TelegramChatbotMockUp1.jpg) 
![TelegramChatbot2](https://github.com/filbert11/Stroke-Prediction-AWS-Sagemaker/blob/main/plot/TelegramChatbotMockUp2.jpg)

## Conclusion
Automated cloud pipeline was created by using Machine Learning model (XGBoost) for stroke prediction. The AWS pipeline has provided ease of managing the data for pre-processing, training and evaluation in an effective manner. This was subsequently deployed for an endpoint interaction with Telegram API. While the AWS learner account utilized is limited for API call, a mock-up deployment was conducted instead. The automated pipeline showed that the project is feasible for interaction with end users, with the potential for scaling for more widespread adoption in the future. 
