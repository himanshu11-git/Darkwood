'''importing the libraries'''

import random
import mysql.connector as sql
import sys
import os
import time
from rich.console import Console
from rich.progress import track
from rich.prompt import Prompt
from rich.table import Table

'''mysql connection'''
con = sql.connect(host="localhost", user="root", passwd="mysql")
cur = con.cursor()
def create_table():
      cur.exeute("create database if not exists Darkwood")
      cur.execute("use Darkwood")
      cur.execute("""create table if not exists profiles (
      name varchar(30) primary key,
      password varchar(30),
      level int(2) default 0,
      xp int(3) default 0,
      strength int(2) default 5,
      speed int(2) default 5,
      defence int(2) default 5,
      stamina int(2) default 5,
      accuracy int(2) default 5,
      weapon varchar(30) default fist,
      )""")
      cur.execute('''
      create table if not exists inventory (
      name varchar(30) primary key foreign key references profiles,
      fist default True,
      kitchen_knife default False,
      kunai default False,
      machete default False,
      katana default False,
      battle_axe default False,
      war_hammer default False,
      blow_gun default False,
      bow default False,
      spear default False,
      crossbow default False)
    ''')
      con.commit()
create_table()


'''defining the functions'''

def loading(desc=''):
  """just a loading bar"""  
  for _ in track(range(100), description=desc):
    time.sleep(random.randint(0,10)/100)

def clear():
  """clears the console"""
  os.system('cls' if os.name == 'nt' else 'clear')
  console.clear()


def print_slow(text, delay=0.01, style=""):
    """Prints the given text with a delay between each character."""
    for char in text:
        console.print(char, end='', style=style)
        time.sleep(delay)
    print()


def welcome(): 
   """Displays a welcome message."""
   console.print(centre('welcome to'), style='bold green on blue')
   console.print(centre('''

8888b.     db    88""Yb 88  dP Yb        dP  dP"Yb   dP"Yb  8888b.  
 8I  Yb   dPYb   88__dP 88odP   Yb  db  dP  dP   Yb dP   Yb  8I  Yb 
 8I  dY  dP__Yb  88"Yb  88"Yb    YbdPYbdP   Yb   dP Yb   dP  8I  dY 
8888Y"  dP""""Yb 88  Yb 88  Yb    YP  YP     YbodP   YbodP  8888Y"    [underline]demo[/]
'''),style="bold green on black")
   console.print( centre("press enter to start" ),style="bold green on blue")
   input()
   clear()



def centre(text): 
  """Centers the given text."""
  return text.center(256-len(text))


class profile:

    def login_profile(self,name,password):
      self.name=name
      self.password=password
      cur.execute("SELECT * FROM profiles WHERE name = %s AND password = %s", (self.name,self.password))
      result = cur.fetchone()
      if result:
        print_slow("Login successful!")
        clear()
        return True
    def signin_profile(self):
      cur.execute("sclect name from profiles")
      l=cur.fetchall()
      if self.name in l:
        print("name already exists")
      else:
        cur.execute("insert into profiles values(%s,%s)",(self.name,self.password))
        con.commit()
        print_slow("profile created")
        yield self.name
        input("press enter to continue")
        clear()


    def login(self):
        """Allows the user to login."""
        print("\033[1mLOGIN\033[0m".center(256),"\n[1] Load existing profile  \n[2] create new profile".center(256))
        choice = input("Enter your choice: ")
        if choice == "1":
          name = input("Enter your name: ")
          password = input("Enter your password: ")
          global playername
          playername=profile.login_profile(player,name,password)
        elif choice == "2":
          profile.signin_profile()
          time.sleep(1)

        else:
          print_slow("\nInvalid choice. Please try again.")
          clear()
          time.sleep(1) 
          profile.login() 
profile=profile()


def menu(): 
  """Main menu of the game."""
  padding=" " * (256 - len("Darkwood"))
  console.print(padding + "Darkwood",style="bold red on white")

  console.print(centre("MENU"),style="bold green")  
  print("[1] Play\n[2] Progress\n[3] Leaderboard\n[4] Credits\n[X] Exit")
  global choice 
  choice = input("Enter your choice: ")
  clear()


def leaderboard():
   cur.execute("select name,level,xp from player")
   table=Table(title="Leaderboard")
   for i in cur.fetchall():
     table.add_row(i[0],i[1],i[2])
   console.print(table)
   input("press enter to continue")
   clear()


def progress():
  console.print(f"{playername}'s Progress",style="green") 
  table = Table(title="")
  table.add_column("Level", justify="center")
  table.add_column("XP", justify="center")
  table.add_column("strength", justify="center")
  table.add_column("speed", justify="center")
  table.add_column("defence", justify="center")
  table.add_column("stamina", justify="center")
  table.add_column("accuracy", justify="center")
  table.add_row(str(player.level), str(player.xp), str(player.strength), str(player.speed), str(player.defence),str( player.stamina), str(player.accuracy))
  console.print(table)
  input("press enter to return to menu")
  clear()


"""the game"""

class character:
  def __init__(self,strength,speed, defence,stamina,accuracy,weapon,level=0,xp=0):
    self.strength = strength
    self.speed = speed
    self.defence = defence
    self.stamina = stamina
    self.accuracy = accuracy
    self.weapon = weapon
    self.level = level
    self.xp = xp
    cur.execute(f"select level,xp from {player}")
    self.level = cur.fetchone()[0]
    self.xp = cur.fetchone()[1]
class weapons:
  def __init__(self, dmg, range, type, back):
      self.damage = dmg
      self.range = range
      self.type = type
      self.back = back
  def display_weapon(self):
      print(f"damage: {self.damage}\nrange: {self.range}\ntype: {self.type}\nback: {self.back}")

fist=weapons(3,2,"melee",[10,10,10,10,10])
player=character(5,5,5,5,5,fist)  


class game:
  def play():
    '''shows levels'''
    clear()
    console.print("Select a level to play".center(256),style="yellow on black")
    print("""
[0]    level 0 : the beginning
[1]    level 1 : the dark forest
[2]    level 2 : the dark forest on light and a beast arrives
[3]    level 3 : welcome back home
[4]    level 4 : 10 years ago
[5]    level 5 : the cave to hell
[X]    exit
    """) 
    global lvl
    lvl=input("select level:")
    if lvl=="0":
      loading("loading level 0")
      clear()
      game.level0()
    elif lvl=="1":
      loading("loading level 1")
      clear()
      game.level1()
    elif lvl=="2":
      loading("loading level 2")
      clear()
      game.level2()
    elif lvl=="3":
      loading("loading level 3")
      clear()
      game.level3()
    elif lvl=="4":
      loading("loading level 4")
      clear()
      game.level4()
    elif lvl=="5":
      loading("loading level 5")
      clear()
      game.level5()
    elif lvl.upper()=="X":
      clear()
      menu()
    else:
      print_slow("invalid choice")
      time.sleep(1)
      clear()
      game.play()

  @staticmethod
  def mid(win,lvl): #interface between 2 lvls
    if player.level<=lvl and win is True:
      player.level+=1
    choice = Prompt.ask('''
    [1] continue game
    [2] go back to main menu
    [3] check progress
    [4] armory
    enter your choice ''',choices=["1","2","3","4"])
    clear()
    if choice=="1":
      game.play()
    elif choice=="2":
      menu()
    elif choice=="3":
      progress()
    elif choice=="4":
      armory()


  def level0():
    lvl=0
    print_slow('level 0 : THe beginning')
    console.print('''
before starting this adventure you may know
    this adventure contains many dangers and 
    many treasures.
    but, to accure these treasures you must 
    fight...

    you should know that people,weapons and monsters are given 
    different stats out of 20 points each
    for example an average person in this world of Darkwood has following stats:''')
    p= 7
    console.print(f"[bold red]strength: [/]{p}\n[bold red]speed:[/] {p}\n[bold red]defence: [/]{p}\n[bold red]stamina: [/]{p}\n[bold red]accuracy: [/]{p}")
    input("and yours is:")
    console.print(f"[bold red]strength: [/]{player.strength}\n[bold red]speed:[/] {player.speed}\n[bold red]defence: [/]{player.defence}\n[bold red]stamina: [/]{player.stamina}\n[bold red]accuracy: [/]{player.accuracy}")
    print('''
well, there aren't much of average people in this world.''' )
    print_slow("actually some are not even much of people.")
    print_slow('if you dare to continue, press enter')
    input()
    clear()
    print('''
you are a brave adventurer,
lets begin your adventure.
but before that lets warm up by some simple training''')
    choice=Prompt.ask('''what would you like to upgrade strength points(+2) or speed points(+2)
    ''',choices= ["strength","speed"])
    train(choice)
    choice=Prompt.ask('''what would you like to upgrade defence points(+2) or stamina points(+2)?
    ''',choices= ["defence","stamina"])
    train(choice)
    game.mid(True,0)
    clear()

  def level1(): #main story starts
      lvl=1
      pts=0
      print_slow('Level 1 : The Dark Forest')
      print_slow("Darkwood island\n")
      print('''
you are leaving a cave and 
there you are again in the dark forest ''')
      print('''ohh no !!! the local tribal people comming towards you quick you have to act fast ''')
      choice=Prompt.ask('''
     [1] run
     [2] fight
enter your choice: ''',choices=['1','2'])
      if choice=="1":
        pts+=1
        print('''
you ran away safely and you are now in the middle of the forest.
oh snap!!!
you fell into hole trap it must belongs to the tribal people.you have to escape from this trap they must be on the way .
its bad you are injured . stay calm otherwise you will loose your conscioness. noo!!!
      ''')
      elif choice=="2":
        pts+=3
        print('''
you are fighting with the tribal people.
you are a brave person but you are not strong enough to fight with them.
you have to escape from this forest.
you are injured.


ah! you fell head on into a hole trap it must belongs to the tribal people.you have to escape from this trap or you will end up dead
        ''')        
      print_slow('''
      \n
. . . 
you woke up now and you are in the middle of the forest''')
      print('''all of your weapons and resources were taken away, other than yourself you don't have anything to defend yourself.       
     ''')
      print('''what a drag !!!!''')
      choice=Prompt.ask('''what will you do?
     [1] try to escape the forest
     [2] find the tribals and take your resources back
    what will you do now? ''' ,choices=['1','2'])
      if choice=="1":
       pts+=2
       print(''' you were isolated by the tribals of forst and all of ypour resources were taken away now you have to run for your life. 
shoot they saw you hurry hurry hurry !!! wait a sec , it doesn't seems like they are chasing you . it looks like the chief of tribe .  
they seems friendly and calm .. they werer discussing something....
looks like they are inviting you into their tribe ...
its a great opportunity to took your resources back we should join them ..
you found out theirs a ritual tonight thays why they invited you as a sacrifice 
       ''')
       print('''pretend you know nothing and join them we have work smart and fast .. they all seems busy for festival its your time to take resources back and run away from this 
       ..  ''')
       print(''' finally you took your resouces back and you are now its your time run !!!! ''')
       print('''hide hide theres a soilder there''')
       print('''you have to sneak kill him and took his blow_gun ''') 
       Prompt.ask("press 1 to slash",choices=['1'])
      elif choice=='2':
       pts+=4
       print('''
you found the tribal village.
going close you found a tirbal soilder''')
       input("""closing in to the soilder, like a tiger.
he only have a machete
press enter to attack""")
       print("""you cracked his head
nice kill.
  you got that machete.""")
      choice=Prompt.ask('''
oh! looks like someone is coming this way.
  [1] hide behind a wall and wait for them
  [2] sneak in the house nearby
  [3] run away
what will you do? ''',choices=['1','2','3'])
      if choice=='1':
        pts+=4
        print('''
you hid behind a wall and waited for them to come.
there goes his soul, what ruckus you made of that soilder''')
        choice=Prompt.ask('''
  [1] enter main village
  [2] slash the other soilder
what will you do? ''',choices=['1','2'])

        if choice=='1':
          pts+=3
          print('''
you entered the main village and you found the tribal chief.
you slashed him and took his spear.
you took his resources and ran away from the midst of panicked tribals
now you are in the middle of the forest.
''')
        elif choice=='2':
          pts+=3
          print('''
he had a blow_gun
he tried to shoot you down but you dodged it.
and you slashed the other soilder in half and took his 
    blow_gun.
    and one last bolt                      
looks like you got a whole party on you''')
          input("""you ran to hide and waited for them to come. 
there is the chief of the tribe.
just within your range
pull out that blow_gun and
get ready to
take the shot.\n
press enter to shoot""")  
          print("""Headshot, you killed the chief of the tribe.
time to run
again you are in the middle of the forest""") 
        pts+=6
        clear()
        print(f"you got {pts} points")
        score(pts)
        game.mid(True,1)
        clear()
      elif choice=='2':
        pts+=3
        print('''
you sneaked in the house and looks like you found the tribal chief.
you took his head off''') 
        print('''seems he got some weapons.
        a blow_gun, a spear and 
        a kitchen_knife.                    
what will you pick? ''')
        input()
        print(''' you got the blow-gun and you have to kill him ''')
        input("press enter to shoot")
        print('''
now it's time to escape
you opened the door ''')
        time.sleep(1)
        print('''
and there is the chief of the tribe. The real one.
the whole tribe is on you.
looks like 
    the end''')
        pts+=1
        print_slow('You died',style='bold red')
        clear()
        print(f"you got {pts} points")
        score(pts)
        game.mid(False,1)
        clear()
      elif choice=='3':
        pts+=4
        print('''

several people ran after you out of nowhere ,they have weapons and they are chasing you.
some guy appeared in front of you and is aiming with a blow_gun.
you have to kill him.''')
        input("press enter to shoot")
        print('''
you killed him and took his blow_gun
you ran away from the tribal people.
you are now in the middle of the forest.
        ''')
        pts+=2
        clear()
        print(f"you got {pts} points")
        score(pts)
        game.mid(True,1)
        clear()

  def level2():
    lvl=2
    pts=0
    print_slow("level 2: The dark forest on light and a beast arrives")
    print('''
killing the tribe chief,and rushing to seek hide in forest.
you are now in the middle of the forest.
trying to find route to escape this island you climbed on a tree.
you saw a light in the distance, seems to be in the tribal village.
No. it's fire, the village is on fire.
to think, it must be due to the chaos you made. by the way

that's not the real problem 
as the fire had burnt all the tribal village and reached the forest, the forest residents are now in chaos
of all the animals and the tribal village is now in chaos.
there comes the real problem
not so clear but something is coming. 
coming towards you.
    ''')
    input("press enter to climb down and find safety")
    print('''
you climbed down and found a beast, some meters away.
it doesn't look like it's in a good mood.''')
    beast=enemy(7,4,6,6,3,fist)
    print_slow('''
so it's time to fight.''')
    console.print(f'''Enemy stats
    Name: [bold red]beast
    [bold red]strength: {beast.strength}
    [bold red]speed: {beast.speed}
    [bold red]defence: {beast.defence}
    [bold red]stamina: {beast.stamina}
    [bold red]accuracy: {beast.accuracy}''')  
    select_weapon()
    input("press 1 to attack")
    print('''thats a preety good hit from a weakass like you''')
    print('''hes coming toward you block his attack with your weapon''')
    input("press 456 to block the attack")
    print(''' you have to be quick and fast to match up with him''')
    print(''' you silly little goose aim for his head with your weapon''')
    input("press 789to jump and aim for his head")
    input("press 123 to hit for his head")
    print('''damn it !!!! 
    his head is way to hard to slice down with your weapon 
    you have to aim for his eyes and kill him''')
    print('''heres another plan for you distract him on the other side for a while and 
    when you are close enough to him , aim for his eyes and he might get down for a 
    while and and you will getyour time ''')
    print('''look theres a giant honey nest on above the tree of the beast aim for that 
    so you can get enough time to get close to him ''')
    input("press 555 to aim for the honey nest")
    input("press 888 to sprint towards the beast")
    input("press 5 to jump and ")
    input("press 9 to aim for his eyes")
    update_stats(player)
    if matching(player, beast) is True:
      print_slow("""
that beast was too strong for you.
but you managed to kill it.""")
      console.print("""
you now have to rush towards the shore of island 
you started running and you saw a boat.
you called for help and the boat is coming.
[red]boater[/red]: 'what are you doing on this island? You should hurry and get on boat or you will be a part of tribal rituals,
as the sacrifice to their god.'
you got on the boat and so great for your luck the boat his heading towards the mainland of Darkwood.""")
      clear ()
      pts+=4+matching(player,beast,True)
      print(f"you got {pts} points")
      game.mid(True,2)
    else:
      print_slow("""
you seemed delicious to that beast.
you made a good food for it.""")
      console.print("you died",style="bold red")
      clear()
      pts+=2+matching(player,beast,True)
      print(f"you got {pts} points")
      game.mid(False,2)
    clear()

  def level3():
    lvl=3
    print_slow("level 3: welcome back home ")
    console.print('''
you are at the mainland of Konoha
you were summoned to capital palace of Darkwood to share the knowledge you gained on that indigenous tribe and Darkwood island. ''')
    print(''' welcome !
          welcome !!
          welcome !!!''')
    console.print(f'''[blue]Someone:[/] we were pleased by your presence {playername} ''')
    console.print('''[blue] assistant of minister,most probably :[/] you were the first person to make alive from that island and the cannibal tribes.
we all admire your bravery and as we saved you from that island . if you dont mind we have a favour to ask''')
    input("press enter to talk")
    input(''' i m thankful to you all but right now I can't tell you anything about the tribe
and and a aa aaa ........ (fainted)''')
    console.print('''[blue]head medic : [/] finally you were awake its been 2 week 
and listen little kid the tribals whom you met and the blow dart that you used had poison on it's nip . 
maybe the the tribals are immune to poison so that doesn't effect them but as you used it you got poisoned .
now you are little much alright to share all the information and experiences you have gained from that island.
dont worry we are working for your antidote of the poison and we will give you the antidote within a week .
and just letting you know that you only have a month and you already wasted 2 weeks of your life 
.
[blue]you : [/]''' ,end='')
    input('''You sure talk a lot doctor but I would rather die instead ''')
    Prompt.ask('''[blue]assistant of minister: [/] ahhhhhhhhhh!!!!
listen kid we will get you anything you want money , fame, anything you want.    ''')
    Prompt.ask('''[blue]You:[/] (thinking) 
it's nothing that I want, but those horrific adventure I had there is far beyond humanity.''')
    Prompt.ask(f"""[blue]assistant of minister: [/] {playername} you are a brave kid but you might know how important is for us to know about that island if it's that horrific, as you said.""")
    Prompt.ask("[blue]You:[/] sure, but first get me out of this bed. I will tell the people everything I know about that island. Though everything is over there. No more questions for now.")
    console.print('''[blue]assistant of minister: [/] sure, will be waiting at community hall.''')
    time.sleep(1)
    print_slow("two days later      \nCommunity  Hall,Konoha",0.02)
    console.print(f'''[blue]Minister: [/] 
welcome to the community hall
The people of Darkwood are waiting for you, {playername}.
Please tell the world about that mysterious island.''')
    input("press enter to tell the world about that island")
    print_slow("story to be continued")
    clear()
    time.sleep(2)
    print("you got 0 points,\ndone nothing just all talk")
    game.mid(True,3)
    clear()

  def level4():
    lvl=4
    pts=0
    global player
    if player.level < 4:
      player=character(5,5,5,5,5,fist)
    print_slow("level 4: 10 Years ago.")
    print_slow("Darkwood island")
    console.print("""From decades after discovery of route to Darkwood island. Many tried to explore the island but failed.
One gone never came back.
And then like many others, You were also destined there, 
with a crew of 30 and two ships, your mission was to explore the island and find the way back to the mainland.
[blue]Captiain:[/] See that kid over there, that is the mysterious island in the legends of monsters. We will be reaching there soon, before finish the chores moron.""")
    input("already done with those. Now may I get some more training before reaching there as you said yesterday.")
    console.print(f"""[blue]Captain: [/] {playername} you are a brave kid.

your current stats are:
[bold red]strength: [/]{player.strength}\n[bold red]speed:[/] {player.speed}\n[bold red]defence: [/]{player.defence}\n[bold red]stamina: [/]{player.stamina}\n[bold red]accuracy: [/]{player.accuracy}""")
    choice=Prompt.ask("what training would you like to do? \n1.strength \n2.speed \n3.defence\n4.stamina \n5.accuracy" ,choices=["strength","speed","defence","stamina","accuracy"])
    train(choice)
    pts+=2
    print(f"increased {choice} by +2")   
    print_slow("some hours later")
    print("""Disembarked on the shore of Darkwood island.""")
    Prompt.ask("""Someone says they saw a strange man in bushes. 
    [blue]Someone:[/] Doesn't looks like a human. Everyone (screaming).. that's not a human, prepare yourself seems there are big animals out here everyone armed yourself up gotta finish this quick be careful that things already took away few of our comerades.""")
    print_slow("you see a beast in the bushes")
    beast=enemy(7,4,6,6,3,fist)
    console.print(f"Enemy stats: \n[bold red]strength:[/] {beast.strength}\n[bold red]speed:[/] {beast.speed}\n[bold red]defence:[/] {beast.defence}\n[bold red]stamina: [/]{beast.stamina}\n[bold red]accuracy:[/] {beast.accuracy}")
    input ()
    console.print("it's just in front of you")
    add_weapon(kunai)
    add_weapon(bow)
    print(f"Time to defned yourself {playername}")
    select_weapon()
    pts+=matching(player,beast,True)
    if matching(player, beast) is True:
      print_slow("""That's the kill,""")
      console.print("""[blue]Someone:[/] Oh my god, that was amazing.
few moments later, a team of 14 memebers were made to explore around the place they had disembarked, You are one of them.
after a few hours of wandering in the outskirts of forest you notice a unknown movement in the bushes.
[blue]Someone:[/] Hey kid you saw that too?
[blue]You:[/] Yes, I saw that too, but this one isn't appearing the same as before.""")
      choice = Prompt.ask("""What to do?
  ignore or investigate""",choice=["ignore","investigate"])
      if choice == "ignore":
        print("""[blue]Someone:[/] Hey kid, you should investigate that.
[blue]You:[/] I don't know what to do, I don't know what to do. Stop asking me for those things tell the team leader.
[blue]That guy:[/] sure, you go and inform that I will do investigation myself.
You told the team leader about the situation and it's been minutes from the guy gone and""")
        input()
        print_slow("you see a herd of beasts coming in the bushes")
        console.print("""[blue]Team leader:[/] Agh not again.... You see that everyone those aren't the same as before. Wait a minute, I think those are something like oversized mutant boars.
[blue]You:[/] That one,   there  that one seems to have eaten that guy who was gone to investigate
[blue]Team leader:[/] (commanding) everyone save your lifes, kill or be killed. (pointing at some kid) Run, run to the base and inform Captain. """)
        time.sleep(10)
        input("\n  press enter to shoot an arrow from your bow") 
        console.print(""" listen to me carefully its getting messy and most of are getting seperatd from the team so dont panic out much and prepare yourself we gotta finish this quick and these boars aren't normal they all mutant and the blood on their mouth means they killed some of us so be careful took your weapon out and kill em all . """)
        input(""" press enter to kill""")
        console.print("""we did it we able to took 2 of em down and now we have to complete it all fast . snap the rest of em are escaping . wait look there we gotta investigate that and there """)

      elif choice == "investigate":
        console.print("""It's running.
[blue]You:[/] (loud)That's a human, A man from the tribes. I am following
the chase begins
everyone is following the man.
that man vanished, but upon further going on his path... """)
        input()
      console.print("""[blue]Someone:[/] Whoa, hey everyone see that's a tribal village.\n[blue]Team leader:[/] (thinking) that's a tribal village... You(yes you) there go and inform captain\n[blue]You:[/] ahh sure, going.
upon heading back to the base, you noticed that there is family of some overseized boars
[blue]You :[/] (shockingly) hm, what are those? some kind of wild boars? not like the ones I ever saw before.  tf, getting late, better hurry 
finnaly arrived at the base.""")
      input("you informed the captain about the situation, the tribes and those boar like creatures")
      console.print("[blue]Captain:[/] (commanding) everyone let's go.")
      input("some of you rushed to the whereabouts of the scout team")
      console.print("[blue]Scout team leader:[/] (running towards you guys with a few of other scouts) run.. run captain. get the hell out of this place.\n[blue]Captain:[/] but, where are the others?\n[blue]Scout team leader:[/] dead. (watching down)fast lets return to base")
      input()
      time.sleep(2)         
    else:
      print_slow("""You Died.""",style="red")
      clear()
      pts+=3
      time.sleep(2)
      print(f"you got {pts} points")
      game.mid(False,4)
    print_slow("upon reaching back to the base.")
    console.print("[red]no one is there.[/]/n[blue]Captain:[/] (shocked and shouting) everyone,where? where are they? Not even our boats are here.[blue]Someone:[/] see there is blood on the beach.[blue]Someone else:[/] (shouting) they are dead. (running towards the beach) \n[blue]Captain:[/] (shouting) (everyone running towards the beach) shut up, must have been fight there isn't even any body here. Seems the rest of crew fleed away. Anyways they left use resources to survive and see there seems like ruins of 2 boats they must have left. btw (looking at scout team leader)What happened there?")
    input()
    console.print("[blue]Scout team leader:[/](in horror) we were attacked by boars. No, no.. they were just like boars but bigger, bigger than even a that beast who welcomed us. They had no flesh, but instead they were made of metals./n[blue]You:[/] metal with life. This island is beyond our understanding as a mere human.")
    console.print("[blue] Captain:[/] (in a high voice) Everyone pick up the resources we had now and together we..(loud noises) What is it now, fast fast everyone get ready we will enter the forest together and find a place to stay. Pick anything you want form here.")
    input("You walked till the weapons tent")
    choice=Prompt.ask("what will you pick?\nmachete or katana",choice=["machete","katanas"])
    add_weapon(choice)
    Prompt.ask("what will you pick?\nbattle_axe or war_hammer",choice=["battle_axe","war_hammer"])
    add_weapon(choice)
    print("And you also picked a bow")
    add_weapon(bow)
    Prompt.ask("[blue]Captain:[/] (shouting) Everyone, get ready. We will enter the forest and find out a shelter.")
    print_slow("you entered the forest")
    input("after sometime the you guys discovered a cave, seemed like a good place to stay. Captian decided enter the cave.")
    time.sleep(2)
    clear()
    print_slow("you entered the cave")
    input()
    time.sleep(2)
    clear()
    print(f"you got {pts} points.\nlevel ends")
    game.mid(True,5)
    clear()

  def level5():
    lvl=5
    pts=0
    print_slow("level 5: The cave to hell.")
    print("you are in the cave, while crew is moving resources inside the cave and you,the captian and remaining of the scout team heads deep into the cave.")
    console.print("here goes the cave in two ways, left or right, \n[blue]Captian[/]: (to scout leader) you go that way and we will go the other cave. If you find something rush back. ")
    input()
    print(f"you and the scout team heads deeper into the cave.\n[blue] Captain:[/] light up the lamps, no sunlight comes here.\n[blue]Someone:[/] there is very less space here to go deeper. (shouting) we should go back. \n[blue]Captain:[/] quiet don't shout there might be bats in there, {playername} you are the only one who can go deeper small kiddo. Head on we will be waiting here (to some scouts) go find the scout leader")
    input("you got into a shallow crack")
    console.print("[blue]You:[/]its glowing....(screaming)what? \n[blue] Captain:[/] what you saw there kid? \n[blue]Someone:[/] (in panic) wait, what's happening? Did anyone feels something? \n[blue]Someone else:[/] (shouting) it's an earthquake.. \n[blue]Captain:[/] (in a loud voice) Get the hell outt of there kid, something isn't.. (loud noises echoing, of what like something fell) wait that was a loud noise coming from mouth of cave, (commanding) get out of here, fast fast")
    input("you got out of that shallow opening and with others rush towards the cave's mouth")
    console.print("[blue]Captain:[/] what happened? \n[blue]Someone:[/] So much dust here trun lamps on. \nthe cave got closed my rocks\n[blue] Captain:[/] are all safe here? \n[blue] Captain's assistant:[/] (he was shfiting resources) (sadly) no, moron can't you see blood in those rocks? and those screams? (there is blood flowing through the rocks and screams of a crew member from outside) \n[blue]From outside:[/] Captain, is that you? if you can here me \n[blue]Captain:[/] (in a loud voice) yes, what happened here ? did those rock fell on him? \n[blue]That outsider:[/] not just him it's just me outside \n[blue]You:[/] just you? aren't here too less people in here for you to be alone? \n[blue]Someone who stayed back:[/] There are many kid, just some under those rocks. \n[blue]Captain:[/] (in a loud voice) (shouting) shit, guess what, as they said we just never should had came here. \n[blue]That one guy outside:[/] anyways, looks like I am not so lonely out here, ahh.. goodbye then.\nyou peeked from a hole between rocks, it's and beast, [blue]You:[/] a beast a beast, (you grabbed a crossbow from the ground) and aimed")
    Prompt.ask("press 0 to shoot",choice=["0"])
    print_slow("you shot the beast")
    pts+=5
    print("another one, aim")
    Prompt.ask("press 0 to shoot",choice=["0"])
    print("more rocks fell blocking the course of charge. the earth is shaking again . A stone smashed your head you are going unconscious")
    input("dozing off slowly you see that captain is pulling you out of rocks that fell on you")
    print_slow("you fell unconscious")
    time.sleep(1)
    console.clear()
    time.sleep(1)
    clear()
    console.print("you woke up in a room, you looked around and saw a door, you opened it and went outside . all the comrades already here . looks like they waiting for me only . oh seems like everyone is happy there did they manage yo find the safe area or what . [blue]Captain:[/] yes we finally found the safe area and all the people from the previous who went for the exploration. we found all the survivors of em and now the situation is under control.gotta admit you done great mate """)
    console.print("""wait captain before goin  faint i saw some lava stream down there between the cracks of the rock in the cave . the cave is kinda hot frok inside too . it felt like i m inside a furnace""")
    console.print(""" that because you are inside the crack hole between the volcano . whenever a volcano deactivated it goes a little low and the crack holes were developed btween them which you Callng cave and  those are really dangerous but rich in all kind of  minerals at same time. that's really a big achievement and we might found some valuable ores and maybe some virus or bacteria from ancient times .  """)
    console.print("""we gotta investigate that in future but now it's enough information for us as the mission is a big success. cheer up boys """)
    console.print("""finally we completed our mission and now its finally over we can go home now """)
    console.print(""" the demo version of this game completed here as the protagonist succed in his mission and the next update of this game is coming out soon on 2300 and with that this demo version comes to an end 
   have a safe night 🌒 """)


"""weapons""" #all stats has max value 20
fist=weapons(3,2,"melee",[player.speed,player.defence,player.stamina,player.strength, player.accuracy])
kitchen_knife=weapons(5,3,"melee",[player.speed-5,player.defence-5,player.strength-3,player.stamina-3,player.accuracy-3])
kunai=weapons(8,3,"melee",[player.speed-10,player.defence-3,player.strength-1,player.stamina-1,player.accuracy-1])
machete=weapons(10,5,"melee",[player.speed-10,player.defence-2,player.strength-4,player.stamina-4,player.accuracy-4])
katana=weapons(12,8,"melee",[player.speed-10,player.defence-3,player.strength-5])
battle_axe=weapons(15,6,"melee",[player.speed-10,player.defence-5,player.strength-6,player.stamina-6,player.accuracy-6])
war_hammer=weapons(17,10,"melee",[player.speed-12,player.defence-10,player.strength-8,player.stamina-8,player.accuracy-8])
blow_gun=weapons(7,12,"ranged",[player.speed-5,player.defence-7,player.strength-3,player.stamina-3,player.accuracy-3])
bow=weapons(10,15,"ranged",[player.speed-10,player.defence-8,player.strength-1,player.stamina-1,player.accuracy-1])
spear=weapons(8,10,"ranged",[player.speed-5,player.defence-5,player.strength-3,player.stamina-3,player.accuracy-3])
crossbow=weapons(10,17,"ranged",[player.speed-10,player.defence-10,player.strength-2,player.stamina-2,player.accuracy-2])

def train(S):
  cur.execute(f"update inventory where name={playername} set {S}={S}+2")
  con.commit()


def armory():
  """Armory of the game."""
  console.print("Armory".center(256),style="yellow on black")
  cur.execute(f"SELECT * FROM inventory WHERE name='{playername}")
  r= cur.fetchall()
  b=0
  d={'fist':r[0][1],'kitchen_knife':r[0][2],'kunai':r[0][3],'machete':r[0][4],'katana':r[0][5],'battle_axe':r[0][6],'war_hammer':r[0][7],'blow_gun':r[0][8],'bow':r[0][9],'spear':r[0][10],'crossbow':r[0][11]}
  for a in d:
    b+=1
    if d[a]==True:
      print(f"{b}. {a} ")


def select_weapon():
  """Allows the user to select a weapon."""
  print("\nSelect a weapon:")
  armory()
  player.weapon=input("enter selected weapon: ")


def add_weapon(weapon):
  """Allows the user to add a weapon to their inventory."""
  cur.execute(f"update inventory set {weapon} = True where name = {playername}")


def update_stats(player, weapon=player.weapon):
    player.speed += weapon.back[0]
    player.defence += weapon.back[1]
    player.stamina += weapon.back[2]
    player.strength += weapon.back[3]
    player.accuracy += weapon.back[4]


def score(pts):
  """Updates the user's xp."""
  cur.execute(f"update {playername} set xp = xp + {pts} where name = {playername}")
  con.commit()

class enemy:  
  def __init__(self, strength,speed, defence, stamina,accuracy,weapon):
    self.strength=strength 
    self.speed=speed
    self.defence=defence
    self.stamina=stamina
    self.accuracy=accuracy
    self.weapon=weapon
    self.accuracy=accuracy
    self.weapon=weapon
    """enemies to be made during story writing """


def matching(player,enemy,T=False):
  """decides who wins the fight, by giving points per stats comparison 
  and is required to calculate overall score of player"""
  playerpoints=player.speed+player.defence+player.stamina+player.strength+player.accuracy
  enemypoints=enemy.speed+enemy.defence+enemy.stamina+enemy.accuracy+enemy.strength  
  if player.accuracy>enemy.accuracy or player.stamina>enemy.stamina:
    playerpoints+=2
  if (player.weapon.range - enemy.weapon.range) <0:
    playerpoints+=-2
    score(playerpoints-enemypoints)
  if T is True: #to give points obtained from a fight
    return score 
  else:
    return playerpoints>enemypoints


def exit_animation():
    print("Confirm exit?".center(256))
    print("\n1. Yes    2. No".center(256))
    choice = input("". center (256))
    if choice == "1":
      print("\nExiting game...")
      loading()
      time.sleep(1)
      print("Goodbye!") 
      clear()
      print_slow('Thank You for Playing Darkwood'.center(256))
      sys.exit()
    elif choice == "2":
      menu()
    else:
      print_slow("\nInvalid choice. Please try again.")
      exit_animation()


'''creating variables'''
choice='enter'
console=Console()
try:
  playername=profile.name
  cur.execute(f"SELECT level FROM profiles WHERE name =  {playername}")
  lvl = cur.fetchone()[0]
except:
  playername="Player"
  lvl=0



"""__main__"""
try:
  welcome()
  profile.login()
  clear()
  while True:
      clear()
      menu()
      if choice == "1":
          console.print("loading levels...".center(256),style="red on black")
          time.sleep(1)
          clear()
          game.play()
          clear()
      elif choice == "2":
          progress()
      elif choice == "3":
          leaderboard()
      elif choice == "4":
          console.print(centre("credits"),style='red on black')
          print_slow("""Computer Science project for class XII Board examinaton 2024.

Developed by:
          Himanshu Kumar() and Piyush Parate().
          under guidance of Mr. Nikhil Verma,
          """)
          input("\npress enter to exit")
          clear()
      elif choice =="x" or choice=="X":
          con.commit()
          exit_animation()        
      else:
          print_slow("\nInvalid choice. Please try again.")
          time.sleep(1)
          clear()
except KeyboardInterrupt:
  exit_animation()
except Exception as e:
          print(f"Error raised: {e}")


          #"""end of the code"""
