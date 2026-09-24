
function money(n){return new Intl.NumberFormat("en-IN",{style:"currency",currency:"INR",maximumFractionDigits:2}).format(Number(n||0));}

function checked(form,name){
  return [...form.querySelectorAll(`input[name="${name}"]:checked`)].map(x=>x.value);
}

function resultHtml(data){
  const r=data.result;
  const breakdown=(r.budget_breakdown||[]).map(x=>`<div class="mini-card"><strong>${escapeHtml(x.category)}</strong><span>${money(x.allocation)}</span><small>${escapeHtml(x.reason||"")}</small></div>`).join("");
  const recs=(r.recommendations||[]).map(x=>`
    <article class="recommendation">
      <div class="rec-main"><span class="badge">${escapeHtml(x.category||"Item")}</span><h3>${escapeHtml(x.item||"Recommendation")}</h3>
      <p>${escapeHtml(x.description||"")}</p><p class="muted">${escapeHtml(x.why||"")}</p></div>
      <div class="rec-price"><strong>${money(x.estimated_price)}</strong><span>Qty ${x.quantity||1}</span>
      <a href="${safeUrl(x.search_url)}" target="_blank" rel="noopener">Shop/search ↗</a></div>
    </article>`).join("");
  return `<div class="result-card">
    <div class="summary"><div><span>Budget</span><strong>${money(r.total_budget)}</strong></div>
    <div><span>Estimated total</span><strong>${money(r.estimated_total)}</strong></div>
    <div><span>Remaining</span><strong>${money(r.remaining_budget)}</strong></div></div>
    <section class="section"><h2>Budget breakdown</h2><div class="grid four">${breakdown}</div></section>
    <section class="section"><h2>Recommendations</h2><div class="recommendations">${recs||'<div class="empty">No recommendations returned.</div>'}</div></section>
    ${(r.additional_suggestions||r.styling_tips)?`<section class="section"><h2>Tips</h2><ul>${[...(r.additional_suggestions||[]),...(r.styling_tips||[])].map(x=>`<li>${escapeHtml(x)}</li>`).join("")}</ul></section>`:""}
    <a class="btn" href="/recommendations/${data.id}">Open full details</a>
  </div>`;
}

function escapeHtml(value){
  return String(value??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]));
}
function safeUrl(value){
  const url=String(value||"");
  return /^(https?:\/\/)/i.test(url)?url:"#";
}
async function postJson(url,payload){
  const response=await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
  const data=await response.json().catch(()=>({detail:"Invalid server response"}));
  if(!response.ok) throw new Error(data.detail||"Request failed");
  return data;
}
function bindHome(){
  const form=document.querySelector("#home-form"); if(!form)return;
  form.addEventListener("submit",async e=>{
    e.preventDefault(); const out=document.querySelector("#result"); out.className="result loading"; out.textContent="Generating…";
    const payload={total_budget:Number(form.total_budget.value),rooms:checked(form,"rooms"),num_lights:Number(form.num_lights.value),num_fans:Number(form.num_fans.value),num_furniture:Number(form.num_furniture.value),num_dining_tables:Number(form.num_dining_tables.value),style:form.style.value,additional_requirements:form.additional_requirements.value};
    try{const data=await postJson("/api/generate-home",payload);out.className="result";out.innerHTML=resultHtml(data)}catch(err){out.innerHTML=`<div class="error">${escapeHtml(err.message)}</div>`}
  });
}
function bindParty(){
  const form=document.querySelector("#party-form"); if(!form)return;
  form.addEventListener("submit",async e=>{
    e.preventDefault(); const out=document.querySelector("#result"); out.className="result loading"; out.textContent="Generating…";
    const payload={total_budget:Number(form.total_budget.value),num_guests:Number(form.num_guests.value),party_type:form.party_type.value,venue_type:form.venue_type.value,needs:checked(form,"needs"),additional_requirements:form.additional_requirements.value};
    try{const data=await postJson("/api/generate-party",payload);out.className="result";out.innerHTML=resultHtml(data)}catch(err){out.innerHTML=`<div class="error">${escapeHtml(err.message)}</div>`}
  });
}
function bindJewelry(){
  const form=document.querySelector("#jewelry-form"); if(!form)return;
  form.addEventListener("submit",async e=>{
    e.preventDefault(); const out=document.querySelector("#result"); out.className="result loading"; out.textContent="Generating…";
    const body=new FormData(form);
    try{const response=await fetch("/api/generate-jewelry",{method:"POST",body});const data=await response.json();if(!response.ok)throw new Error(data.detail||"Request failed");out.className="result";out.innerHTML=resultHtml(data)}catch(err){out.innerHTML=`<div class="error">${escapeHtml(err.message)}</div>`}
  });
}
document.addEventListener("DOMContentLoaded",()=>{bindHome();bindParty();bindJewelry();});
