function toggleSettings(){const m=document.getElementById("settings-dropdown");if(m)m.classList.toggle("open")}
document.addEventListener("click",e=>{const c=document.querySelector(".settings-container"),m=document.getElementById("settings-dropdown");if(c&&m&&!c.contains(e.target))m.classList.remove("open")});
function changeLimit(delta){const input=document.querySelector(".number-control input");if(!input)return;input.value=Math.max(parseInt(input.min||1),parseInt(input.value||0)+delta);if(input.form)input.form.submit()}
document.addEventListener("click",e=>{const el=e.target.closest("[data-confirm]");if(el&&!confirm(el.dataset.confirm))e.preventDefault()});
