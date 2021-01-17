import geocoder
g = geocoder.ip('me')
print("Your location: ")
print(g.latlng)