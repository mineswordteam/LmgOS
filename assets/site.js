(function(){
var d=document,h=d.documentElement;
function setL(l){try{localStorage.setItem("lmglang",l)}catch(e){}h.setAttribute("data-l",l);h.lang=l;h.dir=l=="fa"?"rtl":"ltr"}
var lb=d.getElementById("lang");if(lb)lb.addEventListener("click",function(){setL(h.getAttribute("data-l")=="fa"?"en":"fa")});
var bg=d.getElementById("burger"),nv=d.getElementById("nav");if(bg&&nv)bg.addEventListener("click",function(){nv.classList.toggle("open")});
d.querySelectorAll(".copy").forEach(function(b){b.addEventListener("click",function(){var el=d.getElementById(b.dataset.c);if(!el)return;var t=el.textContent.trim();(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).catch(function(){var r=d.createRange();r.selectNode(el);getSelection().removeAllRanges();getSelection().addRange(r);try{d.execCommand("copy")}catch(e){}});b.style.opacity=.6;setTimeout(function(){b.style.opacity=1},900)})});
var box=d.getElementById("lb");if(box){var im=box.querySelector("img");d.querySelectorAll(".gal img").forEach(function(i){i.addEventListener("click",function(){im.src=i.src;im.alt=i.alt;box.classList.add("on")})});box.addEventListener("click",function(){box.classList.remove("on")});d.addEventListener("keydown",function(e){if(e.key=="Escape")box.classList.remove("on")})}
if("IntersectionObserver"in window){var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");o.unobserve(e.target)}})},{threshold:.1});d.querySelectorAll(".rv").forEach(function(e){o.observe(e)})}else d.querySelectorAll(".rv").forEach(function(e){e.classList.add("in")});
})();
