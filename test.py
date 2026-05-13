
from database import save_profile, load_profile
save_profile('nnavkaur11@gmail.com', {
    'name': 'Navneet',
    'age': 25,
    'weight': 70,
    'height': 165,
    'gender': 'Female',
    'goal': 'Build Muscle',
    'experience': 'Intermediate',
    'email': 'nnavkaur11@gmail.com',
    'equipment': ['Dumbbells']
})
print(load_profile('nnavkaur11@gmail.com'))
