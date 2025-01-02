async function getResponce(){
    let response = await fetch('https://jsonplaceholder.typicode.com/photos')
    var content = await response.json()
    сonsole.log("hh")
    console.log(content[content[1].id])
    сonsole.log("hh")
    function cards(){
        for(let i = 0; i < 10; i++){
        console.log(content[i].id)
        const card = document.createElement('div')
        card.classList.add('card')
        const img_in_card = document.createElement('img')
        img_in_card.classList.add('img_in_card')
        img_in_card.src = content[i].url
        card.append(img_in_card)
        document.querySelector('.works').append(card)
        
        }
    }
    cards()
}

getResponce()