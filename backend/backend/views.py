from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import * # Import the UserInfo model from your Django app
from django.utils import timezone
import json
import requests
from django.http import JsonResponse

def get_follow(request):
    # Get a list of all followed teams from DB
    user = userteams.objects.get(email="jyan00017@gmail.com")
    data = {
        'teams':user.followedteams,
        'players':user.followplayers
    }
    # Return the scores as JSON response
    return JsonResponse(data, safe=False)

def get_nhl(request):
    # Make a GET request to the ESPN API endpoint
    url = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard"
    response = requests.get(url)

    followed = requests.get("http://localhost:8000/api/get-follow")
    teams = followed.json()['teams']
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Extract relevant information from the response
        # For example, you can access today's games and their scores
        today_games = data['events']
        league_info = {
            'name' : data['leagues'][0]['name'],
            'abbr' : data['leagues'][0]['abbreviation'],
        }
        
        games = []
        for game in today_games:
            name = game['name']
            short_name = game['shortName']
            status = game['status']
            home_team = game['competitions'][0]['competitors'][0]['team']['displayName']
            away_team = game['competitions'][0]['competitors'][1]['team']['displayName']
            if (home_team in teams) or (away_team in teams):
                home_score = game['competitions'][0]['competitors'][0]['score']
                away_score = game['competitions'][0]['competitors'][1]['score']
                home_team_record = game['competitions'][0]['competitors'][0]['records'][0]['summary']
                away_team_record = game['competitions'][0]['competitors'][1]['records'][0]['summary']
                games.append({
                    'name' : name,
                    'short_name' : short_name,
                    'status' : status,
                    'ht_record' : home_team_record,
                    'at_record' : away_team_record,
                    'home_team': home_team,
                    'away_team': away_team,
                    'home_score': home_score,
                    'away_score': away_score

                })
        
        # Return the scores as JSON response
        return JsonResponse(games, safe=False)
    else:
        # If the request was not successful, return an error message
        return JsonResponse({'error': 'Failed to fetch ESPN scores'}, status=response.status_code)

@csrf_exempt  # Add this decorator to disable CSRF protection (for simplicity; consider proper CSRF protection in production)
def google_login(request):
    if request.method == 'POST' or request.method == 'GET':
        try:
            print("ran here")
            # Parse the JSON data sent from the React frontend
            data = json.loads(request.body.decode('utf-8'))

            # Process the user data
            sendToDB(data)

            # You can save it to the database, perform authentication, etc.
            
            # Respond with a JSON response (optional)
            response_data = {'message': 'Data received and processed successfully'}
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def sendToDB(data):
    existing_user = userinfo.objects.filter(email=data['email']).first()
    if existing_user:
        existing_user.last_login = timezone.now()
        existing_user.save()
        return {'message': 'User already exists'}

    newEntry(data)
    # Create a new UserInfo instance and set its fields
    

def newEntry(data):
    print("ran newEntry")
    newEntry = userinfo(
        email=data['email'],
        password='',
        name=data['name'],
        created_at=timezone.now(),  # Use timezone.now() to get the current timestamp
        last_login=None  # Optionally, set last_login to None if needed
    )

    # Save the new entry to the database
    newEntry.save()

    existingUser = userinfo.objects.filter(email=data['email']).first()
    
    followedTeams = userteams(
         user = existingUser,
         email = data['email'],
         followedteams = None,
         followplayers = None
    )

    followedTeams.save()
