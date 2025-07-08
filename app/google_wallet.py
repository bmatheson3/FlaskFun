from dotenv import load_dotenv
import os
import uuid

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
from google.auth import jwt, crypt


class GenericPass:
    """
    Class that defines the a Generic Pass using the Google Wallet API.
    
    Initialisers:
        key_file_path: Google ADC (Application Default Credentials)
        issuer_id: Unique ID provided for using Google Wallet API
        class_id: Customisable class name for pass
        auth(): Checks user's credentials to authorise
    """
    
    load_dotenv()
    
    # Class initialiser
    def __init__(self):
        self.key_file_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.issuerId = os.getenv("ISSUER_ID")
        self.classId = self.issuerId + '.flask_noAI_nfc_try'
        self.auth()
        print(self.issuerId)
        print(self.classId)
    
    
    # Authorising user
    def auth(self):
        self.credentials = Credentials.from_service_account_file(
            self.key_file_path,
            scopes=['https://www.googleapis.com/auth/wallet_object.issuer'])
    
        # creates a Google API Client based on name, version & credentials
        self.client = build('walletobjects', 'v1', credentials=self.credentials)
        


    # Create class
    def create_class(self):
        """
        Method to create a base class from which the Google pass objects can instantiate
        """

        # Defining class structure (json)
        # This was taken from Google's developers tutorial (in js) and was adapted for python
        generic_class = {
            'id': self.classId,
            'enableSmartTap': True,
            'classTemplateInfo': {
                'cardTemplateOverride': {
                    'cardRowTemplateInfos': [
                    {
                    'twoItems': {
                        'startItem': {
                        'firstValue': {
                            'fields': [
                            {
                                'fieldPath': 'object.textModulesData["points"]'
                            }
                            ]
                        }
                        },
                        'endItem': {
                        'firstValue': {
                            'fields': [
                            {
                                'fieldPath': 'object.textModulesData["contacts"]'
                            }
                            ]
                        }
                        }
                    }
                    }
                ]
                },
                'detailsTemplateOverride': {
                'detailsItemInfos': [
                    {
                    'item': {
                        'firstValue': {
                        'fields': [
                            {
                            'fieldPath': 'class.imageModulesData["event_banner"]'
                            }
                        ]
                        }
                    }
                    },
                    {
                    'item': {
                        'firstValue': {
                        'fields': [
                            {
                            'fieldPath': 'class.textModulesData["game_overview"]'
                            }
                        ]
                        }
                    }
                    },
                    {
                    'item': {
                        'firstValue': {
                        'fields': [
                            {
                            'fieldPath': 'class.linksModuleData.uris["official_site"]'
                            }
                        ]
                        }
                    }
                    }
                ]
                }
            },
            'imageModulesData': [
                {
                'mainImage': {
                    'sourceUri': {
                    'uri': 'https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/google-io-2021-card.png',
                    },
                    'contentDescription': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Google I/O 2022 Banner'
                    }
                    }
                },
                'id': 'event_banner'
                }
            ],
            'textModulesData': [
                {
                'header': 'Gather points meeting new people at Google I/O',
                'body': 'Join the game and accumulate points in this badge by meeting other attendees in the event.',
                'id': 'game_overview'
                }
            ],
            'linksModuleData': {
                'uris': [
                {
                    'uri': 'https://io.google/2022/',
                    'description': 'Official I/O \'22 Site',
                    'id': 'official_site'
                }
                ]
            }
        }
        
        # Check if the class already exists
        try:
            self.client.genericclass().get(resourceId=self.classId).execute()
        # If it does not, create it
        except HttpError as e:
            # Checking for any unexpected errors (we expect a 404 in the case that the class does not exist)
            if e.status_code != 404:
                print(e.error_details)
                return self.classId
        else:
            print(self.classId + " already exists!")
            return self.classId

        # Creating the class with the generic class json
        self.client.genericclass().insert(body=generic_class).execute()
        print("Created class with ID: " + self.classId)
        
        return self.classId


    # Create pass object
    def create_pass_object(self):
        '''
        Method to generate a URL that allows a unique nfc pass (with a unique ID) to be added to the Google wallet
        '''
        object_suffix = str(uuid.uuid4()).replace('[^\\w.-]', '_')
        object_id = self.issuerId + "." + object_suffix
        
        # This was taken from Google's developers tutorial (in js) and was adapted for python
        genericObject = {
            'id': object_id,
            'classId': self.classId,
            'smartTapRedemptionValue': object_id,
            'genericType': 'GENERIC_TYPE_UNSPECIFIED',
            'hexBackgroundColor': '#4285f4',
            'logo': {
            'sourceUri': {
                'uri': 'https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/pass_google_logo.jpg'
            }
            },
            'cardTitle': {
            'defaultValue': {
                'language': 'en',
                'value': 'Google I/O \'22'
            }
            },
            'subheader': {
            'defaultValue': {
                'language': 'en',
                'value': 'Attendee'
            }
            },
            'header': {
            'defaultValue': {
                'language': 'en',
                'value': 'Alex McJacobs NFC'
            }
            },
            'barcode': {
            'type': 'QR_CODE',
            'value': object_id
            },
            'heroImage': {
            'sourceUri': {
                'uri': 'https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/google-io-hero-demo-only.jpg'
            }
            },
            'textModulesData': [
            {
                'header': 'POINTS',
                'body': '1234',
                'id': 'points'
            },
            {
                'header': 'CONTACTS',
                'body': '20',
                'id': 'contacts'
            }
            ]
        }
        
        # Create the JWT claims 
        claims = {
            'iss': self.credentials.service_account_email,
            'aud': 'google',
            'origins': ['www.example.com'],
            'typ': 'savetowallet',
            'payload': {
                'genericObjects': [genericObject]
            }
        }
        
        # The service account credentials are used to sign the JWT
        signer = crypt.RSASigner.from_service_account_file(self.key_file_path)
        token = jwt.encode(signer, claims).decode('utf-8')

        print('Add to Google Wallet link')
        # long link for now, need to shorten
        print(f'https://pay.google.com/gp/v/save/{token}')
        
        return f'https://pay.google.com/gp/v/save/{token}'