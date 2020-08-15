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
        dictionary={
                    "type": "service_account",
                    "project_id": "barqat-786kmr",
                    "private_key_id": "b0c4863d61bce045d62769a167a452c03fba7194",
                    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDMS/wVyDqfTWdR\nzHUQMCh4WYpaCA5PDpecbulMoKEytT6fxroJiYJtCr9oqM2ona2Fn75eF8NX7FcJ\njfy0Q36YgWRDu7WVqbMAtNL3ClGLZ8DLh+Y1BXCSuNC2t7s3t1/Mk4rXDCsEoR1W\nzDajM+LACrBHeefcoNBJyGS9QEoSEzCPrwJgQjB87t2IhJN8qFYCL+IxUct2bzJZ\nOPCgjjdw5Kpi/5rEKMzvUkW/rtCuinS7G0jriC43q4MrX9neqFpVBiOPBzdIysOr\n0UJP5GDidV4KjSMpceaYKmgZLVUs6hs8AtWZoquvLuE0ZLKvyRx2yi6bPswYL/kD\n4vwa2SpfAgMBAAECggEACV1CRM1UwpCNt9YjV4adlEambNIJtd35XRZIY1bJjMV6\nBWDaji1baRwhAe8a3iu8FG/qDe4Q6irPIoT7nFerqdnkeqZUAHQy3Eltkh1K95Td\n5XZpOuzw6AjIqFdroXYqUfpBVvIb1q575cqehoSOVDcpNV2FHzvP0FH7LCGSQ5nA\ni2hTsiLg4EgPuQzNYDP1Nsg9IrWG8OMkY7xe9nJyHycAJOTFVypt1D3OwMCri4NG\nlcsjG0F/z10x9oelViZm1Lopa7322cUfAHR5q6/q1WBeZdtLG7OU6Ibq+YSQZ69h\nHKjf4oazntp0pNH8Gg8RwTUK8VAFfE9Hi6/BadMd4QKBgQD39ORAARPn9EUJijRR\nkKZ22vcpXUmISQylh7SB0QeAvhkOhkmmYwYmhgD6q/PpF7ap0czzqwgokJaB6WPZ\nrRT3RzrKP/jL1t5BmsweIJ3/O3VEGl3SlfZ75wFrEJ4ATD8qXR4YJjYZBq+WxFwx\nhIcq5vcg2ZJbVdnIu5rCcNaLpQKBgQDS7IdXd4EzeI/rwp1uJoZaUV3igVAMFwzh\nc7X4oF1rOl6Wasd9awpc5RZoLKnV2Q7tP74QiAh0BhoBR/ur1/JolQnjM9aisKXh\nYNSOLyO85cpC/rLPzz9ewIO0Y50kyt6vwm5on4SXo4xJegkblVdvUpGXnJsodu/v\n8cIqh+COswKBgQCBGWZF1MnSeSIAx45Z8WBafcM2LDX+2VnWTYO0G2s2osNVBqIO\nGXy4Tgjwetrxv8EBRhTZwXDr/ev/E89DJJTH8rQvXYNiTitGKRyhiwX4P7LclIXJ\nAP9mn23jmrFJImm42uayWCLOgOanLvF5brEZq0t8NQu4tkg/9T2sgyeRaQKBgC+F\n12Cfrl6YdWTbLnlY+MB0wMB9/jkbIG3TklZ4W1QDjLg7SsM5UNZpT0kddw6Vn0VZ\nLUuwOqdZkJZlT5ECUL27hsTIMz3oqxdCp+F5QYYYCCBcHpGv0klY+tOz9f4KL25O\nUm4EMu2vjbYoZtDuLwsIAYG1aUgOtDTNtb+7aZ79AoGAFIO8KOmCcPG4acZ7k5dJ\nAssnrn3gk4B7HutkeH37hmtPTMm9BG/IvVjh1VhfO6PXcLfWp2w/f6oy20eYbQCi\nlxgwuYA7mXq+yK326TPj2fxO1y16QlBUdKvi5ixNBVPFgkmJnSMmwWAFabOG777v\n0AMz9k3x04eyrG4Nu6AGWSk=\n-----END PRIVATE KEY-----\n",
                    "client_email": "firebase-adminsdk-k5wud@barqat-786kmr.iam.gserviceaccount.com",
                    "client_id": "107390833634558654963",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-k5wud%40barqat-786kmr.iam.gserviceaccount.com"
        }
        cred = credentials.Certificate(dictionary) 
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