Hello There!

In `api` directory `api` contains configuration related to project and `event` contains `APIs` and `VIEWS`.

Create `virtualenv` and install `requirement.txt`.

_Every API is based on authentication by JWT, so user has to use Bearer Token for every API use._

**List of APIs:** 

`/auth/login/` Login and Token

`GET /api/events/` Shows all the public events

`POST /api/events` Adds the event

    Ex. of body
    {
    "title": "t9",
    "event_date": "2019-11-15",
    "limit": 100,
    "public": true,
    "registered_user": [],
    "invited_user": []
    }
    
 `GET /api/invitation/` Shows all the invitations send to the user -- It is the way to show private events to User.
 
 `GET /api/registered-events` Shows all the  invitation that user has Registered.
 
 `GET /api/events/ID` Shows the information of particular event
 
 `DEL /api/events/ID` Deletes the Event. _Only if it is called by author otherwise rejects it._
 
 `POST /api/register/ID` Register the User for particular Event. _Rejects if overlap, Rejects if reaches to Limit_

`POST /api/unregister/ID` Unregister User from particular Event.