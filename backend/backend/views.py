from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from .models import * # Import the UserInfo model from your Django app
from django.utils import timezone
import json
import requests
from django.utils.crypto import get_random_string
import secrets

def add_fav(request):
    team = request.GET.get('team')
    user = userteams.objects.get(email="jyan00017@gmail.com")
    followed = user.followedteams

    if team in followed:
        return JsonResponse({'error': team  + ' is already in your favourites'}, status=300)

    user.followedteams.append(team)
    user.save()
    return JsonResponse({'success': team + ' successfully added to favourites'}, status=200)


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
    follow = request.GET.get('followed')
    
    if follow == "False":
        follow = False
    else :
        follow = True

    followed = requests.get("http://localhost:8000/api/get-follow")
    teams = followed.json()['teams']
    games = []
    # Make a GET request to the ESPN API endpoint

    links = [
        "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard",
        "http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard",
        "http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard",
        #"http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard",
        "http://site.api.espn.com/apis/site/v2/sports/soccer/:league/scoreboard",
    ]

    for i in range(len(links)):
        url = links[i]
        print(links[i])
        response = requests.get(url)

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
            
            for game in today_games:
                name = game['name']
                short_name = game['shortName']
                status = game['status']
                #print(status)
                home_team = game['competitions'][0]['competitors'][0]['team']['displayName']
                away_team = game['competitions'][0]['competitors'][1]['team']['displayName']
                
                if follow:
                    print("ran follow is true")
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
                else:
                    print ("ran follow is false")
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

        else:
            print("get failed for " + url)
    
        # Return the scores as JSON response

    return JsonResponse(games, safe=False)
    #else:
        # If the request was not successful, return an error message
        #return JsonResponse({'error': 'Failed to fetch ESPN scores'}, status=response.status_code)

@csrf_exempt  # Add this decorator to disable CSRF protection (for simplicity; consider proper CSRF protection in production)
def google_login(request):
    if request.method == 'POST' or request.method == 'GET':
        try:
            #print("ran here")
            # Parse the JSON data sent from the React frontend

            data = json.loads(request.body)  # Now using json.loads to parse the request body
            token = data.get('token')
            url = f'https://www.googleapis.com/oauth2/v1/userinfo?access_token={token}'
            headers = {
                'Authorization': f'Bearer {token}',
                'Accept': 'application/json',
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                user_info = response.json()
                print(sendToDB(user_info))
                print(user_info)

                user_token = generate_secure_token()
                user_info['token'] = user_token

                user = userinfo.objects.get(email=user_info['email'])

                login(request, user)
                create_api_token(user, token)
            else:
                print(f"Error: {response.status_code}")


            # You can save it to the database, perform authentication, etc.
            
            # Respond with a JSON response (optional)
            response_data = {'token': 'Data received and processed successfully'}
            return JsonResponse(user_info, status=200)
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
    
    print("new user")
    followedTeams = userteams(
         user = existingUser,
         email = data['email'],
         followedteams = [],
         followplayers = []
    )

    followedTeams.save()

def create_api_token(user, token):
    api_token = APIToken.objects.create(user=user, token=token, user_id=1)
    return api_token


def generate_secure_token():
    token_secrets = secrets.token_urlsafe(32)  # Adjust length as needed
    
    return token_secrets