async function getResponce(content){
    // let response = await fetch('https://jsonplaceholder.typicode.com/photos')
    // var content = await response.json()

    // await console.log(content[content[1].id])

    const orders = document.querySelector('.orders')
    const skills = document.querySelector('.skills')
    const works = document.querySelector('.works')
    function works_func(){ // генерация карточек в раздел мои работы
        for(let i = 0; i < 2; i++){
          console.log(content[i].id)
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
          
          card.append(img_in_card)
          card.append(card_name)
          card.append(card_more)
          works.append(card)
        }
    }
    works_func()

    //при первом нажатии отработать, а потом просто hide 
    function orders_func(){ // генерация карточек в раздел заказы (отображается только у самого кондитера)
      for(let i = 0; i < 2; i++){
        const card = document.createElement('div') //КАРТОЧКА
        card.classList.add('card')
        const img_in_card = document.createElement('img') //КАРТИНКА
        img_in_card.classList.add('img_in_card')
        img_in_card.src = "./otter.jpg"
        const card_name = document.createElement('div') //НАЗВАНИЕ
        card_name.innerHTML = content[i].title
        card_name.classList.add('card_name')
        const card_more = document.createElement('button') //ПОДРОБНЕЕ
        card_more.classList.add('card_more') 
        card_more.innerHTML = 'подробнее...'
        card.append(img_in_card)
        card.append(card_name)
        card.append(card_more)
        orders.append(card)
      }
      orders.classList.add("render")
    }

    function skills_func(){ // генерация карточек в раздел навыки 
      for(let i = 0; i < 2; i++){
        const card = document.createElement('div') //КАРТОЧКА
        card.classList.add('card')
        const img_in_card = document.createElement('img') //КАРТИНКА
        img_in_card.classList.add('img_in_card')
        img_in_card.src = "./otter.jpg"
        const card_name = document.createElement('div') //НАЗВАНИЕ
        card_name.innerHTML = content[i].title
        card_name.classList.add('card_name')
        const card_more = document.createElement('button') //ПОДРОБНЕЕ
        card_more.classList.add('card_more') 
        card_more.innerHTML = 'подробнее...'
        card.append(img_in_card)
        card.append(card_name)
        card.append(card_more)
        skills.append(card)
      }
      skills.classList.add("render")
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
              skills_func()
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
      const soc_url = document.createElement("a")
      soc_url.classList.add("soc_url")
      soc_url.innerHTML = cond[0].social_media[i][0]
      soc_url.innerHTML = cond[0].social_media[i][1]
      soc_url.href = "#"
      social_bt.append(soc_url)
      console.log(cond[0].social_media[i][0])
    }
  }
  soc_med()
}


cont = [
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

cond = [
  {
    "id": 10929878,
    "name": "Name Surname",
    "descript": "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Reprehenderit quis alias doloribus ipsam illum! Necessitatibus!", 
    "ava": "./cat.png", //?????
    "social_media": 
        // [
        //   {"tik_tok": "lala"},
        //   {"inst": "dd"}
        // ]
        [
          ["tik_tok", "lala"],
          ["inst", "dd"]
        ]
      
  }
]
getResponce(cont)
conditer(cond)