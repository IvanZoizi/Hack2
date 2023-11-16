const burger =document.querySelector('.burger')
const container =document.querySelector('.container')
const screens =document.querySelectorAll('.screen')
let shouldExecuteCode = false;

burger.addEventListener('click', () => {
    container.classList.toggle ('active')
    shouldExecuteCode = !shouldExecuteCode;
})


function replaceBg(id) {
    const bg=document.getElementById(id)
    screens.forEach(screen =>{
        screen.style.display ='none'
    })

    bg.style.display='block'
}

function changeBg () {
    const links =document.querySelectorAll('.link')

    links.forEach((link, index ) =>{
        link.addEventListener('mouseenter', e=> {
            e.preventDefault()
            replaceBg(e.target.dataset.link)
        })

        link.addEventListener('click', e=>{
            e.preventDefault()
            container.classList.toggle('active')
            shouldExecuteCode = !shouldExecuteCode;
        })
    })
    

    screens.forEach(screen=>{
        screen.style.display='none'
        screens[0].style.display='block'
    })
}

function changeScreen() {
    const screens = document.querySelectorAll('.screen');

    screens.forEach((screen, index) => {
        screen.addEventListener('click', e => {
            e.preventDefault();
            if (shouldExecuteCode) {
                container.classList.toggle('active');
                shouldExecuteCode = !shouldExecuteCode;
            }
        });
    });

    screens.forEach(screen => {
        screen.style.display = 'none';
        screens[0].style.display = 'block';
    });
}

document.getElementById("client").onclick = function () {
    // Здесь вы можете указать ссылку на вторую HTML страницу
    window.location.href = "/register/user";
  };

document.getElementById("partner").onclick = function () {
    // Здесь вы можете указать ссылку на вторую HTML страницу
    window.location.href = "../the_supplier/index.html";
  };

document.getElementById("provider").onclick = function () {
    // Здесь вы можете указать ссылку на вторую HTML страницу
    window.location.href = "../the_supplier/index.html";
  };

document.getElementById("deliveryman").onclick = function () {
    // Здесь вы можете указать ссылку на вторую HTML страницу
    window.location.href = "../the_supplier/index.html";
  };

changeScreen()
changeBg()


