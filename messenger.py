import json

class User:
    def __init__(self,id:int, name:str):
        self.name=name
        self.id=id
    def __repr__(self):
        return (f"User(name={self.name}, identifiant={self.id})")
    def to_dict(self):
        return{"id":self.id,"name":self.name}

class Channel:
    def __init__(self,id:int,member_ids:list,name:str):
        self.id=id
        self.name=name
        self.member_ids=member_ids
    def to_dict(self):
        return {'id':self.id,'name':self.name,'member_ids':self.member_ids}

class Message:
    def __init__(self, id: int, reception_date: str, sender_id: int, channel: int, content: str):
        self.id=id
        self.reception_date=reception_date
        self.sender_id = sender_id
        self.channel=channel
        self.content=content
    def __repr__(self):
        return(f"Message(identifiant={self.id}), channel={self.channel},content={self.content} ")
    def to_dict(self):
        return {'id':self.id, 'reception_date':self.reception_date, 'sender_id': self.sender_id, 'channel':self.channel,'content':self.content}

class Server:
    def __init__(self, L_users: list[User], L_channels: list[Channel], L_messages: list[Message]):
        self.users=L_users
        self.channels=L_channels
        self.messages=L_messages
    def __repr__(self):
        return(f"Server(users={self.users},channels={self.channels}, messages={self.messages}")
    def save(self):
        # fonction qui passe d'une classe à un dictionnaire afin de faire le json.dump
        serveur={}
        #server.users contient une somme d'objets 
        L_users=[user.to_dict() for user in self.users]
        serveur['users']=L_users
        L_channels=[channel.to_dict() for channel in self.channels]
        serveur["channels"]=L_channels
        L_messages=[message.to_dict() for message in self.messages]
        serveur["messages"]=L_messages
        with open('server.json', 'w') as f:
            json.dump(serveur, f,indent=10)
    @classmethod
    def load(cls):
        with open('server.json') as f:
            server=json.load(f)
            L_messages=[]
            for message in server['messages']:
                id=message['id']
                reception_date=message['reception_date']
                sender_id = message['sender_id']
                channel=message['channel']
                content=message['content']
                element = Message(id, reception_date, sender_id, channel, content)
                L_messages.append(element)
            L_channels=[]
            for channel in server['channels']:
                id=channel['id']
                name=channel['name']
                member_ids=channel['member_ids']
                element=Channel(id,member_ids,name)
                L_channels.append(element)
            L_users=[]
        for user in server['users']:
            id=user['id']
            name=user['name']
            element = User(id, name)
            L_users.append(element)
        return cls(L_users,L_channels,L_messages)

server = Server.load()

def ecran_accueil():
    print('=== Messenger ===')
    print('1. See users')
    print('2. See channel')
    print('x.Leave')
    print(' ')

def fonction_x():
    print('Bye!')

def fonction_user():
    print('Select an option: 1')
    print('User list')
    print('--------')
    for user in server.users:
        print(user.name)
    #for i in range(n):
        #print(i,'.',server['users'][i]["name"])
    print('n. Create user')
    print('x. Main menu')


def fonction_channel():
    for groupe in server.channels:
        print(groupe.id,groupe.name)
    print("x. main menu")
    print("n. ajouter un groupe")


# max([mes['id'] for mess in server['messages]])+1
def fonction_add_user():
    id=max([user.id for user in server.users])+1
    nom=input("donner un nom d'utilisateur")
    #modifier ici, mettre classe
    new_user=User(id,nom)
    server.users.append(new_user)
    #print(server)
    #print(server.users)
    server.save()


ecran_accueil()

def fonction_groupe():
    nom_groupe=input("donner moi le nom du groupe")
    membre=input('donner moi les gens membres du groupe')
    L=membre.split(',')
    L=[user.strip() for user in membre.split(',')]

    new_group_id = max([channel.id for channel in server.channels])+1

    L_members=[]
    for members in L:
        i=0
        while server.users[i].name != members:
            i=i+1
        L_members.append(server.users[i].id)
    new_group = Channel(new_group_id, L_members, nom_groupe)
    server.channels.append(new_group)
    server.save()

def ajout_membre_groupe():
    groupe=input('donner moi le nom du groupe')
    personne=input('donner moi le nom de la nouvelle personne')
    i=0
    while server['users'][i]['name']!=personne:
        i=i+1
    id=server['users'][i]['id']
    j=0
    while server['channels'][j]['name']!=groupe:
        j=j+1
    id=server['channels'][j]['id']
    server["channels"][j]['member_ids'].append(id)
    print(server)
    server.save()

choice = input('Select an option: ')
while choice !='x':
    if choice == 'x':
        fonction_x()
    elif choice == '1':
        fonction_user()
        choice=input('select an option')
        while choice!='x':
            if choice == 'n':
                fonction_add_user()
            choice=input('select an option')
        ecran_accueil()
        #choice=input('select an option')
    elif choice == '2':
        fonction_channel()
        choice=input('select an option')
        while choice!='x':
            if choice == 'n':
                fonction_groupe()
            choice=input('select an option')
        ecran_accueil()
    elif choice =='x':
        print('Bye') 
    else:
        input("taper une commande répertoriée")
    choice = input('Select an option: ')
