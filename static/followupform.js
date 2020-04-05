!function() {
  function check(e) {
    if (e.target.value !== '') {
      return e.target.style.paddingBottom = "1em";
    } 
    
    e.target.style.paddingBottom = "0";
  }
  
  function send(e) {
    e.preventDefault()
    
    this.reset()
  }

  form.addEventListener("keyup", check);
  form.addEventListener("submit", send);
}();