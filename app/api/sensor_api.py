from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.sensor_data import Sensor, sensor_model
import bcrypt
from app.auth.auth import validate_jwt_token
sensor_router = APIRouter()

@sensor_router.get("/", status_code=status.HTTP_200_OK)
async def get_sensor_metadata(token_to_validate: str, db: Session = Depends(get_db)):
    decoded_payload = validate_jwt_token(token_to_validate)
    try:
        if decoded_payload:
            user_id = decoded_payload.get("sub")
            sensors = db.query(Sensor).filter(Sensor.user_id == user_id).all()
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
async def create_sensor(token_to_validate: str, user: sensor_model, db: Session = Depends(get_db)):
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

@sensor_router.delete("/{sensor_id}", status_code=status.HTTP_200_OK)
async def delete_sensor(token_to_validate: str, sensor_id: int, db: Session = Depends(get_db)):
    """Delete a user"""
    decoded_payload = validate_jwt_token(token_to_validate)
    try:
        if decoded_payload:
            # Check if user exists
            user_id = decoded_payload.get('sub')  # or however you store user identity in token

        # Query sensor by id AND user_id to ensure ownership
            db_sensor = db.query(Sensor).filter(
                Sensor.id == sensor_id,
                Sensor.user_id == user_id
            ).first()
            if not db_sensor:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Sensor not found"
                )
            
            # Delete user
            db.delete(db_sensor)
            db.commit()
            
            return {"message": "Sensor deleted successfully"}
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