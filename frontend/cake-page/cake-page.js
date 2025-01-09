function blue() {
    console.log("blue")
}


function choice(data) {
    
    const choice = document.querySelector(".choice")
    const h2 = document.createElement("div")
    h2.classList.add("h2")
    const opts = document.createElement("div")
    opts.classList.add("opts")
    const arr = [choice] 
    //предполагается кидать сюда готовые чойзы для перехода между выборами

    const opt_1 = document.createElement("button")
    opt_1.classList.add("opt")
    opt_1.innerHTML = "Первый вариант"
    opt_1.addEventListener("click", () => {
        console.log("BENGER")
        arr[0].classList.add('hide') 
    })


    const opt_2 = document.createElement("button")
    opt_2.classList.add("opt")
    opt_2.innerHTML = "Второй вариант"
    opt_2.addEventListener("click", () => {
        arr[0].classList.add('hide')
    })


    const opt_3 = document.createElement("button")
    opt_3.classList.add("opt")
    opt_3.innerHTML = "Третий вариант"
    opt_3.addEventListener("click", () => {
        arr[0].classList.add('hide')
    })




    opts.append(opt_1)
    opts.append(opt_2)
    opts.append(opt_3)
    choice.append(opts)
    console.log(arr[0])

}


data = [
    {
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
]

choice(data)
