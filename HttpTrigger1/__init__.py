import logging
import json

import azure.functions as func

from datetime import datetime,date,timezone
import threading
from time import sleep
import uuid

import firebase_admin

from firebase_admin import credentials,firestore
import google.cloud

from google.cloud import firestore as fire



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    objectId = req.params.get('objectId')
    if not objectId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            objectId = req_body.get('objectId')

    if objectId:
        uuidDate=Attendance().update_create_if_missing(objectId)
        body={"uuidDate":uuidDate}
        return func.HttpResponse(
            body=json.dumps(body),
            mimetype="application/json",
            charset="utf-8",
        )
    else:
        return func.HttpResponse(
             "Please pass a objectId on the query string or in the request body",
             status_code=400
        )

class Attendance(object):
    if not firebase_admin._apps:
        cred = credentials.Certificate("HttpTrigger1/serviceAccountKey.json") 
        default_app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    def getUuidDate(self):
        datetime1=datetime.now(timezone.utc)
        min_slot=str((datetime1.hour*60+datetime1.minute)//10)
        Date=datetime1.isoformat()[:10]+'0'*(3-len(min_slot))+min_slot
        uuid1=str(uuid.uuid4())
        uuid1=uuid1[:9]+'0786'+uuid1[13:]
        return uuid1+Date
    def update_create_if_missing(self,objectId):
        # [START update_create_if_missing]
        user_ref = Attendance.db.collection(u'users').document(f"{objectId}")
        uuidDate=self.getUuidDate()
        doc = user_ref.get()
        if doc.exists:
            if self.check(doc):
                user_ref.update({u'contacts_temp': fire.ArrayUnion([f"{uuidDate}"])})
            else:
                user_ref.set({u'contacts_temp': fire.ArrayUnion([f"{uuidDate}"])},merge=True)
        else:
            # Atomically add a new region to the 'regions' array field.
            user_ref.set({u'contacts_temp': fire.ArrayUnion([f"{uuidDate}"])},merge=True)
        return uuidDate
        # [END update_create_if_missing]
    def check(self,doc):
            # [START_EXCLUDE]
            try:
                doc.get(u'contacts_temp')
                return True
            except:
                return False
            # [END_EXCLUDE]
