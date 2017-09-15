# -*- coding: utf-8 -*-
import random
import re
from flask import Flask, render_template
app = Flask(__name__)

# The list of adjectives to use
adjectives = [
	"admiring", "adoring", "agitated", "amazing", "angry", "awesome",
	"backstabbing", "berserk", "big", "boring", "clever", "cocky",
	"compassionate", "condescending", "cranky", "desperate", "determined",
	"distracted", "dreamy", "drunk", "ecstatic", "elated", "elegant",
	"evil", "fervent", "focused", "furious", "gigantic", "gloomy", "goofy",
	"grave", "happy", "high", "hopeful", "hungry", "insane", "jolly", "jovial",
	"kickass", "lonely", "loving", "mad", "modest", "naughty", "nauseous",
	"nostalgic", "pedantic", "pensive", "prickly", "reverent", "romantic",
	"sad", "serene", "sharp", "sick", "silly", "sleepy", "small", "stoic",
	"stupefied", "suspicious", "tender", "thirsty", "tiny", "trusting"
]

# The list of surnames, all notable scientists and hackers.
surnames = [
	("albattani",	"<strong>Muhammad ibn Jābir al-Ḥarrānī al-Battānī</strong> was a founding father of astronomy. https://en.wikipedia.org/wiki/Mu%E1%B8%A5ammad_ibn_J%C4%81bir_al-%E1%B8%A4arr%C4%81n%C4%AB_al-Batt%C4%81n%C4%AB"),
	("allen",		"<strong>Frances E. Allen</strong>, became the first female IBM Fellow in 1989. In 2006, she became the first female recipient of the ACM's Turing Award. https://en.wikipedia.org/wiki/Frances_E._Allen"),
	("almeida",		"<strong>June Almeida</strong>. Scottish virologist who took the first pictures of the rubella virus. https://en.wikipedia.org/wiki/June_Almeida"),
	("archimedes",	"<strong>Archimedes</strong> was a physicist, engineer and mathematician who invented too many things to list them here. https://en.wikipedia.org/wiki/Archimedes"),
	("ardinghelli",	"<strong>Maria Ardinghelli</strong>. Italian translator, mathematician and physicist. https://en.wikipedia.org/wiki/Maria_Ardinghelli"),
	("aryabhata",	"<strong>Aryabhata</strong>. Ancient Indian mathematician-astronomer during 476-550 CE https://en.wikipedia.org/wiki/Aryabhata"),
	("austin",		"<strong>Wanda Austin</strong>. Wanda Austin is the President and CEO of The Aerospace Corporation, a leading architect for the US security space programs. https://en.wikipedia.org/wiki/Wanda_Austin"),
	("babbage",		"<strong>Charles Babbage</strong> invented the concept of a programmable computer. https://en.wikipedia.org/wiki/Charles_Babbage."),
	("banach",		"<strong>Stefan Banach</strong>. Polish mathematician, was one of the founders of modern functional analysis. https://en.wikipedia.org/wiki/Stefan_Banach"),
	("bardeen",		"<strong>John Bardeen</strong> co-invented the transistor. https://en.wikipedia.org/wiki/John_Bardeen"),
	("bartik",		"<strong>Jean Bartik</strong>, born Betty Jean Jennings, was one of the original programmers for the ENIAC computer. https://en.wikipedia.org/wiki/Jean_Bartik"),
	("bassi",		"<strong>Laura Bassi</strong>, the world's first female professor https://en.wikipedia.org/wiki/Laura_Bassi"),
	("bell",		"<strong>Alexander Graham Bell</strong>. an eminent Scottish-born scientist, inventor, engineer and innovator who is credited with inventing the first practical telephone. https://en.wikipedia.org/wiki/Alexander_Graham_Bell"),
	("bhabha",		"<strong>Homi J Bhabha</strong>. was an Indian nuclear physicist, founding director, and professor of physics at the Tata Institute of Fundamental Research. Colloquially known as \"father of Indian nuclear programme\"- https://en.wikipedia.org/wiki/Homi_J._Bhabha"),
	("bhaskara",	"<strong>Bhaskara II</strong>. Ancient Indian mathematician-astronomer whose work on calculus predates Newton and Leibniz by over half a millennium. https://en.wikipedia.org/wiki/Bh%C4%81skara_II#Calculus"),
	("blackwell", 	"<strong>Elizabeth Blackwell</strong>. American doctor and first American woman to receive a medical degree. https://en.wikipedia.org/wiki/Elizabeth_Blackwell"),
	("bohr",		"<strong>Niels Bohr</strong> is the father of quantum theory. https://en.wikipedia.org/wiki/Niels_Bohr."),
	("booth",		"<strong>Kathleen Booth</strong>, she's credited with writing the first assembly language. https://en.wikipedia.org/wiki/Kathleen_Booth"),
	("borg",		"<strong>Anita Borg</strong>. Anita Borg was the founding director of the Institute for Women and Technology (IWT). https://en.wikipedia.org/wiki/Anita_Borg"),
	("bose",		"<strong>Satyendra Nath Bose</strong>. He provided the foundation for Bose–Einstein statistics and the theory of the Bose–Einstein condensate. https://en.wikipedia.org/wiki/Satyendra_Nath_Bose"),
	("boyd",		"<strong>Evelyn Boyd Granville</strong>. She was one of the first African-American woman to receive a Ph.D. in mathematics; she earned it in 1949 from Yale University. https://en.wikipedia.org/wiki/Evelyn_Boyd_Granville"),
	("brahmagupta",	"<strong>Brahmagupta</strong>. Ancient Indian mathematician during 598-670 CE who gave rules to compute with zero. https://en.wikipedia.org/wiki/Brahmagupta#Zero"),
	("brattain",	"<strong>Walter Houser Brattain</strong> co-invented the transistor. https://en.wikipedia.org/wiki/Walter_Houser_Brattain"),
	("brown",		"<strong>Emmett Brown</strong> invented time travel. https://en.wikipedia.org/wiki/Emmett_Brown (thanks Brian Goff)"),
	("carson",		"<strong>Rachel Carson</strong>. American marine biologist and conservationist, her book Silent Spring and other writings are credited with advancing the global environmental movement. https://en.wikipedia.org/wiki/Rachel_Carson"),
	("chandrasekhar","<strong>Subrahmanyan Chandrasekhar</strong>. Astrophysicist known for his mathematical theory on different stages and evolution in structures of the stars. He has won nobel prize for physics. https://en.wikipedia.org/wiki/Subrahmanyan_Chandrasekhar"),
	("colden",		"<strong>Jane Colden</strong>. American botanist widely considered the first female American botanist. https://en.wikipedia.org/wiki/Jane_Colden"),
	("cori",		"<strong>Gerty Theresa Cori</strong>. American biochemist who became the third woman—and first American woman—to win a Nobel Prize in science, and the first woman to be awarded the Nobel Prize in Physiology or Medicine. Cori was born in Prague. https://en.wikipedia.org/wiki/Gerty_Cori"),
	("cray",		"<strong>Seymour Roger Cray</strong> was an American electrical engineer and supercomputer architect who designed a series of computers that were the fastest in the world for decades. https://en.wikipedia.org/wiki/Seymour_Cray"),
	("curie",		"<strong>Marie Curie</strong> discovered radioactivity. https://en.wikipedia.org/wiki/Marie_Curie."),
	("darwin", 		"<strong>Charles Darwin</strong> established the principles of natural evolution. https://en.wikipedia.org/wiki/Charles_Darwin."),
	("davinci", 	"<strong>Leonardo Da Vinci</strong> invented too many things to list here. https://en.wikipedia.org/wiki/Leonardo_da_Vinci."),
	("dijkstra", 	"<strong>Edsger Wybe Dijkstra</strong> was a Dutch computer scientist and mathematical scientist. https://en.wikipedia.org/wiki/Edsger_W._Dijkstra."),
	("dubinsky",	"<strong>Donna Dubinsky</strong>. played an integral role in the development of personal digital assistants (PDAs) serving as CEO of Palm, Inc. and co-founding Handspring. https://en.wikipedia.org/wiki/Donna_Dubinsky"),
	("easley",		"<strong>Annie Easley</strong>. She was a leading member of the team which developed software for the Centaur rocket stage and one of the first African-Americans in her field. https://en.wikipedia.org/wiki/Annie_Easley"),
	("einstein",	"<strong>Albert Einstein</strong> invented the general theory of relativity. https://en.wikipedia.org/wiki/Albert_Einstein"),
	("elion",		"<strong>Gertrude Elion</strong>. American biochemist, pharmacologist and the 1988 recipient of the Nobel Prize in Medicine. https://en.wikipedia.org/wiki/Gertrude_Elion"),
	("engelbart",	"<strong>Douglas Engelbart</strong> gave the mother of all demos: https://en.wikipedia.org/wiki/Douglas_Engelbart"),
	("euclid",		"<strong>Euclid</strong> invented geometry. https://en.wikipedia.org/wiki/Euclid"),
	("euler",		"<strong>Leonhard Euler</strong> invented large parts of modern mathematics. https://de.wikipedia.org/wiki/Leonhard_Euler"),
	("fermat",		"<strong>Pierre de Fermat</strong> pioneered several aspects of modern mathematics. https://en.wikipedia.org/wiki/Pierre_de_Fermat"),
	("fermi",		"<strong>Enrico Fermi</strong> invented the first nuclear reactor. https://en.wikipedia.org/wiki/Enrico_Fermi"),
	("feynman",		"<strong>Richard Feynman</strong> was a key contributor to quantum mechanics and particle physics. https://en.wikipedia.org/wiki/Richard_Feynman"),
	("franklin",	"<strong>Benjamin Franklin</strong> is famous for his experiments in electricity and the invention of the lightning rod."),
	("galileo",		"<strong>Galileo</strong> was a founding father of modern astronomy, and faced politics and obscurantism to establish scientific truth.  https://en.wikipedia.org/wiki/Galileo_Galilei"),
	("gates",		"<strong>William Henry \"Bill\" Gates III</strong> is an American business magnate, philanthropist, investor, computer programmer, and inventor. https://en.wikipedia.org/wiki/Bill_Gates"),
	("goldberg",	"<strong>Adele Goldberg</strong>, was one of the designers and developers of the Smalltalk language. https://en.wikipedia.org/wiki/Adele_Goldberg_(computer_scientist)"),
	("goldstine",	"<strong>Adele Goldstine</strong>, born Adele Katz, wrote the complete technical description for the first electronic digital computer, ENIAC. https://en.wikipedia.org/wiki/Adele_Goldstine"),
	("golick",		"<strong>James Golick</strong>, all around gangster."),
	("goodall",		"<strong>Jane Goodall</strong>. British primatologist, ethologist, and anthropologist who is considered to be the world's foremost expert on chimpanzees. https://en.wikipedia.org/wiki/Jane_Goodall"),
	("hamilton",	"<strong>Margaret Hamilton</strong>. Director of the Software Engineering Division of the MIT Instrumentation Laboratory, which developed on-board flight software for the Apollo space program. https://en.wikipedia.org/wiki/Margaret_Hamilton_(scientist)"),
	("hawking",		"<strong>Stephen Hawking</strong> pioneered the field of cosmology by combining general relativity and quantum mechanics. https://en.wikipedia.org/wiki/Stephen_Hawking"),
	("heisenberg",	"<strong>Werner Heisenberg</strong> was a founding father of quantum mechanics. https://en.wikipedia.org/wiki/Werner_Heisenberg"),
	("heyrovsky",	"<strong>Jaroslav Heyrovský</strong> was the inventor of the polarographic method, father of the electroanalytical method, and recipient of the Nobel Prize in 1959. His main field of work was polarography. https://en.wikipedia.org/wiki/Jaroslav_Heyrovsk%C3%BD"),
	("hodgkin",		"<strong>Dorothy Hodgkin</strong> was a British biochemist, credited with the development of protein crystallography. She was awarded the Nobel Prize in Chemistry in 1964. https://en.wikipedia.org/wiki/Dorothy_Hodgkin"),
	("hoover",		"<strong>Erna Schneider Hoover</strong> revolutionized modern communication by inventing a computerized telephon switching method. https://en.wikipedia.org/wiki/Erna_Schneider_Hoover"),
	("hopper",		"<strong>Grace Hopper</strong> developed the first compiler for a computer programming language and  is credited with popularizing the term \"debugging\" for fixing computer glitches. https://en.wikipedia.org/wiki/Grace_Hopper"),
	("hugle",		"<strong>Frances Hugle</strong>, she was an American scientist, engineer, and inventor who contributed to the understanding of semiconductors, integrated circuitry, and the unique electrical principles of microscopic materials. https://en.wikipedia.org/wiki/Frances_Hugle"),
	("hypatia",		"<strong>Hypatia</strong>. Greek Alexandrine Neoplatonist philosopher in Egypt who was one of the earliest mothers of mathematics. https://en.wikipedia.org/wiki/Hypatia"),
	("jang",		"<strong>Yeong-Sil Jang</strong> was a Korean scientist and astronomer during the Joseon Dynasty; he invented the first metal printing press and water gauge. https://en.wikipedia.org/wiki/Jang_Yeong-sil"),
	("jennings",	"<strong>Betty Jennings</strong>. one of the original programmers of the ENIAC. https://en.wikipedia.org/wiki/ENIAC https://en.wikipedia.org/wiki/Jean_Bartik"),
	("jepsen",		"<strong>Mary Lou Jepsen</strong>, was the founder and chief technology officer of One Laptop Per Child (OLPC), and the founder of Pixel Qi. https://en.wikipedia.org/wiki/Mary_Lou_Jepsen"),
	("joliot",		"<strong>Irène Joliot-Curie</strong>. French scientist who was awarded the Nobel Prize for Chemistry in 1935. Daughter of Marie and Pierre Curie. https://en.wikipedia.org/wiki/Ir%C3%A8ne_Joliot-Curie"),
	("jones",		"<strong>Karen Spärck Jones</strong> came up with the concept of inverse document frequency, which is used in most search engines today. https://en.wikipedia.org/wiki/Karen_Sp%C3%A4rck_Jones"),
	("kalam",		"<strong>A. P. J. Abdul Kalam.</strong> is an Indian scientist aka Missile Man of India for his work on the development of ballistic missile and launch vehicle technology. https://en.wikipedia.org/wiki/A._P._J._Abdul_Kalam"),
	("kare",		"<strong>Susan Kare</strong>, created the icons and many of the interface elements for the original Apple Macintosh in the 1980s, and was an original employee of NeXT, working as the Creative Director. https://en.wikipedia.org/wiki/Susan_Kare"),
	("keller",		"<strong>Mary Kenneth Keller</strong>, Sister Mary Kenneth Keller became the first American woman to earn a PhD in Computer Science in 1965. https://en.wikipedia.org/wiki/Mary_Kenneth_Keller"),
	("khorana",		"<strong>Har Gobind Khorana</strong>. Indian-American biochemist who shared the 1968 Nobel Prize for Physiology. https://en.wikipedia.org/wiki/Har_Gobind_Khorana"),
	("kilby",		"<strong>Jack Kilby</strong> invented silicone integrated circuits and gave Silicon Valley its name. https://en.wikipedia.org/wiki/Jack_Kilby"),
	("kirch",		"<strong>Maria Kirch</strong>. German astronomer and first woman to discover a comet. https://en.wikipedia.org/wiki/Maria_Margarethe_Kirch"),
	("knuth",		"<strong>Donald Knuth</strong>. American computer scientist, author of \"The Art of Computer Programming\" and creator of the TeX typesetting system. https://en.wikipedia.org/wiki/Donald_Knuth"),
	("kowalevski",	"<strong>Sophie Kowalevski</strong>. Russian mathematician responsible for important original contributions to analysis, differential equations and mechanics. https://en.wikipedia.org/wiki/Sofia_Kovalevskaya"),
	("lalande",		"<strong>Marie-Jeanne de Lalande</strong>. French astronomer, mathematician and cataloguer of stars. https://en.wikipedia.org/wiki/Marie-Jeanne_de_Lalande"),
	("lamarr",		"<strong>Hedy Lamarr</strong>. Actress and inventor. The principles of her work are now incorporated into modern Wi-Fi, CDMA and Bluetooth technology. https://en.wikipedia.org/wiki/Hedy_Lamarr"),
	("leakey",		"<strong>Mary Leakey</strong>. British paleoanthropologist who discovered the first fossilized Proconsul skull. https://en.wikipedia.org/wiki/Mary_Leakey"),
	("leavitt",		"<strong>Henrietta Swan Leavitt</strong>. she was an American astronomer who discovered the relation between the luminosity and the period of Cepheid variable stars. https://en.wikipedia.org/wiki/Henrietta_Swan_Leavitt"),
	("lichterman",	"<strong>Ruth Lichterman</strong>. one of the original programmers of the ENIAC. https://en.wikipedia.org/wiki/ENIAC. https://en.wikipedia.org/wiki/Ruth_Teitelbaum"),
	("liskov",		"<strong>Barbara Liskov</strong>. co-developed the Liskov substitution principle. Liskov was also the winner of the Turing Prize in 2008. https://en.wikipedia.org/wiki/Barbara_Liskov"),
	("lovelace",	"<strong>Ada Lovelace</strong> invented the first algorithm. https://en.wikipedia.org/wiki/Ada_Lovelace (thanks James Turnbull)"),
	("lumiere",		"<strong>Auguste and Louis Lumière</strong>. the first filmmakers in history. https://en.wikipedia.org/wiki/Auguste_and_Louis_Lumi%C3%A8re"),
	("mahavira",	"<strong>Mahavira</strong>. Ancient Indian mathematician during 9th century AD who discovered basic algebraic identities. https://en.wikipedia.org/wiki/Mah%C4%81v%C4%ABra_(mathematician)"),
	("mayer",		"<strong>Maria Mayer</strong>. American theoretical physicist and Nobel laureate in Physics for proposing the nuclear shell model of the atomic nucleus. https://en.wikipedia.org/wiki/Maria_Mayer"),
	("mccarthy",	"<strong>John McCarthy</strong> invented LISP: https://en.wikipedia.org/wiki/John_McCarthy_(computer_scientist)"),
	("mcclintock",	"<strong>Barbara McClintock</strong>. a distinguished American cytogeneticist, 1983 Nobel Laureate in Physiology or Medicine for discovering transposons. https://en.wikipedia.org/wiki/Barbara_McClintock"),
	("mclean", 		"<strong>Malcolm McLean</strong> invented the modern shipping container: https://en.wikipedia.org/wiki/Malcom_McLean"),
	("mcnulty",		"<strong>Kay McNulty</strong>. one of the original programmers of the ENIAC. https://en.wikipedia.org/wiki/ENIAC. https://en.wikipedia.org/wiki/Kathleen_Antonelli"),
	("meitner",		"<strong>Lise Meitner</strong>. Austrian/Swedish physicist who was involved in the discovery of nuclear fission. The element meitnerium is named after her. https://en.wikipedia.org/wiki/Lise_Meitner"),
	("meninsky",	"<strong>Carla Meninsky</strong>, was the game designer and programmer for Atari 2600 games Dodge 'Em and Warlords. https://en.wikipedia.org/wiki/Carla_Meninsky"),
	("mestorf",		"<strong>Johanna Mestorf</strong>. German prehistoric archaeologist and first female museum director in Germany. https://en.wikipedia.org/wiki/Johanna_Mestorf"),
	("mirzakhani",	"<strong>Maryam Mirzakhani</strong>. an Iranian mathematician and the first woman to win the Fields Medal. https://en.wikipedia.org/wiki/Maryam_Mirzakhani"),
	("morse",		"<strong>Samuel Morse</strong>. contributed to the invention of a single-wire telegraph system based on European telegraphs and was a co-developer of the Morse code. https://en.wikipedia.org/wiki/Samuel_Morse"),
	("newton",		"<strong>Isaac Newton</strong> invented classic mechanics and modern optics. https://en.wikipedia.org/wiki/Isaac_Newton"),
	("nobel",		"<strong>Alfred Nobel</strong>. a Swedish chemist, engineer, innovator, and armaments manufacturer (inventor of dynamite). https://en.wikipedia.org/wiki/Alfred_Nobel"),
	("noether",		"<strong>Emmy Noether</strong>, German mathematician. Noether's Theorem is named after her. https://en.wikipedia.org/wiki/Emmy_Noether"),
	("northcutt",	"<strong>Poppy Northcutt</strong>. Poppy Northcutt was the first woman to work as part of NASA’s Mission Control. http://www.businessinsider.com/poppy-northcutt-helped-apollo-astronauts-2014-12?op=1"),
	("noyce",		"<strong>Robert Noyce</strong> invented silicone integrated circuits and gave Silicon Valley its name. https://en.wikipedia.org/wiki/Robert_Noyce"),
	("panini",		"<strong>Panini</strong>. Ancient Indian linguist and grammarian from 4th century CE who worked on the world's first formal system. https://en.wikipedia.org/wiki/P%C4%81%E1%B9%87ini#Comparison_with_modern_formal_systems"),
	("pare",		"<strong>Ambroise Pare</strong> invented modern surgery. https://en.wikipedia.org/wiki/Ambroise_Par%C3%A9"),
	("pasteur",		"<strong>Louis Pasteur</strong> discovered vaccination, fermentation and pasteurization. https://en.wikipedia.org/wiki/Louis_Pasteur."),
	("payne",		"<strong>Cecilia Payne-Gaposchkin</strong> was an astronomer and astrophysicist who, in 1925, proposed in her Ph.D. thesis an explanation for the composition of stars in terms of the relative abundances of hydrogen and helium. https://en.wikipedia.org/wiki/Cecilia_Payne-Gaposchkin"),
	("perlman",		"<strong>Radia Perlman</strong> is a software designer and network engineer and most famous for her invention of the spanning-tree protocol (STP). https://en.wikipedia.org/wiki/Radia_Perlman"),
	("pike",		"<strong>Rob Pike </strong>was a key contributor to Unix, Plan 9, the X graphic system, utf-8, and the Go programming language. https://en.wikipedia.org/wiki/Rob_Pike"),
	("poincare",	"<strong>Henri Poincaré</strong> made fundamental contributions in several fields of mathematics. https://en.wikipedia.org/wiki/Henri_Poincar%C3%A9"),
	("poitras",		"<strong>Laura Poitras</strong> is a director and producer whose work, made possible by open source crypto tools, advances the causes of truth and freedom of information by reporting disclosures by whistleblowers such as Edward Snowden. https://en.wikipedia.org/wiki/Laura_Poitras"),
	("ptolemy",		"<strong>Claudius Ptolemy</strong>. a Greco-Egyptian writer of Alexandria, known as a mathematician, astronomer, geographer, astrologer, and poet of a single epigram in the Greek Anthology. https://en.wikipedia.org/wiki/Ptolemy"),
	("raman",		"<strong>C. V. Raman</strong>. Indian physicist who won the Nobel Prize in 1930 for proposing the Raman effect. https://en.wikipedia.org/wiki/C._V._Raman"),
	("ramanujan",	"<strong>Srinivasa Ramanujan.</strong> Indian mathematician and autodidact who made extraordinary contributions to mathematical analysis, number theory, infinite series, and continued fractions. https://en.wikipedia.org/wiki/Srinivasa_Ramanujan"),
	("ride",		"<strong>Sally Kristen Ride</strong> was an American physicist and astronaut. She was the first American woman in space, and the youngest American astronaut. https://en.wikipedia.org/wiki/Sally_Ride"),
	("ritchie",		"<strong>Dennis Ritchie</strong>. co-creator of UNIX and the C programming language. https://en.wikipedia.org/wiki/Dennis_Ritchie"),
	("roentgen",	"<strong>Wilhelm Conrad Röntgen</strong>. German physicist who was awarded the first Nobel Prize in Physics in 1901 for the discovery of X-rays (Röntgen rays). https://en.wikipedia.org/wiki/Wilhelm_R%C3%B6ntgen"),
	("rosalind",	"<strong>Rosalind Franklin</strong>. British biophysicist and X-ray crystallographer whose research was critical to the understanding of DNA. https://en.wikipedia.org/wiki/Rosalind_Franklin"),
	("saha",		"<strong>Meghnad Saha</strong>. Indian astrophysicist best known for his development of the Saha equation, used to describe chemical and physical conditions in stars. https://en.wikipedia.org/wiki/Meghnad_Saha"),
	("sammet",		"<strong>Jean E. Sammet</strong> developed FORMAC, the first widely used computer language for symbolic manipulation of mathematical formulas. https://en.wikipedia.org/wiki/Jean_E._Sammet"),
	("shaw",		"<strong>Carol Shaw</strong>. Originally an Atari employee, Carol Shaw is said to be the first female video game designer. https://en.wikipedia.org/wiki/Carol_Shaw_(video_game_designer)"),
	("shockley", 	"<strong>William Shockley</strong> co-invented the transistor. https://en.wikipedia.org/wiki/William_Shockley"),
	("sinoussi",	"<strong>Françoise Barré-Sinoussi</strong>. French virologist and Nobel Prize Laureate in Physiology or Medicine; her work was fundamental in identifying HIV as the cause of AIDS. https://en.wikipedia.org/wiki/Fran%C3%A7oise_Barr%C3%A9-Sinoussi"),
	("snyder",		"<strong>Betty Snyder</strong>. one of the original programmers of the ENIAC. https://en.wikipedia.org/wiki/ENIAC. https://en.wikipedia.org/wiki/Betty_Holberton"),
	("spence",		"<strong>Frances Spence</strong>. one of the original programmers of the ENIAC. https://en.wikipedia.org/wiki/ENIAC. https://en.wikipedia.org/wiki/Frances_Spence"),
	("stallman",	"<strong>Richard Matthew Stallman</strong>. the founder of the Free Software movement, the GNU project, the Free Software Foundation, and the League for Programming Freedom. He also invented the concept of copyleft to protect the ideals of this movement, and enshrined this concept in the widely-used GPL (General Public License) for software. https://en.wikiquote.org/wiki/Richard_Stallman"),
	("swanson",		"<strong>Janese Swanson</strong> (with others) developed the first of the Carmen Sandiego games. She went on to found Girl Tech. https://en.wikipedia.org/wiki/Janese_Swanson"),
	("swartz",		"<strong>Aaron Swartz</strong> was influential in creating RSS, Markdown, Creative Commons, Reddit, and much of the internet as we know it today. He was devoted to freedom of information on the web. https://en.wikiquote.org/wiki/Aaron_Swartz"),
	("swirles",		"<strong>Bertha Swirles</strong> was a theoretical physicist who made a number of contributions to early quantum theory. https://en.wikipedia.org/wiki/Bertha_Swirles"),
	("tesla",		"<strong>Nikola Tesla</strong> invented the AC electric system and every gadget ever used by a James Bond villain. https://en.wikipedia.org/wiki/Nikola_Tesla"),
	("thompson",	"<strong>Ken Thompson</strong>. co-creator of UNIX and the C programming language. https://en.wikipedia.org/wiki/Ken_Thompson"),
	("torvalds",	"<strong>Linus Torvalds</strong> invented Linux and Git. https://en.wikipedia.org/wiki/Linus_Torvalds"),
	("turing",		"<strong>Alan Turing</strong> was a founding father of computer science. https://en.wikipedia.org/wiki/Alan_Turing."),
	("varahamihira","<strong>Varahamihira</strong>. Ancient Indian mathematician who discovered trigonometric formulae during 505-587 CE. https://en.wikipedia.org/wiki/Var%C4%81hamihira#Contributions"),
	("visvesvaraya","<strong>Sir Mokshagundam Visvesvaraya</strong>. is a notable Indian engineer.  He is a recipient of the Indian Republic's highest honour, the Bharat Ratna, in 1955. On his birthday, 15 September is celebrated as Engineer's Day in India in his memory. https://en.wikipedia.org/wiki/Visvesvaraya"),
	("wescoff",		"<strong>Marlyn Wescoff</strong>. one of the original programmers of the ENIAC. https://en.wikipedia.org/wiki/ENIAC. https://en.wikipedia.org/wiki/Marlyn_Meltzer"),
	("williams",	"<strong>Roberta Williams</strong>, did pioneering work in graphical adventure games for personal computers, particularly the King's Quest series. https://en.wikipedia.org/wiki/Roberta_Williams"),
	("wilson",		"<strong>Sophie Wilson</strong> designed the first Acorn Micro-Computer and the instruction set for ARM processors. https://en.wikipedia.org/wiki/Sophie_Wilson"),
	("wing",		"<strong>Jeannette Wing</strong>. co-developed the Liskov substitution principle. https://en.wikipedia.org/wiki/Jeannette_Wing"),
	("wozniak",		"<strong>Steve Wozniak</strong> invented the Apple I and Apple II. https://en.wikipedia.org/wiki/Steve_Wozniak"),
	("wright",		"<strong>The Wright brothers</strong>, Orville and Wilbur. credited with inventing and building the world's first successful airplane and making the first controlled, powered and sustained heavier-than-air human flight. https://en.wikipedia.org/wiki/Wright_brothers"),
	("yalow", 		"<strong>Rosalyn Sussman Yalow</strong>. Rosalyn Sussman Yalow was an American medical physicist, and a co-winner of the 1977 Nobel Prize in Physiology or Medicine for development of the radioimmunoassay technique. https://en.wikipedia.org/wiki/Rosalyn_Sussman_Yalow"),
	("yonath", 		"<strong>Ada Yonath</strong>. an Israeli crystallographer, the first woman from the Middle East to win a Nobel prize in the sciences. https://en.wikipedia.org/wiki/Ada_Yonath")
]


@app.route("/")
def index():

	adj = "boring"
	name = "wozniak"
	while adj == "boring" and name == "wozniak":
		adj = random.choice(adjectives)
		name, description = random.choice(surnames)

	links = re.findall("https?:\/\/[a-zA-Z.%0-9\-_\/#()\?=]+", description)
	for l in links:
		description=description.replace(l, "")

	upper_adj = adj
	upper_adj = upper_adj[0].upper() + upper_adj[1:]
	description = "<i>" + upper_adj + "</i> " + description

	return render_template('index.html', name=(adj + "_" + name), description=description.decode('utf-8'), links=links)

if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0")
