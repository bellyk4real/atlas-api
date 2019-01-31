# test_app.py
from app import app
from flask import json

def test_app():        
    response = app.test_client().post(
        '/model',
        data=json.dumps({
	                        "Saving accounts":"little", 
	                        "Checking account":"little",
	                        "Age":17,
	                        "Job": 3,
	                        "Housing":"rent",
	                        "Duration": 4,
	                        "Purpose": "furniture/equipment",
	                        "Sex": "female",
	                        "Credit amount":12000
                        }),

        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data["result"]["prediction"] == '0'