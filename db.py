import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore
from firebase_admin.exceptions import FirebaseError

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


#db.collection('medications').add({'name':'paracetamol', 'dose':400})


#Authentication
def sign_in(email, password):
    try:
        user = auth.get_user_by_email(email)
        print('Successfully signed in as:', user.uid)
        return user.uid
    #except auth.AuthError as e:
    except FirebaseError as e:
       # print('Error signing in':, e)
        return None

#create user
def create_user(email, password):
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        print('Successfully created user:', user.uid)
        return user.uid
   # except firebase_admin.auth.AuthError as e:
    except FirebaseError as e:
        print('Error creating user:', e)
        return None
    
#def get_current_user(): # wer hat request abgeschickt

# get meds from db
def get_medication_db():
    medications_ref = db.collection("medication")
    medications = medications_ref.stream()

    medication_names = [medication.to_dict()["name"] for medication in medications]
    return medication_names
    

#create_user(email="jones@doctor.hos", password="123456")

def sign_out():
    try:
        firebase_admin.auth.sign_out()
        print('User successfully logged out.')
    except FirebaseError as e:
        print('Error logging out:', e)
