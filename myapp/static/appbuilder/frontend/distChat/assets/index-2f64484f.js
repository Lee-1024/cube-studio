import{ae as g,d as o,r as h,$ as p,B as r,C as a,J as t,S as m,I as f}from"./index-85f05984.js";function _(){const c=g();return c?c.appContext.config.globalProperties.emitter:null}const w={id:"b-container",class:"container b-container"},b=t("form",{id:"b-form",class:"form",method:"",action:""},[t("h2",{class:"form_title title"}," Sign in to Website "),t("div",{class:"form__icons"},[t("img",{class:"form__icon",src:""}),t("img",{class:"form__icon",src:""}),t("img",{class:"form__icon",src:""})]),t("span",{class:"form__span"},"or use your email account"),t("a",{class:"form__link"},"Forgot your password?"),t("button",{class:"form__button button submit"}," SIGN IN ")],-1),y=[b],v=o({__name:"signIn",setup(c){h(!0);const s=_();return p(()=>{s.on("change",n=>{document.querySelector("#a-container").classList.toggle("is-txl")})}),(n,e)=>(r(),a("div",w,y))}});const x={id:"a-container",class:"container a-container"},C=t("form",{id:"a-form",class:"form",method:"",action:""},[t("h2",{class:"form_title title"}," Create Account "),t("div",{class:"form__icons"},[t("img",{class:"form__icon",src:""}),t("img",{class:"form__icon",src:""}),t("img",{class:"form__icon",src:""})]),t("span",{class:"form__span"},"or use email for registration"),t("input",{class:"form__input",type:"text",placeholder:"Name"}),t("input",{class:"form__input",type:"text",placeholder:"Email"}),t("input",{class:"form__input",type:"password",placeholder:"Password"}),t("button",{class:"form__button button submit"}," SIGN UP ")],-1),S=[C],I=o({__name:"signUp",setup(c){const s=_();return p(()=>{s.on("change",n=>{{const e=document.querySelector("#b-container");e.classList.toggle("is-txl"),e.classList.toggle("is-z200")}})}),(n,e)=>(r(),a("div",x,S))}});const L=t("div",{class:"switch__circle"},null,-1),N=t("div",{class:"switch__circle switch__circle--t"},null,-1),$=t("h2",{class:"switch__title title"}," Welcome Back ! ",-1),k=t("p",{class:"switch__description description"}," To keep connected with us please login with your personal info ",-1),q=t("h2",{class:"switch__title title"}," Hello Friend ! ",-1),B=t("p",{class:"switch__description description"}," Enter your personal details and start journey with us ",-1),G=o({__name:"index",setup(c){const s=h(!0),n=_(),e=()=>{const l=document.querySelector("#switch-c1"),u=document.querySelector("#switch-c2"),d=document.querySelectorAll(".switch__circle"),i=document.querySelector("#switch-cnt");i.classList.add("is-gx"),setTimeout(()=>{i.classList.remove("is-gx")},1500),i.classList.toggle("is-txr"),d[0].classList.toggle("is-txr"),d[1].classList.toggle("is-txr"),l.classList.toggle("is-hidden"),u.classList.toggle("is-hidden"),s.value=!s.value,n.emit("change",s.value)};return(l,u)=>(r(),a(f,null,[t("div",{id:"switch-cnt",class:"switch"},[L,N,t("div",{id:"switch-c1",class:"switch__container"},[$,k,t("button",{class:"switch__button button switch-btn",onClick:e}," SIGN IN ")]),t("div",{id:"switch-c2",class:"switch__container is-hidden"},[q,B,t("button",{class:"switch__button button switch-btn",onClick:e}," SIGN UP ")])]),m(v),m(I)],64))}});export{G as default};
