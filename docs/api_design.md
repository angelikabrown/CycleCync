API Design

Account Creation

Endpoint
POST /users/register

Purpose
Create a new account

Frontend sends

Username
Password
email

Backend returns
Success message
UserID

Used by
Sign up screen


Daily Checkin

Endpoint
POST /checkin

Purpose
Add daily user data

Frontend sends

Temperature
Time taken
Mood
Sleep 
Energy

Backend returns
Success
Saved checkin

Used by
	Check in page

GET /checkin/today

Purpose
Load today's saved check-in.

Backend Returns
Temperature
Mood
Energy
Sleep
Time Taken

Used By
Daily Check-In page

PUT /checkin/{id}

Purpose
Update a previous check-in.

Frontend Sends
Updated check-in data

Backend Returns
Success message

Used By
Edit Check-In screen


Dashboard

Endpoint
Get /dashboard

Purpose
	Visualize user’s data


Backend Returns
	Current cycle day
Today's check-in
Current insight
Current streak


Used by
	Homescreen 


AI Chat

Endpoint
POST /chat

Purpose
	Users can ask questions and gain insight

Frontend sends
Question

Backend returns
	Answer

Use by

	AI chat screen

