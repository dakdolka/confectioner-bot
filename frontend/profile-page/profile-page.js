async function getResponce(){
    let response = await fetch('https://jsonplaceholder.typicode.com/photos')
    var content = await response.json()
    await console.log(content[content[1].id])
    function works(){
        for(let i = 0; i < 10; i++){
        document.querySelector('.orders').classList.add('hide')
        document.querySelector('.skills').classList.add('hide')
        document.querySelector('.works').classList.remove('hide')
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
        document.querySelector('.works').append(card)
        
        }
    }
    works()

    //при первом нажатии отработать, а потом просто hide 
    function orders(){
      for(let i = 0; i < 10; i++){
      document.querySelector('.works').classList.add('hide')
      document.querySelector('.skills').classList.add('hide')
      document.querySelector('.orders').classList.remove('hide')
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
      document.querySelector('.orders').append(card)
      
      }
    }



    function active_navbar(){
      const arr = document.querySelectorAll(".bt")
      for(let i = 0; i < arr.length; i++){
        arr[i].addEventListener("click", () => {
          arr[i].classList.add("active")
          for(let j = 0; j < arr.length; j++){
            if(j != i){
              arr[j].classList.remove("active")
            }
          }
          if (i == 0){
            works()
            console.log('works')
          }
          if (i == 1){
            orders()
            console.log('orders')
          }
        })
      }
    
    }
    active_navbar()

}
getResponce()


cont = [
    {
      "albumId": 1,
      "id": 1,
      "title": "accusamus beatae ad facilis cum similique qui sunt",
      "url": "https://via.placeholder.com/600/92c952",
      "thumbnailUrl": "https://via.placeholder.com/150/92c952"
    },
    {
      "albumId": 1,
      "id": 2,
      "title": "reprehenderit est deserunt velit ipsam",
      "url": "https://via.placeholder.com/600/771796",
      "thumbnailUrl": "https://via.placeholder.com/150/771796"
    },
]