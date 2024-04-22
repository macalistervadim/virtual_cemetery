let header = document.querySelector(".js-header")
headerHeight = document.querySelector(".js-header").clientHeight

document.onscroll = function (){
    let scroll = window.scrollY;

    if (scroll > headerHeight + 33){
        header.classList.add("fixed");
        document.body.style.paddingTop = headerHeight + "px";
    } else{
        header.classList.remove("fixed");
        document.body.removeAttribute("style")
    }
}