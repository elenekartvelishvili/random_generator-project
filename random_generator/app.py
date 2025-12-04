import requests    #პითონის ბიბლიოთეკა,რომელიც გვეხმარება http request-ების  გაგზავნაში.pip-ით დავაყენე.
# #აქ  გამოვიყენე NOAA-დან  მზის ქარის რეალურ დროში მონაცემების მისაღებად.

import random    #ამ ბიბლიოთეკას ვიყენებ დაბლა,როდესაც უკვე მივიღებ seed-ს.

# URL,სადაც შენახულია მონაცემები,რომელიც საჭიროა,random რიცხვების დასაგენერირებლად.(json ფორმატი)
URL = "https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json"



def get_latest_solar_wind():
    response = requests.get(URL) #გავაგზავნე get request,რათა სერვერიდან წამოვიღო მონაცემები.
    data = response.json() #json-ს გარდავქმნი python-ისთვის გასაგებ ლისტად.
    header = data[0]    #ეს არის ჰედერი,რომელიც გვეუბნება რა სახის ინფორმაცია აქ მოცემული. მის დაბლა კი ნამდვილი მონაცემებია.
    latest = data[-1] #რადგან ეს არის ერთი ობიექტების ლისტი,სადაც თარიღების მიხედვით ვიღებთ მონაცამებს,ლისტის ბოლოდან ამოვიღე ყველაზე ახალი მონაცემები.
#NOAA ამ JSON-ს განუწყვეტლივ, რეალურ დროში აახლებს,ამიტომ ყოველთვის ერთი და იგივე მონაცემს ვერ ამოვიღებთ.

    speed_index = header.index("speed")     #ამოვიღე პოზიცია სიჩქარის,სიმკვრივის და ტემეპერატურის ჰეადერეიდან index-ის გამოყენებით.
    density_index = header.index("density")  #ჰეადერში,როგორცაა ამათი პოზიცია განაწილებული ისე იქნება ნამდვილ მონაცმებში.
    temperature_index = header.index("temperature")

    speed = (latest[speed_index])       #ამოვიღე უახლესი მონაცემები.
    density =( latest[density_index])
    temperature = (latest[temperature_index])

    return speed, density, temperature



def build_seed(speed, density, temperature):
    seed_text = speed+ density + temperature   # შევკრიბე. NOAA აბრუნებს რიცხვებს სტრინგის სახით!.
    seed_value = 0
    for i, ch in enumerate(seed_text):
        seed_value += ((i + 1) * ord(ch)) ^ (i + 3)
    #რადგან გენერატორს სჭირდება see-ად int,შევუსაბამე თითოეულ სიმბოლოს თავისი ASCII. რათა უფრო განსხვავებული seed
    #მივიღო გავამრავლე ch-თავის ინდექსზე და გამოვიყენე XOR.
    return seed_value



def generate_random_number(seed_value):
    random.seed(seed_value)          #seed გავხადე build_seed-დან დაბრუნებული seed_value.
    return random.randint(0, 65535)   #seed-ის გამოყენებით ალგორითმი დააგენერირებს 16- ბიტიან რიცხვს



def display_results(speed, density, temperature, seed_value, random_16bit):

    print("***********Solar Wind Random number Generator***********")
    print("Solar wind data (speed||density||temperature):", speed, density, temperature)
    print("Seed integer:", seed_value)
    print("Random 16-bit value:", random_16bit)

#მარტივი ფუნქცია შედეგის სანახავად

def main():
    speed, density, temperature = get_latest_solar_wind()
    seed_value = build_seed(speed, density, temperature)
    random_16bit = generate_random_number(seed_value)
    display_results(speed, density, temperature, seed_value, random_16bit) #შევაჯამოთ ყველა ნაბიჯი.


main() #გამოვიტანოთ შედეგები.
