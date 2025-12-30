# -*- coding: utf-8 -*-
"""
译林版四年级英语单词库（最新版）
按单元分类的单词库 - 2024年新教材
"""

from models.database import db_manager
from models.word import Word
from models.dictionary import Dictionary

VOCABULARY_GRADE_4_VOL1 = {
    "Unit 1 I like dogs": [
        {"word": "dog", "translation": "狗", "phonetic": "/dɒɡ/", "example": "I have a dog."},
        {"word": "cat", "translation": "猫", "phonetic": "/kæt/", "example": "My cat is cute."},
        {"word": "horse", "translation": "马", "phonetic": "/hɔːs/", "example": "The horse is running."},
        {"word": "cow", "translation": "奶牛", "phonetic": "/kaʊ/", "example": "The cow gives milk."},
        {"word": "pig", "translation": "猪", "phonetic": "/pɪɡ/", "example": "The pig is fat."},
        {"word": "sheep", "translation": "绵羊", "phonetic": "/ʃiːp/", "example": "There are many sheep on the farm."},
        {"word": "farm", "translation": "农场", "phonetic": "/fɑːm/", "example": "My uncle has a farm."},
        {"word": "animal", "translation": "动物", "phonetic": "/ˈænɪməl/", "example": "A dog is an animal."},
        {"word": "like", "translation": "喜欢", "phonetic": "/laɪk/", "example": "I like apples."},
        {"word": "these", "translation": "这些", "phonetic": "/ðiːz/", "example": "These are my books."},
        {"word": "those", "translation": "那些", "phonetic": "/ðəʊz/", "example": "Those are his pens."},
        {"word": "very", "translation": "非常", "phonetic": "/ˈveri/", "example": "I am very happy."},
        {"word": "cute", "translation": "可爱的", "phonetic": "/kjuːt/", "example": "The kitten is very cute."},
        {"word": "fat", "translation": "胖的", "phonetic": "/fæt/", "example": "The pig is so fat."},
        {"word": "thin", "translation": "瘦的", "phonetic": "/θɪn/", "example": "The cat is thin."},
        {"word": "big", "translation": "大的", "phonetic": "/bɪɡ/", "example": "I have a big bag."},
        {"word": "small", "translation": "小的", "phonetic": "/smɔːl/", "example": "I have a small ball."},
    ],
    "Unit 2 I have a rabbit": [
        {"word": "rabbit", "translation": "兔子", "phonetic": "/ˈræbɪt/", "example": "The rabbit has long ears."},
        {"word": "parrot", "translation": "鹦鹉", "phonetic": "/ˈpærət/", "example": "The parrot can talk."},
        {"word": "pet", "translation": "宠物", "phonetic": "/pet/", "example": "I have a pet dog."},
        {"word": "have", "translation": "有", "phonetic": "/hæv/", "example": "I have a new bike."},
        {"word": "has", "translation": "有（第三人称单数）", "phonetic": "/hæz/", "example": "She has a red dress."},
        {"word": "elephant", "translation": "大象", "phonetic": "/ˈelɪfənt/", "example": "The elephant has a long nose."},
        {"word": "giraffe", "translation": "长颈鹿", "phonetic": "/dʒəˈrɑːf/", "example": "The giraffe is very tall."},
        {"word": "lion", "translation": "狮子", "phonetic": "/ˈlaɪən/", "example": "The lion is the king of animals."},
        {"word": "monkey", "translation": "猴子", "phonetic": "/ˈmʌŋki/", "example": "The monkey is climbing the tree."},
        {"word": "panda", "translation": "熊猫", "phonetic": "/ˈpændə/", "example": "Pandas are from China."},
        {"word": "tiger", "translation": "老虎", "phonetic": "/ˈtaɪɡə/", "example": "The tiger is running fast."},
        {"word": "zebra", "translation": "斑马", "phonetic": "/ˈziːbrə/", "example": "The zebra has stripes."},
        {"word": "long", "translation": "长的", "phonetic": "/lɒŋ/", "example": "She has long hair."},
        {"word": "short", "translation": "短的", "phonetic": "/ʃɔːt/", "example": "He has short hair."},
        {"word": "tall", "translation": "高的", "phonetic": "/tɔːl/", "example": "My father is very tall."},
    ],
    "Unit 3 How many?": [
        {"word": "how many", "translation": "多少", "phonetic": "/haʊ ˈmeni/", "example": "How many apples do you have?"},
        {"word": "thirteen", "translation": "十三", "phonetic": "/θɜːˈtiːn/", "example": "I am thirteen years old."},
        {"word": "fourteen", "translation": "十四", "phonetic": "/fɔːˈtiːn/", "example": "There are fourteen books on the desk."},
        {"word": "fifteen", "translation": "十五", "phonetic": "/fɪfˈtiːn/", "example": "My sister is fifteen."},
        {"word": "sixteen", "translation": "十六", "phonetic": "/sɪksˈtiːn/", "example": "There are sixteen students in the class."},
        {"word": "seventeen", "translation": "十七", "phonetic": "/ˌsevənˈtiːn/", "example": "I have seventeen pencils."},
        {"word": "eighteen", "translation": "十八", "phonetic": "/eɪˈtiːn/", "example": "There are eighteen chairs."},
        {"word": "nineteen", "translation": "十九", "phonetic": "/naɪnˈtiːn/", "example": "She is nineteen years old."},
        {"word": "twenty", "translation": "二十", "phonetic": "/ˈtwenti/", "example": "I have twenty stickers."},
        {"word": "one", "translation": "一", "phonetic": "/wʌn/", "example": "I have one brother."},
        {"word": "two", "translation": "二", "phonetic": "/tuː/", "example": "I have two sisters."},
        {"word": "three", "translation": "三", "phonetic": "/θriː/", "example": "I have three apples."},
        {"word": "four", "translation": "四", "phonetic": "/fɔː/", "example": "There are four seasons."},
        {"word": "five", "translation": "五", "phonetic": "/faɪv/", "example": "I have five pens."},
        {"word": "six", "translation": "六", "phonetic": "/sɪks/", "example": "Six plus four is ten."},
        {"word": "seven", "translation": "七", "phonetic": "/ˈsevən/", "example": "There are seven days in a week."},
        {"word": "eight", "translation": "八", "phonetic": "/eɪt/", "example": "Eight times eight is sixty-four."},
        {"word": "nine", "translation": "九", "phonetic": "/naɪn/", "example": "Nine from ten is one."},
        {"word": "ten", "translation": "十", "phonetic": "/ten/", "example": "I have ten fingers."},
        {"word": "eleven", "translation": "十一", "phonetic": "/ɪˈlevən/", "example": "The bus comes at eleven."},
        {"word": "twelve", "translation": "十二", "phonetic": "/twelv/", "example": "There are twelve months in a year."},
    ],
    "Unit 4 I can play basketball": [
        {"word": "can", "translation": "能，会", "phonetic": "/kæn/", "example": "I can swim."},
        {"word": "can not", "translation": "不能，不会", "phonetic": "/kæn ˈnɒt/", "example": "I can not fly."},
        {"word": "play", "translation": "玩，打", "phonetic": "/pleɪ/", "example": "Let's play a game."},
        {"word": "basketball", "translation": "篮球", "phonetic": "/ˈbɑːskɪtbɔːl/", "example": "I like playing basketball."},
        {"word": "football", "translation": "足球", "phonetic": "/ˈfʊtbɔːl/", "example": "We play football on the field."},
        {"word": "jump", "translation": "跳", "phonetic": "/dʒʌmp/", "example": "Can you jump high?"},
        {"word": "run", "translation": "跑", "phonetic": "/rʌn/", "example": "I can run fast."},
        {"word": "swim", "translation": "游泳", "phonetic": "/swɪm/", "example": "She can swim very well."},
        {"word": "skate", "translation": "滑冰", "phonetic": "/skeɪt/", "example": "He can skate on the ice."},
        {"word": "cook", "translation": "烹饪", "phonetic": "/kʊk/", "example": "My mother can cook delicious food."},
        {"word": "draw", "translation": "画画", "phonetic": "/drɔː/", "example": "I can draw a cat."},
        {"word": "sing", "translation": "唱歌", "phonetic": "/sɪŋ/", "example": "She can sing beautifully."},
        {"word": "dance", "translation": "跳舞", "phonetic": "/dɑːns/", "example": "I can dance to the music."},
        {"word": "well", "translation": "好地", "phonetic": "/wel/", "example": "She sings very well."},
        {"word": "also", "translation": "也", "phonetic": "/ˈɔːlsəʊ/", "example": "I can also swim."},
        {"word": "grandma", "translation": "奶奶", "phonetic": "/ˈɡrændmɑː/", "example": "My grandma is very kind."},
        {"word": "grandpa", "translation": "爷爷", "phonetic": "/ˈɡrændpɑː/", "example": "My grandpa is tall."},
    ],
    "Unit 5 Our school": [
        {"word": "school", "translation": "学校", "phonetic": "/skuːl/", "example": "I go to school every day."},
        {"word": "classroom", "translation": "教室", "phonetic": "/ˈklɑːsruːm/", "example": "Our classroom is big."},
        {"word": "toilet", "translation": "厕所", "phonetic": "/ˈtɔɪlɪt/", "example": "Where is the toilet?"},
        {"word": "garden", "translation": "花园", "phonetic": "/ˈɡɑːdən/", "example": "The garden has many flowers."},
        {"word": "library", "translation": "图书馆", "phonetic": "/ˈlaɪbrəri/", "example": "I often read books in the library."},
        {"word": "playground", "translation": "操场", "phonetic": "/ˈpleɪɡraʊnd/", "example": "The children are playing in the playground."},
        {"word": "desk", "translation": "书桌", "phonetic": "/desk/", "example": "There is a book on my desk."},
        {"word": "chair", "translation": "椅子", "phonetic": "/tʃeə/", "example": "Please sit on the chair."},
        {"word": "blackboard", "translation": "黑板", "phonetic": "/ˈblækbɔːd/", "example": "The teacher writes on the blackboard."},
        {"word": "picture", "translation": "图片", "phonetic": "/ˈpɪktʃə/", "example": "There is a picture on the wall."},
        {"word": "window", "translation": "窗户", "phonetic": "/ˈwɪndəʊ/", "example": "Please open the window."},
        {"word": "door", "translation": "门", "phonetic": "/dɔː/", "example": "Close the door, please."},
        {"word": "floor", "translation": "地板", "phonetic": "/flɔː/", "example": "The floor is clean."},
        {"word": "wall", "translation": "墙", "phonetic": "/wɔːl/", "example": "There is a map on the wall."},
        {"word": "many", "translation": "许多", "phonetic": "/ˈmeni/", "example": "There are many books in the library."},
        {"word": "our", "translation": "我们的", "phonetic": "/ˈaʊə/", "example": "This is our classroom."},
    ],
    "Unit 6 At the snack bar": [
        {"word": "snack bar", "translation": "小吃店", "phonetic": "/snæk bɑː/", "example": "I want to buy something at the snack bar."},
        {"word": "hamburger", "translation": "汉堡包", "phonetic": "/ˈhæmbɜːɡə/", "example": "I like eating hamburgers."},
        {"word": "sandwich", "translation": "三明治", "phonetic": "/ˈsænwɪtʃ/", "example": "I have a sandwich for lunch."},
        {"word": "tea", "translation": "茶", "phonetic": "/tiː/", "example": "I would like a cup of tea."},
        {"word": "coffee", "translation": "咖啡", "phonetic": "/ˈkɒfi/", "example": "My father drinks coffee every morning."},
        {"word": "juice", "translation": "果汁", "phonetic": "/dʒuːs/", "example": "I like orange juice."},
        {"word": "water", "translation": "水", "phonetic": "/ˈwɔːtə/", "example": "I want a bottle of water."},
        {"word": "hot dog", "translation": "热狗", "phonetic": "/ˈhɒt dɒɡ/", "example": "A hot dog is a kind of food."},
        {"word": "ice cream", "translation": "冰淇淋", "phonetic": "/aɪs kriːm/", "example": "I like ice cream very much."},
        {"word": "would like", "translation": "想要", "phonetic": "/wʊd laɪk/", "example": "I would like a hamburger."},
        {"word": "something", "translation": "某物", "phonetic": "/ˈsʌmθɪŋ/", "example": "I would like something to drink."},
        {"word": "what about", "translation": "怎么样", "phonetic": "/wɒt əˈbaʊt/", "example": "What about some juice?"},
        {"word": "great", "translation": "太好了", "phonetic": "/ɡreɪt/", "example": "Great! We won the game."},
        {"word": "glass", "translation": "玻璃杯", "phonetic": "/ɡlɑːs/", "example": "I need a glass of water."},
        {"word": "bottle", "translation": "瓶子", "phonetic": "/ˈbɒtl/", "example": "This bottle is empty."},
        {"word": "money", "translation": "钱", "phonetic": "/ˈmʌni/", "example": "How much money do you have?"},
    ],
    "Unit 7 How much?": [
        {"word": "how much", "translation": "多少钱", "phonetic": "/haʊ mʌtʃ/", "example": "How much is this book?"},
        {"word": "yuan", "translation": "元（中国货币）", "phonetic": "/juˈɑːn/", "example": "This pen is five yuan."},
        {"word": "money", "translation": "钱", "phonetic": "/ˈmʌni/", "example": "I have no money with me."},
        {"word": "expensive", "translation": "贵的", "phonetic": "/ɪkˈspensɪv/", "example": "This bag is very expensive."},
        {"word": "cheap", "translation": "便宜的", "phonetic": "/tʃiːp/", "example": "This pencil is cheap."},
        {"word": "big", "translation": "大的", "phonetic": "/bɪɡ/", "example": "I want a big one."},
        {"word": "small", "translation": "小的", "phonetic": "/smɔːl/", "example": "I want a small one."},
        {"word": "long", "translation": "长的", "phonetic": "/lɒŋ/", "example": "I want a long ruler."},
        {"word": "short", "translation": "短的", "phonetic": "/ʃɔːt/", "example": "I want a short one."},
        {"word": "T-shirt", "translation": "T恤衫", "phonetic": "/ˈtiː ʃɜːt/", "example": "I like this T-shirt."},
        {"word": "skirt", "translation": "裙子", "phonetic": "/skɜːt/", "example": "My mother bought a new skirt."},
        {"word": "pair", "translation": "双，对", "phonetic": "/peə/", "example": "I want a pair of shoes."},
        {"word": "shoes", "translation": "鞋子", "phonetic": "/ʃuːz/", "example": "These shoes are very comfortable."},
        {"word": "socks", "translation": "袜子", "phonetic": "/sɒks/", "example": "I need a new pair of socks."},
        {"word": "trousers", "translation": "裤子", "phonetic": "/ˈtraʊzəz/", "example": "My father is wearing black trousers."},
        {"word": "colour", "translation": "颜色", "phonetic": "/ˈkʌlə/", "example": "What colour do you like?"},
    ],
    "Unit 8 Dolls": [
        {"word": "doll", "translation": "玩具娃娃", "phonetic": "/dɒl/", "example": "I have a cute doll."},
        {"word": "toy", "translation": "玩具", "phonetic": "/tɔɪ/", "example": "These are my toys."},
        {"word": "bear", "translation": "熊", "phonetic": "/beə/", "example": "I have a teddy bear."},
        {"word": "beautiful", "translation": "美丽的", "phonetic": "/ˈbjuːtɪfəl/", "example": "She is very beautiful."},
        {"word": "long hair", "translation": "长发", "phonetic": "/lɒŋ heə/", "example": "She has long hair."},
        {"word": "short hair", "translation": "短发", "phonetic": "/ʃɔːt heə/", "example": "He has short hair."},
        {"word": "big eyes", "translation": "大眼睛", "phonetic": "/bɪɡ aɪz/", "example": "The doll has big eyes."},
        {"word": "small eyes", "translation": "小眼睛", "phonetic": "/smɔːl aɪz/", "example": "The cat has small eyes."},
        {"word": "round face", "translation": "圆脸", "phonetic": "/raʊnd feɪs/", "example": "She has a round face."},
        {"word": "straight hair", "translation": "直发", "phonetic": "/streɪt heə/", "example": "I have straight hair."},
        {"word": "curly hair", "translation": "卷发", "phonetic": "/ˈkɜːli heə/", "example": "She has curly hair."},
        {"word": "nose", "translation": "鼻子", "phonetic": "/nəʊz/", "example": "The doll has a small nose."},
        {"word": "mouth", "translation": "嘴巴", "phonetic": "/maʊθ/", "example": "Open your mouth."},
        {"word": "ear", "translation": "耳朵", "phonetic": "/ɪə/", "example": "She has big ears."},
        {"word": "eye", "translation": "眼睛", "phonetic": "/aɪ/", "example": "She has beautiful eyes."},
        {"word": "hair", "translation": "头发", "phonetic": "/heə/", "example": "His hair is black."},
        {"word": "face", "translation": "脸", "phonetic": "/feɪs/", "example": "Wash your face."},
        {"word": "new", "translation": "新的", "phonetic": "/njuː/", "example": "I have a new book."},
        {"word": "who", "translation": "谁", "phonetic": "/huː/", "example": "Who is that boy?"},
        {"word": "he", "translation": "他", "phonetic": "/hiː/", "example": "He is my brother."},
        {"word": "she", "translation": "她", "phonetic": "/ʃiː/", "example": "She is my sister."},
    ],
}

VOCABULARY_GRADE_4_VOL2 = {
    "Unit 1 Spring": [
        {"word": "spring", "translation": "春天", "phonetic": "/sprɪŋ/", "example": "Spring is a beautiful season."},
        {"word": "season", "translation": "季节", "phonetic": "/ˈsiːzən/", "example": "There are four seasons in a year."},
        {"word": "warm", "translation": "温暖的", "phonetic": "/wɔːm/", "example": "The weather is warm in spring."},
        {"word": "sunny", "translation": "晴朗的", "phonetic": "/ˈsʌni/", "example": "It is sunny today."},
        {"word": "windy", "translation": "有风的", "phonetic": "/ˈwɪndi/", "example": "It is windy today."},
        {"word": "flower", "translation": "花", "phonetic": "/ˈflaʊə/", "example": "The flowers are very beautiful."},
        {"word": "grass", "translation": "草", "phonetic": "/ɡrɑːs/", "example": "The grass is green."},
        {"word": "tree", "translation": "树", "phonetic": "/triː/", "example": "There are many trees in the park."},
        {"word": "green", "translation": "绿色的", "phonetic": "/ɡriːn/", "example": "The leaves are green."},
        {"word": "nice", "translation": "好的", "phonetic": "/naɪs/", "example": "Nice to meet you."},
        {"word": "cold", "translation": "冷的", "phonetic": "/kəʊld/", "example": "It is very cold in winter."},
        {"word": "hot", "translation": "热的", "phonetic": "/hɒt/", "example": "It is hot in summer."},
        {"word": "cool", "translation": "凉爽的", "phonetic": "/kuːl/", "example": "The weather is cool in autumn."},
    ],
    "Unit 2 After school": [
        {"word": "after school", "translation": "放学后", "phonetic": "/ˈɑːftə skuːl/", "example": "What do you do after school?"},
        {"word": "play football", "translation": "踢足球", "phonetic": "/pleɪ ˈfʊtbɔːl/", "example": "I play football with my friends."},
        {"word": "go home", "translation": "回家", "phonetic": "/ɡəʊ həʊm/", "example": "I go home at five."},
        {"word": "watch TV", "translation": "看电视", "phonetic": "/wɒtʃ ˌtiːˈviː/", "example": "I like to watch TV."},
        {"word": "read a book", "translation": "读书", "phonetic": "/riːd ə bʊk/", "example": "I like to read a book."},
        {"word": "today", "translation": "今天", "phonetic": "/təˈdeɪ/", "example": "Today is Monday."},
        {"word": "always", "translation": "总是", "phonetic": "/ˈɔːlweɪz/", "example": "I always get up at seven."},
        {"word": "usually", "translation": "通常", "phonetic": "/ˈjuːʒuəli/", "example": "I usually have breakfast at home."},
        {"word": "often", "translation": "经常", "phonetic": "/ˈɒfən/", "example": "I often play with my dog."},
        {"word": "sometimes", "translation": "有时", "phonetic": "/ˈsʌmtaɪmz/", "example": "I sometimes go to the park."},
        {"word": "evening", "translation": "晚上", "phonetic": "/ˈiːvnɪŋ/", "example": "I do my homework in the evening."},
        {"word": "homework", "translation": "家庭作业", "phonetic": "/ˈhəʊmwɜːk/", "example": "I have a lot of homework today."},
        {"word": "clean", "translation": "打扫", "phonetic": "/kliːn/", "example": "I clean my room on Sundays."},
        {"word": "bed", "translation": "床", "phonetic": "/bed/", "example": "I go to bed at nine."},
    ],
    "Unit 3 My day": [
        {"word": "get up", "translation": "起床", "phonetic": "/ɡet ʌp/", "example": "I get up at six every day."},
        {"word": "have breakfast", "translation": "吃早餐", "phonetic": "/hæv ˈbrekfəst/", "example": "I have breakfast at home."},
        {"word": "go to school", "translation": "上学", "phonetic": "/ɡəʊ tuː skuːl/", "example": "I go to school by bus."},
        {"word": "have lunch", "translation": "吃午餐", "phonetic": "/hæv lʌntʃ/", "example": "I have lunch at school."},
        {"word": "have dinner", "translation": "吃晚餐", "phonetic": "/hæv ˈdɪnə/", "example": "I have dinner with my family."},
        {"word": "go to bed", "translation": "上床睡觉", "phonetic": "/ɡəʊ tuː bed/", "example": "I go to bed at nine."},
        {"word": "o'clock", "translation": "……点钟", "phonetic": "/əˈklɒk/", "example": "It is seven o'clock now."},
        {"word": "half", "translation": "半", "phonetic": "/hɑːf/", "example": "It is half past six."},
        {"word": "past", "translation": "过", "phonetic": "/pɑːst/", "example": "It is half past six."},
        {"word": "to", "translation": "差", "phonetic": "/tuː/", "example": "It is a quarter to seven."},
        {"word": "quarter", "translation": "一刻钟", "phonetic": "/ˈkwɔːtə/", "example": "It is a quarter past three."},
        {"word": "night", "translation": "晚上，夜间", "phonetic": "/naɪt/", "example": "Good night, Mom."},
        {"word": "when", "translation": "什么时候", "phonetic": "/wen/", "example": "When do you get up?"},
    ],
    "Unit 4 Drawing in the park": [
        {"word": "drawing", "translation": "绘画", "phonetic": "/ˈdrɔːɪŋ/", "example": "I am interested in drawing."},
        {"word": "park", "translation": "公园", "phonetic": "/pɑːk/", "example": "There is a park near my house."},
        {"word": "tree", "translation": "树", "phonetic": "/triː/", "example": "There are many trees in the park."},
        {"word": "flower", "translation": "花", "phonetic": "/ˈflaʊə/", "example": "The flowers are beautiful."},
        {"word": "lake", "translation": "湖", "phonetic": "/leɪk/", "example": "There is a lake in the park."},
        {"word": "boat", "translation": "小船", "phonetic": "/bəʊt/", "example": "There are many boats on the lake."},
        {"word": "bridge", "translation": "桥", "phonetic": "/brɪdʒ/", "example": "The bridge is over the river."},
        {"word": "hill", "translation": "小山", "phonetic": "/hɪl/", "example": "There is a hill behind the school."},
        {"word": "building", "translation": "建筑物", "phonetic": "/ˈbɪldɪŋ/", "example": "There are many tall buildings in the city."},
        {"word": "high", "translation": "高的", "phonetic": "/haɪ/", "example": "The building is very high."},
        {"word": "low", "translation": "低的", "phonetic": "/ləʊ/", "example": "The plane is flying low."},
        {"word": "draw", "translation": "画", "phonetic": "/drɔː/", "example": "I can draw a cat."},
        {"word": "see", "translation": "看见", "phonetic": "/siː/", "example": "I can see a bird in the tree."},
        {"word": "let's", "translation": "让我们", "phonetic": "/lets/", "example": "Let's go to the park."},
    ],
    "Unit 5 Seasons": [
        {"word": "summer", "translation": "夏天", "phonetic": "/ˈsʌmə/", "example": "It is hot in summer."},
        {"word": "autumn", "translation": "秋天", "phonetic": "/ˈɔːtəm/", "example": "Leaves turn yellow in autumn."},
        {"word": "winter", "translation": "冬天", "phonetic": "/ˈwɪntə/", "example": "It is cold in winter."},
        {"word": "rain", "translation": "雨", "phonetic": "/reɪn/", "example": "It is raining now."},
        {"word": "snow", "translation": "雪", "phonetic": "/snəʊ/", "example": "It is snowing heavily."},
        {"word": "wind", "translation": "风", "phonetic": "/wɪnd/", "example": "The wind is blowing strongly."},
        {"word": "sky", "translation": "天空", "phonetic": "/skaɪ/", "example": "The sky is blue."},
        {"word": "cloud", "translation": "云", "phonetic": "/klaʊd/", "example": "There are many clouds in the sky."},
        {"word": "sun", "translation": "太阳", "phonetic": "/sʌn/", "example": "The sun is shining brightly."},
        {"word": "because", "translation": "因为", "phonetic": "/bɪˈkɒz/", "example": "I like summer because I can swim."},
        {"word": "sleep", "translation": "睡觉", "phonetic": "/sliːp/", "example": "Bears sleep in winter."},
        {"word": "fly", "translation": "飞", "phonetic": "/flaɪ/", "example": "Birds fly south in winter."},
    ],
    "Unit 6 Whose gloves?": [
        {"word": "whose", "translation": "谁的", "phonetic": "/huːz/", "example": "Whose book is this?"},
        {"word": "glove", "translation": "手套（单数）", "phonetic": "/ɡlʌv/", "example": "This is my glove."},
        {"word": "gloves", "translation": "手套（复数）", "phonetic": "/ɡlʌvz/", "example": "These are my gloves."},
        {"word": "mine", "translation": "我的", "phonetic": "/maɪn/", "example": "This book is mine."},
        {"word": "yours", "translation": "你的", "phonetic": "/jɔːz/", "example": "Is this pen yours?"},
        {"word": "his", "translation": "他的", "phonetic": "/hɪz/", "example": "This bag is his."},
        {"word": "hers", "translation": "她的", "phonetic": "/hɜːz/", "example": "This dress is hers."},
        {"word": "ours", "translation": "我们的", "phonetic": "/aʊəz/", "example": "This school is ours."},
        {"word": "theirs", "translation": "他们的", "phonetic": "/ðeəz/", "example": "This classroom is theirs."},
        {"word": "new", "translation": "新的", "phonetic": "/njuː/", "example": "I have a new coat."},
        {"word": "old", "translation": "旧的", "phonetic": "/əʊld/", "example": "This is an old book."},
        {"word": "pair", "translation": "双，对", "phonetic": "/peə/", "example": "I need a new pair of shoes."},
        {"word": "wear", "translation": "穿，戴", "phonetic": "/weə/", "example": "I am wearing a red coat."},
        {"word": "scarf", "translation": "围巾", "phonetic": "/skɑːf/", "example": "My mother knitted this scarf."},
        {"word": "coat", "translation": "外套，大衣", "phonetic": "/kəʊt/", "example": "It is cold outside. Put on your coat."},
    ],
    "Unit 7 On the farm": [
        {"word": "farm", "translation": "农场", "phonetic": "/fɑːm/", "example": "My uncle works on a farm."},
        {"word": "a lot of", "translation": "许多", "phonetic": "/ə ˈlɒt əv/", "example": "There are a lot of animals on the farm."},
        {"word": "apple", "translation": "苹果", "phonetic": "/ˈæpl/", "example": "I like eating apples."},
        {"word": "apple tree", "translation": "苹果树", "phonetic": "/ˈæpl triː/", "example": "There are many apple trees on the farm."},
        {"word": "vegetable", "translation": "蔬菜", "phonetic": "/ˈvedʒtəbl/", "example": "I like eating vegetables."},
        {"word": "tomato", "translation": "番茄，西红柿", "phonetic": "/təˈmɑːtəʊ/", "example": "Tomatoes are red."},
        {"word": "potato", "translation": "土豆", "phonetic": "/pəˈteɪtəʊ/", "example": "Potatoes are my favorite vegetable."},
        {"word": "cow", "translation": "奶牛", "phonetic": "/kaʊ/", "example": "The cow is eating grass."},
        {"word": "pig", "translation": "猪", "phonetic": "/pɪɡ/", "example": "The pig is sleeping."},
        {"word": "chicken", "translation": "鸡", "phonetic": "/ˈtʃɪkɪn/", "example": "The chicken is laying eggs."},
        {"word": "duck", "translation": "鸭子", "phonetic": "/dʌk/", "example": "The ducks are swimming in the pond."},
        {"word": "horse", "translation": "马", "phonetic": "/hɔːs/", "example": "The horse is running in the field."},
        {"word": "there is", "translation": "有（单数）", "phonetic": "/ðeə ɪz/", "example": "There is a cat under the tree."},
        {"word": "there are", "translation": "有（复数）", "phonetic": "/ðeə ɑː/", "example": "There are many apples on the tree."},
        {"word": "grape", "translation": "葡萄", "phonetic": "/ɡreɪp/", "example": "I like grapes very much."},
    ],
    "Unit 8 How are you?": [
        {"word": "how are you", "translation": "你好么？（身体状况）", "phonetic": "/haʊ ɑː juː/", "example": "How are you today?"},
        {"word": "fine", "translation": "好的", "phonetic": "/faɪn/", "example": "I am fine, thank you."},
        {"word": "not bad", "translation": "不错", "phonetic": "/nɒt bæd/", "example": "Not bad, thank you."},
        {"word": "tired", "translation": "疲倦的", "phonetic": "/ˈtaɪəd/", "example": "I am very tired today."},
        {"word": "ill", "translation": "生病的", "phonetic": "/ɪl/", "example": "She is ill today."},
        {"word": "happy", "translation": "开心的", "phonetic": "/ˈhæpi/", "example": "I am very happy today."},
        {"word": "sad", "translation": "伤心的", "phonetic": "/sæd/", "example": "He looks sad today."},
        {"word": "phone", "translation": "电话", "phonetic": "/fəʊn/", "example": "I talk to my friend on the phone."},
        {"word": "late", "translation": "晚的，迟到的", "phonetic": "/leɪt/", "example": "I am late for school."},
        {"word": "see you", "translation": "再见", "phonetic": "/siː juː/", "example": "See you tomorrow."},
        {"word": "goodbye", "translation": "再见", "phonetic": "/ɡʊdˈbaɪ/", "example": "Goodbye, my friend."},
        {"word": "email", "translation": "电子邮件", "phonetic": "/ˈiːmeɪl/", "example": "I send an email to my friend."},
        {"word": "take care", "translation": "保重", "phonetic": "/teɪk keə/", "example": "Take care, Mom."},
        {"word": "well", "translation": "身体好的", "phonetic": "/wel/", "example": "I am well now."},
        {"word": "again", "translation": "再，又", "phonetic": "/əˈɡen/", "example": "See you again."},
    ],
}


def create_yilin_grade4_dictionary():
    """创建译林版四年级英语单词库"""
    
    # 创建词库描述
    description = "译林版四年级英语教材单词库，包含上下两册内容，按单元分类。"

    # 创建上册词库
    dict_vol1 = Dictionary(
        name="译林版四年级英语上册",
        description=description,
        language="英语"
    )
    dict_vol1.save()
    print(f"创建词库: {dict_vol1.name} (ID: {dict_vol1.id})")
    
    # 导入上册单词
    for unit, words in VOCABULARY_GRADE_4_VOL1.items():
        for word_data in words:
            word = Word(
                word=word_data["word"],
                translation=word_data["translation"],
                phonetic=word_data["phonetic"],
                example=word_data["example"],
                definition=unit,
                dictionary_id=dict_vol1.id
            )
            word.save()
    
    print(f"上册单词导入完成，共 {sum(len(words) for words in VOCABULARY_GRADE_4_VOL1.values())} 个单词")
    
    # 创建下册词库
    dict_vol2 = Dictionary(
        name="译林版四年级英语下册",
        description=description,
        language="英语"
    )
    dict_vol2.save()
    print(f"创建词库: {dict_vol2.name} (ID: {dict_vol2.id})")
    
    # 导入下册单词
    for unit, words in VOCABULARY_GRADE_4_VOL2.items():
        for word_data in words:
            word = Word(
                word=word_data["word"],
                translation=word_data["translation"],
                phonetic=word_data["phonetic"],
                example=word_data["example"],
                definition=unit,
                dictionary_id=dict_vol2.id
            )
            word.save()
    
    print(f"下册单词导入完成，共 {sum(len(words) for words in VOCABULARY_GRADE_4_VOL2.values())} 个单词")
    
    # 创建合集词库
    dict_all = Dictionary(
        name="译林版四年级英语全套",
        description="译林版四年级英语全套教材单词库，包含上下册所有内容",
        language="英语"
    )
    dict_all.save()
    print(f"创建词库: {dict_all.name} (ID: {dict_all.id})")
    
    # 合并所有单词
    all_vol1_words = VOCABULARY_GRADE_4_VOL1.copy()
    all_vol1_words.update(VOCABULARY_GRADE_4_VOL2)
    
    for unit, words in all_vol1_words.items():
        for word_data in words:
            word = Word(
                word=word_data["word"],
                translation=word_data["translation"],
                phonetic=word_data["phonetic"],
                example=word_data["example"],
                definition=unit,
                dictionary_id=dict_all.id
            )
            word.save()
    
    total_words = sum(len(words) for words in VOCABULARY_GRADE_4_VOL1.values()) + \
                  sum(len(words) for words in VOCABULARY_GRADE_4_VOL2.values())
    print(f"全套单词导入完成，共 {total_words} 个单词")
    
    print("\n词库创建完成！")
    print(f"1. 译林版四年级英语上册 (ID: {dict_vol1.id}) - {sum(len(w) for w in VOCABULARY_GRADE_4_VOL1.values())} 词")
    print(f"2. 译林版四年级英语下册 (ID: {dict_vol2.id}) - {sum(len(w) for w in VOCABULARY_GRADE_4_VOL2.values())} 词")
    print(f"3. 译林版四年级英语全套 (ID: {dict_all.id}) - {total_words} 词")
    
    return dict_vol1.id, dict_vol2.id, dict_all.id


if __name__ == "__main__":
    create_yilin_grade4_dictionary()
