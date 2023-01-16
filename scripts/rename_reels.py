#! /usr/bin/env python

from pathlib import Path
import shutil
import random

movie_names = '''THX.1138.1971.1080p.avi
The.King.Of.Staten.Island.2020.1080p.avi
The.Half.Of.It.2020.1080p.avi
Soul.2020.1080p.mp4
Promising.Young.Woman.2020.720p.mkv
Palm.Springs.2020.1080p.mp4
Nomadland.2020.720p.mkv
Love.And.Monsters.2020.1080p.mp4
Tenet.2020.1080p.avi
Onward.2020.1080p.mp4
Greyhound.2020.1080p.mp4
Enola.Holmes.2020.720p.mp4
Tolkien.2019.1080p.mp4
The.Social.Dilemma.2020.720p.mkv
Polar.2019.1080p.avi
El.cuento.de.las.comadrejas.2019.1080p.mkv
Ready.Or.Not.2019.1080p.mkv
One.Child.Nation.2019.720p.mkv
My.Father.The.Spy.2019.1080p.mp4
A.Hidden.Life.2019.1080p.mkv
Klaus.2019.1080p.mp4
Frozen.II.2019.1080p.mp4
The.Lighthouse.2019.1080p.mp4
American.Factory.2019.720p.mkv
Ford.V.Ferrari.2019.1080p.mp4
I.Lost.My.Body.2019.1080p.mkv
Blinded.by.the.Light.2019.720p.mkv
The.Edge.of.Democracy.2019.720p.mkv
Apollo.11.2019.1080p.mkv
Game.Night.2018.720p.mp4
Hereditary.2018.1080p.mp4
Shadow.2018.1080p.mp4
Creed.II.2018.1080p.mp4
The.Burial.Of.Kojo.2018.1080p.mp4
Ash.Is.Purest.White.2018.1080p.mkv
Birds.Of.Passage.2018.1080p.mp4
The Post 2017 1080p.mkv
One.Cut.of.the.Dead.2017.1080p.mkv
War.For.The.Planet.Of.The.Apes.2017.1080p.mp4
The.Secret.Life.of.Pets.2016.1080p.avi
The Jungle Book 2016 1080p.mkv
Sing 2016 1080p.mkv
Kung Fu Panda 3 2016 1080p.mkv
Midnight.Special.2016.720p.mp4
Banking on Bitcoin 2016 1080p.mkv
The.Girl.with.All.the.Gifts.2016.720p.mp4
The.One.I.Love.2014.1080p.mp4
Interstellar.2014.2014.1080p.mp4
Coherence 2014 1080p.mkv
The.Croods.2013.720p.mp4
Monsters.University.2013.1080p.mp4
Frequencies.2013.720p.mp4
The Shock Doctrine 2009 720p.mp4
A.Scanner.Darkly.2006.1080p.mp4
Noam Chomsky - Rebel Without A Pause 2005 1080p.avi
The.Take.2004.1080p.avi
The.Matrix.Reloaded.2003.1080p.mp4
The.Matrix.1999.1080p.mp4
Contact.1997.1080p.mp4
Highlander 1986.1080p.mp4
Little.Shop.of.Horrors.1986.1080p.mp4
...And Justice for All.1979.1080p.mp4
The.Sting.1973.1080p.mp4
The.Wicker.Man.1973.720p.mp4
Mean Streets 1973 1080p.mkv
High.Plains.Drifter.1973.1080p.avi
Fantastic.Planet.1973.720p.mkv
Enter.the.Dragon.1973.720p.mkv
The.Mechanic.1972.1080p.mp4
The.Godfather.1972.1080p.mp4
Solaris.1972.1080p.mp4
Slaughterhouse-Five.1972.1080p.mp4
Pink.Flamingos.1972.720p.mkv
Last.Tango.In.Paris.1972.720p.mkv
The.Way.of.the.Dragon.1972.720p.mkv
The.French.Connection.1971.720p.mp4
The.Anderson.Tapes.1971.720p.mkv
Le.Mans.(Steve.McQueen).1971.1080p.mkv
Get.Carter.1971.1080p.mp4
Escape.From.The.Planet.of.the.Apes.1971.1080p.mkv
The.AristoCats.1970.1080p.mp4
Where.Eagles.Dare.1968.1080p.mp4
White.Christmas.1954.1080p.mp4
1917.2019.1080p.mp4
Ava.2020.1080p.mp4
Nomadland.2020.720p.mkv
Relic.2020.1080p.mp4
The.Empty.Man.2020.720p.mkv
Godmothered.2020.1080p.mp4
Freaky.2020.720p.mkv
The.New.Mutants.2020.1080p.mkv
The.Outpost.2020.720p.mkv
Holidate.2020.720p.mp4
The.Serpent.2020.720p.mp4
Another.Round.2020.720p.mkv
Tolkien.2019.1080p.mp4
The.Irishman.2019.720p.mp4
Once.Upon.A.Time.....In.Hollywood.2019.1080p.mp4
The.Poison.Rose.2019.720p.mp4
Ad.Astra.2019.1080p.mp4
Widows.2018.720p.mkv
A.Cure.for.Wellness.2016.1080p.mp4
The.Lobster.2015.720p.mp4
Mad.Max.Fury.Road.2015.720p.mp4
Southpaw.2015.1080p.mp4
Sicario 2015 1080p.mkv
Magic.Mike.XXL.2015.720p.mp4
Jurassic.World.2015.720p.mp4
Jaco.2015.720p.mp4
The Man from U.N.C.L.E. (2015) 1080p.mp4
Ex.Machina.2015.1080p.mp4
Spectre 2015 1080p.mkv
Z.for.Zachariah.2015.1080p.mp4
Sin City A Dame to Kill For 2014 720p.mp4
Two.Night.Stand.2014.1080p.mkv
Virunga.2014.720p.mkv
Birdman.2014.720p.mp4
X.Men.Days.of.Future.Past.2014.720p.mp4
The.Babadook.2014.720p.mp4
Autómata.2014.720p.mp4
Leviathan.2014.1080p.mp4
Black.or.White.2014.1080p.mp4
Edge.of.Tomorrow.2014.1080p.mp4
Guardians Of The Galaxy 2014 R6 720p.mkv
The.Theory.of.Everything.2014.1080p.mp4
Boyhood.2014.720p.mp4
The Salt Of The Earth 2014 480p.mp4
12.Years.a.Slave.2013.1080p.mp4
Nymphomaniac Vol.II.2013.Limited.816p.mp4
Nymphomaniac Vol.I.2013.Limited.816p.mp4
Coherence.2013.1080p.mp4
Warm.Bodies.2013.720p.mp4
Upstream.Color.2013.720p.mp4
jOBS.2013.720p.mp4
Side.Effects.2013.720p.mp4
Enemy.2013.720p.mp4
Short.Term.12.2013.720p.mp4
Under.the.Skin.2013.720p.mp4
The.Machine.2013.720p.mp4
Safety.Not.Guaranteed.2012.1080p.mp4
Stuck.in.Love.2012.720p.mp4
Flight.2012.720p.mp4
The.Perks.of.Being.a.Wallflower.2012.720p.mkv
 Life.of.Pi.2012.1080p.mp4
Warrior.2011.720p.mp4
The Devils Double 2011.720p.mp4
The Hunter 2011.720p.mp4
The.Help.2011.720p.mp4
Tyrannosaur.2011.720p.mp4
The.Skin.I.Live.In.2011.720p.mp4
We.Need.to.Talk.About.Kevin.2011.720p.mp4
Headhunters.2011.Limited.720p.mp4
50.50.2011.720p.mp4
The.Conspirator.2010.720p.mp4
Inside.Job.2010.1080p.mp4
Biutiful.2010.720p.mkv
Rango.2009.1080p.mp4
District.9.2009.1080p.mp4
Dogtooth.2009.480p.mkv
Enter.the.Void.2009.720p.mkv
Synecdoche.New.York.2008.1080p.mp4
Get.Smart.2008.720p.mp4
Blindness.2008.720p.mp4
Idiocracy.2006.720p.mkv
The.Host.2006.720p.mkv
2001.A.Space.Odyssey.1968.1080p.mkv
Mulholland Drive (2001) 1080p.mp4
In the Mood for Love (2000) 720p.mkv
Amores Perros (2000) BRRip 720p.mkv
Chicken.Run.2000.1080p.mp4
eXistenZ.1999.1080p.mp4
Funny.Games.1997.720p.mkv
The.crucible.1996.hdtv.720p.mp4
Ghost in the Shell (1995) 720p.mp4
Pulp.Fiction.1994.720p.mp4
Hardware.1990.720p.mp4
They.Live.1988.720p.mp4
Wings.of.Desire.1987.720p.mp4
Laputa.Castle.In.The.Sky.1986.1080p.mp4
Brazil.1985.DC.1080p.mp4
Koyaanisqatsi.1982.1080p.mp4
The.Evil.Dead.1981.1080p.mp4
Eraserhead 1977 1080p.mp4
Futureworld.1976.1080p.mp4
Chinatown.1974.720p.mp4
The.Wicker.Man.1973.720p.mp4
Fantastic.Planet.1973.720p.mkv
Sleeper.1973.720p.mp4
The.Sting.1973.1080p.mp4
The.Godfather.1972.1080p.mp4
Solaris.1972.Criterion.Collection.1080p.mp4
Slaughterhouse-Five.1972.REMASTERED.720p.mkv
The.Mechanic.1972.1080p.mp4
The.Omega.Man.1971.720p.avi
Get.Carter.1971.1080p.mp4
The.Anderson.Tapes.1971.720p.mkv
Where.Eagles.Dare.1968.BluRay.720p.mp4
Fahrenheit.451.1966.1080p.mp4
The.Trial.1962.1080p.mp4
Some.Like.It.Hot.1959.BluRay.720p.mp4
Vertigo.1958.720p.mp4
Citizen Kane (1941) 720p.mp4
THX 1138 (1971) DC 720p.mp4
Das Boot 1981 1080p.mkv
Melancholia.2011.720p.mp4
The Adventures of Buckaroo Banzai Across the 8th Dimension 720p.mp4
The Mask 1994 1080p.avi'''

source = Path('./static/reels')
target = Path('./demoVidLib')
reel_files = [f for f in source.glob('*')]

for f in reel_files:
    print(f.name)

for mv in movie_names.split('\n'):
    rf = random.choice(reel_files)
    if '.DS_Store' in rf.name : continue
    print(f"\nFROM {rf}")
    print(f"TO {target.joinpath(mv)}")
    shutil.copyfile(rf,target.joinpath(mv))

print(f"\nCreated demo video library with {len(movie_names)} entried in {target.name}.\n\n")