from django.shortcuts import render
from api.models import userdetails,Product,wallet,order,hotel,storerestro,Doctor,Complain,Tax,cat,airport,airline,routes,days,book,productComplain,message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from django.http import JsonResponse
import random
from cab.models import cabOrder,cabdetails
# from .serializers import eventSerializer,UserSerializer,participateSerializer,EventSerializer,userDetailsSerializer
from rest_framework.generics import ListAPIView
from cab.serializers import carClassSerializer,cabdetailsSerializer,cabOrderSerializer,kafkaSerializer
import os
from .serializers import ProductSerializer,orderSerializer,userdetailsSerializer,UserSerializer,complainSerializer,transactionSerializer,catSerializer,hotelSerializer,hotelSerializer,airlineSerializer,routesSerializer,daysSerializer,airportSerializer,transactionSerializer,bookSerializer,messageSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
import datetime
import time
import s2geometry as s2
import requests
import joblib
import numpy as np
from datetime import date
# from cab.views import mainnlp
import re
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
# from cab.tasks import dispatchDelivery
from datetime import timedelta
# Create your views here.
def getcorpus():
    corpus = ['wow love place', 'crust good', 'tasti textur nasti', 'stop late may bank holiday rick steve recommend love', 'select menu great price', 'get angri want damn pho', 'honeslti tast fresh', 'potato like rubber could tell made ahead time kept warmer', 'fri great', 'great touch', 'servic prompt', 'would go back', 'cashier care ever say still end wayyy overpr', 'tri cape cod ravoli chicken cranberri mmmm', 'disgust pretti sure human hair', 'shock sign indic cash', 'highli recommend', 'waitress littl slow servic', 'place worth time let alon vega', 'like', 'burritto blah', 'food amaz', 'servic also cute', 'could care less interior beauti', 'perform', 'right red velvet cake ohhh stuff good', 'never brought salad ask', 'hole wall great mexican street taco friendli staff', 'took hour get food tabl restaur food luke warm sever run around like total overwhelm', 'worst salmon sashimi', 'also combo like burger fri beer decent deal', 'like final blow', 'found place accid could happier', 'seem like good quick place grab bite familiar pub food favor look elsewher', 'overal like place lot', 'redeem qualiti restaur inexpens', 'ampl portion good price', 'poor servic waiter made feel like stupid everi time came tabl', 'first visit hiro delight', 'servic suck', 'shrimp tender moist', 'deal good enough would drag establish', 'hard judg whether side good gross melt styrofoam want eat fear get sick', 'posit note server attent provid great servic', 'frozen puck disgust worst peopl behind regist', 'thing like prime rib dessert section', 'bad food damn gener', 'burger good beef cook right', 'want sandwich go firehous', 'side greek salad greek dress tasti pita hummu refresh', 'order duck rare pink tender insid nice char outsid', 'came run us realiz husband left sunglass tabl', 'chow mein good', 'horribl attitud toward custom talk one custom enjoy food', 'portion huge', 'love friendli server great food wonder imagin menu', 'heart attack grill downtown vega absolut flat line excus restaur', 'much seafood like string pasta bottom', 'salad right amount sauc power scallop perfectli cook', 'rip banana rip petrifi tasteless', 'least think refil water struggl wave minut', 'place receiv star appet', 'cocktail handmad delici', 'definit go back', 'glad found place', 'great food servic huge portion give militari discount', 'alway great time do gringo', 'updat went back second time still amaz', 'got food appar never heard salt batter fish chewi', 'great way finish great', 'deal includ tast drink jeff went beyond expect', 'realli realli good rice time', 'servic meh', 'took min get milkshak noth chocol milk', 'guess known place would suck insid excalibur use common sens', 'scallop dish quit appal valu well', 'time bad custom servic', 'sweet potato fri good season well', 'today second time lunch buffet pretti good', 'much good food vega feel cheat wast eat opportun go rice compani', 'come like experienc underwhelm relationship parti wait person ask break', 'walk place smell like old greas trap other eat', 'turkey roast beef bland', 'place', 'pan cake everyon rave tast like sugari disast tailor palat six year old', 'love pho spring roll oh yummi tri', 'poor batter meat ratio made chicken tender unsatisfi', 'say food amaz', 'omelet die', 'everyth fresh delici', 'summari larg disappoint dine experi', 'like realli sexi parti mouth outrag flirt hottest person parti', 'never hard rock casino never ever step forward', 'best breakfast buffet', 'say bye bye tip ladi', 'never go', 'back', 'food arriv quickli', 'good', 'side cafe serv realli good food', 'server fantast found wife love roast garlic bone marrow ad extra meal anoth marrow go', 'good thing waiter help kept bloddi mari come', 'best buffet town price cannot beat', 'love mussel cook wine reduct duck tender potato dish delici', 'one better buffet', 'went tigerlilli fantast afternoon', 'food delici bartend attent person got great deal', 'ambienc wonder music play', 'go back next trip', 'sooooo good', 'real sushi lover let honest yama good', 'least min pass us order food arriv busi', 'realli fantast thai restaur definit worth visit', 'nice spici tender', 'good price', 'check', 'pretti gross', 'better atmospher', 'kind hard mess steak', 'although much like look sound place actual experi bit disappoint', 'know place manag serv blandest food ever eaten prepar indian cuisin', 'worst servic boot least worri', 'servic fine waitress friendli', 'guy steak steak love son steak best worst place said best steak ever eaten', 'thought ventur away get good sushi place realli hit spot night', 'host staff lack better word bitch', 'bland like place number reason want wast time bad review leav', 'phenomen food servic ambianc', 'return', 'definit worth ventur strip pork belli return next time vega', 'place way overpr mediocr food', 'penn vodka excel', 'good select food includ massiv meatloaf sandwich crispi chicken wrap delish tuna melt tasti burger', 'manag rude', 'delici nyc bagel good select cream chees real lox caper even', 'great subway fact good come everi subway meet expect', 'serious solid breakfast', 'one best bar food vega', 'extrem rude realli mani restaur would love dine weekend vega', 'drink never empti made realli great menu suggest', '', 'waiter help friendli rare check us', 'husband ate lunch disappoint food servic', 'red curri much bamboo shoot tasti', 'nice blanket moz top feel like done cover subpar food', 'bathroom clean place well decor', 'menu alway chang food qualiti go servic extrem slow', 'servic littl slow consid serv peopl server food come slow pace', 'give thumb', 'watch waiter pay lot attent tabl ignor us', 'fianc came middl day greet seat right away', 'great restaur mandalay bay', 'wait forti five minut vain', 'crostini came salad stale', 'highlight great qualiti nigiri', 'staff friendli joint alway clean', 'differ cut piec day still wonder tender well well flavor', 'order voodoo pasta first time realli excel pasta sinc go gluten free sever year ago', 'place good', 'unfortun must hit bakeri leftov day everyth order stale', 'came back today sinc reloc still impress', 'seat immedi', 'menu divers reason price', 'avoid cost', 'restaur alway full never wait', 'delici', 'place hand one best place eat phoenix metro area', 'go look good food', 'never treat bad', 'bacon hella salti', 'also order spinach avocado salad ingredi sad dress liter zero tast', 'realli vega fine dine use right menu hand ladi price list', 'waitress friendli', 'lordi khao soi dish miss curri lover', 'everyth menu terrif also thrill made amaz accommod vegetarian daughter', 'perhap caught night judg review inspir go back', 'servic leav lot desir', 'atmospher modern hip maintain touch cozi', 'weekli haunt definit place come back everi', 'liter sat minut one ask take order', 'burger absolut flavor meat total bland burger overcook charcoal flavor', 'also decid send back waitress look like verg heart attack', 'dress treat rude', 'probabl dirt', 'love place hit spot want someth healthi lack quantiti flavor', 'order lemon raspberri ice cocktail also incred', 'food suck expect suck could imagin', 'interest decor', 'realli like crepe station', 'also serv hot bread butter home made potato chip bacon bit top origin good', 'watch prepar delici food', 'egg roll fantast', 'order arriv one gyro miss', 'salad wing ice cream dessert left feel quit satisfi', 'realli sure joey vote best hot dog valley reader phoenix magazin', 'best place go tasti bowl pho', 'live music friday total blow', 'never insult felt disrespect', 'friendli staff', 'worth drive', 'heard good thing place exceed everi hope could dream', 'food great serivc', 'warm beer help', 'great brunch spot', 'servic friendli invit', 'good lunch spot', 'live sinc first last time step foot place', 'worst experi ever', 'must night place', 'side delish mix mushroom yukon gold pure white corn beateou', 'bug never show would given sure side wall bug climb kitchen', 'minut wait salad realiz come time soon', 'friend love salmon tartar', 'go back', 'extrem tasti', 'waitress good though', 'soggi good', 'jamaican mojito delici', 'small worth price', 'food rich order accordingli', 'shower area outsid rins take full shower unless mind nude everyon see', 'servic bit lack', 'lobster bisqu bussel sprout risotto filet need salt pepper cours none tabl', 'hope bode go busi someon cook come', 'either cold enough flavor bad', 'love bacon wrap date', 'unbeliev bargain', 'folk otto alway make us feel welcom special', 'main also uninspir', 'place first pho amaz', 'wonder experi made place must stop whenev town', 'food bad enough enjoy deal world worst annoy drunk peopl', 'fun chef', 'order doubl cheeseburg got singl patti fall apart pictur upload yeah still suck', 'great place coupl drink watch sport event wall cover tv', 'possibl give zero star', 'descript said yum yum sauc anoth said eel sauc yet anoth said spici mayo well none roll sauc', 'say would hardest decis honestli dish tast suppos tast amaz', 'roll eye may stay sure go back tri', 'everyon attent provid excel custom servic', 'horribl wast time money', 'dish quit flavour', 'time side restaur almost empti excus', 'busi either also build freez cold', 'like review said pay eat place', 'drink took close minut come one point', 'serious flavor delight folk', 'much better ayc sushi place went vega', 'light dark enough set mood', 'base sub par servic receiv effort show gratitud busi go back', 'owner realli great peopl', 'noth privileg work eat', 'greek dress creami flavor', 'overal think would take parent place made similar complaint silent felt', 'pizza good peanut sauc tasti', 'tabl servic pretti fast', 'fantast servic', 'well would given godfath zero star possibl', 'know make', 'tough short flavor', 'hope place stick around', 'bar vega ever recal charg tap water', 'restaur atmospher exquisit', 'good servic clean inexpens boot', 'seafood fresh gener portion', 'plu buck', 'servic par either', 
    'thu far visit twice food absolut delici time', 'good year ago', 'self proclaim coffe cafe wildli disappoint', 'veggitarian platter world',
     'cant go wrong food', 'beat', 'stop place madison ironman friendli kind staff',
      'chef friendli good job', 'better dedic boba tea spot even jenni pho', 
      'like patio servic outstand', 'goat taco skimp meat wow flavor', 'think', 
      'mac salad pretti bland get', 'went bachi burger friend recommend disappoint', 
      'servic stink', 'wait wait', 'place qualiti sushi qualiti restaur',
       'would definit recommend wing well pizza', 'great pizza salad', 'thing went wrong burn saganaki',
        'wait hour breakfast could done time better home', 'place amaz',
         'hate disagre fellow yelper husband disappoint place',
          'wait hour never got either pizza mani around us came later', 'know slow',
           'staff great food delish incred beer select', 'live neighborhood disappoint back conveni locat', 'know pull pork could soooo delici', 'get incred fresh fish prepar care', 'go gave star rate pleas know third time eat bachi burger write review', 'love fact everyth menu worth', 'never dine place', 'food excel servic good', 'good beer drink select good food select', 'pleas stay away shrimp stir fri noodl', 'potato chip order sad could probabl count mani chip box probabl around', 'food realli bore', 'good servic check', 'greedi corpor never see anoth dime', 'never ever go back', 'much like go back get pass atroci servic never return', 'summer dine charm outdoor patio delight', 'expect good', 'fantast food', 'order toast english muffin came untoast', 'food good', 'never go back', 'great food price high qualiti hous made', 'bu boy hand rude', 'point friend basic figur place joke mind make publicli loudli known', 'back good bbq lighter fare reason price tell public back old way', 'consid two us left full happi go wrong', 'bread made hous', 'downsid servic', 'also fri without doubt worst fri ever', 'servic except food good review', 'coupl month later return amaz meal', 'favorit place town shawarrrrrrma', 'black eye pea sweet potato unreal', 'disappoint', 'could serv vinaigrett may make better overal dish still good', 'go far mani place never seen restaur serv egg breakfast especi', 'mom got home immedi got sick bite salad', 'server pleasant deal alway honor pizza hut coupon', 'truli unbeliev good glad went back', 'fantast servic pleas atmospher', 'everyth gross', 'love place', 'great servic food', 'first bathroom locat dirti seat cover replenish plain yucki', 'burger got gold standard burger kind disappoint', 'omg food delicioso', 'noth authent place', 'spaghetti noth special whatsoev', 'dish salmon best great', 'veget fresh sauc feel like authent thai', 'worth drive tucson', 'select probabl worst seen vega none', 'pretti good beer select', 'place like chipotl better', 'classi warm atmospher fun fresh appet succul steak basebal steak', 'star brick oven bread app', 'eaten multipl time time food delici', 'sat anoth ten minut final gave left', 'terribl', 'everyon treat equal special', 'take min pancak egg', 'delici', 'good side staff genuin pleasant enthusiast real treat', 'sadli gordon ramsey steak place shall sharpli avoid next trip vega', 'alway even wonder food delici', 'best fish ever life', 'bathroom next door nice', 'buffet small food offer bland', 'outstand littl restaur best food ever tast', 'pretti cool would say', 'definit turn doubt back unless someon els buy', 'server great job handl larg rowdi tabl', 'find wast food despic food', 'wife lobster bisqu soup lukewarm', 'would come back sushi crave vega', 'staff great ambianc great', 'deserv star', 'left stomach ach felt sick rest day', 'drop ball', 'dine space tini elegantli decor comfort', 'custom order way like usual eggplant green bean stir fri love', 'bean rice mediocr best', 'best taco town far', 'took back money got outta', 'interest part town place amaz', 'rude inconsider manag', 'staff friendli wait time serv horribl one even say hi first minut', 'back', 'great dinner', 'servic outshin definit recommend halibut', 'food terribl', 'never ever go back told mani peopl happen', 'recommend unless car break front starv', 'come back everi time vega', 'place deserv one star food', 'disgrac', 'def come back bowl next time', 'want healthi authent ethic food tri place', 'continu come ladi night andddd date night highli recommend place anyon area', 'sever time past experi alway great', 'walk away stuf happi first vega buffet experi', 'servic excel price pretti reason consid vega locat insid crystal shop mall aria', 'summar food incred nay transcend noth bring joy quit like memori pneumat condiment dispens', 'probabl one peopl ever go ian like', 'kid pizza alway hit lot great side dish option kiddo', 'servic perfect famili atmospher nice see', 'cook perfect servic impecc', 'one simpli disappoint', 'overal disappoint qualiti food bouchon', 'account know get screw', 'great place eat remind littl mom pop shop san francisco bay area', 'today first tast buldogi gourmet hot dog tell ever thought possibl', 'left frustrat', 'definit soon', 'food realli good got full petti fast', 'servic fantast', 'total wast time', 'know kind best ice tea', 'come hungri leav happi stuf', 'servic give star', 'assur disappoint', 'take littl bad servic food suck', 'gave tri eat crust teeth still sore', 'complet gross', 'realli enjoy eat', 'first time go think quickli becom regular', 'server nice even though look littl overwhelm need stay profession friendli end', 'dinner companion told everyth fresh nice textur tast', 'ground right next tabl larg smear step track everywher pile green bird poop', 'furthermor even find hour oper websit', 'tri like place time think done', 'mistak', 'complaint', 'serious good pizza expert connisseur topic', 'waiter jerk', 'strike want rush', 'nicest restaur owner ever come across', 'never come', 'love biscuit', 'servic quick friendli', 'order appet took minut pizza anoth minut', 'absolutley fantast', 'huge awkward lb piec cow th gristl fat', 'definit come back', 'like steiner dark feel like bar', 'wow spici delici', 'familiar check', 'take busi dinner dollar elsewher', 'love go back', 'anyway fs restaur wonder breakfast lunch', 'noth special', 'day week differ deal delici', 'mention combin pear almond bacon big winner', 'back', 'sauc tasteless', 'food delici spici enough sure ask spicier prefer way', 'ribey steak cook perfectli great mesquit flavor', 'think go back anytim soon', 'food gooodd', 'far sushi connoisseur definit tell differ good food bad food certainli bad food', 'insult', 'last time lunch bad', 'chicken wing contain driest chicken meat ever eaten', 'food good enjoy everi mouth enjoy relax venu coupl small famili group etc', 'nargil think great', 'best tater tot southwest', 'love place', 'definit worth paid', 'vanilla ice cream creami smooth profiterol choux pastri fresh enough', 'im az time new spot', 'manag worst', 'insid realli quit nice clean', 'food outstand price reason', 'think run back carli anytim soon food', 'due fact took minut acknowledg anoth minut get food kept forget thing', 'love margarita', 'first vega buffet disappoint', 'good though', 'one note ventil could use upgrad', 'great pork sandwich', 'wast time', 'total letdown would much rather go camelback flower shop cartel coffe', 'third chees friend burger cold', 'enjoy pizza brunch', 'steak well trim also perfectli cook', 'group claim would handl us beauti', 'love', 'ask bill leav without eat bring either', 'place jewel la vega exactli hope find nearli ten year live', 'seafood limit boil shrimp crab leg crab leg definit tast fresh', 'select food best', 'delici absolut back', 'small famili restaur fine dine establish', 'toro tartar cavier extraordinari like thinli slice wagyu white truffl', 'dont think back long time', 'attach ga station rare good sign', 'awesom', 'back mani time soon', 'menu much good stuff could decid', 'wors humili worker right front bunch horribl name call', 'conclus fill meal', 'daili special alway hit group', 'tragedi struck', 'pancak also realli good pretti larg', 'first crawfish experi delici', 'monster chicken fri steak egg time favorit', 'waitress sweet funni', 'also tast mom multi grain pumpkin pancak pecan butter amaz fluffi delici', 'rather eat airlin food serious', 'cant say enough good thing place', 'ambianc incred', 'waitress manag friendli', 'would recommend place', 'overal impress noca', 'gyro basic lettuc', 'terribl servic', 'thoroughli disappoint', 'much pasta love homemad hand made pasta thin pizza', 'give tri happi', 'far best cheesecurd ever', 'reason price also', 'everyth perfect night', 'food good typic bar food', 'drive get', 'first glanc love bakeri cafe nice ambianc clean friendli staff', 'anyway think go back', 'point finger item menu order disappoint', 'oh thing beauti restaur', 'gone go', 'greasi unhealthi meal', 'first time might last', 'burger amaz', 'similarli deliveri man say word apolog food minut late', 'way expens', 'sure order dessert even need pack go tiramisu cannoli die', 'first time wait next', 'bartend also nice', 'everyth good tasti', 'place two thumb way', 'best place vega breakfast check sat sun', 'love authent mexican food want whole bunch interest yet delici meat choos need tri place', 'terribl manag', 'excel new restaur experienc frenchman', 'zero star would give zero star', 'great steak great side great wine amaz dessert', 'worst martini ever', 'steak shrimp opinion best entre gc', 'opportun today sampl amaz pizza', 'wait thirti minut seat although vacant tabl folk wait', 'yellowtail carpaccio melt mouth fresh', 'tri go back even empti', 'go eat potato found stranger hair', 'spici enough perfect actual', 'last night second time dine happi decid go back', 'even hello right', 'dessert bit strang', 'boyfriend came first time recent trip vega could pleas qualiti food servic', 'realli recommend place go wrong donut place', 'nice ambianc', 'would recommend save room', 'guess mayb went night disgrac', 'howev recent experi particular locat good', 'know like restaur someth', 'avoid establish', 'think restaur suffer tri hard enough', 'tapa dish delici', 'heart place', 'salad bland vinegrett babi green heart palm', 'two felt disgust', 'good time', 'believ place great stop huge belli hanker sushi', 'gener portion great tast', 'never go back place never ever recommend place anyon', 'server went back forth sever time even much help', 'food delici', 'hour serious', 'consid theft', 'eew locat need complet overhaul', 'recent wit poor qualiti manag toward guest well', 'wait wait wait', 'also came back check us regularli excel servic', 'server super nice check us mani time', 'pizza tast old super chewi good way', 'swung give tri deepli disappoint', 'servic good compani better', 'staff also friendli effici', 
           'servic fan quick serv nice folk', 'boy sucker dri', 'rate', 'look authent thai food go els', 'steak recommend', 'pull car wait anoth minut acknowledg', 'great food great servic clean friendli set', 'assur back', 'hate thing much cheap qualiti black oliv', 'breakfast perpar great beauti present giant slice toast lightli dust powder sugar', 'kid play area nasti', 'great place fo take eat', 'waitress friendli happi accomod vegan veggi option', 'omg felt like never eaten thai food dish', 'extrem crumbi pretti tasteless', 'pale color instead nice char flavor', 'crouton also tast homemad extra plu', 'got home see driest damn wing ever', 'regular stop trip phoenix', 'realli enjoy crema caf expand even told friend best breakfast', 'good money', 'miss wish one philadelphia', 'got sit fairli fast end wait minut place order anoth minut food arriv', 'also best chees crisp town', 'good valu great food great servic', 'ask satisfi meal', 'food good', 'awesom', 'want leav', 'made drive way north scottsdal one bit disappoint', 'eat', 'owner realli realli need quit soooooo cheap let wrap freak sandwich two paper one', 'check place coupl year ago impress', 'chicken got definit reheat ok wedg cold soggi', 'sorri get food anytim soon', 'absolut must visit', 'cow tongu cheek taco amaz', 'friend like bloodi mari', 'despit hard rate busi actual rare give star', 'realli want make experi good one', 'return', 'chicken pho tast bland', 'disappoint', 'grill chicken tender yellow saffron season', 'drive thru mean want wait around half hour food somehow end go make us wait wait', 'pretti awesom place', 'ambienc perfect', 'best luck rude non custom servic focus new manag', 'grandmoth make roast chicken better one', 'ask multipl time wine list time ignor went hostess got one', 'staff alway super friendli help especi cool bring two small boy babi', 'four star food guy blue shirt great vibe still let us eat', 'roast beef sandwich tast realli good', 'even drastic sick', 'high qualiti chicken chicken caesar salad', 'order burger rare came done', 'promptli greet seat', 'tri go lunch madhous', 'proven dead wrong sushi bar qualiti great servic fast food impecc', 'wait hour seat greatest mood', 'good joint', 'macaron insan good', 'eat', 'waiter attent friendli inform', 'mayb cold would somewhat edibl', 'place lot promis fail deliv', 'bad experi', 'mistak', 'food averag best', 'great food', 'go back anytim soon', 'disappoint order big bay plater', 'great place relax awesom burger beer', 'perfect sit famili meal get togeth friend', 'much flavor poorli construct', 'patio seat comfort', 'fri rice dri well', 'hand favorit italian restaur', 'scream legit book somethat also pretti rare vega', 'fun experi', 'atmospher great love duo violinist play song request', 'person love hummu pita baklava falafel baba ganoush amaz eggplant', 'conveni sinc stay mgm', 'owner super friendli staff courteou', 'great', 'eclect select', 'sweet potato tot good onion ring perfect close', 'staff attent', 'chef gener time even came around twice take pictur', 'owner use work nobu place realli similar half price', 'googl mediocr imagin smashburg pop', 'dont go', 'promis disappoint', 'sushi lover avoid place mean', 'great doubl cheeseburg', 'awesom servic food', 'fantast neighborhood gem', 'wait go back', 'plantain worst ever tast', 'great place highli recommend', 'servic slow attent', 'gave star give star', 'staff spend time talk', 'dessert panna cotta amaz', 'good food great atmospher', 'damn good steak', 'total brunch fail', 'price reason flavor spot sauc home made slaw drench mayo', 'decor nice piano music soundtrack pleasant', 'steak amaz rge fillet relleno best seafood plate ever', 'good food good servic', 'absolut amaz', 'probabl back honest', 'definit back', 'sergeant pepper beef sandwich auju sauc excel sandwich well', 'hawaiian breez mango magic pineappl delight smoothi tri far good', 'went lunch servic slow', 'much say place walk expect amaz quickli disappoint', 'mortifi', 'needless say never back', 'anyway food definit fill price pay expect', 'chip came drip greas mostli edibl', 'realli impress strip steak', 'go sinc everi meal awesom', 'server nice attent serv staff', 'cashier friendli even brought food', 'work hospit industri paradis valley refrain recommend cibo longer', 'atmospher fun', 'would recommend other', 'servic quick even go order like like', 'mean realli get famou fish chip terribl', 'said mouth belli still quit pleas', 'thing', 'thumb', 'read pleas go', 'love grill pizza remind legit italian pizza', 'pro larg seat area nice bar area great simpl drink menu best brick oven pizza homemad dough', 'realli nice atmospher', 'tonight elk filet special suck', 'one bite hook', 'order old classic new dish go time sore disappoint everyth', 'cute quaint simpl honest', 'chicken delici season perfect fri outsid moist chicken insid', 'food great alway compliment chef', 'special thank dylan recommend order yummi tummi', 'awesom select beer', 'great food awesom servic', 'one nice thing ad gratuiti bill sinc parti larger expect tip', 'fli appl juic fli', 'han nan chicken also tasti', 'servic thought good', 'food bare lukewarm must sit wait server bring us', 'ryan bar definit one edinburgh establish revisit', 'nicest chines restaur', 'overal like food servic', 'also serv indian naan bread hummu spici pine nut sauc world', 'probabl never come back recommend', 'friend pasta also bad bare touch', 'tri airport experi tasti food speedi friendli servic', 'love decor chines calligraphi wall paper', 'never anyth complain', 'restaur clean famili restaur feel', 'way fri', 'sure long stood long enough begin feel awkwardli place', 'open sandwich impress good way', 'back', 'warm feel servic felt like guest special treat', 'extens menu provid lot option breakfast', 'alway order vegetarian menu dinner wide array option choos', 'watch price inflat portion get smaller manag attitud grow rapidli', 'wonder lil tapa ambienc made feel warm fuzzi insid', 'got enjoy seafood salad fabul vinegrett', 'wonton thin thick chewi almost melt mouth', 'level spici perfect spice whelm soup', 'sat right time server get go fantast', 'main thing enjoy crowd older crowd around mid', 'side town definit spot hit', 'wait minut get drink longer get arepa', 'great place eat', 'jalapeno bacon soooo good', 'servic poor that nice', 'food good servic good price good', 'place clean food oh stale', 'chicken dish ok beef like shoe leather', 'servic beyond bad', 'happi', 'tast like dirt', 'one place phoenix would defin go back', 'block amaz', 'close hous low key non fanci afford price good food', 'hot sour egg flower soup absolut star', 'sashimi poor qualiti soggi tasteless', 'great time famili dinner sunday night', 'food tasti say real tradit hunan style', 'bother slow servic', 'flair bartend absolut amaz', 'frozen margarita way sugari tast', 'good order twice', 'nutshel restaraunt smell like combin dirti fish market sewer', 'girlfriend veal bad', 'unfortun good', 'pretti satifi experi', 'join club get awesom offer via email', 'perfect someon like beer ice cold case even colder', 'bland flavorless good way describ bare tepid meat', 'chain fan beat place easili', 'nacho must', 'come back', 'mani word say place everyth pretti well', 'staff super nice quick even crazi crowd downtown juri lawyer court staff', 'great atmospher friendli fast servic', 'receiv pita huge lot meat thumb', 'food arriv meh', 'pay hot dog fri look like came kid meal wienerschnitzel idea good meal', 'classic main lobster roll fantast', 'brother law work mall ate day guess sick night', 'good go review place twice herea tribut place tribut event held last night', 'chip salsa realli good salsa fresh', 'place great', 'mediocr food', 'get insid impress place', 'super pissd', 'servic super friendli', 'sad littl veget overcook', 'place nice surpris', 'golden crispi delici', 'high hope place sinc burger cook charcoal grill unfortun tast fell flat way flat', 'could eat bruschetta day devin', 'singl employe came see ok even need water refil final serv us food', 'lastli mozzarella stick best thing order', 'first time ever came amaz experi still tell peopl awesom duck', 'server neglig need made us feel unwelcom would suggest place', 'servic terribl though', 'place overpr consist boba realli overpr', 'pack', 'love place', 'say dessert yummi', 'food terribl', 'season fruit fresh white peach pure', 'kept get wors wors offici done', 'place honestli blown', 'definit would eat', 'wast money', 'love put food nice plastic contain oppos cram littl paper takeout box', 'cr pe delic thin moist', 'aw servic', 'ever go', 'food qualiti horribl', 'price think place would much rather gone', 'servic fair best', 'love sushi found kabuki price hip servic', 'favor stay away dish', 'poor servic', 'one tabl thought food averag worth wait', 'best servic food ever maria server good friendli made day', 'excel', 'paid bill tip felt server terribl job', 'lunch great experi', 'never bland food surpris consid articl read focus much spice flavor', 'food way overpr portion fuck small', 'recent tri caballero back everi week sinc', 'buck head realli expect better food', 'food came good pace', 'ate twice last visit especi enjoy salmon salad', 'back', 'could believ dirti oyster', 'place deserv star', 'would recommend place', 'fact go round star awesom', 'disbelief dish qualifi worst version food ever tast', 'bad day low toler rude custom servic peopl job nice polit wash dish otherwis', 'potato great biscuit', 'probabl would go', 'flavor perfect amount heat', 'price reason servic great', 'wife hate meal coconut shrimp friend realli enjoy meal either', 'fella got huevo ranchero look appeal', 'went happi hour great list wine', 'may say buffet pricey think get pay place get quit lot', 'probabl come back', 'worst food servic', 'place pretti good nice littl vibe restaur', 'talk great custom servic cours back', 
           'hot dish hot cold dish close room temp watch staff prepar food bare hand glove everyth deep fri oil', 'love fri bean', 'alway pleasur deal', 'plethora salad sandwich everyth tri get seal approv', 'place awesom want someth light healthi summer', 'sushi strip place go', 'servic great even manag came help tabl', 'feel dine room colleg cook cours high class dine servic slow best', 'start review two star edit give one', 'worst sushi ever eat besid costco', 'excel restaur highlight great servic uniqu menu beauti set', 'boyfriend sat bar complet delight experi', 'weird vibe owner', 'hardli meat', 'better bagel groceri store', 'go place gyro', 'love owner chef one authent japanes cool dude', 'burger good pizza use amaz doughi flavorless', 'found six inch long piec wire salsa', 'servic terribl food mediocr', 'defin enjoy', 'order albondiga soup warm tast like tomato soup frozen meatbal', 'three differ occas ask well done medium well three time got bloodiest piec meat plate', 'two bite refus eat anymor', 'servic extrem slow', 'minut wait got tabl', 'serious killer hot chai latt', 'allergi warn menu waitress absolut clue meal contain peanut', 'boyfriend tri mediterranean chicken salad fell love', 'rotat beer tap also highlight place', 'price bit concern mellow mushroom', 'worst thai ever', 'stay vega must get breakfast least', 'want first say server great perfect servic', 'pizza select good', 'strawberri tea good', 'highli unprofession rude loyal patron', 'overal great experi', 'spend money elsewher', 'regular toast bread equal satisfi occasion pat butter mmmm', 'buffet bellagio far anticip', 'drink weak peopl', 'order correct', 'also feel like chip bought made hous', 'disappoint dinner went elsewher dessert', 'chip sal amaz', 'return', 'new fav vega buffet spot', 'serious cannot believ owner mani unexperienc employe run around like chicken head cut', 'sad', 'felt insult disrespect could talk judg anoth human like', 'call steakhous properli cook steak understand', 'impress concept food', 'thing crazi guacamol like pur ed', 'realli noth postino hope experi better', 'got food poison buffet', 'brought fresh batch fri think yay someth warm', 'hilari yummi christma eve dinner rememb biggest fail entir trip us', 'needless say go back anytim soon', 'place disgust', 'everi time eat see care teamwork profession degre', 'ri style calamari joke', 'howev much garlic fondu bare edibl', 'could bare stomach meal complain busi lunch', 'bad lost heart finish', 'also took forev bring us check ask', 'one make scene restaur get definit lost love one', 'disappoint experi', 'food par denni say good', 'want wait mediocr food downright terribl servic place', 'waaaaaayyyyyyyyyi rate say', 'go back', 'place fairli clean food simpli worth', 'place lack style', 'sangria half glass wine full ridicul', 'bother come', 'meat pretti dri slice brisket pull pork', 'build seem pretti neat bathroom pretti trippi eat', 'equal aw', 'probabl hurri go back', 'slow seat even reserv', 'good stretch imagin', 'cashew cream sauc bland veget undercook', 'chipolt ranch dip saus tasteless seem thin water heat', 'bit sweet realli spici enough lack flavor', 'disappoint', 'place horribl way overpr', 'mayb vegetarian fare twice thought averag best', 'busi know', 'tabl outsid also dirti lot time worker alway friendli help menu', 'ambianc feel like buffet set douchey indoor garden tea biscuit', 'con spotti servic', 'fri hot neither burger', 'came back cold', 'food came disappoint ensu', 'real disappoint waiter', 'husband said rude even apolog bad food anyth', 'reason eat would fill night bing drink get carb stomach', 'insult profound deuchebaggeri go outsid smoke break serv solidifi', 'someon order two taco think may part custom servic ask combo ala cart', 'quit disappoint although blame need place door', 'rave review wait eat disappoint', 'del taco pretti nasti avoid possibl', 'hard make decent hamburg', 'like', 'hell go back', 'gotten much better servic pizza place next door servic receiv restaur', 'know big deal place back ya', 'immedi said want talk manag want talk guy shot firebal behind bar', 'ambianc much better', 'unfortun set us disapppoint entre', 'food good', 'server suck wait correct server heimer suck', 'happen next pretti put', 'bad caus know famili own realli want like place', 'overpr get', 'vomit bathroom mid lunch', 'kept look time soon becom minut yet still food', 'place eat circumst would ever return top list', 'start tuna sashimi brownish color obvious fresh', 'food averag', 'sure beat nacho movi would expect littl bit come restaur', 'ha long bay bit flop', 'problem charg sandwich bigger subway sub offer better amount veget', 'shrimp unwrap live mile brushfir liter ice cold', 'lack flavor seem undercook dri', 'realli impress place close', 'would avoid place stay mirag', 'refri bean came meal dri crusti food bland', 'spend money time place els', 'ladi tabl next us found live green caterpillar salad', 'present food aw', 'tell disappoint', 'think food flavor textur lack', 'appetit instantli gone', 'overal impress would go back', 'whole experi underwhelm think go ninja sushi next time', 'wast enough life pour salt wound draw time took bring check']

    return corpus

def downloadwords(request):
    nltk.download('stopwords')
    
def mainnlp(comment):
    # nltk.download('stopwords')
    # comment = request.GET.get('review')
    corpus = getcorpus()
    review = re.sub('[^a-zA-Z]',' ', comment)
    review = review.lower()
    review=review.split()
    ps=PorterStemmer()
    review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
    review = ' '.join(review)
    corpus.append(review)

    cv= CountVectorizer(max_features=1500)
    x=cv.fit_transform(corpus).toarray()

    BASE_DIRS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir= os.path.join(BASE_DIRS,'cab/ReviewNLP.pkl')
    mdl = joblib.load(model_dir)

    s = mdl.predict(x[-1].reshape(1,-1)).tolist()
    # print(s)
    
    for i in s:
        a = i

    return i


def signup(request):
    userName = request.GET.get('username')
    eMail = request.GET.get('email')
    firstname = request.GET.get('firstname')
    lastname = request.GET.get('lastname')
    Password = request.GET.get('password')
    Mobile = request.GET.get('mobile')
    Airport = request.GET.get('airport')
    Category1 = request.GET.get('category')
    Object_name = request.GET.get('object_name')
    service = request.GET.get('services')
    D=request.GET.get('doctor')
    lat = request.GET.get('latitude')
    longi = request.GET.get('longitude')


    check = User.objects.filter(username = userName)
    checkEmail = User.objects.filter(email = eMail)
    checkHouse = userdetails.objects.filter(mobile=Mobile)
   

    if len(check) > 0:
        
            return JsonResponse({'result':0,'message':'Username already exist'})
    
    elif len(checkEmail) > 0:

            return JsonResponse({'result':0,'message':'Email address already exist'})


    elif len(checkHouse) > 0:
             return JsonResponse({'result':0,'message':'Mobile already registered'}) 

    
    else:
        # if Cab == 'y':
        #     Cab = True
        # else:
        #     Cab = False
        
        # if Hotel == 'y':
        #     Hotel = True
        # else:
        #     Hotel = False

        # if Restro == 'y':
        #     Restro = True
        # else:
        #     Restro = False

        # if Store == 'y':
        #     Store = True
        # else:
        #     Store = False    

        if Category1 is not None:
            Category1 = Category1.upper()
            
        else:
            Category1 = 'NA'

        if Object_name is None:
            Object_name = 'NA'

        if Airport is None:
            Airport = 'NA'

        if service is None:
            service = None
        else:
            if Category1 == 'STORE':
                c = cat.objects.filter(name=service.upper(),store=True)
                if len(c) > 0:
                    service=c[0]
                else:
                    z = cat(name=service.upper(),airport=Airport,store=True) 
                    z.save()
                    service=z   

            elif Category1 == 'RESTAURANTS':
                c = cat.objects.filter(name=service.upper(),restaurants=True)
                if len(c) > 0:
                    service=c[0]
                else:
                    z = cat(name=service.upper(),airport=Airport,restaurants=True) 
                    z.save()
                    service=z   
            
            elif Category1 == 'HOTEL':
                c = cat.objects.filter(name=service.upper(),hotel=True)
                if len(c) > 0:
                    service=c[0]
                else:
                    z = cat(name=service.upper(),airport=Airport,hotel=True) 
                    z.save()
                    service=z   
        


        if D is not None:
            D = True
        else:
            D = False

        if longi is None:
            longi = '0.0'
        if lat is None:
            lat = '0.0'

        user1 = User.objects.create_user(username = userName, email=eMail, password=Password, first_name = firstname , last_name = lastname)
        userD = userdetails(user=user1,mobile=Mobile,resturants=False,category=Category1,airport=Airport,objectname=Object_name,serves=service,doctor=D,longitude=longi,latitude=lat)

        w = wallet(user=user1)
        w.save()
        user1.save()
        userD.save()
        return JsonResponse({'result':1,'message':'success'})

def getWallet(request):
    Username = request.GET.get('username')

    w = wallet.objects.get(user__username=Username)

    return JsonResponse({'wallet':w.amount})


def staticimg(request):
    Username = request.GET.get('username')
    D = request.GET.get('dp')

    ud = userdetails.objects.get(user__username=Username)
    
    ud.dp=D
    ud.save()
    return JsonResponse({'result':1,'message':'success'})



def login(request):
    userName = request.GET.get('username')
    Password = request.GET.get('password')
    

    user1 = authenticate(username=userName, password=Password)
    
    if user1 is not None:
        house = userdetails.objects.get(user = user1)
        return JsonResponse({'result':1,'username':user1.username,'email':user1.email,'firstname':user1.first_name,
                                'lastname':user1.last_name,'mobile':house.mobile,'objectName':house.objectname,
                                'address':house.airport,'category':house.category,'airport':house.airport,'latitude':house.latitude,'longitude':house.longitude,'vip':house.vip,'risk':house.risk,'tSime':house.time,'approved':house.approve,'storeActive':house.complain})
    
    else:
        return JsonResponse({'result':0,'message':'Incorrect username or password'})


def addProduct(request):
    Username = request.GET.get('username')
    Name = request.GET.get('name')
    Description = request.GET.get('description')
    Stock = request.GET.get('stock')
    Active = request.GET.get('active')
    Display = request.GET.get('dp')
    cost = request.GET.get('costprice')
    sell = request.GET.get('sellprice')
    Discount= request.GET.get('discount')
    service = request.GET.get('category')

    if Active == 'y':
        Active = True
    else:
        Active = False    


    ud = userdetails.objects.get(user__username=Username)
    

    c = cat.objects.filter(name=service.upper(),airport=ud.airport)
    if len(c) > 0:
        
        if ud.airport == c[0].airport:
            service=c[0]


    else:
        Airport = ud.airport
        z = cat(name=service.upper(),airport=Airport) 
        z.save()
        service=z   
            
    print(service)
    user1 = User.objects.get(username=Username)
    # userD = userdetails.object.get(user = user1)
    proid = "PROD"+str(random.randint(9999,99999))
    add = Product(user=user1,productName=Name,productid=proid,productDescription=Description,stock=Stock,active=Active,display=Display,costPrice=cost,sellingPrice=sell,discount=Discount,category=service)
    add.save()



    return JsonResponse({'result':1,'message':'Success'})

def editproduct(request):
    Name = request.GET.get('Name')
    Description = request.GET.get('description')
    Stock = request.GET.get('stock')
    Active = request.GET.get('active')
    Display = request.GET.get('dp')
    cost = request.GET.get('costprice')
    Sell = request.GET.get('sellprice')
    Discount= request.GET.get('discount')
    proid = request.GET.get('productid')
        
    p = Product.objects.get(productid=proid)

    if Name is not None:
        p.productName = Name

    if Description is not None:
        p.productDescription = Description

    if Stock is not None:
        p.stock = int(Stock)

    if Active is not None:
        if Active == 'y':
            Active = True
        else:
            Active = False    
        p.active = Active

    if Display is not None:
        p.display = Display

    if cost is not None:
        p.costPrice = float(cost)

    if Sell is not None:
        p.sellingPrice = float(Sell)
        
    if Discount is not None:
        p.discount = float(Discount)

    p.save() 
    return JsonResponse({'result':1,'message':'Success'})

def viewProduct(request):
    proid = request.GET.get('productid')
    isALL = request.GET.get('all')
    Username = request.GET.get('username')
    

    
    list = []
    catego = []


    if isALL == 'y':
        Airport = request.GET.get('airport').upper()
        servi = request.GET.get('services').upper()     
        
        p = Product.objects.all()        
        
        cc = cat.objects.filter(airport=Airport)
        for w in cc:
            if servi == 'STORE':
                if w.store == True and w.airport == Airport:
                    ss = catSerializer(w)
                    catego.append(ss.data)

            elif servi == 'RESTAURANTS':
                if w.restaurants == True and w.airport == Airport:
                    ss = catSerializer(w)
                    catego.append(ss.data)

            else:
                if w.hotel == True and w.airport == Airport:
                    ss = catSerializer(w)
                    catego.append(ss.data)


        for a in p:
            serial = ProductSerializer(a)

            if serial.data['category']['airport'] == Airport:

                
                
                ud = userdetails.objects.get(user__username=serial.data['user']['username'])
                if ud.category == servi:
                    serialud = userdetailsSerializer(ud)
                    list.append({'product details':serial.data,'store details':serialud.data,})
                
        return JsonResponse({'result':1,'categories':catego,'Product':list})
    
    elif Username is not None:
        user1 = User.objects.get(username=Username)    
        p = Product.objects.filter(user=user1)        
        # print(p)

        for a in p:
            serial = ProductSerializer(a)
            ser = User.objects.get(username=serial.data['user']['username'])
            
            c = catSerializer(a.category)
            if c.data not in catego:
                catego.append(c.data)

            ud = userdetails.objects.get(user=ser)
            serialud = userdetailsSerializer(ud)
            list.append({'product details':serial.data,'store details':serialud.data})
        
        return JsonResponse({'result':1,'categories':catego,'Product':list})
 
    else:
        p = Product.objects.get(productid=proid)
        serial = ProductSerializer(p)
        ser = User.objects.get(username=serial.data['user']['username'])
            
        ud = userdetails.objects.get(user=ser)
        serialud = userdetailsSerializer(ud)
        list.append({'product details':serial.data,'store details':serialud.data})
         
    return JsonResponse({'result':1,'Product':list})
 
def gettxnid():
    txnid1 = random.randint(100,999) + random.randint(9999,10000) 

    txn = "TXN15"+str(txnid1)
    
    return txn

def getcompid():
    txnid1 = random.randint(100,999) + random.randint(9999,10000) 

    txn = "COMP45"+str(txnid1)
    
    return txn

def recentcabs(request):
    Airport = request.GET.get('airport')
    Username = request.GET.get('username')

    c = cabOrder.objects.filter(user__username=Username).exclude(accept=0).exclude(accept=1).exclude(accept=2)
    list = []
    for i in c:
        serial = cabOrderSerializer(i)
        list.append(serial.data)

    return JsonResponse({'result':list})


def placeOrder(request):
    proid = request.GET.get('productid')
    Username = request.GET.get('username')    
    Q = request.GET.get('quantity')
    Pickup = request.GET.get('selfpickup')
    Date = request.GET.get('date')
    vid = request.GET.get('cabid')
    Pnr = request.GET.get('pnr')

    if Pnr is not None:
        Book = book.objects.get(pnr=Pnr)
    else:
        Book = None

    if vid is not None:
        cord = cabOrder.objects.get(cabid=vid)
    else:
        cord = None

    if Date is None:
        Date = timezone.now()
    else:
        Date = datetime.datetime.strptime(Date, '%Y-%m-%d')    

    if Pickup == 'y':
        Pickup=True
    else:    
        Pickup=False


    user1 = User.objects.get(username=Username)
    user2 = User.objects.get(username='admin')
    p = Product.objects.get(productid=proid)
    w = wallet.objects.get(user = user1)
    w1 = wallet.objects.get(user = p.user)
    w3 = wallet.objects.get(user__username = 'admin')
    Q = int(Q)
    
    
    a = Q*(p.sellingPrice - p.sellingPrice*(p.discount/100))
    if Pickup is False:
        aa = 0.25*a + a
    else:
        aa = 0.2*a + a        

    proid = "OD"+str(random.randint(999999,9999999))
    
    w.amount = w.amount - a
    w1.amount = w1.amount - aa
    w3.amount = w3.amount + 0.2*a


    o = order(flight=Book,user=user1,cab=cord,product=p,amount=a,orderid=proid,quantity=Q,selfpickup=Pickup,pickupDate=Date)
    o.save()
    w.save()
    w1.save()
    w3.save()

    txn = gettxnid()
    
    t = Tax(user = user1,Order=o,txnid=txn,credit=False,amount=a)
    t.save()

    txn = gettxnid()

    t = Tax(user = p.user,Order=o,txnid=txn,credit=True,amount=aa)
    t.save()


    txn = gettxnid()

    t = Tax(user = user2,Order=o,txnid=txn,credit=True,amount=a*0.2)
    t.save()

    ud = userdetails.objects.get(user = p.user)
    if ud.category == 'HOTEL':
        n = hotel(Order=o)
        n.save()
    
    
    return JsonResponse({'result':1,'message':'Success','orderid':proid})


def viewliveStoreorders(request):
    Username = request.GET.get('username')    
    
    user1 = User.objects.get(username=Username)
    
    o = order.objects.filter(product__user=user1).exclude(accept=3).exclude(accept=4)
    list = []

    for a in o:
        serial = orderSerializer(a)
        ser = User.objects.get(username=serial.data['product']['user']['username'])
        ud = userdetails.objects.get(user=ser)
        serialud = userdetailsSerializer(ud)
        ho = []
        if ud.category == 'HOTEL':
            h = hotel.objects.get(Order=a)
            hotelserial = hotelSerializer(h)
            ho.append({'hotel':hotelserial.data})
        list.append({'product details':serial.data,'store details':serialud.data,'hotel':ho})
                
    return JsonResponse({'result':list})
         
        
def acceptorder(request):
    proid = request.GET.get('orderid')

    o = order.objects.get(orderid=proid)

    o.accept=0
    ud = userdetails.objects.get(user = o.product.user)
    if ud.category == 'HOTEL':
        print(1)
    else:
        n = storerestro(Order=o)
        n.save()
            
    o.save()
    

    return JsonResponse({'result':1,'status':o.accept})

def userorder(request):
    userName = request.GET.get('username')

    user1 = User.objects.get(username=userName)
    o = order.objects.filter(user=user1)

    list = []

    for a in o:
        serial = orderSerializer(a)
        ser = User.objects.get(username=serial.data['product']['user']['username'])
        ud = userdetails.objects.get(user=ser)
        serialud = userdetailsSerializer(ud)
        checkIn = 'NA'
        CheckOUT= 'NA'
        if ud.category == 'HOTEL':
            h = hotel.objects.get(Order=a)
            hotelserial = hotelSerializer(h)
            checkIn = hotelserial.data['checkin']
            CheckOUT = hotelserial.data['checkout']
        list.append({'order':serial.data,'store_details':serialud.data,'checkin':checkIn,'checkout':CheckOUT})

    list2 = []

    cb = cabOrder.objects.filter(user=user1)

    for c in cb:
        serial = cabOrderSerializer(c)
        list2.append(serial.data)


    list3 = []

    bk = book.objects.filter(user=user1)

    for f in bk:
        serial = bookSerializer(f)
        list3.append(serial.data)


    return JsonResponse({'result':list,'cab':list2,'flight':list3})


def storeorderr(request):
    userName = request.GET.get('username')

    user1 = User.objects.get(username=userName)
    print(user1)
    o = order.objects.filter(product__user=user1)
    
    list = []

    for a in o:
        serial = orderSerializer(a)
        ser = User.objects.get(username=serial.data['product']['user']['username'])
        ud = userdetails.objects.get(user=ser)
        serialud = userdetailsSerializer(ud)
        Userde = userdetails.objects.get(user__username=serial.data['user']['username'])
        udd = userdetailsSerializer(Userde)
        checkIn = 'NA'
        CheckOUT= 'NA'
        if ud.category == 'HOTEL':
            h = hotel.objects.get(Order=a)
            hotelserial = hotelSerializer(h)
            checkIn = hotelserial.data['checkin']
            CheckOUT = hotelserial.data['checkout']
        list.append({'order':serial.data,'store_details':serialud.data,'checkin':checkIn,'checkout':CheckOUT,'user details':udd.data})
        
    return JsonResponse({'result':list})
   
def addcheckin(request):
    Orderid = request.GET.get('orderid')
    Op = request.GET.get('operation')

    o = order.objects.get(orderid=Orderid)
    
    if Op == 'checkin':
        o.accept = 2
    else:
        o.accept = 3

    return JsonResponse({'status':o.accept})

def hotelorder(request):
    odid = request.GET.get('orderid')
    checki = request.GET.get('checkin')
    checko = request.GET.get('checko')
    rating1 = request.GET.get('rating')

    d = order.objects.get(orderid=odid)
    o = hotel.objects.get(Order=d)

    if checki is not None:
        o.checkin = checki
        # d.accept=2

    if checko is not None:
        o.checkout = checko
        # d.accept=3

    if rating1 is not None:
        o.Rating = rating
    
    o.save()
    return JsonResponse({'result':1})

def storeorder(request):
    odid = request.GET.get('orderid')
    prepare = request.GET.get('preparing_packaging')
    dispatched1 = request.GET.get('dispatched')
    delivered1 = request.GET.get('delivered')
    rating1 = request.GET.get('rating')
    

    d = order.objects.get(orderid=odid)

    o = storerestro.objects.get(Order=d)

    if prepare is not None:
        o.preparing_packaging = True
        
        if d.cab is not None:
            print(1)
            # dispatchDelivery.apply_async(args=[d.orderid],eta=timezone.now())
            # dispatchDelivery.apply_async(args=[d.orderid],eta=d.cab.pickupTime - timedelta(minutes=15))
            d.accept = 1
        else:
            d.accept = 1
        print(d.accept)
        
    if dispatched1 is not None:
        o.dispatched = True
        d.accept = 2
    
    if delivered1 is not None:
        o.delivered = True
        d.accept = 3

    if rating1 is not None:
        o.Rating = True

    d.save()
    o.save()    
    return JsonResponse({'result':1,'status':d.accept})

def updatestoreRating(request):
    odid = request.GET.get('orderid')
    rating1 = float(request.GET.get('productrating'))
    rating2 = float(request.GET.get('storerating'))
    rating3 = request.GET.get('deliveryrating')

    d = order.objects.get(orderid=odid)

    o = storerestro.objects.get(Order=d)

    
    o.Rating = rating1

    if rating3 is not None:
        rating3 = float(rating3)


        ud = userdetails.objects.get(user=d.delivery)
        ud.total += 1
        ud.rating = ((ud.rating * ud.total) + rating3)/ud.total
        ud.save()

    ud = userdetails.objects.get(user=d.product.user)
    ud.total += 1
    
    ud.rating = ((ud.rating * ud.total) + rating2)/ud.total
    ud.save()

    d.product.total += 1
    d.product.rating = ((d.product.rating * d.product.total) + rating1)/d.product.total


    
    d.save() 
    o.save()   
    return JsonResponse({'result':1,'status':d.accept})

 

def paytmCall1(request):
        username1 = request.GET.get('username')
        am = request.GET.get('TXN_AMOUNT')

        w = wallet.objects.get(user__username=username1)
        w.amount = w.amount + float(am)
        
        txnid1 = random.randint(100,999) + random.randint(9999,10000)
        w.save()
        txn = "TXN25"+str(txnid1)
        user1 = User.objects.get(username=username1)
        t = Tax(user = user1,Order=None,txnid=txnid1,credit=True,amount=float(am))
        t.save()

        return JsonResponse({'result':1})



class transactionListView(ListAPIView):
    queryset = Tax.objects.all()
    serializer_class = transactionSerializer
        



def hotelRating(request):
    odid = request.GET.get('orderid')
    rating1 = float(request.GET.get('roomrating'))
    rating2 = float(request.GET.get('hotelrating'))
    

    
    d = order.objects.get(orderid=odid)
    o = hotel.objects.get(Order=d)

    o.Rating = rating1

    d.product.total += 1
    d.product.rating = ((d.product.rating * d.product.total) + rating1)/d.product.total

    ud = userdetails.objects.get(user=d.product.user)
    ud.total += 1
    ud.rating = ((ud.rating * ud.total) + rating2)/ud.total
    ud.save()
    d.save()
    return JsonResponse({'result':1,'status':d.accept})

def showtrans(request):
    Username = request.GET.get('username')

    t = Tax.objects.filter(user__username=Username)
    list = []
    for i in t:
        serial = transactionSerializer(i)
        list.append({'data':serial.data})

    return JsonResponse({'result':list})




###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
#########        ####          #####################################################
######### ###### #### #############################################################
######### ###### ####        ######################################################
######### ###### #### #############################################################
######### ###### ####        ######################################################
######### ###### #### #############################################################
#########        ####        ######################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################







def showorderstate(Orderid):
    o =order.objects.get(orderid=Orderid)
    if o.accept==1 or o.accept ==10:
        #show store details
        serial = UserSerializer(o.product.user)
        ud = userdetails.objects.get(user = o.product.user)
        serialud = userdetailsSerializer(ud)

        return JsonResponse({'result':'You already have a existing delivery please complete to get more','parameter':2,'Store Details':serial.data,'more details':serialud.data,'orderid':Orderid})

    elif o.accept == 2:
        os = orderSerializer(o)
        return JsonResponse({'result':os.data,'parameter':3})



def deliverypending(request):
    Username = request.GET.get('username')

    ud = userdetails.objects.get(user__username=Username)
    if(ud.deli == False):
        ss = order.objects.filter(accept=1,delivery=None).exclude(selfpickup=True)
        
        list = []
        for s in ss:
            
            ud1 = userdetails.objects.get(user=s.product.user)
            if ud1.airport == ud.airport:
                serial = orderSerializer(s)
                ser = User.objects.get(username=serial.data['user']['username'])
                serialud = userdetailsSerializer(ud1)
                list.append({'order details':serial.data,'User details':serialud.data,'parameter':1})

        return JsonResponse({'result':list,'parameter':1})
    else:

        return showorderstate(ud.co.orderid)



def acceptdelivery(request):
    Username = request.GET.get('username')
    Orderid=request.GET.get('orderid')            

    o = order.objects.get(orderid=Orderid)
    o.accept = 10
    user1 = User.objects.get(username=Username)

    o.delivery = user1
    o.save()

    ud = userdetails.objects.get(user__username=Username)
    ud.co = o
    ud.deli=True
    ud.save()
    return JsonResponse({'orderid':o.orderid})

def generateqr(request):
    Orderid=request.GET.get('orderid')            


    o = order.objects.get(orderid=orderid)

    return JsonResponse({'orderid':o.orderid})

def scanqr(request):
    Orderid=request.GET.get('orderid')            
    o = order.objects.get(orderid=Orderid)
    o.accept = 2
    o.save()
    return JsonResponse({'orderid':o.orderid})

def deliverproduct(request):
    Orderid=request.GET.get('orderid')            
    o = order.objects.get(orderid=Orderid)
    ud = userdetails.objects.get(user=o.delivery)
    ud.deli=False
    ud.co=None
    
    ud.save()
    o.accept = 3
    o.save()
   
    txn = gettxnid()
    
    t = Tax(user = o.delivery,Order=o,txnid=txn,credit=True,amount=o.amount*0.05)
    t.save()

    return JsonResponse({'result':'success'})


def showinfo(request):
    Orderid=request.GET.get('orderid')            
    return showorderstate(Orderid)



def deliveryhistory(request):
    Username = request.GET.get('username')
    o = order.objects.filter(delivery__username=Username)
    list = []
    for i in o:
        serial = orderSerializer(i)
        list.append(serial.data)

    return JsonResponse({'result':list})




###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################



def addAirport(request):
    Name = request.GET.get('name')
    City = request.GET.get('city')
    State = request.GET.get('state')
    Latitude = request.GET.get('latitude')
    Longitude = request.GET.get('longitude')

    s = airport(name=Name.upper(),city=City.upper(),state=State.upper(),latitude=Latitude,longitude=Longitude)
    s.save()

    return JsonResponse({'result':1})

def viewUsers(request):
    Airport = request.GET.get('airport')

    ud = userdetails.objects.filter(airport=Airport.upper()).exclude(category='NA')
    store = []
    hotel = []
    cab = []
    restro=[]

    for u in ud:
            if u.category == 'STORE':
                serial = userdetailsSerializer(u)
                store.append(serial.data)
            elif u.category == 'HOTEL':
                serial = userdetailsSerializer(u)
                hotel.append(serial.data)
            elif u.category == 'RESTAURANTS':
                serial = userdetailsSerializer(u)
                restro.append(serial.data)
            elif u.category == 'CAB':
                serial = userdetailsSerializer(u)
                cab.append(serial.data)

    return JsonResponse({'store':store,'hotel':hotel,'cab':cab,'restro':restro})


def addAirline(request):
    Name = request.GET.get('name')
    Logo = request.GET.get('logo')

    a = airline(name=Name.upper(),logo=Logo)
    a.save()

    return JsonResponse({'result':1})

def addFlight(request):
    Origin = request.GET.get('origin')
    Destination = request.GET.get('destination')
    AIrline = request.GET.get('airline')
    Arrival = request.GET.get('arrival')
    Departure = request.GET.get('departure')
    Seat = request.GET.get('seat')
    Name = request.GET.get('name')


    fid = 'FL'+str(random.randint(999999,9999999))
    Seat = int(Seat)        
    a = airline.objects.get(name=AIrline.upper())
    Arrival = datetime.datetime.strptime(Arrival, '%H:%M:%S')
    # Arrival = datetime.datetime(Arrival)
    Departure = datetime.datetime.strptime(Departure, '%H:%M:%S')
    route = routes(flightid=fid,name=Name.upper(),origin=Origin.upper(),destination=Destination.upper(),Airline=a,departure=str(Departure),arrival=str(Arrival),seat=Seat)
    route.save()
    return JsonResponse({'result':1})

def setFrequency(request):
    fid = request.GET.get('flightid')
    startDate = request.GET.get('start')
    endDate = request.GET.get('end')
    Price = float(request.GET.get('price'))
    r = routes.objects.get(flightid=fid)

    startDate=datetime.datetime.strptime(startDate, '%Y-%m-%d')
    endDate=datetime.datetime.strptime(endDate, '%Y-%m-%d')

    c = 0
    
    while startDate <= endDate:
        ro = 'ROUTE'+str(random.randint(999999,99999999))
        a = days(date=startDate,routeid=ro,Route=r,seat=r.seat,price=Price)
        startDate = startDate + datetime.timedelta(days=1)
        c += 1
        a.save()

    return JsonResponse({'flights added':c})
            
def findFlights(request):
    Origin = request.GET.get('origin')
    Destination = request.GET.get('destination')
    D = request.GET.get('Date')
    D=datetime.datetime.strptime(D, '%Y-%m-%d')

    r  = routes.objects.filter(origin=Origin.upper(),destination=Destination.upper())
    
    list = []
    for i in r:
        print(i)
        Da = days.objects.filter(date=D,Route=i)
        
        
        for da in Da:
            serial = daysSerializer(da)
            list.append(serial.data)

    return JsonResponse({'flights_available':list})

def bookFlights(request):
    ro = request.GET.get('routeid')
    Username = request.GET.get('username')
    Seat = request.GET.get('seat')
    Seat = int(Seat)

    bo = 'PNR'+str(random.randint(9999,99999))
    user1 = User.objects.get(username=Username)
    w = wallet.objects.get(user__username=Username)
    w1 = wallet.objects.get(user__username='admin')
    
    d = days.objects.get(routeid=ro)
    w.amount = w.amount - Seat*d.price
    w1.amount = w1.amount + Seat*d.price
    w.save()
    w1.save()

    b = book(dayobject=d,seat=Seat,pnr=bo,amount=Seat*d.price,user=user1)
    b.save()
    
    return JsonResponse({'pnr':b.pnr})


def listAirport(request):

    a = airport.objects.all()
    list = []
    for i in a:
        serial = airportSerializer(i)
        list.append(serial.data)

    return JsonResponse({'result':list})    

def listAirline(request):

    a = airline.objects.all()
    list = []
    for i in a:
        serial = airlineSerializer(i)
        list.append(serial.data)

    return JsonResponse({'result':list})    


def listflight(request):
    City = request.GET.get('city')
    a = routes.objects.filter(origin=City.upper())
    list = []
    for i in a:
        serial = routesSerializer(i)
        list.append(serial.data)

    a = routes.objects.filter(destination=City.upper())
    list1 = []
    for i in a:
        serial = routesSerializer(i)
        list1.append(serial.data)

    return JsonResponse({'arrival':list,'departure':list1})    





def godseye(request):
    Airport = request.GET.get('airport')

    userall = userdetails.objects.all()

    listuser = []
    listdelivery = []
    listcab = []
    for u in userall:
        if u.category == 'NA':
            serial = userdetailsSerializer(u)
            listuser.append({'first_name':serial.data['user']['first_name'],'username':serial.data['user']['username'],'risk':serial.data['risk']})
        elif u.category == 'DELIVERY' and u.airport == Airport:
            serial = userdetailsSerializer(u)
            listdelivery.append({'first_name':serial.data['user']['first_name'],'username':serial.data['user']['username'],'Ondelivery':serial.data['deli']})
        elif u.category == 'CAB' and u.airport == Airport:
            serial = userdetailsSerializer(u)
            z = cabdetails.objects.filter(user=u.user)
            for c in z:
                listcab.append({'first_name':serial.data['user']['first_name'],'username':serial.data['user']['username'],'isIdle':serial.data['cabIdle'],'Going to':serial.data['cabO'],'cabModel':c.carModel,'cabtype':c.cartype.cartype,'cabRegistration':c.carRegistration})
                 
    return JsonResponse({'Users':listuser,'delivery':listdelivery,'listcab':listcab})    













###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################




def setdocactive(request):
    userName = request.GET.get('username')
    

    user1 = userdetails.objects.get(user__username=userName)
    
    user1.active = not user1.active
    user1.save()
    return JsonResponse({'result':1})

def risk(request):
    userName = request.GET.get('username')
    Risk = request.GET.get('risk')
    # Time = request.GET.get('time')

    user1 = userdetails.objects.get(user__username=userName)
    
    Time = timezone.now()

    user1.risk = int(Risk)
    user1.time = Time
    user1.save()
    return JsonResponse({'result':1})

def viewdoctor(request):
    users = userdetails.objects.filter(doctor=True)
    list = []
    for u in users:
        serialud = userdetailsSerializer(u)
        list.append({'doctor':serialud.data})
        

    return JsonResponse({'result':list})

def meetcall(request):
    userName = request.GET.get('username')
    duserName = request.GET.get('docusername')
    Meet = request.GET.get('meet')
    Call = request.GET.get('chat')
    
    user1 = User.objects.get(username=userName)
    user2 = User.objects.get(username=duserName)


    if Meet is not None:
        Meet = True
    else:
        Meet = False

    if Call is not None:
        Call = True 
    else:
        Call = False       

    d = Doctor(user=user1,doctor=user2,meet=Meet,chat=Call)    
    d.save()
    return JsonResponse({'result':1})

def acceptpatient(request):
    userName = request.GET.get('username')
    duserName = request.GET.get('docusername')


    user1 = User.objects.get(username=userName)
    user2 = User.objects.get(username=duserName)    
    d = Doctor.objects.get(user=user1,doctor=user2)

    d.pending = True
    d.save()

    return JsonResponse({'result':1})

def viewpendingpatient(request):
    duserName = request.GET.get('docusername')


    user2 = User.objects.get(username=duserName)    
    
    ds = Doctor.objects.filter(doctor=user2,pending=False)

    list = []
    for d in ds:
        serial = UserSerializer(d.user)
        
        ud = userdetails.objects.get(user__username=serial.data['username'])
        serialud = userdetailsSerializer(ud)
        list.append({'Patient details':serial.data,'other info':serialud.data})
        
    return JsonResponse({'result':list})
        

class complainListView(ListAPIView):
    queryset = Complain.objects.all()
    serializer_class = complainSerializer

def complainss(request):
    userName = request.GET.get('username')
    complains = request.GET.get('complain')
    complainid1 = request.GET.get('complainid')



    user1 = User.objects.get(username=userName)

    complaint = random.randint(100,999) + random.randint(9999,10000) + user1.pk
    
    complaint = "COMP25"+str(complaint)

    print(complaint)
    comp = Complain(complain = complains,complainid = complainid1,complaintxn = complaint )
    comp.user = user1
    comp.save()    

    return JsonResponse({'result': 1})

def resolveComplain(request):
    get_id = request.GET.get('id')

    comp = Complain.objects.get(pk=get_id)
    comp.status = True

    comp.save()
    return JsonResponse({'result':1})  





#######################################################
#######################################################
#######################################################
#######################################################
#######################################################
#######################################################
#######################################################
#######################################################
###########################################################
#######################################################
#######################################################


def currentorders(request):
    Username = request.GET.get('username')

    o = order.objects.filter(user__username=Username).exclude(accept=3).exclude(accept=2).exclude(accept=4)

    list = []

    for a in o:
        serial = orderSerializer(a)
        ser = User.objects.get(username=serial.data['product']['user']['username'])
        ud = userdetails.objects.get(user=ser)
        serialud = userdetailsSerializer(ud)
        checkIn = 'NA'
        CheckOUT= 'NA'
        if ud.category == 'HOTEL':
            h = hotel.objects.get(Order=a)
            hotelserial = hotelSerializer(h)
            checkIn = hotelserial.data['checkin']
            CheckOUT = hotelserial.data['checkout']
        list.append({'order':serial.data,'store_details':serialud.data,'checkin':checkIn,'checkout':CheckOUT})

    o = order.objects.filter(user__username=Username,accept=3)
    list3 = []
    for a in o:
        serial = orderSerializer(a)
        ser = User.objects.get(username=serial.data['product']['user']['username'])
        ud = userdetails.objects.get(user=ser)
        serialud = userdetailsSerializer(ud)
        checkIn = 'NA'
        CheckOUT= 'NA'
        if ud.category == 'HOTEL':
            h = hotel.objects.get(Order=a)
            hotelserial = hotelSerializer(h)
            checkIn = hotelserial.data['checkin']
            CheckOUT = hotelserial.data['checkout']
        list3.append({'order':serial.data,'store_details':serialud.data,'checkin':checkIn,'checkout':CheckOUT})


    list1 = []


    c = cabOrder.objects.filter(user__username=Username).exclude(accept=1).exclude(accept=2)
    for i in c:
        serial = cabOrderSerializer(i)
        list1.append(serial.data)
        

    return JsonResponse({'orders':list,'cab':list1,'previous':list3})  

def cancelOrder(request):
    Orderid = request.GET.get('orderid')

    o = order.objects.get(orderid=Orderid)
    o.accept = 4
    o.save()

    w = wallet.objects.get(user=o.product.user)
    w.amount = w.amount - o.amount*0.75
    w.save()

    txn = gettxnid()

    t = Tax(user = o.product.user,Order=o,txnid=txn,credit=False,amount=o.amount*0.75)
    t.save()

    w = wallet.objects.get(user=o.user)
    w.amount = w.amount + o.amount*0.75
    w.save()

    txn = gettxnid()

    t = Tax(user = o.user,Order=o,txnid=txn,credit=True,amount=o.amount*0.75)
    t.save()


    return JsonResponse({'amount refunded':o.amount*0.75})  
    
def cancelcab(request):
    Orderid = request.GET.get('cabid')

    o = cabOrder.objects.get(cabid=Orderid)
    o.accept = 4
    o.save()
    
    

    
    w = wallet.objects.get(user=o.user)
    w.amount = w.amount + o.price*0.80
    w.save()

    txn = gettxnid()

    t = Tax(user = o.user,txnid=txn,credit=True,amount=o.price*0.75)
    t.save()


    return JsonResponse({'amount refunded':o.price*0.80})  

def addComplains(request):
    Username = request.GET.get('username')    
    Orderid = request.GET.get('orderid')
    Complain = request.GET.get('complain')
    
    compid = getcompid()
    user1 = User.objects.get(username=Username)
    o = order.objects.get(orderid=Orderid)
    c = productComplain(Order=o,user=user1,complainref=compid)
    c.save()

    return JsonResponse({'compid':c.complainref})

def isInside(lat,long,p):
    latlng1 = s2.S2LatLng.FromDegrees(lat,long)
    cell1 = s2.S2CellId(latlng1)
    return p.contains(cell1)

def arogyasetu(request):
    Username = request.GET.get('username')
    # Username = 'sayak'

    link1 = 'https://vimansathi.firebaseio.com/user/'+ Username +'.json'
    # link1 = 'https://vimansathi.firebaseio.com/user/sayak.json'
    # print(link1)
    response1 = requests.get(link1)
    response1 = response1.json()

    latlng = s2.S2LatLng.FromDegrees(response1['latitude'], response1['longitude'])
    cell = s2.S2CellId(latlng)
    
    level = [13,12,11,10]

    p = cell.parent(13)
    

    userall = userdetails.objects.all().exclude(user__username=Username)
    list = []
        
    count = 0

    link1 = 'https://vimansathi.firebaseio.com/user.json'
    response = requests.get(link1)
    response = response.json()

    for u in userall:
        if u.category == 'NA' and u.risk == 3 and u.user.username != Username:
            try:
                response3 = response[u.user.username]   
                if response3!=None and response3['address'] == response1['address']:
                    result = isInside(float(response3['latitude']),float(response3['longitude']),p)
                    if result == True:
                        count += 1        
            except KeyError:
                continue
    list.append(count)                
                
    return JsonResponse({'count':list})

def addReview(request):
    Orderid = request.GET.get('orderid')
    Review = request.GET.get('review')
    print(Review)
    o = order.objects.get(orderid=Orderid)
    o.review = Review
    a = mainnlp(Review)
    print(a)
    o.reviewState = a
    o.save()

    return JsonResponse({'result':1})

def showProductReview(request):
    proid = request.GET.get('productid')

    o = order.objects.filter(product__productid=proid)
    list = []
    for i in o:
        if i.review != 'NA':
            list.append({'review':i.review,'reviewState':i.reviewState})


    return JsonResponse({'result':list})

def ohevalue(df):
    BASE_DIRS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir= os.path.join(BASE_DIRS,'api/fare_ohe.pkl')
    ohe_col = joblib.load(model_dir)
    cat_columns=['class']
    df_processed = pd.get_dummies(df, columns=cat_columns)
    print(df_processed)
    newdict={}
    print(ohe_col)
    for i in ohe_col:
        if i in df_processed.columns:
    	    newdict[i]=df_processed[i].values
        else:
    	    newdict[i]=0
    
    newdf=pd.DataFrame(newdict)
    print(newdf)
    return newdf

def approve(unit):
    try:
        BASE_DIRS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_dir= os.path.join(BASE_DIRS,'api/fare_pred_model.pkl')
    
        mdl=joblib.load(model_dir)
        
        X=unit
        X=np.array(unit).tolist()

        # print(X[0][3])
        Y = np.array([int(X[0][3]),int(X[0][4]),int(X[0][5]),int(X[0][6]),int(X[0][0]),int(X[0][1]),int(X[0][2])])
        Y=Y.reshape(1,-1)
        print(Y)
        y_pred=mdl.predict(Y)
        print(y_pred)
        # newdf=pd.DataFrame(y_pred>0.58, columns=['fare'])
        # print(newdf)
        # K.clear_session()
        return y_pred
    except ValueError as e:
        return (e.args[0])

def cxcontact(request):
    myDict = (request.GET).dict()
    print(myDict)
    df=pd.DataFrame(myDict, index=[0])
    answer=approve(ohevalue(df)).tolist()
    # a = answer[0]
    
    for i in answer:
        a = i 
    return JsonResponse({'result':i})

def isVip(request):
    Username = request.GET.get('username')

    ud = userdetails.objects.get(user__username=Username)

    ud.save()
    return JsonResponse({'result':ud.vip})



def approveShop(request):
    Username = request.GET.get('username')

    ud = userdetails.objects.get(user__username=Username)
    ud.approve = True

    ud.save()

    return JsonResponse({'result':1})

def complainShop(request):
    Complain = request.GET.get('disable')
    Username = request.GET.get('username')
    
    ud = userdetails.objects.get(user__username=Username)

    if Complain == 'y':
        ud.complain = True
        p = Product.objects.filter(user__username=Username)
        for i in p:
            i.active = False
            i.save()
    else:
        ud.complain = False
        
            
    ud.save()

    return JsonResponse({'result':1})

def approves(request):
    ud = userdetails.objects.filter(approve=False).exclude(category='NA')
    list = []
    for u in ud:
        serial = userdetailsSerializer(u)
        list.append(serial.data)

    return JsonResponse({'result':list})

def recentflightOrders(request):
    Username = request.GET.get('username')

    d = date.today()
    b = book.objects.filter(dayobject__date__gte=d,user__username=Username)
    list = []
    for i in b:
        serial = bookSerializer(i)
        list.append(serial.data)

    return JsonResponse({'result':list})    

def nlpreviews(request):
    Username = request.GET.get('username')

    s = order.objects.filter(product__user__username=Username)
    list = []
    for i in s:
        list.append(i.reviewState)

    return JsonResponse({'result':list})    

def notifyStore(request):
    Username = request.GET.get('username')
    Message1 = request.GET.get('message')

    user1 = User.objects.get(username=Username)
    m = message(user=user1,Message=Message1)

    m.save()
    return JsonResponse({'result':1})    

def getmessages(request):
    Username = request.GET.get('username')
    # Message1 = request.GET.get('message')
    m = message.objects.filter(user__username=Username)
    list = []
    for i in m:
        serial = messageSerializer(i)
        list.append(serial.data)

    return JsonResponse({'result':list})  


