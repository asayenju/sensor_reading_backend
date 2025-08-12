from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.sensor_data import Sensor, sensor_model
import bcrypt
from app.auth.auth import validate_jwt_token
sensor_router = APIRouter()

@sensor_router.get("/", status_code=status.HTTP_200_OK)
async def get_sensor_metadata(token_to_validate, db: Session = Depends(get_db)):
    decoded_payload = validate_jwt_token(token_to_validate)
    try:
        if decoded_payload:
            sensors = db.query(Sensor).all()
            return {"sensors": [{"id": sensor.id, "uuid": sensor.uuid, "user_id": sensor.user_id} for sensor in sensors]}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not validate token"
            )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
@sensor_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_sensor(token_to_validate, user: sensor_model, db: Session = Depends(get_db)):
    """Create a new sensor"""
    decoded_payload = validate_jwt_token(token_to_validate)
    try:
        if decoded_payload:
            existing_sensor = db.query(Sensor).filter(Sensor.uuid == user.uuid).first()
            if existing_sensor:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="uuid already registered"
                )

            print(decoded_payload.get('id'))
            db_sensor = Sensor(
                uuid=user.uuid,  
                user_id=decoded_payload.get('sub')  # or from your decoded token payload
            )

            db.add(db_sensor)
            db.commit()
            db.refresh(db_sensor)

            return {"message": "successful creation", "sensor_id": db_sensor.id}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not validate token"
            )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
