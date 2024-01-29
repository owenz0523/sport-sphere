from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import userinfo # Import the UserInfo model from your Django app
from django.utils import timezone
import json

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
    # Create a new UserInfo instance and set its fields
    new_entry = userinfo(
        email=data['email'],
        password='',
        name=data['name'],
        created_at=timezone.now(),  # Use timezone.now() to get the current timestamp
        last_login=None  # Optionally, set last_login to None if needed
    )

    # Save the new entry to the database
    new_entry.save()