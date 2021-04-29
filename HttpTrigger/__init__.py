import azure.functions as func
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core import Workspace
from azureml.core.webservice.aci import AciWebservice
import random
import numpy
import logging
import json
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        sp = ServicePrincipalAuthentication(tenant_id= os.environ["tenantID"],
                                    service_principal_id=os.environ["clientId"],
                                    service_principal_password=os.environ["clientSecret"])
        ws = Workspace.get(name=os.environ["workspace"],
                        auth=sp,
                        subscription_id=os.environ["subscription_id"],
                        resource_group=os.environ["resource_group"] )   
        
        aci_service_name_1 = os.environ["service_collaborative_filtering"]
        
        service_1 = AciWebservice(ws, name=aci_service_name_1)

        aci_service_name_2 = os.environ["service_content_based"]
        
        service_2 = AciWebservice(ws, name=aci_service_name_2)      

    except ValueError:
        return func.HttpResponse(
             "Error. L'un ou les deux services n'est peut-être pas demarrer!",
             status_code=200
             )

    userId = req.params.get('userId')
    if not userId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            userId = req_body.get('userId')
    
    if userId:
        try:
            userId = int(userId)
            dico = dict()
            dico["userId"] = str(userId)
            input_data = json.dumps(dico) 
            response_1 = service_1.run(input_data)
            logging.info('response acirec')
            print(response_1)
            response_2 = service_2.run(input_data)
            logging.info('response acicontbase2gb')
            print(response_2)
            logging.info('Choix au hazard')
            response = response_1 + response_2
            Final_response = random.sample(response, 5)
                        
            #melanger les resultats
            random.shuffle(Final_response)
            logging.info('Recommandation faite!')
            arr = numpy.array(Final_response)
            
            return func.HttpResponse(json.dumps(arr.tolist()))
        except ValueError:
             return func.HttpResponse(
             "Error. L'un des deux services n'est peut-être pas demarrer!",
             status_code=200
             )
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a userId in the query string.Or the services are down!",
             status_code=200
        )