from pydantic.networks import HttpUrl
from sqlalchemy.sql.functions import mode
from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    
    # first check if the post is available
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mentioned post {vote.post_id} is not available")
    
    #vote query to identify if there is already a vote
    vote_query =  db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        # avoid adding vote again - duplicate votes
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        # Add new vote as it's not available
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully added the Vote"}  
    else:
        # If not vote available cannot delete vote
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        # Vote is available so delete the vote
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted Vote"}
