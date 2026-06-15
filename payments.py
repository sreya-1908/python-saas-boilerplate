# from fastapi import APIRouter, Depends, HTTPException, Request, Header
# from sqlalchemy.orm import Session
# import database
# import models

# router = APIRouter()

# # 1. This endpoint simulates what happens after a user finishes checkout
# @router.post("/stripe/webhook")
# async def stripe_webhook(request: Request, db: Session = Depends(database.get_db)):
#     # In production, you would verify Stripe's cryptographic signature here.
#     # For the boilerplate template core, we parse the incoming payment event:
#     payload = await request.json()
    
#     event_type = payload.get("type")
    
#     if event_type == "checkout.session.completed":
#         session = payload.get("data", {}).get("object", {})
#         user_email = session.get("customer_details", {}).get("email")
        
#         if user_email:
#             # Look up the user who just paid and upgrade their account
#             user = db.query(models.User).filter(models.User.email == user_email).first()
#             if user:
#                 user.is_premium = True
#                 db.commit()
#                 print(f"💰 SUCCESS: Upgraded {user_email} to Premium status!")
#                 return {"status": "success", "message": "User upgraded"}
                
#     return {"status": "ignored"}

# from fastapi import APIRouter, Depends, Request
# from sqlalchemy.orm import Session
# import database
# import models

# router = APIRouter()

# @router.post("/stripe/webhook")
# async def stripe_webhook(request: Request, db: Session = Depends(database.get_db)):
#     payload = await request.json()
#     event_type = payload.get("type")
    
#     if event_type == "checkout.session.completed":
#         session = payload.get("data", {}).get("object", {})
#         user_email = session.get("customer_details", {}).get("email")
        
#         if user_email:
#             user = db.query(models.User).filter(models.User.email == user_email).first()
#             if user:
#                 user.is_premium = True
#                 db.commit()
#                 return {"status": "success", "message": f"Upgraded {user_email}"}
                
#     return {"status": "ignored"}

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import database
import models

router = APIRouter()

# This tells FastAPI exactly what structure to display in Swagger
class WebhookPayload(BaseModel):
    type: str
    data: dict

@router.post("/stripe/webhook")
async def stripe_webhook(payload: WebhookPayload, db: Session = Depends(database.get_db)):
    event_type = payload.type
    
    if event_type == "checkout.session.completed":
        session = payload.data.get("object", {})
        user_email = session.get("customer_details", {}).get("email")
        
        if user_email:
            user = db.query(models.User).filter(models.User.email == user_email).first()
            if user:
                user.is_premium = True
                db.commit()
                return {"status": "success", "message": f"Upgraded {user_email} successfully!"}
                
    return {"status": "ignored"}