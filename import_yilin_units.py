import sqlite3

yilin_grade4_units = {
    "Unit 1 我的教室": [
        {"word": "classroom", "translation": "教室", "phonetic": "['klɑːsrʊm]", "definition": "a room where students learn", "example": "This is our classroom."},
        {"word": "window", "translation": "窗户", "phonetic": "['wɪndəʊ]", "definition": "an opening in a wall for light and air", "example": "Open the window, please."},
        {"word": "blackboard", "translation": "黑板", "phonetic": "['blækbɔːd]", "definition": "a dark board for writing on", "example": "The teacher writes on the blackboard."},
        {"word": "light", "translation": "灯", "phonetic": "[laɪt]", "definition": "something that gives light", "example": "Turn on the light."},
        {"word": "picture", "translation": "图画;照片", "phonetic": "['pɪktʃə]", "definition": "a representation of something", "example": "Look at the picture."},
        {"word": "door", "translation": "门", "phonetic": "[dɔː]", "definition": "an opening in a wall", "example": "Close the door."},
        {"word": "teacher's desk", "translation": "讲台", "phonetic": "['tiːtʃəz desk]", "definition": "the desk for the teacher", "example": "The teacher stands at the teacher's desk."},
        {"word": "computer", "translation": "电脑", "phonetic": "[kəm'pjuːtə]", "definition": "an electronic device for computing", "example": "I have a computer."},
        {"word": "fan", "translation": "风扇", "phonetic": "[fæn]", "definition": "a device for moving air", "example": "The fan is on the table."},
        {"word": "wall", "translation": "墙壁", "phonetic": "[wɔːl]", "definition": "the side of a room", "example": "There is a map on the wall."},
        {"word": "schoolbag", "translation": "书包", "phonetic": "['skuːlbæɡ]", "definition": "a bag for carrying books", "example": "My schoolbag is new."},
        {"word": "book", "translation": "书", "phonetic": "[bʊk]", "definition": "pages bound together", "example": "This is an English book."},
        {"word": "desk", "translation": "书桌;课桌", "phonetic": "[desk]", "definition": "a table for writing", "example": "This is my desk."},
        {"word": "chair", "translation": "椅子", "phonetic": "[tʃeə]", "definition": "a seat with a back", "example": "Sit on the chair."},
        {"word": "pencil", "translation": "铅笔", "phonetic": "['pensl]", "definition": "a writing instrument", "example": "This is a pencil."},
        {"word": "pen", "translation": "钢笔", "phonetic": "[pen]", "definition": "a writing instrument with ink", "example": "I have a new pen."},
        {"word": "ruler", "translation": "尺子", "phonetic": "['ruːlə]", "definition": "a tool for measuring", "example": "My ruler is long."},
        {"word": "eraser", "translation": "橡皮", "phonetic": "['reɪzə]", "definition": "a tool for removing pencil marks", "example": "Pass me the eraser."},
        {"word": "crayon", "translation": "蜡笔", "phonetic": "['kreɪən]", "definition": "a drawing tool", "example": "I have many crayons."},
        {"word": "bag", "translation": "包", "phonetic": "[bæɡ]", "definition": "a container for carrying", "example": "Put the book in the bag."},
        {"word": "new", "translation": "新的", "phonetic": "[njuː]", "definition": "not used before", "example": "I have a new friend."},
        {"word": "nice", "translation": "好的;漂亮的", "phonetic": "[naɪs]", "definition": "pleasant", "example": "Nice to meet you."},
        {"word": "have", "translation": "有", "phonetic": "[hæv]", "definition": "to possess", "example": "I have a cat."},
        {"word": "look", "translation": "看;瞧", "phonetic": "[lʊk]", "definition": "to use your eyes", "example": "Look at the blackboard."},
        {"word": "at", "translation": "在", "phonetic": "[æt]", "definition": "preposition of place", "example": "Look at me."},
    ],
    "Unit 2 我的房间": [
        {"word": "room", "translation": "房间", "phonetic": "[ruːm]", "definition": "a part of a building", "example": "This is my room."},
        {"word": "bedroom", "translation": "卧室", "phonetic": "['bedrʊm]", "definition": "a room for sleeping", "example": "I have a big bedroom."},
        {"word": "bathroom", "translation": "卫生间", "phonetic": "['bæθrʊm]", "definition": "a room for washing", "example": "Where is the bathroom?"},
        {"word": "living room", "translation": "客厅", "phonetic": "['lɪvɪŋ ruːm]", "definition": "a room for relaxing", "example": "We watch TV in the living room."},
        {"word": "kitchen", "translation": "厨房", "phonetic": "['kɪtʃɪn]", "definition": "a room for cooking", "example": "My mother is in the kitchen."},
        {"word": "bed", "translation": "床", "phonetic": "[bed]", "definition": "a piece of furniture for sleeping", "example": "I like my bed."},
        {"word": "phone", "translation": "电话", "phonetic": "[fəʊn]", "definition": "a device for talking", "example": "Call me on my phone."},
        {"word": "table", "translation": "桌子", "phonetic": "['teɪbl]", "definition": "a piece of furniture", "example": "There is a table in the room."},
        {"word": "sofa", "translation": "沙发", "phonetic": "['səʊfə]", "definition": "a soft seat", "example": "I am sitting on the sofa."},
        {"word": "shelf", "translation": "书架", "phonetic": "[ʃelf]", "definition": "a board for storing books", "example": "There are many books on the shelf."},
        {"word": "fridge", "translation": "冰箱", "phonetic": "[frɪdʒ]", "definition": "an appliance for keeping food cold", "example": "The fridge is in the kitchen."},
        {"word": "armchair", "translation": "扶手椅", "phonetic": "['ɑːmtʃeə]", "definition": "a comfortable chair with arms", "example": "The armchair is soft."},
        {"word": "mirror", "translation": "镜子", "phonetic": "['mɪrə]", "definition": "a glass for seeing yourself", "example": "Look at the mirror."},
        {"word": "closet", "translation": "衣柜", "phonetic": "['klɒzɪt]", "definition": "a cupboard for clothes", "example": "Open the closet."},
        {"word": "end table", "translation": "茶几", "phonetic": "['end teɪbl]", "definition": "a small table", "example": "The lamp is on the end table."},
        {"word": "TV", "translation": "电视", "phonetic": "['tiːviː]", "definition": "television", "example": "Watch TV on Sundays."},
        {"word": "clock", "translation": "时钟", "phonetic": "[klɒk]", "definition": "a device for showing time", "example": "Look at the clock."},
        {"word": "lamp", "translation": "台灯", "phonetic": "[læmp]", "definition": "a light on a table", "example": "Turn on the lamp."},
        {"word": "toy", "translation": "玩具", "phonetic": "[tɔɪ]", "definition": "something to play with", "example": "I have many toys."},
        {"word": "key", "translation": "钥匙", "phonetic": "[kiː]", "definition": "something for opening locks", "example": "This is the key."},
        {"word": "near", "translation": "在……旁边", "phonetic": "[nɪə]", "definition": "close to", "example": "The bed is near the window."},
        {"word": "behind", "translation": "在……后面", "phonetic": "[bɪ'haɪnd]", "definition": "at the back of", "example": "The cat is behind the door."},
        {"word": "in front of", "translation": "在……前面", "phonetic": "[ɪn frʌnt ɒv]", "definition": "before", "example": "The tree is in front of the house."},
        {"word": "between", "translation": "在……中间", "phonetic": "[bɪ'twiːn]", "definition": "in the middle of", "example": "The chair is between two tables."},
        {"word": "beside", "translation": "在……旁边", "phonetic": "[bɪ'saɪd]", "definition": "next to", "example": "Sit beside me."},
    ],
    "Unit 3 我的家人": [
        {"word": "family", "translation": "家庭", "phonetic": "['fæmɪlɪ]", "definition": "a group of relatives", "example": "I have a happy family."},
        {"word": "father", "translation": "父亲;爸爸", "phonetic": "['fɑːðə]", "definition": "a male parent", "example": "My father is a doctor."},
        {"word": "mother", "translation": "母亲;妈妈", "phonetic": "['mʌðə]", "definition": "a female parent", "example": "My mother is a teacher."},
        {"word": "dad", "translation": "爸爸", "phonetic": "[dæd]", "definition": "informal word for father", "example": "I love my dad."},
        {"word": "mum", "translation": "妈妈", "phonetic": "[mʌm]", "definition": "informal word for mother", "example": "My mum cooks well."},
        {"word": "parent", "translation": "父亲;母亲", "phonetic": "['peərənt]", "definition": "a mother or father", "example": "My parents are at home."},
        {"word": "brother", "translation": "兄弟", "phonetic": "['brʌðə]", "definition": "a male sibling", "example": "I have a brother."},
        {"word": "sister", "translation": "姐妹", "phonetic": "['sɪstə]", "definition": "a female sibling", "example": "My sister is tall."},
        {"word": "grandfather", "translation": "祖父;外祖父", "phonetic": "['ɡrændˌfɑːðə]", "definition": "father of a parent", "example": "My grandfather is old."},
        {"word": "grandmother", "translation": "祖母;外祖母", "phonetic": "['ɡrændˌmʌðə]", "definition": "mother of a parent", "example": "My grandmother lives with us."},
        {"word": "grandpa", "translation": "爷爷;外公", "phonetic": "['ɡrænpɑː]", "definition": "informal for grandfather", "example": "I love my grandpa."},
        {"word": "grandma", "translation": "奶奶;外婆", "phonetic": "['ɡrænmɑː]", "definition": "informal for grandmother", "example": "My grandma tells me stories."},
        {"word": "uncle", "translation": "叔叔;舅舅", "phonetic": "['ʌŋkl]", "definition": "brother of a parent", "example": "My uncle is funny."},
        {"word": "aunt", "translation": "阿姨;姑妈", "phonetic": "[ɑːnt]", "definition": "sister of a parent", "example": "My aunt lives in Beijing."},
        {"word": "cousin", "translation": "堂(表)兄弟姐妹", "phonetic": "['kʌzn]", "definition": "child of uncle or aunt", "example": "My cousin is my friend."},
        {"word": "friend", "translation": "朋友", "phonetic": "[frend]", "definition": "a person you like", "example": "She is my good friend."},
        {"word": "who", "translation": "谁", "phonetic": "[huː]", "definition": "what person", "example": "Who is he?"},
        {"word": "he", "translation": "他", "phonetic": "[hiː]", "definition": "male pronoun", "example": "He is my brother."},
        {"word": "she", "translation": "她", "phonetic": "[ʃiː]", "definition": "female pronoun", "example": "She is my sister."},
        {"word": "his", "translation": "他的", "phonetic": "[hɪz]", "definition": "belonging to him", "example": "This is his book."},
        {"word": "her", "translation": "她的", "phonetic": "[hɜː]", "definition": "belonging to her", "example": "That is her bag."},
        {"word": "man", "translation": "男人", "phonetic": "[mæn]", "definition": "adult male", "example": "The man is tall."},
        {"word": "woman", "translation": "女人", "phonetic": "['wʊmən]", "definition": "adult female", "example": "The woman is my mother."},
        {"word": "boy", "translation": "男孩", "phonetic": "[bɔɪ]", "definition": "young male", "example": "The boy is my brother."},
        {"word": "girl", "translation": "女孩", "phonetic": "[ɡɜːl]", "definition": "young female", "example": "The girl is my sister."},
    ],
    "Unit 4 我的职业": [
        {"word": "job", "translation": "工作", "phonetic": "[dʒɒb]", "definition": "a type of work", "example": "What is your job?"},
        {"word": "doctor", "translation": "医生", "phonetic": "['dɒktə]", "definition": "a person who treats illness", "example": "My mother is a doctor."},
        {"word": "nurse", "translation": "护士", "phonetic": "[nɜːs]", "definition": "a person who helps doctors", "example": "The nurse is kind."},
        {"word": "driver", "translation": "司机", "phonetic": "['draɪvə]", "definition": "a person who drives", "example": "My father is a driver."},
        {"word": "cook", "translation": "厨师", "phonetic": "[kʊk]", "definition": "a person who makes food", "example": "My mother is a good cook."},
        {"word": "farmer", "translation": "农民", "phonetic": "['fɑːmə]", "definition": "a person who works on a farm", "example": "The farmer is working."},
        {"word": "policeman", "translation": "警察", "phonetic": "[pə'liːsmən]", "definition": "a law enforcement officer", "example": "The policeman is tall."},
        {"word": "policewoman", "translation": "女警察", "phonetic": "[pə'liːsˌwʊmən]", "definition": "female police officer", "example": "The policewoman helps people."},
        {"word": "teacher", "translation": "教师", "phonetic": "['tiːtʃə]", "definition": "a person who teaches", "example": "My teacher is kind."},
        {"word": "student", "translation": "学生", "phonetic": "['stjuːdənt]", "definition": "a person who studies", "example": "I am a student."},
        {"word": "worker", "translation": "工人", "phonetic": "['wɜːkə]", "definition": "a person who works", "example": "The worker is busy."},
        {"word": "singer", "translation": "歌手", "phonetic": "['sɪŋə]", "definition": "a person who sings", "example": "She is a famous singer."},
        {"word": "dancer", "translation": "舞蹈家", "phonetic": "['dɑːnsə]", "definition": "a person who dances", "example": "The dancer is very graceful."},
        {"word": "artist", "translation": "艺术家", "phonetic": "['ɑːtɪst]", "definition": "a person who creates art", "example": "My uncle is an artist."},
        {"word": "engineer", "translation": "工程师", "phonetic": "[,endʒɪ'nɪə]", "definition": "a person who designs things", "example": "My father is an engineer."},
        {"word": "accountant", "translation": "会计", "phonetic": "[ə'kaʊntənt]", "definition": "a person who handles money", "example": "She is an accountant."},
        {"word": "secretary", "translation": "秘书", "phonetic": "['sekrɪtərɪ]", "definition": "an office worker", "example": "He works as a secretary."},
        {"word": "manager", "translation": "经理", "phonetic": "['mænɪdʒə]", "definition": "a person in charge", "example": "The manager is in the office."},
        {"word": "waiter", "translation": "男服务员", "phonetic": "['weɪtə]", "definition": "a man who serves food", "example": "The waiter is helpful."},
        {"word": "waitress", "translation": "女服务员", "phonetic": "['weɪtrɪs]", "definition": "a woman who serves food", "example": "The waitress is friendly."},
        {"word": "what", "translation": "什么", "phonetic": "[wɒt]", "definition": "asking for information", "example": "What is your name?"},
        {"word": "want", "translation": "想要", "phonetic": "[wɒnt]", "definition": "to desire", "example": "I want an apple."},
        {"word": "play", "translation": "玩;打(球)", "phonetic": "[pleɪ]", "definition": "to have fun", "example": "Let's play football."},
        {"word": "help", "translation": "帮助", "phonetic": "[help]", "definition": "to assist", "example": "Can you help me?"},
        {"word": "go", "translation": "去", "phonetic": "[ɡəʊ]", "definition": "to move to a place", "example": "Let's go home."},
    ],
    "Unit 5 我的食物": [
        {"word": "hungry", "translation": "饥饿的", "phonetic": "['hʌŋɡrɪ]", "definition": "feeling a need for food", "example": "I am hungry."},
        {"word": "bread", "translation": "面包", "phonetic": "[bred]", "definition": "food made from flour", "example": "I like bread."},
        {"word": "egg", "translation": "鸡蛋", "phonetic": "[eɡ]", "definition": "food from chickens", "example": "I want an egg."},
        {"word": "milk", "translation": "牛奶", "phonetic": "[mɪlk]", "definition": "a white drink", "example": "I drink milk every day."},
        {"word": "water", "translation": "水", "phonetic": "['wɔːtə]", "definition": "a clear drink", "example": "I need some water."},
        {"word": "rice", "translation": "米饭", "phonetic": "[raɪs]", "definition": "food from Asia", "example": "I eat rice for lunch."},
        {"word": "noodles", "translation": "面条", "phonetic": "['nuːdlz]", "definition": "long thin food", "example": "I like noodles."},
        {"word": "fish", "translation": "鱼", "phonetic": "[fɪʃ]", "definition": "a sea animal", "example": "I like to eat fish."},
        {"word": "chicken", "translation": "鸡肉", "phonetic": "['tʃɪkɪn]", "definition": "meat from a bird", "example": "I like chicken."},
        {"word": "meat", "translation": "肉", "phonetic": "[miːt]", "definition": "food from animals", "example": "I eat meat every day."},
        {"word": "vegetable", "translation": "蔬菜", "phonetic": "['vedʒtəbl]", "definition": "a plant food", "example": "I eat vegetables."},
        {"word": "fruit", "translation": "水果", "phonetic": "[fruːt]", "definition": "sweet plant food", "example": "I like fruit."},
        {"word": "apple", "translation": "苹果", "phonetic": "['æpl]", "definition": "a red or green fruit", "example": "An apple a day."},
        {"word": "banana", "translation": "香蕉", "phonetic": "[bə'nɑːnə]", "definition": "a yellow fruit", "example": "I like bananas."},
        {"word": "orange", "translation": "橙子", "phonetic": "['ɒrɪndʒ]", "definition": "a round orange fruit", "example": "I want an orange."},
        {"word": "cake", "translation": "蛋糕", "phonetic": "[keɪk]", "definition": "sweet baked food", "example": "It's my birthday cake."},
        {"word": "juice", "translation": "果汁", "phonetic": "[dʒuːs]", "definition": "drink from fruit", "example": "I like orange juice."},
        {"word": "coffee", "translation": "咖啡", "phonetic": "['kɒfɪ]", "definition": "a hot drink", "example": "My father drinks coffee."},
        {"word": "tea", "translation": "茶", "phonetic": "[tiː]", "definition": "a hot drink", "example": "I drink tea."},
        {"word": "soup", "translation": "汤", "phonetic": "[suːp]", "definition": "liquid food", "example": "I like vegetable soup."},
        {"word": "sandwich", "translation": "三明治", "phonetic": "['sænwɪdʒ]", "definition": "food with bread", "example": "I have a sandwich."},
        {"word": "hamburger", "translation": "汉堡包", "phonetic": "['hæmbɜːɡə]", "definition": "a type of sandwich", "example": "I like hamburgers."},
        {"word": "pizza", "translation": "披萨", "phonetic": "['piːtsə]", "definition": "Italian food with cheese", "example": "Let's eat pizza."},
        {"word": "ice cream", "translation": "冰淇淋", "phonetic": "[aɪs kriːm]", "definition": "frozen sweet food", "example": "I like ice cream."},
        {"word": "sweet", "translation": "甜的", "phonetic": "[swiːt]", "definition": "tasting like sugar", "example": "The cake is sweet."},
    ],
    "Unit 6 我的动物": [
        {"word": "animal", "translation": "动物", "phonetic": "['ænɪml]", "definition": "a living creature", "example": "I love animals."},
        {"word": "cat", "translation": "猫", "phonetic": "[kæt]", "definition": "a small pet", "example": "I have a cat."},
        {"word": "dog", "translation": "狗", "phonetic": "[dɒɡ]", "definition": "a loyal pet", "example": "Dogs are cute."},
        {"word": "rabbit", "translation": "兔子", "phonetic": "['ræbɪt]", "definition": "a small animal with long ears", "example": "The rabbit is white."},
        {"word": "hamster", "translation": "仓鼠", "phonetic": "['hæmstə]", "definition": "a small rodent", "example": "I keep a hamster."},
        {"word": "mouse", "translation": "老鼠", "phonetic": "[maʊs]", "definition": "a small rodent", "example": "The mouse is small."},
        {"word": "bird", "translation": "鸟", "phonetic": "[bɜːd]", "definition": "a flying animal", "example": "The bird can fly."},
        {"word": "chicken", "translation": "鸡", "phonetic": "['tʃɪkɪn]", "definition": "a farm bird", "example": "The chicken lays eggs."},
        {"word": "duck", "translation": "鸭子", "phonetic": "[dʌk]", "definition": "a water bird", "example": "The duck is swimming."},
        {"word": "pig", "translation": "猪", "phonetic": "[pɪɡ]", "definition": "a farm animal", "example": "The pig is fat."},
        {"word": "cow", "translation": "牛", "phonetic": "[kaʊ]", "definition": "a farm animal", "example": "The cow gives milk."},
        {"word": "horse", "translation": "马", "phonetic": "[hɔːs]", "definition": "a large animal", "example": "The horse is running."},
        {"word": "sheep", "translation": "绵羊", "phonetic": "[ʃiːp]", "definition": "a farm animal with wool", "example": "The sheep has wool."},
        {"word": "goat", "translation": "山羊", "phonetic": "[ɡəʊt]", "definition": "a horned animal", "example": "The goat is climbing."},
        {"word": "elephant", "translation": "大象", "phonetic": "['elɪfənt]", "definition": "a very large animal", "example": "The elephant has a long nose."},
        {"word": "lion", "translation": "狮子", "phonetic": "['laɪən]", "definition": "a big cat", "example": "The lion is the king."},
        {"word": "tiger", "translation": "老虎", "phonetic": "['taɪɡə]", "definition": "a big wild cat", "example": "The tiger is fierce."},
        {"word": "monkey", "translation": "猴子", "phonetic": "['mʌŋkɪ]", "definition": "a clever animal", "example": "The monkey is funny."},
        {"word": "panda", "translation": "熊猫", "phonetic": "['pændə]", "definition": "a black and white bear", "example": "Pandas are cute."},
        {"word": "zebra", "translation": "斑马", "phonetic": "['ziːbrə]", "definition": "a striped animal", "example": "The zebra has stripes."},
        {"word": "giraffe", "translation": "长颈鹿", "phonetic": "[dʒɪ'rɑːf]", "definition": "a tall animal with a long neck", "example": "The giraffe is tall."},
        {"word": "snake", "translation": "蛇", "phonetic": "[sneɪk]", "definition": "a long reptile", "example": "The snake can crawl."},
        {"word": "fish", "translation": "鱼", "phonetic": "[fɪʃ]", "definition": "a water animal", "example": "The fish is swimming."},
        {"word": "small", "translation": "小的", "phonetic": "[smɔːl]", "definition": "not big", "example": "The mouse is small."},
        {"word": "big", "translation": "大的", "phonetic": "[bɪɡ]", "definition": "large", "example": "The elephant is big."},
    ],
    "Unit 7 我的衣物": [
        {"word": "clothes", "translation": "衣服", "phonetic": "[kləʊðz]", "definition": "things you wear", "example": "I need new clothes."},
        {"word": "jacket", "translation": "夹克衫", "phonetic": "['dʒækɪt]", "definition": "a short coat", "example": "I have a blue jacket."},
        {"word": "coat", "translation": "外套;大衣", "phonetic": "[kəʊt]", "definition": "a warm outer garment", "example": "Put on your coat."},
        {"word": "shirt", "translation": "衬衫", "phonetic": "[ʃɜːt]", "definition": "a top garment", "example": "I wear a white shirt."},
        {"word": "T-shirt", "translation": "T恤衫", "phonetic": "['tiːʃɜːt]", "definition": "a casual top", "example": "I like this T-shirt."},
        {"word": "dress", "translation": "连衣裙", "phonetic": "[dres]", "definition": "a garment for girls", "example": "She wears a red dress."},
        {"word": "skirt", "translation": "裙子", "phonetic": "[skɜːt]", "definition": "a garment for girls", "example": "My skirt is blue."},
        {"word": "jeans", "translation": "牛仔裤", "phonetic": "[dʒiːnz]", "definition": "blue trousers", "example": "I am wearing jeans."},
        {"word": "trousers", "translation": "裤子", "phonetic": "['traʊzəz]", "definition": "clothing for legs", "example": "My trousers are black."},
        {"word": "shorts", "translation": "短裤", "phonetic": "[ʃɔːts]", "definition": "short trousers", "example": "I wear shorts in summer."},
        {"word": "sweater", "translation": "毛衣", "phonetic": "['swetə]", "definition": "a warm top", "example": "The sweater is warm."},
        {"word": "socks", "translation": "袜子", "phonetic": "[sɒks]", "definition": "footwear", "example": "I need new socks."},
        {"word": "shoes", "translation": "鞋子", "phonetic": "[ʃuːz]", "definition": "footwear", "example": "My shoes are new."},
        {"word": "boots", "translation": "靴子", "phonetic": "[buːts]", "definition": "high shoes", "example": "I have brown boots."},
        {"word": "hat", "translation": "帽子", "phonetic": "[hæt]", "definition": "head covering", "example": "I wear a hat."},
        {"word": "cap", "translation": "帽子", "phonetic": "[kæp]", "definition": "a soft hat", "example": "My baseball cap."},
        {"word": "scarf", "translation": "围巾", "phonetic": "[skɑːf]", "definition": "neck covering", "example": "The scarf is warm."},
        {"word": "gloves", "translation": "手套", "phonetic": "[ɡlʌvz]", "definition": "hand coverings", "example": "My gloves are red."},
        {"word": "umbrella", "translation": "雨伞", "phonetic": "[ʌm'brelə]", "definition": "protection from rain", "example": "Take an umbrella."},
        {"word": "new", "translation": "新的", "phonetic": "[njuː]", "definition": "not used before", "example": "My new dress."},
        {"word": "old", "translation": "旧的;老的", "phonetic": "[əʊld]", "definition": "not new", "example": "This is an old book."},
        {"word": "colour", "translation": "颜色", "phonetic": "['kʌlə]", "definition": "a shade", "example": "What colour is it?"},
        {"word": "whose", "translation": "谁的", "phonetic": "[huːz]", "definition": "belonging to whom", "example": "Whose coat is this?"},
        {"word": "try", "translation": "试穿", "phonetic": "[traɪ]", "definition": "to test", "example": "Can I try it on?"},
    ],
    "Unit 8 我的日常": [
        {"word": "time", "translation": "时间", "phonetic": "[taɪm]", "definition": "the passing of hours", "example": "What time is it?"},
        {"word": "o'clock", "translation": "……点钟", "phonetic": "[ə'klɒk]", "definition": "showing hours", "example": "It is seven o'clock."},
        {"word": "morning", "translation": "早晨;上午", "phonetic": "['mɔːnɪŋ]", "definition": "early day", "example": "Good morning!"},
        {"word": "afternoon", "translation": "下午", "phonetic": "['ɑːftə'nuːn]", "definition": "middle of the day", "example": "Good afternoon!"},
        {"word": "evening", "translation": "傍晚;晚上", "phonetic": "['iːvnɪŋ]", "definition": "end of the day", "example": "Good evening!"},
        {"word": "night", "translation": "夜晚", "phonetic": "[naɪt]", "definition": "dark time", "example": "Good night!"},
        {"word": "today", "translation": "今天", "phonetic": "[tə'deɪ]", "definition": "this day", "example": "Today is Monday."},
        {"word": "week", "translation": "周;星期", "phonetic": "[wiːk]", "definition": "seven days", "example": "I play football every week."},
        {"word": "Monday", "translation": "星期一", "phonetic": "['mʌndeɪ]", "definition": "first day of the week", "example": "I go to school on Monday."},
        {"word": "Tuesday", "translation": "星期二", "phonetic": "['tjuːzdeɪ]", "definition": "second day", "example": "I have PE on Tuesday."},
        {"word": "Wednesday", "translation": "星期三", "phonetic": "['wenzdeɪ]", "definition": "third day", "example": "Wednesday is busy."},
        {"word": "Thursday", "translation": "星期四", "phonetic": "['θɜːzdeɪ]", "definition": "fourth day", "example": "I like Thursday."},
        {"word": "Friday", "translation": "星期五", "phonetic": "['fraɪdeɪ]", "definition": "fifth day", "example": "Friday is fun."},
        {"word": "Saturday", "translation": "星期六", "phonetic": "['sætədeɪ]", "definition": "sixth day", "example": "I play games on Saturday."},
        {"word": "Sunday", "translation": "星期日", "phonetic": "['sʌndeɪ]", "definition": "seventh day", "example": "I rest on Sunday."},
        {"word": "weekend", "translation": "周末", "phonetic": "['wiːk'end]", "definition": "Saturday and Sunday", "example": "I play on the weekend."},
        {"word": "get up", "translation": "起床", "phonetic": "[ɡet ʌp]", "definition": "to rise from bed", "example": "I get up at seven."},
        {"word": "have breakfast", "translation": "吃早餐", "phonetic": "[hæv 'brekfəst]", "definition": "to eat morning meal", "example": "I have breakfast at home."},
        {"word": "go to school", "translation": "上学", "phonetic": "[ɡəʊ tə skuːl]", "definition": "to leave for school", "example": "I go to school by bus."},
        {"word": "have lunch", "translation": "吃午餐", "phonetic": "[hæv lʌntʃ]", "definition": "to eat noon meal", "example": "I have lunch at school."},
        {"word": "go home", "translation": "回家", "phonetic": "[ɡəʊ həʊm]", "definition": "to return home", "example": "I go home at five."},
        {"word": "have dinner", "translation": "吃晚餐", "phonetic": "['hæv 'dɪnə]", "definition": "to eat evening meal", "example": "I have dinner with family."},
        {"word": "go to bed", "translation": "睡觉", "phonetic": "[ɡəʊ tə bed]", "definition": "to sleep", "example": "I go to bed at nine."},
        {"word": "when", "translation": "什么时候", "phonetic": "[wen]", "definition": "at what time", "example": "When do you get up?"},
        {"word": "usually", "translation": "通常", "phonetic": "['juːʒuəlɪ]", "definition": "normally", "example": "I usually get up at seven."},
    ],
}

def import_yilin_vocabulary():
    conn = sqlite3.connect('wordmaster.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM dictionaries WHERE name = ?', ('四年级',))
    result = cursor.fetchone()
    
    if result:
        old_dict_id = result[0]
        cursor.execute('DELETE FROM words WHERE dictionary_id = ?', (old_dict_id,))
        cursor.execute('DELETE FROM dictionaries WHERE id = ?', (old_dict_id,))
        print(f"已删除旧词库 (ID: {old_dict_id})")
    
    for unit_name, words in yilin_grade4_units.items():
        cursor.execute('''
            INSERT INTO dictionaries (name, description, language, word_count)
            VALUES (?, ?, ?, ?)
        ''', (unit_name, '译林版小学四年级英语词汇', 'English', len(words)))
        
        dict_id = cursor.lastrowid
        print(f"创建词库: {unit_name} (ID: {dict_id}), 单词数: {len(words)}")
        
        for word in words:
            cursor.execute('''
                INSERT INTO words (word, translation, phonetic, definition, example, dictionary_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (word['word'], word['translation'], word['phonetic'], 
                  word['definition'], word['example'], dict_id))
    
    conn.commit()
    
    total_words = sum(len(words) for words in yilin_grade4_units.values())
    total_units = len(yilin_grade4_units)
    print(f"\n成功创建 {total_units} 个单元词库, 共 {total_words} 个单词!")
    
    cursor.execute('SELECT id, name, word_count FROM dictionaries ORDER BY id')
    dictionaries = cursor.fetchall()
    print("\n当前词库列表:")
    for d in dictionaries:
        print(f"  ID:{d[0]} 名称:{d[1]} 单词数:{d[2]}")
    
    conn.close()

if __name__ == '__main__':
    import_yilin_vocabulary()
