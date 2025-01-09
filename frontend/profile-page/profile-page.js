async function getResponce(content, orders_data){
    let response = await fetch('https://jsonplaceholder.typicode.com/photos')
    var content = await response.json()

    await console.log(content[content[1].id])

    const orders = document.querySelector('.orders')
    const skills = document.querySelector('.skills')
    const works = document.querySelector('.works')
    function works_func(){ // генерация карточек в раздел мои работы
        for(let i = 0; i < 10; i++){
          const card = document.createElement('div') //КАРТОЧКА
          card.classList.add('card')
          const img_in_card = document.createElement('img') //КАРТИНКА
          img_in_card.classList.add('img_in_card')
          img_in_card.src = "./card.png"
          const card_name = document.createElement('div') //НАЗВАНИЕ
          card_name.innerHTML = content[i].title
          card_name.classList.add('card_name')
          const card_more = document.createElement('button') //ПОДРОБНЕЕ
          card_more.classList.add('card_more') 
          card_more.innerHTML = 'подробнее...'
          card_more.addEventListener("click", () => {
            console.log("benger");
          }) // ?!!!!
          
          
          card.append(img_in_card)
          card.append(card_name)
          card.append(card_more)
          works.append(card)
        }
    }
    works_func()

    function orders_func(){ // генерация карточек в раздел заказы (отображается только у самого кондитера)
      for(let i = 0; i < orders_data.length; i++){
        const order = document.createElement('div') 
        order.classList.add('order')
        const date = document.createElement('div') 
        date.innerHTML = `(i) дедлайн: ${orders_data[i].date}`
        date.classList.add('date')
        const inf_order = document.createElement('div') 
        inf_order.classList.add('inf_order')
        for(let k = 0; k < orders_data[i].inf.length; k++){
          const cake_param = document.createElement("div")
          cake_param.classList.add("cake_param")
          cake_param.innerHTML = `${orders_data[i].inf[k][0]}: ${orders_data[i].inf[k][1]}`
          inf_order.append(cake_param)
        }
        const bottom_btns = document.createElement('div') 
        bottom_btns.classList.add('bottom_btns') 
        const chat = document.createElement("button")
        chat.classList.add('chat')
        chat.innerHTML = "чат"
        bottom_btns.append(chat)
        const cost = document.createElement("div")
        cost.classList.add("cost")
        cost.innerHTML += `${orders_data[i].cost} P`
        bottom_btns.append(cost)
        const ord_cond = document.createElement("div")
        ord_cond.classList.add("ord_cond")
        order.append(date)
        ord_cond.append(inf_order)
        ord_cond.append(bottom_btns)
        order.append(ord_cond)
        orders.append(order)
      }
      orders.classList.add("render")
    }

    function active_navbar(){ //включает видимость или генерацию карточек
      const arr = document.querySelectorAll(".bt")
      for(let i = 0; i < arr.length; i++){
        arr[i].addEventListener("click", () => {
          arr[i].classList.add("active")
          for(let j = 0; j < arr.length; j++){
            if(j != i){
              arr[j].classList.remove("active")
            }
          }
          if (i == 0){ //works
            orders.classList.add('hide')
            skills.classList.add('hide')
            works.classList.remove('hide') 
          }
          if (i == 1){ //ord добавить проверку рендерилось ли оно уже
            if (orders.classList.contains("render")){
              works.classList.add('hide')
              skills.classList.add('hide')
              orders.classList.remove('hide') 
            }
            else {
              orders_func()
              works.classList.add('hide')
              skills.classList.add('hide')
              orders.classList.remove('hide') 
              console.log("ORDERS")
            }
          }
          if (i == 2){ //skills
            if (skills.classList.contains("render")){
              works.classList.add('hide')
              skills.classList.remove('hide')
              orders.classList.add('hide')
            }
            else {
              
              works.classList.add('hide')
              skills.classList.remove('hide')
              orders.classList.add('hide')
            }
          }
        })
      }
    
    }
    active_navbar()
}


async function conditer(cond) {
  social_bt = document.querySelector(".dropdown-content") //выпадаюзая менюшка с соцсетями
  document.querySelector(".username").innerHTML = cond[0].name //0->id
  document.querySelector(".descript").innerHTML = cond[0].descript
  document.querySelector(".ava").src = cond[0].ava

  function soc_med(){ 
    console.log(cond[0].social_media.length) //object hasn't param lenght 
    for(let i = 0; i < cond[0].social_media.length; i++){
      const soc_url = document.createElement("div")
      soc_url.classList.add("soc_url") //-?-
      const p = document.createElement("p")
      p.innerHTML = `${cond[0].social_media[i][0]}: `
      soc_url.append(p)

      const field = document.createElement("div")
      field.classList.add("field")
      soc_url.append(field)
      
      const data_sm = document.createElement("div")
      data_sm.id = "data_sm"
      data_sm.innerHTML = cond[0].social_media[i][1]
      field.append(data_sm)
      const img = document.createElement("img")
      img.classList.add("copy")
      img.src = "./copy.png"
      field.append(img)

      social_bt.append(soc_url)
      console.log(cond[0].social_media[i][0])
    }
  }
  soc_med()
  function skills() { //глобально надо бы, чтоюы можно было как-то запустить из первой функции
    const for_i = document.querySelector(".for_i")
    const block_i_cakes = document.createElement("div")
    block_i_cakes.classList.add("i")
    const arr_cakes = document.createElement("div")
    arr_cakes.classList.add("arr")
    block_i_cakes.innerHTML = "Виды тортов"
    for(let k = 0; k < cond[0].skills.cakes.length; k++){
      console.log(cond[0].skills.cakes)
      const opt = document.createElement('div')
      opt.classList.add("opt")
      opt.innerHTML = cond[0].skills.cakes[k]
      arr_cakes.append(opt)
    }
    
    const plus = document.createElement("button")
    plus.classList.add("plus")
    plus.classList.add("opt")

    plus.innerHTML = "+ добавить"
    arr_cakes.append(plus)
    block_i_cakes.append(arr_cakes)

    for_i.append(block_i_cakes)
  } //спросить как сделать глобальнее
  //ыа, чет я не понимаю как это блин делать вообще
  skills()
}


cont = [ //константы с тортиками
    {
      "id": 1,
      "title": "accusamus beatae ad facilis cum similique qui sunt",
      "url": "https://via.placeholder.com/600/92c952"
      
    },
    {
      "albumId": 1,
      "id": 2,
      "title": "reprehenderit est deserunt velit ipsam",
      "url": "https://via.placeholder.com/600/771796",
      "thumbnailUrl": "https://via.placeholder.com/150/771796"
    },
]

cond = [ //константы кондитера
  {
    "id": 10929878,
    "name": "Name Surname",
    "descript": "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Reprehenderit quis alias doloribus ipsam illum! Necessitatibus!", 
    "ava": "./cat.png", //?????
    "social_media": 
        [
          ["tik_tok", "lala_lisa"],
          ["inst", "@lalalisa"]
        ],
    "skills": {
      "cakes": [
        "мусс",
        "блиннный",
        "шоколадный коржик"
      ],
      "decor": [
        "шоколадные фигурки",
        "велюр",
        "вафельная бумага"
      ],
      "feeling": [
        "киви",
        "мята",
        "маскарпоне"
      ]
      
    }

  }
]

orders_data = [
  {
    "cost": "1000",
    "date": "13.01",
    "inf": [
      ["тип торта", "муссовый"],
      ["начинка", "вишня"],
      ["декор", "шоколадные фигурки"]

      ]
    
  },
  {
    "cost": "13000",
    "date": "14.01",
    "inf": [
      ["тип торта", "блинный"],
      ["крем", "сметанный"],
      ["добавки в крем", "смородина"],
      ["декор", "цветы из крема"]

      ]
    
  },
  {
    "cost": "13000",
    "date": "14.01",
    "inf": [
      ["тип торта", "блинный"],
      ["крем", "сметанный"],
      ["добавки в крем", "смородина"],
      ["декор", "цветы из крема"]

      ]
    
  },
  {
    "cost": "13000",
    "date": "14.01",
    "inf": [
      ["тип торта", "блинный"],
      ["крем", "сметанный"],
      ["добавки в крем", "смородина"],
      ["декор", "цветы из крема"]

      ]
    
  }
]
getResponce(cont, orders_data)
conditer(cond)
