import yaml

user = []
pswd = []
pro = 0

def readConfig():
    with open("./config/config.yaml", 'r', encoding='utf8') as s:
        stream = s.read()
    return yaml.safe_load(stream)

try:
    streamConfig = readConfig()
    configTimeIntervals = streamConfig['time_intervals']
    userData = streamConfig['User_login']
except FileNotFoundError:
    print('Error: config.yaml file not found, rename EXAMPLE-config.yaml to config.yaml inside /config folder')
    print('Erro: Arquivo config.yaml não encontrado, renomear EXAMPLE-config.yaml para config.yaml dentro da pasta /config')
    exit()
    
acc = configTimeIntervals['acc']
n = acc+1
def accounts():
    for w in range(1,n):
        print("Profile",w)
        account = str(input("user account:\t"))
        password = str(input("password:\t"))
        user.append(account)
        pswd.append(password)
