p_sitio = "/s"
p_user = "/u"
p_password = "/p"
p_token = "/t"


with open("ejemplo.txt", "r") as f:
    print(dir(f))
    print(f.readlines())